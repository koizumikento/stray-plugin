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


def test_prepare_preserves_names_and_stable_ids_from_another_workspace(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    monkeypatch.chdir(workspace)
    asset_ids = []
    for index, name in enumerate(("招き猫", "招き猫", "Lucky Cat")):
        run_dir = workspace / f"run-{index}"
        result = run_script(
            "prepare_asset_run.py", "--asset-name", name, "--output-dir", run_dir
        )
        assert result.returncode == 0, result.stderr
        request = json.loads((run_dir / "asset_request.json").read_text(encoding="utf-8"))
        assert request["display_name"] == name
        assert name in (run_dir / "prompts/base-asset.md").read_text(encoding="utf-8")
        assert request["asset_id"] == load_manifest(run_dir)["asset_id"]
        asset_ids.append(request["asset_id"])

    assert asset_ids[0] == asset_ids[1]
    assert asset_ids[0].startswith("asset-")
    assert asset_ids[0].isascii() and asset_ids[0].replace("-", "").isalnum()
    assert asset_ids[2] == "lucky-cat"
    assert {path.name for path in workspace.iterdir()} == {"run-0", "run-1", "run-2"}


def test_prepare_still_rejects_names_without_letters_or_digits(tmp_path: Path) -> None:
    run_dir = tmp_path / "run"
    result = run_script(
        "prepare_asset_run.py", "--asset-name", "../!!!", "--output-dir", run_dir
    )
    assert result.returncode != 0
    assert "asset name must contain at least one letter or digit" in result.stderr
    assert not run_dir.exists()


@pytest.mark.parametrize(
    ("background", "key", "motion"),
    [
        ("chroma-key", "#00ff00", "loop: walking right with alternating foot contact"),
        ("transparent", "#FF00FF", "single action: crouch, jump to apex, descend, land"),
    ],
)
def test_prepare_animation_preserves_visual_contract(
    tmp_path: Path, background: str, key: str, motion: str
) -> None:
    run_dir = tmp_path / "animation"
    result = run_script(
        "prepare_asset_run.py",
        "--asset-name", "Pink Cat",
        "--description", "A pink cat with purple eyes",
        "--sheet-structure", "sprite-row",
        "--target-size", "32x48",
        "--frame-count", "6",
        "--motion-beats", motion,
        "--background", background,
        "--chroma-key", key,
        "--output-dir", run_dir,
    )
    assert result.returncode == 0, result.stderr
    request = json.loads((run_dir / "asset_request.json").read_text(encoding="utf-8"))
    assert request["background"] == {"strategy": background, "chroma_key": key.upper()}
    assert request["sheet"]["used_cells"] == 6
    assert (request["sheet"]["width"], request["sheet"]["height"]) == (192, 48)
    base = (run_dir / "prompts/base-asset.md").read_text(encoding="utf-8")
    sheet = (run_dir / "prompts/asset-sheet.md").read_text(encoding="utf-8")
    assert "pink cat with purple eyes" in base
    assert "6 animation frames" in sheet and "32x48" in sheet
    assert motion in sheet
    assert "body scale, pixel size" in sheet
    assert "shared baseline for ground contact" in sheet
    assert "preserve intentional jump height" in sheet
    assert "clear background gaps" in sheet
    assert request["sheet"]["extraction"] == "components"
    assert "without forcing a return to the first pose" in sheet
    assert "honor the action's specified position changes" in sheet
    assert "complete centered pose" not in sheet
    for prompt in (base, sheet):
        if background == "transparent":
            assert "clean transparent background" in prompt
            assert "chroma-key background" not in prompt and key not in prompt
        else:
            assert key.upper() in prompt
            assert "subject's reference colors preserved" in prompt
    job = load_manifest(run_dir)["jobs"][1]
    assert job["depends_on"] == ["base"]
    assert job["input_images"][-1]["path"] == "references/canonical-base.png"
    assert job["status"] == "pending"
    assert not list((run_dir / "decoded").iterdir())
    repair = run_script("queue_asset_repairs.py", "--run-dir", run_dir)
    assert repair.returncode == 0, repair.stderr
    repaired = (run_dir / "prompts/asset-sheet.md").read_text(encoding="utf-8")
    assert motion in repaired
    repair_note = repaired.split("Repair attempt 1:", 1)[1]
    assert "honor the action's specified position changes" in repair_note
    assert "complete centered asset" not in repair_note


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


def test_default_output_rejects_symlinked_output_directory(tmp_path: Path) -> None:
    working = tmp_path / "working"
    outside = tmp_path / "outside"
    working.mkdir()
    outside.mkdir()
    (working / "output").symlink_to(outside, target_is_directory=True)
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
