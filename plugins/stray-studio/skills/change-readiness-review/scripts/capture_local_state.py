#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import stat
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import Any

from _snapshot_common import (
    CaptureError,
    canonical_json_bytes,
    run_checked,
    run_result,
    seal_state,
    sha256_bytes,
    write_artifact_set,
)


_OID_RE = re.compile(r"(?:[0-9a-f]{40}|[0-9a-f]{64})")
_READ_SIZE = 1024 * 1024


def _git(repo: Path, *arguments: str) -> bytes:
    return run_checked(
        ["git", "-c", "core.fsmonitor=false", "-C", str(repo), *arguments],
        label=f"git {arguments[0] if arguments else 'command'}",
    )


def _git_result(repo: Path, *arguments: str):
    return run_result(
        ["git", "-c", "core.fsmonitor=false", "-C", str(repo), *arguments]
    )


def _repository_root(repo_argument: str) -> Path:
    candidate = Path(repo_argument).expanduser().resolve()
    raw = _git(candidate, "rev-parse", "--path-format=absolute", "--show-toplevel")
    value = os.fsdecode(raw.rstrip(b"\n"))
    if not value:
        raise CaptureError("Git returned an empty repository root")
    return Path(value).resolve(strict=True)


def _resolve_commit(repo: Path, revision: str, *, label: str) -> str:
    if not revision:
        raise CaptureError(f"{label} must not be empty")
    raw = _git(
        repo,
        "rev-parse",
        "--verify",
        "--end-of-options",
        f"{revision}^{{commit}}",
    ).rstrip(b"\n")
    value = raw.decode("ascii", "strict")
    if not _OID_RE.fullmatch(value):
        raise CaptureError(f"Git returned an invalid OID for {label}")
    return value


def _merge_base(repo: Path, base_oid: str, head_oid: str) -> str:
    values = _git(repo, "merge-base", "--all", base_oid, head_oid).splitlines()
    if len(values) != 1:
        if not values:
            raise CaptureError("the base and HEAD do not have a common ancestor")
        raise CaptureError("the base and HEAD have multiple merge bases")
    value = values[0].decode("ascii", "strict")
    if not _OID_RE.fullmatch(value):
        raise CaptureError("Git returned an invalid merge-base OID")
    return value


def _branch(repo: Path) -> str | None:
    result = _git_result(repo, "symbolic-ref", "--quiet", "--short", "HEAD")
    if result.returncode == 1:
        return None
    if result.returncode != 0:
        raise CaptureError("cannot resolve the current branch")
    return os.fsdecode(result.stdout.rstrip(b"\n"))


def _safe_paths(raw: bytes, *, label: str) -> list[bytes]:
    if not raw:
        return []
    if not raw.endswith(b"\0"):
        raise CaptureError(f"Git returned a malformed {label} path list")
    values = raw[:-1].split(b"\0")
    if any(not value for value in values) or len(values) != len(set(values)):
        raise CaptureError(f"Git returned an invalid {label} path list")
    for value in values:
        if value.startswith(b"/") or b".." in value.split(b"/"):
            raise CaptureError(f"Git returned an unsafe {label} path")
    return sorted(values)


def _diff_paths(repo: Path, *arguments: str, label: str) -> list[bytes]:
    raw = _git(
        repo,
        "diff",
        "--name-only",
        "-z",
        "--no-renames",
        "--no-ext-diff",
        "--no-textconv",
        *arguments,
        "--",
    )
    return _safe_paths(raw, label=label)


def _untracked_paths(repo: Path) -> list[bytes]:
    raw = _git(
        repo,
        "ls-files",
        "--others",
        "--exclude-standard",
        "-z",
        "--",
    )
    return _safe_paths(raw, label="untracked")


def _file_record(repo: Path, relative: bytes) -> dict[str, Any]:
    absolute = os.path.join(os.fsencode(repo), relative)
    try:
        initial = os.lstat(absolute)
    except FileNotFoundError:
        return {"path": os.fsdecode(relative), "kind": "missing"}
    except OSError as error:
        raise CaptureError(
            f"cannot inspect changed path {os.fsdecode(relative)!r}: {error}"
        ) from error

    base = {
        "path": os.fsdecode(relative),
        "mode": stat.S_IMODE(initial.st_mode),
        "size": initial.st_size,
        "mtime_ns": initial.st_mtime_ns,
    }
    if stat.S_ISLNK(initial.st_mode):
        target = os.readlink(absolute)
        final = os.lstat(absolute)
        if (initial.st_ino, initial.st_mtime_ns, initial.st_size) != (
            final.st_ino,
            final.st_mtime_ns,
            final.st_size,
        ):
            raise CaptureError(f"changed path moved while capturing: {base['path']!r}")
        return {
            **base,
            "kind": "symlink",
            "target_sha256": sha256_bytes(
                target if isinstance(target, bytes) else os.fsencode(target)
            ),
        }
    if stat.S_ISDIR(initial.st_mode):
        return {**base, "kind": "directory"}
    if not stat.S_ISREG(initial.st_mode):
        raise CaptureError(f"unsupported changed file type: {base['path']!r}")

    flags = os.O_RDONLY
    if hasattr(os, "O_CLOEXEC"):
        flags |= os.O_CLOEXEC
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    descriptor = os.open(absolute, flags)
    try:
        opened = os.fstat(descriptor)
        if (initial.st_dev, initial.st_ino) != (opened.st_dev, opened.st_ino):
            raise CaptureError(f"changed path moved while opening: {base['path']!r}")
        hasher = hashlib.sha256()
        while True:
            chunk = os.read(descriptor, _READ_SIZE)
            if not chunk:
                break
            hasher.update(chunk)
        final = os.fstat(descriptor)
        if (opened.st_size, opened.st_mtime_ns) != (
            final.st_size,
            final.st_mtime_ns,
        ):
            raise CaptureError(f"changed path changed while reading: {base['path']!r}")
    finally:
        os.close(descriptor)
    return {**base, "kind": "file", "content_sha256": hasher.hexdigest()}


def _paths_fingerprint(repo: Path, paths: Sequence[bytes], *, domain: str) -> str:
    records = [_file_record(repo, value) for value in sorted(paths)]
    hasher = hashlib.sha256()
    hasher.update(domain.encode("ascii"))
    hasher.update(b"\0")
    hasher.update(canonical_json_bytes(records))
    return hasher.hexdigest()


def _gitlinks(index_state: bytes) -> set[bytes]:
    if index_state and not index_state.endswith(b"\0"):
        raise CaptureError("Git returned a malformed index state")
    values: set[bytes] = set()
    for record in index_state[:-1].split(b"\0") if index_state else ():
        try:
            metadata, path = record.split(b"\t", 1)
            mode, _oid, _stage = metadata.split(b" ")
        except ValueError as error:
            raise CaptureError("Git returned a malformed index entry") from error
        if mode == b"160000":
            values.add(path)
    return values


def capture_state(repo_argument: str, base: str) -> dict[str, Any]:
    repo = _repository_root(repo_argument)
    base_ref_oid = _resolve_commit(repo, base, label="--base")
    head_oid = _resolve_commit(repo, "HEAD", label="HEAD")
    base_oid = _merge_base(repo, base_ref_oid, head_oid)

    committed = _diff_paths(repo, f"{base_oid}..{head_oid}", label="committed")
    staged = _diff_paths(repo, "--cached", "HEAD", label="staged")
    unstaged = _diff_paths(repo, label="unstaged")
    untracked = _untracked_paths(repo)
    index_state = _git(repo, "ls-files", "--stage", "-z", "--")
    commits = _git(
        repo, "rev-list", "--reverse", "--topo-order", f"{base_oid}..{head_oid}"
    )
    gitlinks = _gitlinks(index_state)
    changed_gitlinks = sorted(gitlinks.intersection(set(committed + staged + unstaged)))

    state = {
        "kind": "LOCAL_PUSH",
        "repository_root": str(repo),
        "branch": _branch(repo),
        "base_ref": base,
        "base_ref_oid": base_ref_oid,
        "base_oid": base_oid,
        "head_oid": head_oid,
        "commits_sha256": sha256_bytes(commits),
        "index_sha256": sha256_bytes(index_state),
        "tracked_worktree_sha256": _paths_fingerprint(
            repo, unstaged, domain="change-readiness-tracked-v1"
        ),
        "untracked_sha256": _paths_fingerprint(
            repo, untracked, domain="change-readiness-untracked-v1"
        ),
        "committed_files": [os.fsdecode(value) for value in committed],
        "staged_files": [os.fsdecode(value) for value in staged],
        "unstaged_files": [os.fsdecode(value) for value in unstaged],
        "untracked_files": [os.fsdecode(value) for value in untracked],
        "changed_gitlinks": [os.fsdecode(value) for value in changed_gitlinks],
        "coverage_gaps": (
            ["changed_gitlink_requires_separate_repository_review"]
            if changed_gitlinks
            else []
        ),
    }
    return seal_state(state, domain="change-readiness-local-snapshot-v1")


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Capture a read-only fingerprint of local Git push state."
    )
    parser.add_argument("--repo", default=".")
    parser.add_argument("--base", required=True)
    parser.add_argument("--snapshot-dir", required=True)
    parser.add_argument("--name", required=True)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    arguments = _parser().parse_args(argv)
    try:
        state = capture_state(arguments.repo, arguments.base)
        root = Path(state["repository_root"])
        paths = write_artifact_set(
            arguments.snapshot_dir,
            arguments.name,
            {"json": canonical_json_bytes(state) + b"\n"},
            forbidden_roots=[root],
        )
    except (CaptureError, OSError, UnicodeError, ValueError) as error:
        sys.stderr.write(f"error: {error}\n")
        return 1

    summary = {
        "kind": state["kind"],
        "base_ref": state["base_ref"],
        "base_oid": state["base_oid"],
        "head_oid": state["head_oid"],
        "snapshot_sha256": state["snapshot_sha256"],
        "snapshot_path": paths["json"],
        "counts": {
            "committed": len(state["committed_files"]),
            "staged": len(state["staged_files"]),
            "unstaged": len(state["unstaged_files"]),
            "untracked": len(state["untracked_files"]),
            "changed_gitlinks": len(state["changed_gitlinks"]),
        },
    }
    sys.stdout.write(json.dumps(summary, sort_keys=True) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
