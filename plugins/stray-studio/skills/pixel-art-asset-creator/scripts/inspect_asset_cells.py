#!/usr/bin/env python3
"""Inspect extracted pixel-art asset cells for occupancy, edges, and size outliers."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from statistics import median

from PIL import Image


def load_json(path: Path) -> dict[str, object]:
    if not path.exists():
        raise SystemExit(f"missing JSON file: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def alpha_nonzero_count(image: Image.Image) -> int:
    alpha = image.getchannel("A")
    return sum(alpha.histogram()[1:])


def alpha_bbox(image: Image.Image) -> tuple[int, int, int, int] | None:
    return image.getchannel("A").getbbox()


def inspect_cell(
    path: Path,
    *,
    index: int,
    expected_size: tuple[int, int],
    min_used_pixels: int,
    edge_padding: int,
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
    return (
        {
            "index": index,
            "file": str(path),
            "ok": not errors,
            "nontransparent_pixels": nontransparent,
            "bbox": bbox,
            "errors": errors,
            "warnings": warnings,
        },
        nontransparent,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cells-dir", required=True)
    parser.add_argument("--json-out", default="")
    parser.add_argument("--min-used-pixels", type=int, default=20)
    parser.add_argument("--edge-padding", type=int, default=1)
    parser.add_argument("--small-outlier-ratio", type=float, default=0.35)
    parser.add_argument("--large-outlier-ratio", type=float, default=2.5)
    args = parser.parse_args()

    cells_dir = Path(args.cells_dir).expanduser().resolve()
    manifest = load_json(cells_dir / "cells-manifest.json")
    sheet = manifest.get("sheet")
    if not isinstance(sheet, dict):
        raise SystemExit("cells manifest is missing sheet contract")
    expected_size = int(sheet["cell_width"]), int(sheet["cell_height"])

    rows = []
    areas: list[int] = []
    for item in manifest.get("cells", []):
        if not isinstance(item, dict) or not item.get("used"):
            continue
        raw_path = item.get("path")
        if not isinstance(raw_path, str):
            rows.append({"index": item.get("index"), "ok": False, "errors": ["used cell has no file path"], "warnings": []})
            continue
        index = int(item.get("index", 0))
        result, area = inspect_cell(
            cells_dir / raw_path,
            index=index,
            expected_size=expected_size,
            min_used_pixels=args.min_used_pixels,
            edge_padding=args.edge_padding,
        )
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
    result = {
        "ok": not errors,
        "cells_dir": str(cells_dir),
        "errors": errors,
        "warnings": warnings,
        "cells": rows,
    }
    output = Path(args.json_out).expanduser().resolve() if args.json_out else cells_dir / "review.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in result.items() if k != "cells"}, indent=2))
    raise SystemExit(0 if result["ok"] else 1)


if __name__ == "__main__":
    main()
