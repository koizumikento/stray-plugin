#!/usr/bin/env python3
"""Render a simple GIF preview for sprite-row pixel-art asset sheets."""

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
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--image", default="")
    parser.add_argument("--output", default="")
    parser.add_argument("--duration", type=int, default=140)
    parser.add_argument("--scale", type=int, default=4)
    parser.add_argument("--force-non-row", action="store_true")
    args = parser.parse_args()

    run_dir = Path(args.run_dir).expanduser().resolve()
    request = load_json(run_dir / "asset_request.json")
    sheet = request.get("sheet")
    if not isinstance(sheet, dict):
        raise SystemExit("asset_request.json is missing sheet contract")
    if sheet.get("structure") != "sprite-row" and not args.force_non_row:
        print(json.dumps({"ok": True, "skipped": True, "reason": "asset is not a sprite-row"}, indent=2))
        return

    image_path = Path(args.image).expanduser().resolve() if args.image else run_dir / "final" / "asset.png"
    output = Path(args.output).expanduser().resolve() if args.output else run_dir / "qa" / "previews" / "animation.gif"
    output.parent.mkdir(parents=True, exist_ok=True)
    columns = int(sheet["columns"])
    cell_w = int(sheet["cell_width"])
    cell_h = int(sheet["cell_height"])
    used = int(sheet["used_cells"])
    frames: list[Image.Image] = []

    with Image.open(image_path) as opened:
        source = opened.convert("RGBA")
        for index in range(used):
            row = index // columns
            column = index % columns
            frame = source.crop((column * cell_w, row * cell_h, (column + 1) * cell_w, (row + 1) * cell_h))
            if args.scale != 1:
                frame = frame.resize((cell_w * args.scale, cell_h * args.scale), Image.Resampling.NEAREST)
            frames.append(frame)

    if not frames:
        raise SystemExit("no frames to render")
    frames[0].save(
        output,
        save_all=True,
        append_images=frames[1:],
        duration=args.duration,
        loop=0,
        disposal=2,
        transparency=0,
    )
    print(json.dumps({"ok": True, "preview": str(output), "frames": len(frames)}, indent=2))


if __name__ == "__main__":
    main()
