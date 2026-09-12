"""Regression checks for the imported RGB matte and the shared packaging path."""
import sys
from pathlib import Path

import pytest
from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from _chroma_background import detect_background_key_rgb, remove_chroma_background
from test_output_pipeline_safety import run_script, write_json


def test_painted_background_unmix_and_subject_preservation():
    # Gray subject plus a 50% blue blend, on a dark painted blue background.
    key = (0, 0, 255)
    painted = (0, 0, 200)
    im = Image.new("RGBA", (40, 40), (*painted, 255))
    ImageDraw.Draw(im).rectangle((10, 8, 29, 31), fill=(160, 160, 160, 255))
    im.putpixel((9, 20), (80, 80, 180, 255))
    im.putpixel((20, 20), (170, 75, 35, 255))  # Required warm material.
    assert detect_background_key_rgb(im, key) == painted
    out = remove_chroma_background(im, key, 96, 180, 20)
    assert out.getpixel((0, 0)) == (0, 0, 0, 0)
    assert out.getpixel((9, 20)) == (160, 160, 160, 128)
    assert out.getpixel((20, 20)) == im.getpixel((20, 20))
    assert im.getpixel((0, 0)) == (*painted, 255)  # Never mutate source.


def test_small_spill_corrected_without_holes_and_large_material_kept():
    im = Image.new("RGBA", (80, 60), (0, 255, 0, 255))
    draw = ImageDraw.Draw(im)
    draw.rectangle((5, 5, 74, 54), fill=(100, 50, 50, 255))
    draw.rectangle((15, 15, 25, 25), fill=(120, 155, 120, 255))
    im.putpixel((55, 30), (60, 130, 60, 255))
    out = remove_chroma_background(im, (0, 255, 0), 96, 180, 20)
    assert out.getpixel((20, 20)) == im.getpixel((20, 20))
    r, g, b, alpha = out.getpixel((55, 30))
    assert alpha == 255 and g <= r + 1 and g <= b + 1


def test_package_uses_shared_cleanup_and_refuses_component_bypass(tmp_path):
    from extract_sheet_cells import remove_chroma_key
    from package_asset_run import remove_chroma_key as package_remove
    assert package_remove is remove_chroma_key
    for tolerance in (-1, 442):
        with pytest.raises(SystemExit):
            remove_chroma_key(Image.new("RGBA", (2, 2)), (0, 255, 0), tolerance)
    run = tmp_path / "run"
    write_json(run / "asset_request.json", {"sheet": {"extraction": "components"}})
    result = run_script("package_asset_run.py", "--run-dir", run)
    assert result.returncode != 0 and "finalize_asset_run.py" in result.stderr
    assert not (run / "final").exists()
