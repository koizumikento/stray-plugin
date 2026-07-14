#!/usr/bin/env python3
"""Compose extracted pixel-art cells into a normalized asset sheet."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image

from _output_pipeline import commit_outputs, resolve_output, stage_image, stage_text
from _run_safety import resolve_run_path


def load_json(path: Path) -> dict[str, object]:
    if not path.exists():
        raise SystemExit(f"missing JSON file: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cells-dir", required=True)
    parser.add_argument("--run-dir", default="")
    parser.add_argument("--output", required=True)
    parser.add_argument("--webp-output", default="")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    cells_dir = Path(args.cells_dir).expanduser().resolve()
    run_dir = Path(args.run_dir).expanduser().resolve() if args.run_dir else cells_dir.parent
    manifest = load_json(resolve_run_path(cells_dir, "cells-manifest.json", field="cells manifest"))
    sheet = manifest.get("sheet")
    if not isinstance(sheet, dict):
        raise SystemExit("cells manifest is missing sheet contract")
    columns = int(sheet["columns"])
    cell_w = int(sheet["cell_width"])
    cell_h = int(sheet["cell_height"])
    width = int(sheet["width"])
    height = int(sheet["height"])
    output = resolve_output(
        run_dir,
        args.output,
        field="composed PNG output",
        force=args.force,
    )
    webp_output = resolve_output(
        run_dir,
        args.webp_output or output.with_suffix(".webp"),
        field="composed WebP output",
        force=args.force,
    )
    summary_path = resolve_output(
        run_dir,
        output.parent / "compose-summary.json",
        field="compose summary output",
        force=args.force,
    )
    asset_manifest_path = resolve_output(
        run_dir,
        output.parent / "asset-manifest.json",
        field="asset manifest output",
        force=args.force,
    )

    image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    for item in manifest.get("cells", []):
        if not isinstance(item, dict) or not item.get("used"):
            continue
        raw_path = item.get("path")
        if not isinstance(raw_path, str):
            raise SystemExit(f"used cell {item.get('index')} has no path")
        index = int(item["index"])
        row = index // columns
        column = index % columns
        cell_path = resolve_run_path(cells_dir, raw_path, field=f"cell {index} path")
        with Image.open(cell_path) as opened:
            cell = opened.convert("RGBA")
        if cell.size != (cell_w, cell_h):
            cell = cell.resize((cell_w, cell_h), Image.Resampling.NEAREST)
        image.alpha_composite(cell, (column * cell_w, row * cell_h))

    summary = {"ok": True, "output": str(output), "webp_output": str(webp_output), "sheet": sheet}
    asset_manifest = {
        "asset_id": manifest.get("asset_id"),
        "display_name": manifest.get("display_name"),
        "description": manifest.get("description"),
        "asset_type": manifest.get("asset_type"),
        "target_use": manifest.get("target_use"),
        "sheet": sheet,
        "items": manifest.get("items", []),
        "tiles": manifest.get("tiles", []),
        "files": {"png": output.name, "webp": webp_output.name},
    }
    staged_outputs: list[tuple[Path, Path]] = []
    try:
        staged_outputs.append((stage_image(output, image, image_format="PNG"), output))
        staged_outputs.append(
            (
                stage_image(
                    webp_output,
                    image,
                    image_format="WEBP",
                    lossless=True,
                    quality=100,
                    method=6,
                ),
                webp_output,
            )
        )
        staged_outputs.append(
            (
                stage_text(summary_path, json.dumps(summary, indent=2) + "\n"),
                summary_path,
            )
        )
        staged_outputs.append(
            (
                stage_text(
                    asset_manifest_path,
                    json.dumps(asset_manifest, indent=2) + "\n",
                ),
                asset_manifest_path,
            )
        )
        commit_outputs(run_dir, staged_outputs, force=args.force)
    finally:
        for staged, _ in staged_outputs:
            staged.unlink(missing_ok=True)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
