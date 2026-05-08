#!/usr/bin/env python3
"""Slice a packaged pixel-art asset sheet into per-cell PNG files."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from PIL import Image


def load_json(path: Path) -> dict[str, object]:
    if not path.exists():
        raise SystemExit(f"missing JSON file: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-{2,}", "-", value)
    return value.strip("-") or "asset"


def cell_names(request: dict[str, object], used_cells: int) -> list[str]:
    items = request.get("items") if isinstance(request.get("items"), list) else []
    tiles = request.get("tiles") if isinstance(request.get("tiles"), list) else []
    names = [str(item) for item in (items or tiles)]
    while len(names) < used_cells:
        names.append(f"cell-{len(names):02d}")
    return [slugify(name) for name in names[:used_cells]]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--image", default="")
    parser.add_argument("--output-dir", default="")
    parser.add_argument("--include-unused", action="store_true")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    run_dir = Path(args.run_dir).expanduser().resolve()
    request = load_json(run_dir / "asset_request.json")
    sheet = request.get("sheet")
    if not isinstance(sheet, dict):
        raise SystemExit("asset_request.json is missing sheet contract")
    columns = int(sheet["columns"])
    rows = int(sheet["rows"])
    cell_w = int(sheet["cell_width"])
    cell_h = int(sheet["cell_height"])
    used_cells = int(sheet["used_cells"])

    image_path = Path(args.image).expanduser().resolve() if args.image else run_dir / "final" / "asset.png"
    output_dir = Path(args.output_dir).expanduser().resolve() if args.output_dir else run_dir / "final" / "cells"
    if output_dir.exists() and any(output_dir.iterdir()) and not args.force:
        raise SystemExit(f"{output_dir} is not empty; pass --force to replace files")
    output_dir.mkdir(parents=True, exist_ok=True)

    names = cell_names(request, used_cells)
    written: list[str] = []
    with Image.open(image_path) as opened:
        image = opened.convert("RGBA")
        for index in range(columns * rows):
            if index >= used_cells and not args.include_unused:
                continue
            row = index // columns
            column = index % columns
            crop = image.crop((column * cell_w, row * cell_h, (column + 1) * cell_w, (row + 1) * cell_h))
            name = names[index] if index < len(names) else f"unused-{index:02d}"
            target = output_dir / f"{index:02d}-{name}.png"
            crop.save(target)
            written.append(str(target))

    manifest = {"ok": True, "output_dir": str(output_dir), "files": written}
    (output_dir / "cells-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
