#!/usr/bin/env python3
"""Create a labeled contact sheet for a pixel-art asset sheet."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from _output_pipeline import commit_outputs, resolve_output, stage_image
from _run_safety import resolve_run_path

LABEL_HEIGHT = 22


def load_json(path: Path) -> dict[str, object]:
    if not path.exists():
        raise SystemExit(f"missing JSON file: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def checker(size: tuple[int, int], square: int = 8) -> Image.Image:
    image = Image.new("RGB", size, "#ffffff")
    draw = ImageDraw.Draw(image)
    for y in range(0, size[1], square):
        for x in range(0, size[0], square):
            if (x // square + y // square) % 2:
                draw.rectangle((x, y, x + square - 1, y + square - 1), fill="#e8e8e8")
    return image


def load_request(args: argparse.Namespace) -> tuple[dict[str, object], Path, Path]:
    run_dir = Path(args.run_dir).expanduser().resolve()
    request = load_json(resolve_run_path(run_dir, "asset_request.json", field="asset request"))
    image_path = (
        Path(args.image).expanduser().resolve()
        if args.image
        else resolve_run_path(run_dir, "final/asset.png", field="default asset image")
    )
    return request, image_path, run_dir


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--image", default="")
    parser.add_argument("--output", default="")
    parser.add_argument("--scale", type=float, default=2.0)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    request, image_path, run_dir = load_request(args)
    output_path = resolve_output(
        run_dir,
        args.output or "qa/contact-sheet.png",
        field="contact sheet output",
        force=args.force,
    )
    sheet = request.get("sheet")
    if not isinstance(sheet, dict):
        raise SystemExit("asset_request.json is missing sheet contract")
    columns = int(sheet["columns"])
    rows = int(sheet["rows"])
    cell_w = int(sheet["cell_width"])
    cell_h = int(sheet["cell_height"])
    used_cells = int(sheet["used_cells"])

    with Image.open(image_path) as opened:
        image = opened.convert("RGBA")

    view_w = max(1, round(cell_w * args.scale))
    view_h = max(1, round(cell_h * args.scale))
    width = columns * view_w
    height = rows * (view_h + LABEL_HEIGHT)
    contact = Image.new("RGB", (width, height), "#f7f7f7")
    draw = ImageDraw.Draw(contact)
    font = ImageFont.load_default()

    for row in range(rows):
        y = row * (view_h + LABEL_HEIGHT)
        draw.rectangle((0, y, width, y + LABEL_HEIGHT - 1), fill="#111111")
        draw.text((6, y + 5), f"row {row}", fill="#ffffff", font=font)
        for column in range(columns):
            index = row * columns + column
            crop = image.crop((column * cell_w, row * cell_h, (column + 1) * cell_w, (row + 1) * cell_h))
            crop = crop.resize((view_w, view_h), Image.Resampling.NEAREST)
            bg = checker((view_w, view_h))
            bg.paste(crop, (0, 0), crop)
            x = column * view_w
            contact.paste(bg, (x, y + LABEL_HEIGHT))
            outline = "#18a058" if index < used_cells else "#cc3344"
            draw.rectangle((x, y + LABEL_HEIGHT, x + view_w - 1, y + LABEL_HEIGHT + view_h - 1), outline=outline)
            draw.text((x + 4, y + LABEL_HEIGHT + 4), str(index), fill="#111111", font=font)

    staged = stage_image(output_path, contact, image_format="PNG")
    commit_outputs(run_dir, [(staged, output_path)], force=args.force)
    print(json.dumps({"ok": True, "contact_sheet": str(output_path)}, indent=2))


if __name__ == "__main__":
    main()
