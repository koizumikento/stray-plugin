from __future__ import annotations

import json
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
    assert request["animation"] == {"registration": "fixed", "motion_beats": "loop: blink only"}
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
