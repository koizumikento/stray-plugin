#!/usr/bin/env python3
"""Validate dimensions, transparency, and cell occupancy for a pixel-art asset sheet."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image

from _output_pipeline import commit_outputs, resolve_output, stage_text
from _run_safety import resolve_run_path


def load_json(path: Path) -> dict[str, object]:
    if not path.exists():
        raise SystemExit(f"missing JSON file: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def alpha_nonzero_count(image: Image.Image) -> int:
    alpha = image.getchannel("A")
    return sum(alpha.histogram()[1:])


def request_from_args(
    args: argparse.Namespace,
    image_path: Path,
) -> tuple[dict[str, object] | None, Path, Path]:
    if args.run_dir:
        run_dir = Path(args.run_dir).expanduser().resolve()
        request = load_json(resolve_run_path(run_dir, "asset_request.json", field="asset request"))
        path = (
            Path(args.image).expanduser().resolve()
            if args.image
            else resolve_run_path(run_dir, "final/asset.png", field="default asset image")
        )
        return request, path, run_dir
    if not args.image:
        raise SystemExit("pass --run-dir or --image")
    path = image_path.expanduser().resolve()
    return None, path, path.parent


def sheet_from_request(request: dict[str, object] | None, args: argparse.Namespace) -> dict[str, int]:
    if request is not None:
        sheet = request.get("sheet")
        if not isinstance(sheet, dict):
            raise SystemExit("asset_request.json is missing sheet contract")
        return {
            "columns": int(sheet["columns"]),
            "rows": int(sheet["rows"]),
            "cell_width": int(sheet["cell_width"]),
            "cell_height": int(sheet["cell_height"]),
            "width": int(sheet["width"]),
            "height": int(sheet["height"]),
            "used_cells": int(sheet["used_cells"]),
        }
    if not all([args.columns, args.rows, args.cell_width, args.cell_height]):
        raise SystemExit("--image validation requires --columns, --rows, --cell-width, and --cell-height")
    columns = int(args.columns)
    rows = int(args.rows)
    cell_width = int(args.cell_width)
    cell_height = int(args.cell_height)
    return {
        "columns": columns,
        "rows": rows,
        "cell_width": cell_width,
        "cell_height": cell_height,
        "width": columns * cell_width,
        "height": rows * cell_height,
        "used_cells": int(args.used_cells or columns * rows),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", default="")
    parser.add_argument("--image", default="")
    parser.add_argument("--columns", type=int)
    parser.add_argument("--rows", type=int)
    parser.add_argument("--cell-width", type=int)
    parser.add_argument("--cell-height", type=int)
    parser.add_argument("--used-cells", type=int)
    parser.add_argument("--json-out", default="")
    parser.add_argument("--min-used-pixels", type=int, default=20)
    parser.add_argument("--allow-opaque", action="store_true")
    parser.add_argument("--allow-unused-content", action="store_true")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    request, image_path, output_root = request_from_args(
        args,
        Path(args.image) if args.image else Path(),
    )
    json_output = (
        resolve_output(
            output_root,
            args.json_out,
            field="validation JSON output",
            force=args.force,
        )
        if args.json_out
        else None
    )
    sheet = sheet_from_request(request, args)
    errors: list[str] = []
    warnings: list[str] = []
    cells: list[dict[str, object]] = []

    try:
        with Image.open(image_path) as opened:
            source_format = opened.format
            source_mode = opened.mode
            image = opened.convert("RGBA")
    except Exception as exc:  # noqa: BLE001
        result = {"ok": False, "errors": [f"could not open image: {exc}"], "warnings": []}
        print(json.dumps(result, indent=2))
        raise SystemExit(1)

    if image.size != (sheet["width"], sheet["height"]):
        errors.append(
            f"expected {sheet['width']}x{sheet['height']}, got {image.width}x{image.height}"
        )
    if source_format not in {"PNG", "WEBP"}:
        warnings.append(f"expected PNG or WebP for packaged assets, got {source_format}")
    if "A" not in source_mode and not args.allow_opaque:
        errors.append("image does not have an alpha channel")

    used_cells = sheet["used_cells"]
    capacity = sheet["columns"] * sheet["rows"]
    if used_cells > capacity:
        errors.append(f"used_cells {used_cells} exceeds grid capacity {capacity}")

    for index in range(capacity):
        row = index // sheet["columns"]
        column = index % sheet["columns"]
        left = column * sheet["cell_width"]
        top = row * sheet["cell_height"]
        cell = image.crop((left, top, left + sheet["cell_width"], top + sheet["cell_height"]))
        nontransparent = alpha_nonzero_count(cell)
        used = index < used_cells
        cells.append(
            {
                "index": index,
                "row": row,
                "column": column,
                "used": used,
                "nontransparent_pixels": nontransparent,
            }
        )
        if used and nontransparent < args.min_used_pixels:
            errors.append(f"cell {index} is empty or too sparse ({nontransparent} pixels)")
        if not used and nontransparent and not args.allow_unused_content:
            errors.append(f"unused cell {index} is not transparent ({nontransparent} pixels)")

    alpha_count = alpha_nonzero_count(image)
    if alpha_count == image.width * image.height:
        message = "image is fully opaque; this often means the background was not removed"
        if args.allow_opaque:
            warnings.append(message)
        else:
            errors.append(message)

    result = {
        "ok": not errors,
        "file": str(image_path),
        "format": source_format,
        "mode": source_mode,
        "width": image.width,
        "height": image.height,
        "sheet": sheet,
        "errors": errors,
        "warnings": warnings,
        "cells": cells,
    }
    if json_output is not None:
        staged = stage_text(json_output, json.dumps(result, indent=2) + "\n")
        commit_outputs(output_root, [(staged, json_output)], force=args.force)
    print(json.dumps({k: v for k, v in result.items() if k != "cells"}, indent=2))
    raise SystemExit(0 if result["ok"] else 1)


if __name__ == "__main__":
    main()
