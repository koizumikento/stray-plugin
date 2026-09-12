#!/usr/bin/env python3
"""Render GIF and portable interactive HTML previews for sprite sheets."""

from __future__ import annotations

import argparse
import base64
import io
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
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--image", default="")
    parser.add_argument("--output", default="")
    parser.add_argument("--html-output", default="")
    parser.add_argument("--duration", type=int, default=140)
    parser.add_argument("--scale", type=int, default=4)
    parser.add_argument("--force-non-row", action="store_true")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    if not 10 <= args.duration <= 655350 or args.scale < 1:
        raise SystemExit("duration must be 10..655350 ms and scale must be positive")

    run_dir = Path(args.run_dir).expanduser().resolve()
    request = load_json(resolve_run_path(run_dir, "asset_request.json", field="asset request"))
    sheet = request.get("sheet")
    if not isinstance(sheet, dict):
        raise SystemExit("asset_request.json is missing sheet contract")
    if sheet.get("structure") != "sprite-row" and not args.force_non_row:
        print(json.dumps({"ok": True, "skipped": True, "reason": "asset is not a sprite-row"}, indent=2))
        return

    image_path = (
        Path(args.image).expanduser().resolve()
        if args.image
        else resolve_run_path(run_dir, "final/asset.png", field="default asset image")
    )
    output = resolve_output(
        run_dir,
        args.output or "qa/previews/animation.gif",
        field="animation preview output",
        force=args.force,
    )
    html_output = resolve_output(
        run_dir,
        args.html_output or "qa/previews/animation.html",
        field="HTML animation preview output",
        force=args.force,
    )
    if output == html_output:
        raise SystemExit("GIF and HTML outputs must be different")
    fields = ("columns", "rows", "cell_width", "cell_height", "used_cells", "width", "height")
    if any(type(sheet.get(key)) is not int or sheet[key] <= 0 for key in fields):
        raise SystemExit("sheet dimensions and used_cells must be positive integers")
    columns, rows, cell_w, cell_h, used, width, height = (sheet[key] for key in fields)
    if used > columns * rows or (width, height) != (columns * cell_w, rows * cell_h):
        raise SystemExit("sheet dimensions or frame count conflict with the grid")
    frames: list[Image.Image] = []

    with Image.open(image_path) as opened:
        if opened.size != (width, height):
            raise SystemExit(f"asset image must be {width}x{height}, got {opened.width}x{opened.height}")
        source = opened.convert("RGBA")
        for index in range(used):
            row = index // columns
            column = index % columns
            frame = source.crop((column * cell_w, row * cell_h, (column + 1) * cell_w, (row + 1) * cell_h))
            if args.scale != 1:
                frame = frame.resize((cell_w * args.scale, cell_h * args.scale), Image.Resampling.NEAREST)
            frames.append(frame)

    png = io.BytesIO()
    source.save(png, format="PNG")
    config = dict(columns=columns, rows=rows, width=cell_w, height=cell_h,
                  count=used, duration=args.duration, scale=args.scale,
                  image="data:image/png;base64," + base64.b64encode(png.getvalue()).decode("ascii"))
    template = Path(__file__).with_name("animation_preview.html").read_text(encoding="utf-8")
    html = template.replace("__PREVIEW_CONFIG__", json.dumps(config))
    staged_outputs = []
    try:
        staged_outputs.append((stage_image(
            output, frames[0], image_format="GIF", save_all=True, append_images=frames[1:],
            duration=args.duration, loop=0, disposal=2, transparency=0,
        ), output))
        staged_outputs.append((stage_text(html_output, html), html_output))
        commit_outputs(run_dir, staged_outputs, force=args.force)
    finally:
        for staged, _ in staged_outputs:
            staged.unlink(missing_ok=True)
    print(json.dumps({"ok": True, "preview": str(output), "html_preview": str(html_output),
                      "frames": len(frames)}, indent=2))


if __name__ == "__main__":
    main()
