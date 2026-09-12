from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest
from PIL import Image, ImageDraw

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/extract_sheet_cells.py"
sys.path.insert(0, str(SCRIPT.parent))
from extract_sheet_cells import contact_anchor, extract_components  # noqa: E402


def contract(registration: str = "fixed", *, width: int = 48, height: int = 64) -> dict:
    return {"animation": {"registration": registration}, "background": {"strategy": "transparent"},
            "sheet": {"structure": "sprite-row", "extraction": "components", "columns": 2, "rows": 1,
                      "cell_width": width, "cell_height": height, "width": width * 2, "height": height, "used_cells": 2}}


def art() -> Image.Image:
    image = Image.new("RGBA", (120, 80))
    image.paste("red", (20, 25, 40, 60))
    image.paste("blue", (82, 12, 102, 47))
    image.paste("yellow", (16, 21, 18, 23))
    return image


def make_run(tmp_path: Path, request: dict | None = None, source: Image.Image | None = None) -> Path:
    run = tmp_path / "run"
    (run / "decoded").mkdir(parents=True)
    (run / "asset_request.json").write_text(json.dumps(request or contract()))
    (run / "imagegen-jobs.json").write_text(json.dumps({"jobs": [{"id": "asset-sheet", "output_path": "decoded/sheet.png"}]}))
    (source or art()).save(run / "decoded/sheet.png")
    return run


def run_extract(run: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, str(SCRIPT), "--run-dir", str(run), *args],
                          capture_output=True, text=True, check=False,
                          env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})


def test_native_components_keep_detached_parts_and_align_contact(tmp_path: Path) -> None:
    run = make_run(tmp_path)
    result = run_extract(run)
    assert result.returncode == 0, result.stderr
    manifest = json.loads((run / "cells/cells-manifest.json").read_text())
    with Image.open(run / "cells/source-normalized.png") as normalized:
        assert normalized.size == (120, 80) and normalized.tobytes() == art().tobytes()
    extracted = [Image.open(run / "cells" / cell["path"]) for cell in manifest["cells"]]
    assert contact_anchor(extracted[0]) == contact_anchor(extracted[1]) == (23.5, 62)
    metadata = [cell["component_extraction"] for cell in manifest["cells"]]
    assert [item["common_scale"] for item in metadata] == [1, 1]
    assert [len(item["source_components"]) for item in metadata] == [2, 1]
    assert metadata[0]["source_bbox"] == [16, 21, 40, 60]
    assert sum(sum(image.getchannel("A").histogram()[1:]) for image in extracted) == 1404
    assert (255, 255, 0, 255) in [color for _, color in extracted[0].getcolors()]
    assert manifest["extraction"] == "components" and not manifest["warnings"]
    for image in extracted:
        image.close()


@pytest.mark.parametrize("registration", ["free", "unspecified"])
def test_free_motion_retains_virtual_slot_offset_and_original_height(registration: str) -> None:
    sheet = contract(registration, width=100, height=100)["sheet"]
    cells = extract_components(art(), sheet, registration, no_resize=False)
    anchors = [contact_anchor(image) for image, _ in cells]
    assert anchors[1][0] - anchors[0][0] == 2
    assert anchors[1][1] - anchors[0][1] == -13
    assert {meta["common_scale"] for _, meta in cells} == {1}


def test_common_scale_is_shared_and_never_upscales() -> None:
    source = art().resize((240, 160), Image.Resampling.NEAREST)
    cells = extract_components(source, contract()["sheet"], "fixed", no_resize=False)
    scales = [metadata["common_scale"] for _, metadata in cells]
    assert 0 < scales[0] == scales[1] < 1
    anchors = [contact_anchor(image) for image, _ in cells]
    assert abs(anchors[0][0] - anchors[1][0]) <= .5 and anchors[0][1] == anchors[1][1]
    with pytest.raises(SystemExit, match="--no-resize"):
        extract_components(source, contract()["sheet"], "fixed", no_resize=True)


@pytest.mark.parametrize("failure", ["missing", "extra", "edge", "ambiguous", "overlap"])
def test_unreliable_components_fail_before_any_output(tmp_path: Path, failure: str) -> None:
    source = Image.new("RGBA", (140, 80))
    source.paste("red", (20, 20, 40, 60))
    if failure != "missing": source.paste("blue", (80, 20, 100, 60))
    if failure == "extra": source.paste("red", (110, 20, 130, 60))
    if failure == "edge": source.putpixel((0, 40), (255, 0, 0, 255))
    if failure == "ambiguous": source.paste("yellow", (59, 35, 61, 37))
    if failure == "overlap":
        source = Image.new("RGBA", (140, 80))
        draw = ImageDraw.Draw(source)
        draw.line([(10, 40), (10, 10), (40, 10)], fill="red", width=4)
        source.paste("blue", (25, 25, 45, 50))
    run = make_run(tmp_path, source=source)
    result = run_extract(run)
    assert result.returncode != 0
    assert not (run / "cells").exists() and not list(run.glob(".cells.*"))


def test_single_pixel_part_is_not_silently_lost_on_downscale() -> None:
    source = Image.new("RGBA", (200, 120))
    source.paste("red", (20, 20, 60, 100))
    source.paste("blue", (120, 20, 160, 100))
    source.putpixel((19, 16), (255, 255, 0, 255))
    with pytest.raises(SystemExit, match="component disappears"):
        extract_components(source, contract(width=16, height=24)["sheet"], "fixed", no_resize=False)


def test_explicit_grid_override_preserves_legacy_behavior(tmp_path: Path) -> None:
    run = make_run(tmp_path)
    result = run_extract(run, "--extraction", "grid")
    assert result.returncode == 0, result.stderr
    with Image.open(run / "cells/source-normalized.png") as image:
        assert image.size == (96, 64)
    manifest = json.loads((run / "cells/cells-manifest.json").read_text())
    assert manifest["extraction"] == "grid" and manifest["warnings"]
    assert all(cell["component_extraction"] is None for cell in manifest["cells"])


@pytest.mark.parametrize("args", [("--trim-align",), ("--output-dir", "../outside"), ("--output-dir", "/outside")])
def test_invalid_combination_or_output_path_does_not_write(tmp_path: Path, args: tuple) -> None:
    run = make_run(tmp_path)
    result = run_extract(run, *args)
    assert result.returncode != 0
    assert not (run / "cells").exists() and not (tmp_path / "outside").exists()


def test_component_overwrite_requires_force(tmp_path: Path) -> None:
    run = make_run(tmp_path)
    assert run_extract(run).returncode == 0
    original = (run / "cells/cell-00.png").read_bytes()
    result = run_extract(run)
    assert result.returncode != 0 and "--force" in result.stderr
    assert (run / "cells/cell-00.png").read_bytes() == original
    result = run_extract(run, "--force")
    assert result.returncode == 0, result.stderr


def test_component_symlink_output_is_rejected(tmp_path: Path) -> None:
    run = make_run(tmp_path)
    outside = tmp_path / "outside"
    outside.mkdir()
    try:
        (run / "cells").symlink_to(outside, target_is_directory=True)
    except OSError as error:
        if getattr(error, "winerror", None) == 1314:
            pytest.skip("Windows symlink privilege unavailable")
        raise
    result = run_extract(run, "--force")
    assert result.returncode != 0 and not list(outside.iterdir())
