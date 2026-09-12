import hashlib
import json
import sys
from pathlib import Path

import pytest
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from extract_sheet_cells import lock_frame_pixels, pixel_lock_mask
from test_trim_align import make_run
from test_output_pipeline_safety import run_script


def test_fixed_rgba_palette_and_transparent_replacement():
    reference = Image.new("RGBA", (8, 8), (100, 50, 20, 255))
    reference.putpixel((0, 0), (0, 0, 0, 0))
    frame = Image.new("RGBA", (8, 8), (102, 51, 21, 128))
    frame.putpixel((3, 3), (0, 0, 0, 0))
    mask = pixel_lock_mask(reference.size, {"mutable_rects": [[2, 2, 5, 5]]})
    result, metadata = lock_frame_pixels(reference, frame, mask)
    assert result.getpixel((0, 0)) == (0, 0, 0, 0)
    assert result.getpixel((3, 3)) == (0, 0, 0, 0)  # Erase a moving edge, no base ghost.
    assert result.getpixel((2, 2)) == (100, 50, 20, 128)
    assert metadata["changed_outside_before"] == 55
    assert metadata["changed_outside_after"] == 0
    assert frame.getpixel((0, 0)) == (102, 51, 21, 128)  # Inputs untouched.
    assert lock_frame_pixels(reference, reference, mask)[0].tobytes() == reference.tobytes()


@pytest.mark.parametrize("fill", [(0, 0, 0, 0), (255, 255, 255, 255)])
def test_missing_or_opaque_frame_is_not_hidden_by_lock(tmp_path, fill):
    run = make_run(tmp_path)
    enable_lock(run)
    source = run / "decoded/sheet.png"
    with Image.open(source) as opened:
        sheet = opened.convert("RGBA")
    sheet.paste(fill, (20, 0, 40, 24))
    sheet.save(source)
    (run / "cells").mkdir()
    (run / "cells/keep.txt").write_text("keep")
    result = run_script("extract_sheet_cells.py", "--run-dir", run, "--force")
    assert result.returncode != 0 and "missing/opaque source frames" in result.stderr
    assert (run / "cells/keep.txt").read_text() == "keep"
    assert not list(run.glob(".cells.*"))


@pytest.mark.parametrize("config", [None, {}, {"mutable_rects": []},
    {"mutable_rects": [[0, 0, 4, 8], [4, 0, 8, 8]]},
    {"mutable_rects": [[-1, 0, 3, 3]]}, {"mutable_rects": [[1, 1, 9, 3]]},
    {"mutable_rects": [[1, 1, 1, 3]]}, {"mutable_rects": [[True, 1, 3, 3]]}])
def test_invalid_masks_fail(config):
    with pytest.raises(SystemExit):
        pixel_lock_mask((8, 8), config)


def enable_lock(run, registration="fixed"):
    path = run / "asset_request.json"
    request = json.loads(path.read_text())
    request["animation"] = {"registration": registration, "pixel_lock": {"mutable_rects": [[4, 4, 12, 10]]}}
    path.write_text(json.dumps(request))


def test_finalizer_and_independent_inspection(tmp_path):
    run = make_run(tmp_path)
    enable_lock(run)
    source = run / "decoded/sheet.png"
    before = hashlib.sha256(source.read_bytes()).hexdigest()
    result = run_script("finalize_asset_run.py", "--run-dir", run)
    assert result.returncode == 0, result.stderr
    assert hashlib.sha256(source.read_bytes()).hexdigest() == before
    cells = json.loads((run / "cells/cells-manifest.json").read_text())["cells"]
    assert cells[1]["pixel_lock"]["changed_outside_before"] > 0
    assert cells[1]["pixel_lock"]["changed_outside_after"] == 0
    assert json.loads((run / "final/asset-manifest.json").read_text())["animation"]["pixel_lock"]
    path = run / "cells/cell-01.png"
    with Image.open(path) as image:
        changed = image.convert("RGBA")
    changed.putpixel((10, 18), (255, 0, 255, 255))
    changed.save(path)
    result = run_script("inspect_asset_cells.py", "--run-dir", run, "--cells-dir", run / "cells")
    assert result.returncode != 0 and "outside mutable_rects" in result.stdout


@pytest.mark.parametrize("registration", ["free", "unspecified"])
def test_unsupported_motion_preserves_existing_outputs(tmp_path, registration):
    run = make_run(tmp_path)
    enable_lock(run, registration)
    (run / "cells").mkdir()
    (run / "cells/keep.txt").write_text("keep")
    result = run_script("extract_sheet_cells.py", "--run-dir", run, "--force")
    assert result.returncode != 0 and "fixed sprite-row" in result.stderr
    assert (run / "cells/keep.txt").read_text() == "keep"
    assert not list(run.glob(".cells.*"))
    result = run_script("package_asset_run.py", "--run-dir", run)
    assert result.returncode != 0 and "finalize_asset_run.py" in result.stderr
