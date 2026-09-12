#!/usr/bin/env python3
"""Inspect extracted pixel-art asset cells for occupancy, edges, and size outliers."""

from __future__ import annotations

import argparse
import colorsys
import json
from pathlib import Path
from statistics import median

from PIL import Image

from _output_pipeline import commit_outputs, resolve_output, stage_text
from _run_safety import resolve_run_path
from extract_sheet_cells import contact_anchor, parse_hex_color, pixel_lock_mask


def load_json(path: Path) -> dict[str, object]:
    if not path.exists():
        raise SystemExit(f"missing JSON file: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def alpha_nonzero_count(image: Image.Image) -> int:
    alpha = image.getchannel("A")
    return sum(alpha.histogram()[1:])


def alpha_bbox(image: Image.Image) -> tuple[int, int, int, int] | None:
    return image.getchannel("A").getbbox()


def edge_key_pixels(image: Image.Image, key: tuple[int, int, int] | None) -> int:
    """Flag saturated key-colored edge pixels; never remove subject colors."""
    if key is None:
        return 0
    hue, saturation, _ = colorsys.rgb_to_hsv(*(value / 255 for value in key))
    if saturation < 0.35:
        return 0
    pixels = image.load()
    count = 0
    # ponytail: hue is only a spill hint; visual review must distinguish real palette colors.
    for y in range(image.height):
        for x in range(image.width):
            r, g, b, alpha = pixels[x, y]
            if not alpha:
                continue
            h, s, _ = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
            distance = abs(h - hue)
            if s < 0.35 or min(distance, 1 - distance) > 1 / 12:
                continue
            if any(0 <= nx < image.width and 0 <= ny < image.height and pixels[nx, ny][3] == 0
                   for nx, ny in ((x-1,y), (x+1,y), (x,y-1), (x,y+1))):
                count += 1
    return count


def registration_warnings(rows: list[dict[str, object]], policy: str) -> list[str]:
    anchors = [row.get("contact_anchor") for row in rows]
    anchors = [anchor for anchor in anchors if anchor is not None]
    if policy != "fixed" or len(anchors) < 2:
        return []
    dx = max(a[0] for a in anchors) - min(a[0] for a in anchors)
    dy = max(a[1] for a in anchors) - min(a[1] for a in anchors)
    if max(dx, dy) <= 1:
        return []
    return [f"fixed contact anchor drift: x={dx:g}px, y={dy:g}px; verify planted feet visually (lowest pixels may be props or effects)"]


def inspect_cell(
    path: Path,
    *,
    index: int,
    expected_size: tuple[int, int],
    min_used_pixels: int,
    edge_padding: int,
    chroma_key: tuple[int, int, int] | None = None,
) -> tuple[dict[str, object], int]:
    errors: list[str] = []
    warnings: list[str] = []
    with Image.open(path) as opened:
        source_mode = opened.mode
        image = opened.convert("RGBA")
    if image.size != expected_size:
        errors.append(
            f"expected {expected_size[0]}x{expected_size[1]}, got {image.width}x{image.height}"
        )
    nontransparent = alpha_nonzero_count(image)
    if nontransparent < min_used_pixels:
        errors.append(f"cell is empty or too sparse ({nontransparent} pixels)")
    if "A" not in source_mode:
        warnings.append("cell source did not have an alpha channel before conversion")
    bbox = alpha_bbox(image)
    if bbox is not None:
        left, top, right, bottom = bbox
        if left < edge_padding or top < edge_padding or image.width - right < edge_padding or image.height - bottom < edge_padding:
            warnings.append("non-transparent pixels are close to the cell edge; inspect for clipping")
    if nontransparent == image.width * image.height:
        errors.append("cell is fully opaque; background removal probably failed")
    key_pixels = edge_key_pixels(image, chroma_key)
    if key_pixels:
        warnings.append(f"cell {index}: {key_pixels} key-colored edge pixels; inspect for chroma fringe on white and dark backgrounds")
    return (
        {
            "index": index,
            "file": str(path),
            "ok": not errors,
            "nontransparent_pixels": nontransparent,
            "bbox": bbox,
            "contact_anchor": contact_anchor(image),
            "key_colored_edge_pixels": key_pixels,
            "errors": errors,
            "warnings": warnings,
        },
        nontransparent,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cells-dir", required=True)
    parser.add_argument("--run-dir", default="")
    parser.add_argument("--json-out", default="")
    parser.add_argument("--min-used-pixels", type=int, default=20)
    parser.add_argument("--edge-padding", type=int, default=1)
    parser.add_argument("--small-outlier-ratio", type=float, default=0.35)
    parser.add_argument("--large-outlier-ratio", type=float, default=2.5)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    cells_dir = Path(args.cells_dir).expanduser().resolve()
    run_dir = Path(args.run_dir).expanduser().resolve() if args.run_dir else cells_dir.parent
    manifest = load_json(resolve_run_path(cells_dir, "cells-manifest.json", field="cells manifest"))
    sheet = manifest.get("sheet")
    if not isinstance(sheet, dict):
        raise SystemExit("cells manifest is missing sheet contract")
    expected_size = int(sheet["cell_width"]), int(sheet["cell_height"])
    background = manifest.get("background", {})
    chroma_key = None
    if background.get("strategy") == "chroma-key":
        chroma_key = parse_hex_color(str(background.get("chroma_key", "#FF00FF")))

    rows = []
    areas: list[int] = []
    lock_config = manifest.get("animation", {}).get("pixel_lock")
    mutable = list(pixel_lock_mask(expected_size, lock_config).get_flattened_data()) if lock_config is not None else None
    locked_reference = None
    for item in manifest.get("cells", []):
        if not isinstance(item, dict) or not item.get("used"):
            continue
        raw_path = item.get("path")
        if not isinstance(raw_path, str):
            rows.append({"index": item.get("index"), "ok": False, "errors": ["used cell has no file path"], "warnings": []})
            continue
        index = int(item.get("index", 0))
        cell_path = resolve_run_path(cells_dir, raw_path, field=f"cell {index} path")
        result, area = inspect_cell(
            cell_path,
            index=index,
            expected_size=expected_size,
            min_used_pixels=args.min_used_pixels,
            edge_padding=args.edge_padding,
            chroma_key=chroma_key,
        )
        if mutable is not None:
            with Image.open(cell_path) as opened:
                pixels = list(opened.convert("RGBA").get_flattened_data())
            if locked_reference is None:
                if index != 0:
                    raise SystemExit("pixel_lock inspection requires reference cell 0 first")
                locked_reference = pixels
            mismatch = sum(a != b and not m for a, b, m in zip(locked_reference, pixels, mutable))
            result["changed_outside_reference"] = mismatch
            if mismatch:
                result["errors"].append(f"cell {index}: {mismatch} pixels changed outside mutable_rects")
                result["ok"] = False
        rows.append(result)
        areas.append(area)

    if areas:
        med = median(areas)
        for row in rows:
            area = int(row.get("nontransparent_pixels", 0))
            warnings = row.setdefault("warnings", [])
            if isinstance(warnings, list) and med > 0:
                if area < med * args.small_outlier_ratio:
                    warnings.append(f"cell is much smaller than the median ({area} vs {med:.0f})")
                if area > med * args.large_outlier_ratio:
                    warnings.append(f"cell is much larger than the median ({area} vs {med:.0f})")

    errors = [error for row in rows for error in row.get("errors", []) if isinstance(row, dict)]
    warnings = [warning for row in rows for warning in row.get("warnings", []) if isinstance(row, dict)]
    warnings.extend(registration_warnings(rows, manifest.get("animation", {}).get("registration", "unspecified")))
    result = {
        "ok": not errors,
        "visual_qa": "unverified",
        "cells_dir": str(cells_dir),
        "errors": errors,
        "warnings": warnings,
        "cells": rows,
    }
    output = resolve_output(
        run_dir,
        args.json_out or (cells_dir / "review.json"),
        field="cell review output",
        force=args.force,
    )
    staged = stage_text(output, json.dumps(result, indent=2) + "\n")
    commit_outputs(run_dir, [(staged, output)], force=args.force)
    print(json.dumps({k: v for k, v in result.items() if k != "cells"}, indent=2))
    raise SystemExit(0 if result["ok"] else 1)


if __name__ == "__main__":
    main()
