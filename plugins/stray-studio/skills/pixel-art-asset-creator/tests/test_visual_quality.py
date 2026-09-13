from __future__ import annotations

import hashlib
import json

import pytest
import sys
from pathlib import Path

from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from inspect_asset_cells import contact_anchor, inspect_cell, registration_warnings
from test_output_pipeline_safety import run_script, write_json


def test_fringe_warning_and_opaque_checker_failure(tmp_path: Path) -> None:
    image = Image.new("RGBA", (16, 16))
    ImageDraw.Draw(image).rectangle((4, 3, 11, 13), fill=(110, 70, 50, 255))
    image.putpixel((3, 5), (25, 180, 20, 255))
    path = tmp_path / "cell.png"
    image.save(path)
    row, _ = inspect_cell(path, index=0, expected_size=(16, 16), min_used_pixels=20,
                          edge_padding=1, chroma_key=(0, 255, 0))
    assert row["ok"] and row["key_colored_edge_pixels"] == 1
    assert any("chroma fringe" in warning for warning in row["warnings"])
    for y in range(16):
        for x in range(16):
            image.putpixel((x, y), ((180 if (x+y) % 2 else 255),) * 3 + (255,))
    image.save(path)
    row, _ = inspect_cell(path, index=0, expected_size=(16, 16), min_used_pixels=20, edge_padding=1)
    assert not row["ok"] and "fully opaque" in row["errors"][0]


def test_contact_anchor_ignores_hair_width_and_preserves_travel() -> None:
    image = Image.new("RGBA", (20, 20))
    draw = ImageDraw.Draw(image)
    draw.rectangle((8, 10, 11, 17), fill="brown")
    anchor = contact_anchor(image)
    draw.rectangle((0, 2, 19, 7), fill="yellow")
    assert contact_anchor(image) == anchor == (9.5, 17)
    rows = [{"contact_anchor": anchor}, {"contact_anchor": (12.5, 14)}]
    assert registration_warnings(rows, "fixed")
    assert not registration_warnings(rows, "free")
    assert not registration_warnings(rows, "unspecified")


def test_generated_contract_and_visual_defects_reach_repair(tmp_path: Path) -> None:
    run_dir = tmp_path / "run"
    result = run_script("prepare_asset_run.py", "--asset-name", "Blink", "--frame-count", 2,
                        "--registration", "fixed", "--motion-beats", "loop: blink only",
                        "--output-dir", run_dir)
    assert result.returncode == 0, result.stderr
    request = json.loads((run_dir / "asset_request.json").read_text())
    assert request["animation"] == {"registration": "fixed", "motion_beats": "loop: blink only", "stage": "stationary"}
    result = run_script("queue_asset_repairs.py", "--run-dir", run_dir,
                        "--visual-defect", "green fringe at left ribbon",
                        "--visual-defect", "feet slide 3px")
    assert result.returncode == 0, result.stderr
    prompt = (run_dir / "prompts/asset-sheet.md").read_text()
    assert "green fringe at left ribbon" in prompt and "feet slide 3px" in prompt
    assert "lock the torso" in prompt and "intentional travel" in prompt
    assert "do not switch it implicitly" in prompt
    assert "regenerate with a clean alpha background" not in prompt
    assert "#FF00FF" in prompt
    assert json.loads((run_dir / "asset_request.json").read_text())["background"]["strategy"] == "chroma-key"


def test_motion_prompt_excludes_finish_context_and_repairs_do_not_accumulate(tmp_path: Path) -> None:
    run_dir = tmp_path / "run"
    motion = "loop: energetic run in place with landing compression and chest rising at push-off"
    paint = "Skin base #FBEEDD; hair shadow #886622"
    result = run_script("prepare_asset_run.py", "--asset-name", "Runner", "--frame-count", 6,
                        "--registration", "free", "--motion-beats", motion,
                        "--style-notes", paint, "--output-dir", run_dir)
    assert result.returncode == 0, result.stderr
    assert paint in (run_dir / "prompts/base-asset.md").read_text(encoding="utf-8")
    prompt_path = run_dir / "prompts/asset-sheet.md"
    prompt = prompt_path.read_text(encoding="utf-8")
    assert paint not in prompt and "color-coded dummy" in prompt
    assert motion in prompt and "passing under the pelvis" in prompt
    assert "shoulder/hip counter-rotation" in prompt and "Do not pin every foot or head" in prompt
    assert "restore reference pixels" not in prompt
    for defect in ("left ankle missing", "right passing pose needs correction"):
        result = run_script("queue_asset_repairs.py", "--run-dir", run_dir, "--visual-defect", defect)
        assert result.returncode == 0, result.stderr
        if defect == "left ankle missing":
            with prompt_path.open("a", encoding="utf-8") as handle:
                handle.write("\nUser note outside repair context: preserve the planned camera view.\n")
    repaired = prompt_path.read_text(encoding="utf-8")
    assert "left ankle missing" not in repaired and "right passing pose needs correction" in repaired
    assert repaired.count("Repair attempt") == 1 and "Repair attempt 2:" in repaired
    assert "User note outside repair context" in repaired
    assert paint not in repaired and "Stage: flat-color" not in repaired and "Stage: finish" not in repaired
    job = json.loads((run_dir / "imagegen-jobs.json").read_text())["jobs"][1]
    assert len(job["repair_history"]) == 2
    assert job["repair_history"][0]["prompt_before"] == prompt
    assert "left ankle missing" in job["repair_history"][1]["prompt_before"]


@pytest.mark.parametrize("stage", ["flat-color", "finish"])
def test_paint_stage_requires_and_copies_previous_cycle(tmp_path: Path, stage: str) -> None:
    design, prior = tmp_path / "design.png", tmp_path / "cycle.png"
    Image.new("RGB", (8, 8), "red").save(design)
    Image.new("RGB", (16, 8), "blue").save(prior)
    run_dir = tmp_path / "run"
    args = ["--asset-name", "Paint", "--frame-count", 2, "--registration", "free",
            "--animation-stage", stage, "--reference", design, "--output-dir", run_dir]
    result = run_script("prepare_asset_run.py", *args)
    assert result.returncode != 0 and "requires --stage-reference" in result.stderr
    assert not run_dir.exists()
    result = run_script("prepare_asset_run.py", *args, "--stage-reference", prior)
    assert result.returncode == 0, result.stderr
    request = json.loads((run_dir / "asset_request.json").read_text())
    previous = request["references"][-1]
    assert request["animation"]["stage"] == stage
    assert request["animation"]["stage_reference"] == previous["path"]
    assert (run_dir / previous["path"]).read_bytes() == prior.read_bytes()
    assert previous["sha256"] == hashlib.sha256(prior.read_bytes()).hexdigest()
    jobs = json.loads((run_dir / "imagegen-jobs.json").read_text())["jobs"]
    assert previous not in jobs[0]["input_images"] and previous in jobs[1]["input_images"]
    expected_role = "accepted motion-block" if stage == "flat-color" else "accepted flat-color"
    assert expected_role in previous["role"]
    result = run_script("queue_asset_repairs.py", "--run-dir", run_dir, "--visual-defect", "skin changed")
    assert result.returncode == 0, result.stderr
    prompt = (run_dir / "prompts/asset-sheet.md").read_text(encoding="utf-8")
    assert f"Stage: {stage}." in prompt and "Stage: motion." not in prompt
    if stage == "flat-color":
        assert "No optional shadows" in prompt and "Add only the planned hair" not in prompt
    else:
        assert "follow-through" in prompt and "accepted flat-color cycle" in prompt


@pytest.mark.parametrize("extra", [
    ["--animation-stage", "motion", "--registration", "fixed"],
    ["--animation-stage", "stationary", "--registration", "free"],
    ["--sheet-structure", "standalone", "--animation-stage", "motion"],
    ["--animation-stage", "finish"],
])
def test_invalid_stage_contract_does_not_create_run(tmp_path: Path, extra: list[str]) -> None:
    run_dir = tmp_path / "run"
    result = run_script("prepare_asset_run.py", "--asset-name", "Invalid", "--frame-count", 2,
                        "--output-dir", run_dir, *extra)
    assert result.returncode != 0
    assert not run_dir.exists()


def test_untrusted_stage_cannot_read_template_paths_or_mutate_repair(tmp_path: Path) -> None:
    run_dir = tmp_path / "run"
    result = run_script("prepare_asset_run.py", "--asset-name", "Stage safety", "--frame-count", 2,
                        "--output-dir", run_dir)
    assert result.returncode == 0, result.stderr
    request_path = run_dir / "asset_request.json"
    request = json.loads(request_path.read_text())
    request["animation"]["stage"] = "../../../../outside"
    write_json(request_path, request)
    manifest_before = (run_dir / "imagegen-jobs.json").read_bytes()
    prompt_before = (run_dir / "prompts/asset-sheet.md").read_bytes()
    output = run_dir / "decoded/asset-sheet.png"
    output.write_bytes(b"keep existing output")
    result = run_script("queue_asset_repairs.py", "--run-dir", run_dir)
    assert result.returncode != 0 and "unknown animation stage" in result.stderr
    assert (run_dir / "imagegen-jobs.json").read_bytes() == manifest_before
    assert (run_dir / "prompts/asset-sheet.md").read_bytes() == prompt_before
    assert output.read_bytes() == b"keep existing output"


def test_partial_checker_is_never_automatically_accepted(tmp_path: Path) -> None:
    run_dir = tmp_path / "run"
    request = {"sheet": {"structure": "standalone", "columns": 1, "rows": 1,
                          "cell_width": 16, "cell_height": 16, "width": 16, "height": 16, "used_cells": 1},
               "background": {"strategy": "transparent"}, "animation": {"registration": "unspecified"}}
    write_json(run_dir / "asset_request.json", request)
    write_json(run_dir / "imagegen-jobs.json", {"jobs": [{"id": "base", "status": "complete", "output_path": "decoded/base.png"}]})
    (run_dir / "decoded").mkdir()
    image = Image.new("RGBA", (16, 16))
    for y in range(2, 14):
        for x in range(2, 14):
            image.putpixel((x, y), ((180 if (x+y) % 2 else 255),) * 3 + (255,))
    image.save(run_dir / "decoded/base.png")
    result = run_script("finalize_asset_run.py", "--run-dir", run_dir)
    assert result.returncode == 0, result.stderr
    summary = json.loads((run_dir / "qa/run-summary.json").read_text())
    assert summary["automated_ok"] is True
    assert summary["accepted"] is False and summary["visual_qa"] == "unverified"


def test_extraction_carries_quality_contract_to_inspection(tmp_path: Path) -> None:
    run_dir = tmp_path / "run"
    result = run_script("prepare_asset_run.py", "--asset-name", "Idle", "--frame-count", 2,
                        "--target-size", "16x16", "--registration", "fixed",
                        "--chroma-key", "#00FF00", "--output-dir", run_dir)
    assert result.returncode == 0, result.stderr
    image = Image.new("RGBA", (32, 16), (0, 255, 0, 255))
    draw = ImageDraw.Draw(image)
    draw.rectangle((3, 3, 8, 13), fill="brown")
    draw.rectangle((22, 3, 27, 13), fill="brown")
    image.putpixel((2, 5), (25, 180, 20, 255))
    image.save(run_dir / "decoded/asset-sheet.png")
    result = run_script("extract_sheet_cells.py", "--run-dir", run_dir)
    assert result.returncode == 0, result.stderr
    result = run_script("inspect_asset_cells.py", "--cells-dir", run_dir / "cells", "--run-dir", run_dir)
    assert result.returncode == 0, result.stderr
    review = json.loads((run_dir / "cells/review.json").read_text())
    assert not any("chroma fringe" in warning for warning in review["warnings"])
    assert not any("anchor drift" in warning for warning in review["warnings"])
    cells = json.loads((run_dir / "cells/cells-manifest.json").read_text())
    assert cells["background"] == {"strategy": "chroma-key", "chroma_key": "#00FF00"}
    assert cells["animation"]["registration"] == "fixed"


def test_finalize_preflights_html_before_any_writes(tmp_path: Path) -> None:
    run_dir = tmp_path / "run"
    write_json(run_dir / "asset_request.json", {"sheet": {"structure": "sprite-row", "columns": 2, "rows": 1, "used_cells": 2}})
    write_json(run_dir / "imagegen-jobs.json", {"jobs": []})
    html = run_dir / "qa/previews/animation.html"
    html.parent.mkdir(parents=True)
    html.write_text("keep")
    result = run_script("finalize_asset_run.py", "--run-dir", run_dir)
    assert result.returncode != 0 and "already exists" in result.stderr
    assert html.read_text() == "keep" and not (run_dir / "cells").exists()
