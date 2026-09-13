from __future__ import annotations

import json
import importlib.util
import os
import subprocess
import sys
from pathlib import Path

import pytest
from filesystem_support import assert_private_file, make_symlink


SKILL_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = SKILL_ROOT / "scripts" / "capture_local_state.py"
COMMON_SPEC = importlib.util.spec_from_file_location(
    "snapshot_common_under_test", SKILL_ROOT / "scripts" / "_snapshot_common.py"
)
assert COMMON_SPEC and COMMON_SPEC.loader
snapshot_common = importlib.util.module_from_spec(COMMON_SPEC)
COMMON_SPEC.loader.exec_module(snapshot_common)
CaptureError = snapshot_common.CaptureError
write_artifact_set = snapshot_common.write_artifact_set


def run(command: list[str], *, cwd: Path) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        command,
        cwd=cwd,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def git(repo: Path, *arguments: str) -> bytes:
    result = run(["git", *arguments], cwd=repo)
    assert result.returncode == 0, result.stderr.decode("utf-8", "backslashreplace")
    return result.stdout


def make_repo(tmp_path: Path) -> tuple[Path, str]:
    repo = tmp_path / "repo"
    repo.mkdir()
    git(repo, "init", "-b", "main")
    git(repo, "config", "user.name", "Test User")
    git(repo, "config", "user.email", "test@example.com")
    (repo / "tracked.txt").write_text("initial\n", encoding="utf-8")
    git(repo, "add", "tracked.txt")
    git(repo, "commit", "-m", "initial")
    return repo, git(repo, "rev-parse", "HEAD").strip().decode("ascii")


def capture(
    repo: Path,
    snapshot_dir: Path,
    *,
    base: str,
    name: str,
) -> subprocess.CompletedProcess[bytes]:
    return run(
        [
            sys.executable,
            str(SCRIPT),
            "--repo",
            str(repo),
            "--base",
            base,
            "--snapshot-dir",
            str(snapshot_dir),
            "--name",
            name,
        ],
        cwd=repo,
    )


def test_clean_capture_is_read_only_deterministic_and_private(tmp_path: Path) -> None:
    repo, initial_oid = make_repo(tmp_path)
    snapshot_dir = tmp_path / "snapshots"
    snapshot_dir.mkdir(mode=0o700)
    before = git(repo, "status", "--porcelain=v1", "-z", "--untracked-files=all")

    first = capture(repo, snapshot_dir, base=initial_oid, name="initial")
    second = capture(repo, snapshot_dir, base=initial_oid, name="final")

    assert first.returncode == 0, first.stderr
    assert second.returncode == 0, second.stderr
    first_state = json.loads((snapshot_dir / "initial.json").read_text())
    second_state = json.loads((snapshot_dir / "final.json").read_text())
    assert first_state == second_state
    assert first_state["base_ref_oid"] == initial_oid
    assert first_state["base_oid"] == initial_oid
    assert first_state["head_oid"] == initial_oid
    assert first_state["committed_files"] == []
    assert first_state["staged_files"] == []
    assert first_state["unstaged_files"] == []
    assert first_state["untracked_files"] == []
    assert_private_file(snapshot_dir / "initial.json")
    after = git(repo, "status", "--porcelain=v1", "-z", "--untracked-files=all")
    assert after == before


def test_capture_distinguishes_outgoing_and_local_state(tmp_path: Path) -> None:
    repo, initial_oid = make_repo(tmp_path)
    snapshot_dir = tmp_path / "snapshots"
    snapshot_dir.mkdir(mode=0o700)

    (repo / "tracked.txt").write_text("outgoing\n", encoding="utf-8")
    git(repo, "add", "tracked.txt")
    git(repo, "commit", "-m", "outgoing")
    (repo / "tracked.txt").write_text("outgoing plus local\n", encoding="utf-8")
    (repo / "staged.txt").write_text("staged\n", encoding="utf-8")
    git(repo, "add", "staged.txt")
    (repo / "untracked.txt").write_text("untracked\n", encoding="utf-8")

    first = capture(repo, snapshot_dir, base=initial_oid, name="initial")
    assert first.returncode == 0, first.stderr
    first_state = json.loads((snapshot_dir / "initial.json").read_text())
    assert first_state["committed_files"] == ["tracked.txt"]
    assert first_state["staged_files"] == ["staged.txt"]
    assert first_state["unstaged_files"] == ["tracked.txt"]
    assert first_state["untracked_files"] == ["untracked.txt"]

    (repo / "untracked.txt").write_text("changed during review\n", encoding="utf-8")
    second = capture(repo, snapshot_dir, base=initial_oid, name="final")
    assert second.returncode == 0, second.stderr
    second_state = json.loads((snapshot_dir / "final.json").read_text())
    assert second_state["untracked_sha256"] != first_state["untracked_sha256"]
    assert second_state["snapshot_sha256"] != first_state["snapshot_sha256"]


def test_refuses_repository_internal_or_symlink_snapshot_directory(
    tmp_path: Path,
) -> None:
    repo, initial_oid = make_repo(tmp_path)
    internal = repo / "snapshots"
    internal.mkdir()

    internal_result = capture(repo, internal, base=initial_oid, name="initial")
    assert internal_result.returncode == 1
    assert b"outside the protected root" in internal_result.stderr
    assert not (internal / "initial.json").exists()

    external = tmp_path / "external"
    external.mkdir()
    symlink = tmp_path / "snapshot-link"
    make_symlink(symlink, external, target_is_directory=True)
    symlink_result = capture(repo, symlink, base=initial_oid, name="initial")
    assert symlink_result.returncode == 1
    assert b"must not be a symlink" in symlink_result.stderr


def test_refuses_overwrite_and_preserves_existing_artifact(tmp_path: Path) -> None:
    repo, initial_oid = make_repo(tmp_path)
    snapshot_dir = tmp_path / "snapshots"
    snapshot_dir.mkdir(mode=0o700)
    existing = snapshot_dir / "initial.json"
    existing.write_bytes(b"existing")

    result = capture(repo, snapshot_dir, base=initial_oid, name="initial")

    assert result.returncode == 1
    assert b"refusing to overwrite" in result.stderr
    assert existing.read_bytes() == b"existing"


def test_untracked_symlink_target_changes_snapshot_without_following_target(
    tmp_path: Path,
) -> None:
    repo, initial_oid = make_repo(tmp_path)
    snapshot_dir = tmp_path / "snapshots"
    snapshot_dir.mkdir(mode=0o700)
    outside = tmp_path / "outside-secret.txt"
    outside.write_text("secret value never read\n", encoding="utf-8")
    link = repo / "link"
    make_symlink(link, outside)

    first = capture(repo, snapshot_dir, base=initial_oid, name="initial")
    assert first.returncode == 0, first.stderr
    first_state = json.loads((snapshot_dir / "initial.json").read_text())
    outside.write_text("changed secret content\n", encoding="utf-8")
    second = capture(repo, snapshot_dir, base=initial_oid, name="final")
    assert second.returncode == 0, second.stderr
    second_state = json.loads((snapshot_dir / "final.json").read_text())
    assert second_state["untracked_sha256"] == first_state["untracked_sha256"]


def test_snapshot_file_has_no_group_or_other_permissions(tmp_path: Path) -> None:
    repo, initial_oid = make_repo(tmp_path)
    snapshot_dir = tmp_path / "snapshots"
    snapshot_dir.mkdir(mode=0o777)

    result = capture(repo, snapshot_dir, base=initial_oid, name="initial")

    assert result.returncode == 0, result.stderr
    assert_private_file(snapshot_dir / "initial.json")


def test_artifact_set_preflights_all_targets_before_writing(tmp_path: Path) -> None:
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    snapshot_dir = tmp_path / "snapshots"
    snapshot_dir.mkdir(mode=0o700)
    existing_diff = snapshot_dir / "initial.diff"
    existing_diff.write_bytes(b"existing diff")

    with pytest.raises(CaptureError, match="refusing to overwrite"):
        write_artifact_set(
            str(snapshot_dir),
            "initial",
            {"json": b"{}\n", "diff": b"new diff"},
            forbidden_roots=[workspace],
        )

    assert not (snapshot_dir / "initial.json").exists()
    assert existing_diff.read_bytes() == b"existing diff"


def test_artifact_name_rejects_path_traversal(tmp_path: Path) -> None:
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    snapshot_dir = tmp_path / "snapshots"
    snapshot_dir.mkdir(mode=0o700)

    with pytest.raises(CaptureError, match="--name"):
        write_artifact_set(
            str(snapshot_dir),
            "../escape",
            {"json": b"{}\n"},
            forbidden_roots=[workspace],
        )

    assert list(snapshot_dir.iterdir()) == []


def test_artifact_bytes_and_permissions_before_payload(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    snapshot_dir = tmp_path / "日本語 ' [snapshots]"
    snapshot_dir.mkdir()
    target = snapshot_dir / "initial.diff"
    payload = b"LF\nCRLF\r\nNUL\x00EOF\x1a\xff\n"
    original_write = os.write

    def inspect_write(descriptor: int, data: memoryview) -> int:
        assert_private_file(target)
        return original_write(descriptor, data)

    monkeypatch.setattr(snapshot_common.os, "write", inspect_write)
    write_artifact_set(str(snapshot_dir), "initial", {"diff": payload}, forbidden_roots=[])
    assert target.read_bytes() == payload


def test_failed_write_removes_only_created_artifacts(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    keep = tmp_path / "keep.txt"
    keep.write_bytes(b"existing")
    original_write = os.write
    calls = 0

    def fail_second_write(descriptor: int, data: memoryview) -> int:
        nonlocal calls
        calls += 1
        if calls == 2:
            raise OSError("disk write failed")
        return original_write(descriptor, data)

    monkeypatch.setattr(snapshot_common.os, "write", fail_second_write)
    with pytest.raises(OSError, match="disk write failed"):
        write_artifact_set(str(tmp_path), "initial", {"json": b"{}", "diff": b"diff"},
                           forbidden_roots=[])
    assert list(tmp_path.iterdir()) == [keep]
    assert keep.read_bytes() == b"existing"


@pytest.mark.skipif(os.name != "nt", reason="Windows exclusive ACL creation")
def test_acl_creation_collision_preserves_existing_file_and_rolls_back(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    original_create = snapshot_common.create_private_windows_file

    def race_create(target: Path) -> None:
        if target.suffix == ".diff":
            target.write_bytes(b"created by another writer")
        original_create(target)

    monkeypatch.setattr(snapshot_common, "create_private_windows_file", race_create)
    with pytest.raises(CaptureError, match="private Windows artifact creation failed"):
        write_artifact_set(str(tmp_path), "initial", {"json": b"{}", "diff": b"private"},
                           forbidden_roots=[])
    assert not (tmp_path / "initial.json").exists()
    assert (tmp_path / "initial.diff").read_bytes() == b"created by another writer"


def test_option_like_base_is_not_executed_as_a_git_option(tmp_path: Path) -> None:
    repo, _initial_oid = make_repo(tmp_path)
    snapshot_dir = tmp_path / "snapshots"
    snapshot_dir.mkdir(mode=0o700)

    result = capture(repo, snapshot_dir, base="--help", name="initial")

    assert result.returncode != 0
    assert not (snapshot_dir / "initial.json").exists()
    assert b"usage: git" not in (result.stdout + result.stderr).lower()
