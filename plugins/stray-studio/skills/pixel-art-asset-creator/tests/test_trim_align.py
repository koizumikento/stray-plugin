from collections import Counter
import json
import sys
from pathlib import Path

import pytest
from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from extract_sheet_cells import contact_anchor, trim_align_cell
from test_output_pipeline_safety import run_script, write_json


def sprite(dx=0, dy=0):
    image = Image.new("RGBA", (20, 24))
    draw = ImageDraw.Draw(image)
    draw.rectangle((4+dx, 4+dy, 11+dx, 9+dy), fill="yellow")
    draw.rectangle((6+dx, 10+dy, 9+dx, 18+dy), fill="brown")
    image.putpixel((3+dx, 6+dy), (100, 90, 80, 64))
    return image


def test_trim_align_preserves_all_visible_pixels_and_common_contact():
    outputs = []
    for image in (sprite(), sprite(3, 2)):
        before = Counter(pixel for pixel in image.get_flattened_data() if pixel[3])
        result, metadata = trim_align_cell(image)
        assert result.size == image.size
        assert Counter(pixel for pixel in result.get_flattened_data() if pixel[3]) == before
        assert contact_anchor(result) == (9.5, 22)
        assert metadata["alpha_bbox_before"] == image.getchannel("A").getbbox()
        outputs.append(result.tobytes())
    assert outputs[0] == outputs[1]


def test_hair_width_does_not_change_foot_alignment():
    image = sprite()
    ImageDraw.Draw(image).rectangle((1, 4, 15, 6), fill="yellow")
    assert trim_align_cell(image)[1]["translation"] == trim_align_cell(sprite())[1]["translation"]


@pytest.mark.parametrize("kind", ["empty", "faint", "opaque", "edge", "overflow"])
def test_unsafe_trim_rejected_without_mutating_image(kind):
    image = sprite()
    if kind == "empty": image = Image.new("RGBA", image.size)
    if kind == "faint": image = Image.new("RGBA", image.size, (1, 2, 3, 64))
    if kind == "opaque": image = Image.new("RGBA", image.size, "white")
    if kind == "edge": image.putpixel((0, 4), (0, 0, 0, 255))
    if kind == "overflow":
        image = Image.new("RGBA", (20, 24))
        ImageDraw.Draw(image).rectangle((1, 2, 18, 6), fill="yellow")
        image.putpixel((2, 20), (50, 25, 10, 255))
    before = image.tobytes()
    with pytest.raises(SystemExit): trim_align_cell(image)
    assert image.tobytes() == before


def make_run(tmp_path, policy="fixed"):
    run = tmp_path / "run"
    write_json(run / "asset_request.json", {
        "sheet": {"structure": "sprite-row", "columns": 2, "rows": 1, "cell_width": 20,
                  "cell_height": 24, "width": 40, "height": 24, "used_cells": 2},
        "background": {"strategy": "transparent"}, "animation": {"registration": policy}})
    write_json(run / "imagegen-jobs.json", {"jobs": [{"id": "asset-sheet", "status": "complete", "output_path": "decoded/sheet.png"}]})
    (run / "decoded").mkdir()
    sheet = Image.new("RGBA", (40, 24))
    sheet.paste(sprite(), (0, 0))
    sheet.paste(sprite(3, 2), (20, 0))
    sheet.save(run / "decoded/sheet.png")
    return run


def test_finalizer_alignment_and_metadata(tmp_path):
    run = make_run(tmp_path)
    result = run_script("finalize_asset_run.py", "--run-dir", run, "--trim-align")
    assert result.returncode == 0, result.stderr
    manifest = json.loads((run / "cells/cells-manifest.json").read_text())
    assert manifest["trim_align"] is True
    assert [c["alignment"]["translation"] for c in manifest["cells"]] == [[2, 4], [-1, 2]]
    with Image.open(run / "final/asset.png") as image:
        assert image.crop((0, 0, 20, 24)).tobytes() == image.crop((20, 0, 40, 24)).tobytes()
    assert (run / "qa/previews/animation.html").exists()


@pytest.mark.parametrize("policy", ["free", "unspecified"])
def test_intentional_motion_preserved_unless_fixed(tmp_path, policy):
    run = make_run(tmp_path, policy)
    refused = run_script("extract_sheet_cells.py", "--run-dir", run, "--trim-align")
    assert refused.returncode != 0 and "fixed-contact" in refused.stderr
    assert not (run / "cells").exists()
    result = run_script("extract_sheet_cells.py", "--run-dir", run)
    assert result.returncode == 0, result.stderr
    with Image.open(run / "cells/cell-01.png") as cell:
        assert cell.tobytes() == sprite(3, 2).tobytes()


def test_failed_forced_alignment_preserves_previous_outputs(tmp_path):
    run = make_run(tmp_path)
    (run / "cells").mkdir()
    (run / "cells/keep.txt").write_text("original")
    with Image.open(run / "decoded/sheet.png") as image:
        image.putpixel((20, 4), (0, 0, 0, 255))  # Second cell fails after first was staged.
        image.save(run / "decoded/sheet.png")
    result = run_script("extract_sheet_cells.py", "--run-dir", run, "--trim-align", "--force")
    assert result.returncode != 0 and "edge-touching" in result.stderr
    assert (run / "cells/keep.txt").read_text() == "original"
    assert not list(run.glob(".cells.*"))
