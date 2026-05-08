#!/usr/bin/env python3
"""Compose extracted pixel-art cells into a normalized asset sheet."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image


def load_json(path: Path) -> dict[str, object]:
    if not path.exists():
        raise SystemExit(f"missing JSON file: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cells-dir", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--webp-output", default="")
    args = parser.parse_args()

    cells_dir = Path(args.cells_dir).expanduser().resolve()
    manifest = load_json(cells_dir / "cells-manifest.json")
    sheet = manifest.get("sheet")
    if not isinstance(sheet, dict):
        raise SystemExit("cells manifest is missing sheet contract")
    columns = int(sheet["columns"])
    cell_w = int(sheet["cell_width"])
    cell_h = int(sheet["cell_height"])
    width = int(sheet["width"])
    height = int(sheet["height"])
    output = Path(args.output).expanduser().resolve()
    output.parent.mkdir(parents=True, exist_ok=True)

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
        with Image.open(cells_dir / raw_path) as opened:
            cell = opened.convert("RGBA")
        if cell.size != (cell_w, cell_h):
            cell = cell.resize((cell_w, cell_h), Image.Resampling.NEAREST)
        image.alpha_composite(cell, (column * cell_w, row * cell_h))

    image.save(output)
    webp_output = Path(args.webp_output).expanduser().resolve() if args.webp_output else output.with_suffix(".webp")
    webp_output.parent.mkdir(parents=True, exist_ok=True)
    image.save(webp_output, format="WEBP", lossless=True, quality=100, method=6)
    summary = {"ok": True, "output": str(output), "webp_output": str(webp_output), "sheet": sheet}
    (output.parent / "compose-summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
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
    (output.parent / "asset-manifest.json").write_text(json.dumps(asset_manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
