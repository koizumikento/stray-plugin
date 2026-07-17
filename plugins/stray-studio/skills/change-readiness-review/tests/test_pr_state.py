from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest


SKILL_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = SKILL_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))
SPEC = importlib.util.spec_from_file_location(
    "capture_pr_state_under_test", SCRIPTS / "capture_pr_state.py"
)
assert SPEC and SPEC.loader
capture_pr = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(capture_pr)


BASE = "a" * 40
HEAD = "b" * 40


def pull(*, comments: int = 0, review_comments: int = 0) -> dict[str, object]:
    return {
        "state": "open",
        "number": 7,
        "base": {"sha": BASE, "ref": "main"},
        "head": {"sha": HEAD, "ref": "feature"},
        "commits": 1,
        "changed_files": 1,
        "comments": comments,
        "review_comments": review_comments,
        "html_url": "https://github.com/example/repo/pull/7",
        "user": {"login": "author"},
        "draft": True,
        "title": "Change",
        "body": "Implements the requirement.",
        "updated_at": "2026-07-16T00:00:00Z",
    }


def commit() -> dict[str, object]:
    return {
        "sha": HEAD,
        "commit": {"message": "Implement change"},
        "parents": [{"sha": BASE}],
    }


def changed_file(*, patch: str | None = "@@ -1 +1 @@\n-old\n+new") -> dict[str, object]:
    return {
        "filename": "src/app.py",
        "previous_filename": None,
        "status": "modified",
        "additions": 1,
        "deletions": 1,
        "changes": 2,
        "patch": patch,
    }


def check_run(*, head: str = HEAD) -> dict[str, object]:
    return {
        "id": 10,
        "name": "tests",
        "head_sha": head,
        "status": "completed",
        "conclusion": "success",
        "details_url": "https://github.com/example/repo/actions/runs/1",
    }


def status() -> dict[str, object]:
    return {
        "id": 20,
        "context": "lint",
        "state": "success",
        "description": "passed",
        "target_url": "https://example.test/lint",
        "created_at": "2026-07-16T00:00:00Z",
        "sha": HEAD,
    }


def install_api(
    monkeypatch: pytest.MonkeyPatch,
    *,
    pr: dict[str, object],
    check_head: str = HEAD,
    patch: str | None = "@@ -1 +1 @@\n-old\n+new",
) -> list[str]:
    calls: list[str] = []

    def fake_json(endpoint: str, *, paginate: bool = False):
        calls.append(endpoint)
        if endpoint == "repos/example/repo/pulls/7":
            return pr
        if "/commits?" in endpoint:
            return [[commit()]]
        if "/files?" in endpoint:
            return [[changed_file(patch=patch)]]
        if "/check-runs?" in endpoint:
            return [{"total_count": 1, "check_runs": [check_run(head=check_head)]}]
        if "/statuses/" in endpoint:
            return [[status()]]
        if "/reviews?" in endpoint:
            return [
                [
                    {
                        "id": 30,
                        "user": {"login": "reviewer"},
                        "state": "CHANGES_REQUESTED",
                        "body": "Please handle the failure.",
                        "commit_id": HEAD,
                        "submitted_at": "2026-07-16T00:01:00Z",
                    }
                ]
            ]
        if "/issues/7/comments?" in endpoint:
            return [
                [
                    {
                        "id": 40,
                        "user": {"login": "author"},
                        "body": "Fixed.",
                        "created_at": "2026-07-16T00:02:00Z",
                        "updated_at": "2026-07-16T00:02:00Z",
                    }
                ]
            ]
        if "/pulls/7/comments?" in endpoint:
            return [
                [
                    {
                        "id": 50,
                        "user": {"login": "reviewer"},
                        "body": "This still fails.",
                        "created_at": "2026-07-16T00:03:00Z",
                        "updated_at": "2026-07-16T00:03:00Z",
                        "path": "src/app.py",
                        "line": 1,
                        "original_line": 1,
                        "commit_id": HEAD,
                        "in_reply_to_id": None,
                    }
                ]
            ]
        raise AssertionError(f"unexpected endpoint: {endpoint}")

    monkeypatch.setattr(capture_pr, "_gh_json", fake_json)
    monkeypatch.setattr(
        capture_pr,
        "_gh_diff",
        lambda endpoint: b"diff --git a/src/app.py b/src/app.py\n@@ -1 +1 @@\n-old\n+new\n",
    )
    monkeypatch.setattr(
        capture_pr,
        "_closing_issues",
        lambda *_args: [
            {
                "number": 11,
                "url": "https://github.com/example/repo/issues/11",
                "title": "Requirement",
                "body": "Acceptance criteria",
                "state": "OPEN",
                "updatedAt": "2026-07-16T00:00:00Z",
                "repository": {"nameWithOwner": "example/repo"},
            }
        ],
    )
    return calls


def test_initial_capture_binds_checks_and_skips_feedback(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls = install_api(monkeypatch, pr=pull())
    monkeypatch.setattr(
        capture_pr,
        "_review_threads",
        lambda *_args: (_ for _ in ()).throw(
            AssertionError("feedback should be skipped")
        ),
    )

    state, diff = capture_pr.capture_state("example/repo", 7, "initial")

    assert state["kind"] == "PR_REVIEW_REQUEST"
    assert state["head_oid"] == HEAD
    assert state["check_runs"][0]["head_oid"] == HEAD
    assert state["reviews"] == []
    assert state["review_threads"] == []
    assert state["closing_issues"][0]["number"] == 11
    assert state["remote_diff_may_be_incomplete"] is False
    assert diff.startswith(b"diff --git")
    assert not any("/reviews?" in endpoint for endpoint in calls)


def test_rerequest_capture_includes_feedback_and_thread_state(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    install_api(monkeypatch, pr=pull(comments=1, review_comments=1))
    monkeypatch.setattr(
        capture_pr,
        "_review_threads",
        lambda *_args: [
            {
                "id": "thread-1",
                "isResolved": False,
                "isOutdated": False,
                "path": "src/app.py",
                "line": 1,
                "originalLine": 1,
                "comments": {
                    "nodes": [
                        {
                            "databaseId": 60,
                            "body": "Still failing.",
                            "createdAt": "2026-07-16T00:04:00Z",
                            "updatedAt": "2026-07-16T00:04:00Z",
                            "url": "https://github.com/example/repo/pull/7#discussion_r60",
                            "author": {"login": "reviewer"},
                        }
                    ],
                    "pageInfo": {"hasNextPage": False},
                },
            }
        ],
    )

    state, _diff = capture_pr.capture_state("example/repo", 7, "rerequest")

    assert state["reviews"][0]["state"] == "CHANGES_REQUESTED"
    assert state["issue_comments"][0]["body"] == "Fixed."
    assert state["review_comments"][0]["path"] == "src/app.py"
    assert state["review_threads"][0]["is_resolved"] is False


def test_rejects_check_run_from_old_head(monkeypatch: pytest.MonkeyPatch) -> None:
    install_api(monkeypatch, pr=pull(), check_head="c" * 40)

    with pytest.raises(capture_pr.CaptureError, match="different head OID"):
        capture_pr.capture_state("example/repo", 7, "initial")


def test_flags_missing_textual_patch_as_incomplete_remote_diff(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    install_api(monkeypatch, pr=pull(), patch=None)

    state, _diff = capture_pr.capture_state("example/repo", 7, "initial")

    assert state["remote_diff_may_be_incomplete"] is True
    assert "file_without_textual_patch" in state["remote_diff_limit_reasons"]


def test_rejects_incomplete_paginated_file_list(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    metadata = pull()
    metadata["changed_files"] = 2
    install_api(monkeypatch, pr=metadata)

    with pytest.raises(capture_pr.CaptureError, match="incomplete files"):
        capture_pr.capture_state("example/repo", 7, "initial")


def test_keeps_only_latest_status_per_context() -> None:
    old = capture_pr._normalize_status(
        {
            **status(),
            "id": 19,
            "state": "failure",
            "created_at": "2026-07-15T23:00:00Z",
        },
        HEAD,
    )
    new = capture_pr._normalize_status(status(), HEAD)

    assert capture_pr._latest_statuses([new, old]) == [new]


def test_cli_writes_private_snapshot_and_diff_outside_workspace(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    snapshot_dir = tmp_path / "snapshots"
    snapshot_dir.mkdir(mode=0o700)
    state = {
        "kind": "PR_REVIEW_REQUEST",
        "cycle": "initial",
        "repository": "example/repo",
        "number": 7,
        "base_oid": BASE,
        "head_oid": HEAD,
        "snapshot_sha256": "d" * 64,
        "diff_sha256": "e" * 64,
        "remote_diff_may_be_incomplete": False,
        "remote_diff_limit_reasons": [],
        "commits": [],
        "files": [],
        "closing_issues": [],
        "check_runs": [],
        "statuses": [],
        "reviews": [],
        "review_threads": [],
    }
    monkeypatch.setattr(
        capture_pr, "capture_state", lambda *_args: (state, b"exact diff\n")
    )

    result = capture_pr.main(
        [
            "--repo",
            "example/repo",
            "--pr",
            "7",
            "--cycle",
            "initial",
            "--workspace-root",
            str(workspace),
            "--snapshot-dir",
            str(snapshot_dir),
            "--name",
            "initial",
            "--write-diff",
        ]
    )

    assert result == 0
    assert (snapshot_dir / "initial.json").is_file()
    assert (snapshot_dir / "initial.diff").read_bytes() == b"exact diff\n"
    assert (snapshot_dir / "initial.json").stat().st_mode & 0o077 == 0
    assert (snapshot_dir / "initial.diff").stat().st_mode & 0o077 == 0
