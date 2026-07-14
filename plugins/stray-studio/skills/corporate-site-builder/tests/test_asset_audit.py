from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path

import pytest
from PIL import Image


SCRIPT = Path(__file__).parents[1] / "scripts" / "asset_audit.py"
SPEC = importlib.util.spec_from_file_location("asset_audit", SCRIPT)
assert SPEC and SPEC.loader
asset_audit = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(asset_audit)


def args() -> argparse.Namespace:
    return argparse.Namespace(
        max_width=2400,
        quality=82,
        max_image_kb=800,
        max_pdf_kb=5000,
        max_video_kb=8000,
    )


def make_image(path: Path, image_format: str | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    Image.new("RGB", (8, 8), "red").save(path, format=image_format)


def row(path: str, extension: str) -> dict[str, object]:
    return {
        "path": path,
        "kind": "image",
        "extension": extension,
        "size_kb": 1.0,
        "width": 8,
        "height": 8,
        "warnings": [],
    }


def test_writes_project_derivative_inside_optimize_dir(tmp_path: Path) -> None:
    project_root = tmp_path / "project"
    source = project_root / "src" / "assets" / "hero.png"
    out_dir = tmp_path / "optimized"
    make_image(source)

    written = asset_audit.optimize_images(
        [row("src/assets/hero.png", ".png")], project_root, out_dir, args()
    )

    target = out_dir / "src" / "assets" / "hero.webp"
    assert target.is_file()
    assert written == [
        {
            "source": "src/assets/hero.png",
            "output": target.as_posix(),
            "source_kb": 1.0,
            "output_kb": asset_audit.kb(target.stat().st_size),
        }
    ]


def test_external_absolute_source_stays_inside_optimize_dir(tmp_path: Path) -> None:
    project_root = tmp_path / "project"
    project_root.mkdir()
    source = tmp_path / "outside" / "hero.webp"
    out_dir = tmp_path / "optimized"
    make_image(source, "WEBP")
    original = source.read_bytes()
    rows = asset_audit.scan([source.resolve()], project_root.resolve(), args())
    assert rows[0]["path"] == source.resolve().as_posix()

    written = asset_audit.optimize_images(rows, project_root, out_dir, args())

    outputs = list(out_dir.rglob("*.webp"))
    assert len(outputs) == 1
    assert outputs[0].resolve().is_relative_to(out_dir.resolve())
    assert outputs[0] != source
    assert source.read_bytes() == original
    assert "error" not in written[0]


def test_refuses_to_overwrite_source_asset(tmp_path: Path) -> None:
    project_root = tmp_path / "project"
    source = project_root / "hero.webp"
    make_image(source, "WEBP")
    original = source.read_bytes()

    written = asset_audit.optimize_images(
        [row("hero.webp", ".webp")], project_root, project_root, args()
    )

    assert "refusing to overwrite source asset" in written[0]["error"]
    assert source.read_bytes() == original


def test_refuses_to_overwrite_existing_output(tmp_path: Path) -> None:
    project_root = tmp_path / "project"
    source = project_root / "hero.png"
    target = project_root / "hero.webp"
    make_image(source)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(b"existing-output")

    written = asset_audit.optimize_images(
        [row("hero.png", ".png")], project_root, project_root, args()
    )

    assert "refusing to overwrite existing output" in written[0]["error"]
    assert target.read_bytes() == b"existing-output"


def test_refuses_symlink_escape_from_optimize_dir(tmp_path: Path) -> None:
    project_root = tmp_path / "project"
    source = project_root / "assets" / "hero.png"
    out_dir = tmp_path / "optimized"
    escaped_dir = tmp_path / "escaped"
    make_image(source)
    out_dir.mkdir()
    escaped_dir.mkdir()
    try:
        (out_dir / "assets").symlink_to(escaped_dir, target_is_directory=True)
    except OSError:
        pytest.skip("directory symlinks are unavailable")

    written = asset_audit.optimize_images(
        [row("assets/hero.png", ".png")], project_root, out_dir, args()
    )

    assert "output path escapes optimize directory" in written[0]["error"]
    assert not (escaped_dir / "hero.webp").exists()
