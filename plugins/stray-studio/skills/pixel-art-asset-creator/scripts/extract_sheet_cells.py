#!/usr/bin/env python3
"""Normalize a generated pixel-art asset image and extract grid cells."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image

from _output_pipeline import (
    cleanup_staged_directory,
    commit_staged_directory,
    create_staged_directory,
    preflight_directory_outputs,
    resolve_output_directory,
    write_staged_image,
    write_staged_text,
)
from _run_safety import resolve_run_path


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
            path = resolve_run_path(
                run_dir,
                output,
                field=f"job {job_id} output_path",
                allowed_roots=("decoded",),
            )
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
    request = load_json(resolve_run_path(run_dir, "asset_request.json", field="asset request"))
    manifest = load_json(resolve_run_path(run_dir, "imagegen-jobs.json", field="job manifest"))
    source = Path(args.source).expanduser().resolve() if args.source else selected_output(run_dir, request, manifest)
    output_dir = resolve_output_directory(
        run_dir,
        args.output_dir or "cells",
        field="cells output directory",
    )

    sheet = request.get("sheet")
    if not isinstance(sheet, dict):
        raise SystemExit("asset_request.json is missing sheet contract")
    columns = int(sheet["columns"])
    rows = int(sheet["rows"])
    cell_w = int(sheet["cell_width"])
    cell_h = int(sheet["cell_height"])
    used_cells = int(sheet["used_cells"])
    output_names = ["source-normalized.png"]
    output_names.extend(
        f"cell-{index:02d}.png"
        for index in range(columns * rows)
        if index < used_cells or args.include_unused
    )
    output_names.append("cells-manifest.json")
    preflight_directory_outputs(
        run_dir,
        output_dir,
        output_names,
        field="extracted cell output",
        force=args.force,
    )

    image, warnings = normalize_source(
        source,
        request,
        chroma_tolerance=args.chroma_tolerance,
        no_resize=args.no_resize,
    )
    staged_dir = create_staged_directory(output_dir)
    normalized = output_dir / "source-normalized.png"
    manifest_path = output_dir / "cells-manifest.json"
    try:
        write_staged_image(staged_dir / normalized.name, image, image_format="PNG")

        cells: list[dict[str, object]] = []
        for index in range(columns * rows):
            used = index < used_cells
            if not used and not args.include_unused:
                cells.append({"index": index, "used": False, "path": None})
                continue
            row = index // columns
            column = index % columns
            crop = image.crop(
                (
                    column * cell_w,
                    row * cell_h,
                    (column + 1) * cell_w,
                    (row + 1) * cell_h,
                )
            )
            name = f"cell-{index:02d}.png"
            write_staged_image(staged_dir / name, crop, image_format="PNG")
            cells.append(
                {
                    "index": index,
                    "row": row,
                    "column": column,
                    "used": used,
                    "path": name,
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
        write_staged_text(
            staged_dir / manifest_path.name,
            json.dumps(cell_manifest, indent=2) + "\n",
        )
        commit_staged_directory(
            run_dir,
            staged_dir,
            output_dir,
            output_names,
            field="cells output directory",
            force=args.force,
        )
    finally:
        cleanup_staged_directory(staged_dir)
    print(json.dumps({"ok": True, "cells_dir": str(output_dir), "manifest": str(manifest_path), "warnings": warnings}, indent=2))


if __name__ == "__main__":
    main()
