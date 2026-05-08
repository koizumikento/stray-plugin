#!/usr/bin/env python3
"""Normalize a generated pixel-art asset image and extract grid cells."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image


def load_json(path: Path) -> dict[str, object]:
    if not path.exists():
        raise SystemExit(f"missing JSON file: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def jobs(manifest: dict[str, object]) -> list[dict[str, object]]:
    raw = manifest.get("jobs")
    if not isinstance(raw, list):
        raise SystemExit("invalid imagegen-jobs.json: jobs must be a list")
    return [job for job in raw if isinstance(job, dict)]


def selected_output(run_dir: Path, request: dict[str, object], manifest: dict[str, object]) -> Path:
    structure = str(request.get("sheet", {}).get("structure", "standalone"))
    job_id = "base" if structure == "standalone" else "asset-sheet"
    for job in jobs(manifest):
        if job.get("id") == job_id:
            output = job.get("output_path")
            if not isinstance(output, str):
                raise SystemExit(f"job {job_id} has no output_path")
            path = run_dir / output
            if not path.is_file():
                raise SystemExit(f"job {job_id} output is missing: {path}")
            return path
    raise SystemExit(f"job not found: {job_id}")


def parse_hex_color(value: str) -> tuple[int, int, int]:
    raw = value.strip().lstrip("#")
    if len(raw) != 6:
        raise SystemExit(f"invalid chroma key: {value}")
    return int(raw[0:2], 16), int(raw[2:4], 16), int(raw[4:6], 16)


def remove_chroma_key(image: Image.Image, key: tuple[int, int, int], tolerance: int) -> Image.Image:
    rgba = image.convert("RGBA")
    kr, kg, kb = key
    pixels = rgba.load()
    for y in range(rgba.height):
        for x in range(rgba.width):
            r, g, b, a = pixels[x, y]
            if abs(r - kr) <= tolerance and abs(g - kg) <= tolerance and abs(b - kb) <= tolerance:
                pixels[x, y] = (r, g, b, 0)
    return rgba


def normalize_source(
    source: Path,
    request: dict[str, object],
    *,
    chroma_tolerance: int,
    no_resize: bool,
) -> tuple[Image.Image, list[str]]:
    with Image.open(source) as opened:
        image = opened.convert("RGBA")
    warnings: list[str] = []
    background = request.get("background") if isinstance(request.get("background"), dict) else {}
    if background.get("strategy") == "chroma-key":
        key = parse_hex_color(str(background.get("chroma_key", "#FF00FF")))
        image = remove_chroma_key(image, key, chroma_tolerance)

    sheet = request.get("sheet")
    if not isinstance(sheet, dict):
        raise SystemExit("asset_request.json is missing sheet contract")
    expected = int(sheet["width"]), int(sheet["height"])
    if image.size != expected:
        message = f"resized source from {image.width}x{image.height} to {expected[0]}x{expected[1]}"
        if no_resize:
            raise SystemExit(message)
        image = image.resize(expected, Image.Resampling.NEAREST)
        warnings.append(message)
    return image, warnings


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--source", default="")
    parser.add_argument("--output-dir", default="")
    parser.add_argument("--chroma-tolerance", type=int, default=8)
    parser.add_argument("--no-resize", action="store_true")
    parser.add_argument("--include-unused", action="store_true")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    run_dir = Path(args.run_dir).expanduser().resolve()
    request = load_json(run_dir / "asset_request.json")
    manifest = load_json(run_dir / "imagegen-jobs.json")
    source = Path(args.source).expanduser().resolve() if args.source else selected_output(run_dir, request, manifest)
    output_dir = Path(args.output_dir).expanduser().resolve() if args.output_dir else run_dir / "cells"
    if output_dir.exists() and any(output_dir.iterdir()) and not args.force:
        raise SystemExit(f"{output_dir} is not empty; pass --force to replace it")
    output_dir.mkdir(parents=True, exist_ok=True)

    sheet = request.get("sheet")
    if not isinstance(sheet, dict):
        raise SystemExit("asset_request.json is missing sheet contract")
    columns = int(sheet["columns"])
    rows = int(sheet["rows"])
    cell_w = int(sheet["cell_width"])
    cell_h = int(sheet["cell_height"])
    used_cells = int(sheet["used_cells"])

    image, warnings = normalize_source(
        source,
        request,
        chroma_tolerance=args.chroma_tolerance,
        no_resize=args.no_resize,
    )
    normalized = output_dir / "source-normalized.png"
    image.save(normalized)

    cells: list[dict[str, object]] = []
    for index in range(columns * rows):
        used = index < used_cells
        if not used and not args.include_unused:
            cells.append({"index": index, "used": False, "path": None})
            continue
        row = index // columns
        column = index % columns
        crop = image.crop((column * cell_w, row * cell_h, (column + 1) * cell_w, (row + 1) * cell_h))
        target = output_dir / f"cell-{index:02d}.png"
        crop.save(target)
        cells.append(
            {
                "index": index,
                "row": row,
                "column": column,
                "used": used,
                "path": target.name,
                "width": cell_w,
                "height": cell_h,
            }
        )

    cell_manifest = {
        "ok": True,
        "source": str(source),
        "normalized_source": str(normalized),
        "asset_id": request.get("asset_id"),
        "display_name": request.get("display_name"),
        "description": request.get("description"),
        "asset_type": request.get("asset_type"),
        "target_use": request.get("target_use"),
        "items": request.get("items", []),
        "tiles": request.get("tiles", []),
        "sheet": sheet,
        "warnings": warnings,
        "cells": cells,
    }
    manifest_path = output_dir / "cells-manifest.json"
    manifest_path.write_text(json.dumps(cell_manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"ok": True, "cells_dir": str(output_dir), "manifest": str(manifest_path), "warnings": warnings}, indent=2))


if __name__ == "__main__":
    main()
