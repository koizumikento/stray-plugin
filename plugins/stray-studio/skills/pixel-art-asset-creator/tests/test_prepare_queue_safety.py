from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest
from PIL import Image

SKILL_DIR = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = SKILL_DIR / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from _run_safety import require_safe_managed_replacement  # noqa: E402


def run_script(name: str, *args: object) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    return subprocess.run(
        [sys.executable, str(SCRIPTS_DIR / name), *(str(arg) for arg in args)],
        capture_output=True,
        text=True,
        env=env,
        check=False,
    )


def prepare_run(tmp_path: Path) -> Path:
    run_dir = tmp_path / "run"
    result = run_script(
        "prepare_asset_run.py",
        "--asset-name",
        "Safety Test",
        "--output-dir",
        run_dir,
    )
    assert result.returncode == 0, result.stderr
    return run_dir


def load_manifest(run_dir: Path) -> dict[str, object]:
    return json.loads((run_dir / "imagegen-jobs.json").read_text(encoding="utf-8"))


def save_manifest(run_dir: Path, manifest: dict[str, object]) -> None:
    (run_dir / "imagegen-jobs.json").write_text(
        json.dumps(manifest, indent=2) + "\n",
        encoding="utf-8",
    )


def base_job(manifest: dict[str, object]) -> dict[str, object]:
    jobs = manifest["jobs"]
    assert isinstance(jobs, list) and isinstance(jobs[0], dict)
    return jobs[0]


def test_force_replacement_rejects_reference_inside_run(tmp_path: Path) -> None:
    run_dir = prepare_run(tmp_path)
    reference = run_dir / "references" / "self.png"
    Image.new("RGB", (4, 4), "red").save(reference)
    before = (run_dir / "asset_request.json").read_bytes()

    result = run_script(
        "prepare_asset_run.py",
        "--asset-name",
        "Replacement",
        "--output-dir",
        run_dir,
        "--reference",
        reference,
        "--force",
    )

    assert result.returncode != 0
    assert "contains its own reference image" in result.stderr
    assert reference.is_file()
    assert (run_dir / "asset_request.json").read_bytes() == before


def test_force_replacement_rejects_symlinked_run_destination(tmp_path: Path) -> None:
    run_dir = prepare_run(tmp_path)
    stale = run_dir / "stale.txt"
    stale.write_text("keep", encoding="utf-8")
    alias = tmp_path / "alias"
    alias.symlink_to(run_dir, target_is_directory=True)

    result = run_script(
        "prepare_asset_run.py",
        "--asset-name",
        "Replacement",
        "--output-dir",
        alias,
        "--force",
    )

    assert result.returncode != 0
    assert "must not contain symlink components" in result.stderr
    assert alias.is_symlink()
    assert stale.read_text(encoding="utf-8") == "keep"


def test_force_replacement_rejects_intermediate_symlink_component(tmp_path: Path) -> None:
    run_dir = prepare_run(tmp_path)
    stale = run_dir / "stale.txt"
    stale.write_text("keep", encoding="utf-8")
    alias = tmp_path / "alias"
    alias.symlink_to(run_dir, target_is_directory=True)
    disguised = alias / "prompts" / ".."

    result = run_script(
        "prepare_asset_run.py",
        "--asset-name",
        "Replacement",
        "--output-dir",
        disguised,
        "--force",
    )

    assert result.returncode != 0
    assert "must not contain symlink components" in result.stderr
    assert stale.read_text(encoding="utf-8") == "keep"


def test_default_output_rejects_symlinked_tmp_directory(tmp_path: Path) -> None:
    working = tmp_path / "working"
    outside = tmp_path / "outside"
    working.mkdir()
    outside.mkdir()
    (working / "tmp").symlink_to(outside, target_is_directory=True)
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"

    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPTS_DIR / "prepare_asset_run.py"),
            "--asset-name",
            "Safety Test",
        ],
        cwd=working,
        capture_output=True,
        text=True,
        env=env,
        check=False,
    )

    assert result.returncode != 0
    assert "must not contain symlink components" in result.stderr
    assert not list(outside.iterdir())


def test_queue_repair_rejects_repairs_symlink_without_data_loss(tmp_path: Path) -> None:
    run_dir = prepare_run(tmp_path)
    output = run_dir / "decoded" / "base.png"
    Image.new("RGBA", (4, 4), "red").save(output)
    manifest = load_manifest(run_dir)
    base_job(manifest)["status"] = "complete"
    save_manifest(run_dir, manifest)
    manifest_before = (run_dir / "imagegen-jobs.json").read_bytes()
    prompt_before = (run_dir / "prompts" / "base-asset.md").read_bytes()
    output_before = output.read_bytes()

    outside = tmp_path / "outside"
    outside.mkdir()
    (run_dir / "repairs").symlink_to(outside, target_is_directory=True)

    result = run_script("queue_asset_repairs.py", "--run-dir", run_dir)

    assert result.returncode != 0
    assert "escapes the asset run" in result.stderr or "symlink" in result.stderr
    assert not list(outside.iterdir())
    assert output.read_bytes() == output_before
    assert (run_dir / "imagegen-jobs.json").read_bytes() == manifest_before
    assert (run_dir / "prompts" / "base-asset.md").read_bytes() == prompt_before


def test_queue_repair_preflights_prompt_before_archiving(tmp_path: Path) -> None:
    run_dir = prepare_run(tmp_path)
    output = run_dir / "decoded" / "base.png"
    Image.new("RGBA", (4, 4), "red").save(output)
    manifest = load_manifest(run_dir)
    job = base_job(manifest)
    job["status"] = "complete"
    job["prompt_file"] = "asset_request.json"
    save_manifest(run_dir, manifest)
    manifest_before = (run_dir / "imagegen-jobs.json").read_bytes()
    output_before = output.read_bytes()

    result = run_script("queue_asset_repairs.py", "--run-dir", run_dir)

    assert result.returncode != 0
    assert "must stay below one of: prompts/" in result.stderr
    assert output.read_bytes() == output_before
    assert (run_dir / "imagegen-jobs.json").read_bytes() == manifest_before
    assert not (run_dir / "repairs").exists()


def test_managed_replacement_refuses_current_worktree_ancestor() -> None:
    with pytest.raises(SystemExit, match="protected directory"):
        require_safe_managed_replacement(Path.cwd().parent)
