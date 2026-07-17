#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from _snapshot_common import (
    CaptureError,
    canonical_json_bytes,
    run_checked,
    seal_state,
    sha256_bytes,
    write_artifact_set,
)


_REPOSITORY_RE = re.compile(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+")
_OID_RE = re.compile(r"(?:[0-9a-f]{40}|[0-9a-f]{64})")
# Conservative sentinels from GitHub's documented pull-request diff limits.
# Keep these aligned with references/pull-request-gate.md.
_DIFF_MAX_FILES = 300
_DIFF_MAX_LINES = 20_000
_DIFF_MAX_BYTES = 1024 * 1024
_DIFF_MAX_FILE_BYTES = 500 * 1024


_THREAD_QUERY = """
query($owner: String!, $name: String!, $number: Int!, $cursor: String) {
  repository(owner: $owner, name: $name) {
    pullRequest(number: $number) {
      reviewThreads(first: 100, after: $cursor) {
        nodes {
          id
          isResolved
          isOutdated
          path
          line
          originalLine
          comments(first: 100) {
            nodes {
              databaseId
              body
              createdAt
              updatedAt
              url
              author { login }
            }
            pageInfo { hasNextPage }
          }
        }
        pageInfo { hasNextPage endCursor }
      }
    }
  }
}
"""


_CLOSING_ISSUES_QUERY = """
query($owner: String!, $name: String!, $number: Int!, $cursor: String) {
  repository(owner: $owner, name: $name) {
    pullRequest(number: $number) {
      closingIssuesReferences(first: 100, after: $cursor) {
        nodes {
          number
          url
          title
          body
          state
          updatedAt
          repository { nameWithOwner }
        }
        pageInfo { hasNextPage endCursor }
      }
    }
  }
}
"""


def _mapping(value: Any, label: str) -> Mapping[str, Any]:
    if not isinstance(value, dict):
        raise CaptureError(f"GitHub returned invalid {label}")
    return value


def _array(value: Any, label: str) -> list[Any]:
    if not isinstance(value, list):
        raise CaptureError(f"GitHub returned invalid {label}")
    return value


def _text(value: Any, label: str, *, optional: bool = False) -> str | None:
    if value is None and optional:
        return None
    if not isinstance(value, str):
        raise CaptureError(f"GitHub returned invalid {label}")
    return value


def _integer(value: Any, label: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise CaptureError(f"GitHub returned invalid {label}")
    return value


def _oid(value: Any, label: str) -> str:
    text = _text(value, label)
    assert text is not None
    if not _OID_RE.fullmatch(text):
        raise CaptureError(f"GitHub returned invalid {label}")
    return text


def _gh_json(endpoint: str, *, paginate: bool = False) -> Any:
    command = ["gh", "api"]
    if paginate:
        command.extend(["--paginate", "--slurp"])
    command.append(endpoint)
    raw = run_checked(command, label="gh api")
    try:
        return json.loads(raw)
    except json.JSONDecodeError as error:
        raise CaptureError("gh api returned malformed JSON") from error


def _gh_diff(endpoint: str) -> bytes:
    return run_checked(
        ["gh", "api", "-H", "Accept: application/vnd.github.v3.diff", endpoint],
        label="gh api diff",
    )


def _gh_graphql(query: str, variables: Mapping[str, Any]) -> Any:
    command = ["gh", "api", "graphql", "-f", f"query={query}"]
    for name, value in variables.items():
        flag = "-F" if isinstance(value, int) else "-f"
        command.extend([flag, f"{name}={value}"])
    raw = run_checked(command, label="gh api graphql")
    try:
        return json.loads(raw)
    except json.JSONDecodeError as error:
        raise CaptureError("gh api graphql returned malformed JSON") from error


def _array_pages(endpoint: str, *, label: str) -> list[Mapping[str, Any]]:
    pages = _array(_gh_json(endpoint, paginate=True), f"{label} pages")
    values: list[Mapping[str, Any]] = []
    for page in pages:
        for value in _array(page, label):
            values.append(_mapping(value, f"{label} item"))
    return values


def _check_runs(endpoint: str) -> list[Mapping[str, Any]]:
    pages = _array(_gh_json(endpoint, paginate=True), "check-run pages")
    values: list[Mapping[str, Any]] = []
    expected: int | None = None
    for page in pages:
        payload = _mapping(page, "check-run page")
        total = _integer(payload.get("total_count"), "check-run total_count")
        expected = total if expected is None else expected
        if total != expected:
            raise CaptureError("GitHub returned inconsistent check-run totals")
        for value in _array(payload.get("check_runs"), "check runs"):
            values.append(_mapping(value, "check run"))
    if expected is None:
        expected = 0
    if len(values) != expected:
        raise CaptureError(
            f"GitHub returned incomplete check runs: expected {expected}, received {len(values)}"
        )
    return values


def _review_threads(owner: str, name: str, number: int) -> list[Mapping[str, Any]]:
    cursor: str | None = None
    values: list[Mapping[str, Any]] = []
    while True:
        variables: dict[str, Any] = {"owner": owner, "name": name, "number": number}
        if cursor is not None:
            variables["cursor"] = cursor
        payload = _mapping(_gh_graphql(_THREAD_QUERY, variables), "GraphQL response")
        if payload.get("errors"):
            raise CaptureError("GitHub returned GraphQL errors for review threads")
        data = _mapping(payload.get("data"), "GraphQL data")
        repository = _mapping(data.get("repository"), "GraphQL repository")
        pull = _mapping(repository.get("pullRequest"), "GraphQL pull request")
        threads = _mapping(pull.get("reviewThreads"), "review threads")
        for raw_thread in _array(threads.get("nodes"), "review-thread nodes"):
            thread = _mapping(raw_thread, "review thread")
            comments = _mapping(thread.get("comments"), "review-thread comments")
            page_info = _mapping(comments.get("pageInfo"), "review-comment page info")
            if page_info.get("hasNextPage") is True:
                raise CaptureError(
                    "a review thread has more than 100 comments; complete capture is unavailable"
                )
            values.append(thread)
        page_info = _mapping(threads.get("pageInfo"), "review-thread page info")
        if page_info.get("hasNextPage") is not True:
            return values
        cursor_value = _text(page_info.get("endCursor"), "review-thread endCursor")
        assert cursor_value is not None
        if not cursor_value or cursor_value == cursor:
            raise CaptureError("GitHub returned an invalid review-thread cursor")
        cursor = cursor_value


def _closing_issues(owner: str, name: str, number: int) -> list[Mapping[str, Any]]:
    cursor: str | None = None
    values: list[Mapping[str, Any]] = []
    while True:
        variables: dict[str, Any] = {
            "owner": owner,
            "name": name,
            "number": number,
        }
        if cursor is not None:
            variables["cursor"] = cursor
        payload = _mapping(
            _gh_graphql(_CLOSING_ISSUES_QUERY, variables), "GraphQL response"
        )
        if payload.get("errors"):
            raise CaptureError("GitHub returned GraphQL errors for closing issues")
        data = _mapping(payload.get("data"), "GraphQL data")
        repository = _mapping(data.get("repository"), "GraphQL repository")
        pull = _mapping(repository.get("pullRequest"), "GraphQL pull request")
        issues = _mapping(
            pull.get("closingIssuesReferences"), "closing issue references"
        )
        for raw_issue in _array(issues.get("nodes"), "closing issue nodes"):
            values.append(_mapping(raw_issue, "closing issue"))
        page_info = _mapping(issues.get("pageInfo"), "closing issue page info")
        if page_info.get("hasNextPage") is not True:
            return values
        cursor_value = _text(page_info.get("endCursor"), "closing issue endCursor")
        assert cursor_value is not None
        if not cursor_value or cursor_value == cursor:
            raise CaptureError("GitHub returned an invalid closing issue cursor")
        cursor = cursor_value


def _user(value: Any) -> str | None:
    if value is None:
        return None
    return _text(_mapping(value, "user").get("login"), "user.login", optional=True)


def _normalize_commit(value: Mapping[str, Any]) -> dict[str, Any]:
    commit = _mapping(value.get("commit"), "commit details")
    return {
        "oid": _oid(value.get("sha"), "commit sha"),
        "message": _text(commit.get("message"), "commit message") or "",
        "parents": [
            _oid(_mapping(parent, "commit parent").get("sha"), "parent sha")
            for parent in _array(value.get("parents"), "commit parents")
        ],
    }


def _normalize_file(value: Mapping[str, Any]) -> dict[str, Any]:
    patch = value.get("patch")
    if patch is not None and not isinstance(patch, str):
        raise CaptureError("GitHub returned an invalid file patch")
    return {
        "path": _text(value.get("filename"), "file path") or "",
        "previous_path": _text(
            value.get("previous_filename"), "previous file path", optional=True
        ),
        "status": _text(value.get("status"), "file status") or "",
        "additions": _integer(value.get("additions"), "file additions"),
        "deletions": _integer(value.get("deletions"), "file deletions"),
        "changes": _integer(value.get("changes"), "file changes"),
        "patch_available": patch is not None,
    }


def _normalize_check(value: Mapping[str, Any], head_oid: str) -> dict[str, Any]:
    check_oid = _oid(value.get("head_sha"), "check-run head sha")
    if check_oid != head_oid:
        raise CaptureError("GitHub returned a check run for a different head OID")
    return {
        "id": _integer(value.get("id"), "check-run id"),
        "name": _text(value.get("name"), "check-run name") or "",
        "head_oid": check_oid,
        "status": _text(value.get("status"), "check-run status") or "",
        "conclusion": _text(
            value.get("conclusion"), "check-run conclusion", optional=True
        ),
        "details_url": _text(
            value.get("details_url"), "check-run details_url", optional=True
        ),
    }


def _normalize_status(value: Mapping[str, Any], head_oid: str) -> dict[str, Any]:
    status_oid = value.get("sha")
    if status_oid is not None and _oid(status_oid, "status sha") != head_oid:
        raise CaptureError("GitHub returned a status for a different head OID")
    return {
        "id": _integer(value.get("id"), "status id"),
        "context": _text(value.get("context"), "status context") or "",
        "state": _text(value.get("state"), "status state") or "",
        "description": _text(
            value.get("description"), "status description", optional=True
        ),
        "target_url": _text(
            value.get("target_url"), "status target_url", optional=True
        ),
        "created_at": _text(value.get("created_at"), "status created_at") or "",
    }


def _latest_statuses(values: Sequence[dict[str, Any]]) -> list[dict[str, Any]]:
    newest = sorted(
        values,
        key=lambda value: (value["context"], value["created_at"], value["id"]),
        reverse=True,
    )
    by_context: dict[str, dict[str, Any]] = {}
    for value in newest:
        by_context.setdefault(value["context"], value)
    return sorted(by_context.values(), key=lambda value: value["context"])


def _normalize_review(value: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "id": _integer(value.get("id"), "review id"),
        "author": _user(value.get("user")),
        "state": _text(value.get("state"), "review state") or "",
        "body": _text(value.get("body"), "review body", optional=True) or "",
        "commit_oid": _text(value.get("commit_id"), "review commit_id", optional=True),
        "submitted_at": _text(
            value.get("submitted_at"), "review submitted_at", optional=True
        ),
    }


def _normalize_comment(value: Mapping[str, Any], *, review: bool) -> dict[str, Any]:
    result: dict[str, Any] = {
        "id": _integer(value.get("id"), "comment id"),
        "author": _user(value.get("user")),
        "body": _text(value.get("body"), "comment body") or "",
        "created_at": _text(value.get("created_at"), "comment created_at") or "",
        "updated_at": _text(value.get("updated_at"), "comment updated_at") or "",
    }
    if review:
        result.update(
            {
                "path": _text(value.get("path"), "review-comment path") or "",
                "line": value.get("line"),
                "original_line": value.get("original_line"),
                "commit_oid": _text(
                    value.get("commit_id"), "review-comment commit_id", optional=True
                ),
                "in_reply_to_id": value.get("in_reply_to_id"),
            }
        )
    return result


def _normalize_thread(value: Mapping[str, Any]) -> dict[str, Any]:
    comments = _mapping(value.get("comments"), "review-thread comments")
    normalized_comments = []
    for raw in _array(comments.get("nodes"), "review-thread comment nodes"):
        comment = _mapping(raw, "review-thread comment")
        normalized_comments.append(
            {
                "id": comment.get("databaseId"),
                "author": _user(comment.get("author")),
                "body": _text(comment.get("body"), "thread comment body") or "",
                "created_at": _text(
                    comment.get("createdAt"), "thread comment createdAt"
                )
                or "",
                "updated_at": _text(
                    comment.get("updatedAt"), "thread comment updatedAt"
                )
                or "",
                "url": _text(comment.get("url"), "thread comment url") or "",
            }
        )
    return {
        "id": _text(value.get("id"), "review-thread id") or "",
        "is_resolved": value.get("isResolved") is True,
        "is_outdated": value.get("isOutdated") is True,
        "path": _text(value.get("path"), "review-thread path") or "",
        "line": value.get("line"),
        "original_line": value.get("originalLine"),
        "comments": normalized_comments,
    }


def _normalize_closing_issue(value: Mapping[str, Any]) -> dict[str, Any]:
    repository = _mapping(value.get("repository"), "closing issue repository")
    return {
        "repository": _text(
            repository.get("nameWithOwner"), "closing issue repository name"
        )
        or "",
        "number": _integer(value.get("number"), "closing issue number"),
        "url": _text(value.get("url"), "closing issue url") or "",
        "title": _text(value.get("title"), "closing issue title") or "",
        "body": _text(value.get("body"), "closing issue body", optional=True) or "",
        "state": _text(value.get("state"), "closing issue state") or "",
        "updated_at": _text(value.get("updatedAt"), "closing issue updatedAt") or "",
    }


def _diff_limit_reasons(files: Sequence[Mapping[str, Any]], diff: bytes) -> list[str]:
    reasons: list[str] = []
    if any(value.get("patch_available") is False for value in files):
        reasons.append("file_without_textual_patch")
    if len(files) >= _DIFF_MAX_FILES:
        reasons.append("at_least_300_files")
    changed_lines = sum(
        int(value.get("additions", 0)) + int(value.get("deletions", 0))
        for value in files
    )
    if changed_lines >= _DIFF_MAX_LINES:
        reasons.append("at_least_20000_changed_lines")
    raw_lines = diff.count(b"\n") + int(bool(diff) and not diff.endswith(b"\n"))
    if raw_lines >= _DIFF_MAX_LINES:
        reasons.append("at_least_20000_raw_diff_lines")
    if len(diff) >= _DIFF_MAX_BYTES:
        reasons.append("at_least_1_mb_raw_diff")

    starts: list[int] = [0] if diff.startswith(b"diff --git ") else []
    offset = 0
    marker = b"\ndiff --git "
    while True:
        index = diff.find(marker, offset)
        if index < 0:
            break
        starts.append(index + 1)
        offset = index + len(marker)
    for index, start in enumerate(starts):
        end = starts[index + 1] if index + 1 < len(starts) else len(diff)
        if end - start >= _DIFF_MAX_FILE_BYTES:
            reasons.append("single_file_at_least_500_kb_raw_diff")
            break
    return sorted(set(reasons))


def capture_state(
    repository: str, number: int, cycle: str
) -> tuple[dict[str, Any], bytes]:
    if not _REPOSITORY_RE.fullmatch(repository):
        raise CaptureError("--repo must use owner/repository form")
    if number <= 0:
        raise CaptureError("--pr must be a positive integer")
    if cycle not in {"initial", "rerequest"}:
        raise CaptureError("--cycle must be initial or rerequest")

    owner, name = repository.split("/", 1)
    prefix = f"repos/{repository}"
    pull = _mapping(_gh_json(f"{prefix}/pulls/{number}"), "pull request")
    if (_text(pull.get("state"), "pull request state") or "").lower() != "open":
        raise CaptureError("pull request is not open")
    returned_number = _integer(pull.get("number"), "pull request number")
    if returned_number != number:
        raise CaptureError("GitHub returned a different pull request number")
    base = _mapping(pull.get("base"), "pull request base")
    head = _mapping(pull.get("head"), "pull request head")
    base_oid = _oid(base.get("sha"), "pull request base sha")
    head_oid = _oid(head.get("sha"), "pull request head sha")

    raw_commits = _array_pages(
        f"{prefix}/pulls/{number}/commits?per_page=100", label="commits"
    )
    expected_commits = _integer(pull.get("commits"), "pull request commits")
    if len(raw_commits) != expected_commits:
        raise CaptureError(
            f"GitHub returned incomplete commits: expected {expected_commits}, received {len(raw_commits)}"
        )
    commits = [_normalize_commit(value) for value in raw_commits]
    if not commits or commits[-1]["oid"] != head_oid:
        raise CaptureError(
            "GitHub commit list does not end at the pull request head OID"
        )

    raw_files = _array_pages(
        f"{prefix}/pulls/{number}/files?per_page=100", label="files"
    )
    expected_files = _integer(pull.get("changed_files"), "pull request changed_files")
    if len(raw_files) != expected_files:
        raise CaptureError(
            f"GitHub returned incomplete files: expected {expected_files}, received {len(raw_files)}"
        )
    files = sorted(
        (_normalize_file(value) for value in raw_files), key=lambda value: value["path"]
    )
    if len({value["path"] for value in files}) != len(files):
        raise CaptureError("GitHub returned duplicate file paths")

    checks = [
        _normalize_check(value, head_oid)
        for value in _check_runs(
            f"{prefix}/commits/{head_oid}/check-runs?filter=latest&per_page=100"
        )
    ]
    statuses = _latest_statuses(
        [
            _normalize_status(value, head_oid)
            for value in _array_pages(
                f"{prefix}/statuses/{head_oid}?per_page=100", label="statuses"
            )
        ]
    )
    closing_issues = sorted(
        (
            _normalize_closing_issue(value)
            for value in _closing_issues(owner, name, number)
        ),
        key=lambda value: (value["repository"], value["number"]),
    )

    reviews: list[dict[str, Any]] = []
    issue_comments: list[dict[str, Any]] = []
    review_comments: list[dict[str, Any]] = []
    threads: list[dict[str, Any]] = []
    if cycle == "rerequest":
        reviews = [
            _normalize_review(value)
            for value in _array_pages(
                f"{prefix}/pulls/{number}/reviews?per_page=100", label="reviews"
            )
        ]
        issue_comments = [
            _normalize_comment(value, review=False)
            for value in _array_pages(
                f"{prefix}/issues/{number}/comments?per_page=100",
                label="issue comments",
            )
        ]
        expected_issue_comments = _integer(
            pull.get("comments"), "pull request comments"
        )
        if len(issue_comments) != expected_issue_comments:
            raise CaptureError(
                "GitHub returned an incomplete pull-request issue-comment list"
            )
        review_comments = [
            _normalize_comment(value, review=True)
            for value in _array_pages(
                f"{prefix}/pulls/{number}/comments?per_page=100",
                label="review comments",
            )
        ]
        expected_review_comments = _integer(
            pull.get("review_comments"), "pull request review_comments"
        )
        if len(review_comments) != expected_review_comments:
            raise CaptureError("GitHub returned an incomplete review-comment list")
        threads = [
            _normalize_thread(value) for value in _review_threads(owner, name, number)
        ]

    diff = _gh_diff(f"{prefix}/pulls/{number}")
    diff_reasons = _diff_limit_reasons(files, diff)
    feedback = {
        "reviews": sorted(reviews, key=lambda value: value["id"]),
        "issue_comments": sorted(issue_comments, key=lambda value: value["id"]),
        "review_comments": sorted(review_comments, key=lambda value: value["id"]),
        "review_threads": sorted(threads, key=lambda value: value["id"]),
    }
    check_state = {
        "check_runs": sorted(checks, key=lambda value: value["id"]),
        "statuses": sorted(
            statuses,
            key=lambda value: (value["context"], value["created_at"], value["id"]),
        ),
    }
    state = {
        "kind": "PR_REVIEW_REQUEST",
        "cycle": cycle,
        "repository": repository,
        "number": number,
        "url": _text(pull.get("html_url"), "pull request url") or "",
        "author": _user(pull.get("user")),
        "is_draft": pull.get("draft") is True,
        "title": _text(pull.get("title"), "pull request title") or "",
        "body": _text(pull.get("body"), "pull request body", optional=True) or "",
        "updated_at": _text(pull.get("updated_at"), "pull request updated_at") or "",
        "base_ref": _text(base.get("ref"), "pull request base ref") or "",
        "base_oid": base_oid,
        "head_ref": _text(head.get("ref"), "pull request head ref") or "",
        "head_oid": head_oid,
        "diff_sha256": sha256_bytes(diff),
        "remote_diff_may_be_incomplete": bool(diff_reasons),
        "remote_diff_limit_reasons": diff_reasons,
        "commits": commits,
        "commits_sha256": sha256_bytes(canonical_json_bytes(commits)),
        "files": files,
        "files_sha256": sha256_bytes(canonical_json_bytes(files)),
        "closing_issues": closing_issues,
        "closing_issues_sha256": sha256_bytes(canonical_json_bytes(closing_issues)),
        **check_state,
        "checks_sha256": sha256_bytes(canonical_json_bytes(check_state)),
        **feedback,
        "feedback_sha256": sha256_bytes(canonical_json_bytes(feedback)),
    }
    return seal_state(state, domain="change-readiness-pr-snapshot-v1"), diff


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Capture a read-only fingerprint of GitHub pull-request state."
    )
    parser.add_argument("--repo", required=True)
    parser.add_argument("--pr", required=True, type=int)
    parser.add_argument("--cycle", choices=("initial", "rerequest"), required=True)
    parser.add_argument(
        "--workspace-root",
        required=True,
        help="local workspace root that the snapshot directory must remain outside",
    )
    parser.add_argument("--snapshot-dir", required=True)
    parser.add_argument("--name", required=True)
    parser.add_argument("--write-diff", action="store_true")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    arguments = _parser().parse_args(argv)
    try:
        state, diff = capture_state(arguments.repo, arguments.pr, arguments.cycle)
        payloads = {"json": canonical_json_bytes(state) + b"\n"}
        if arguments.write_diff:
            payloads["diff"] = diff
        paths = write_artifact_set(
            arguments.snapshot_dir,
            arguments.name,
            payloads,
            forbidden_roots=[Path(arguments.workspace_root)],
        )
    except (CaptureError, OSError, UnicodeError, ValueError) as error:
        sys.stderr.write(f"error: {error}\n")
        return 1

    summary = {
        "kind": state["kind"],
        "cycle": state["cycle"],
        "repository": state["repository"],
        "number": state["number"],
        "base_oid": state["base_oid"],
        "head_oid": state["head_oid"],
        "snapshot_sha256": state["snapshot_sha256"],
        "diff_sha256": state["diff_sha256"],
        "remote_diff_may_be_incomplete": state["remote_diff_may_be_incomplete"],
        "remote_diff_limit_reasons": state["remote_diff_limit_reasons"],
        "artifact_paths": paths,
        "counts": {
            "commits": len(state["commits"]),
            "files": len(state["files"]),
            "closing_issues": len(state["closing_issues"]),
            "check_runs": len(state["check_runs"]),
            "statuses": len(state["statuses"]),
            "reviews": len(state["reviews"]),
            "review_threads": len(state["review_threads"]),
        },
    }
    sys.stdout.write(json.dumps(summary, sort_keys=True) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
