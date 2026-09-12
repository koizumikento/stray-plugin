#!/usr/bin/env python3
"""Normalize a generated pixel-art asset image and extract grid cells."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

from PIL import Image, ImageDraw

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
    if not 0 <= tolerance <= 441:
        raise SystemExit("chroma tolerance must be 0..441 (RGB distance)")
    try:
        from _chroma_background import remove_chroma_background
    except ModuleNotFoundError as error:
        if error.name != "numpy":
            raise
        raise SystemExit("chroma removal requires NumPy; run with uv run --with numpy==2.4.3 --with pillow==12.3.0 python ...") from None

    return remove_chroma_background(image, key, threshold=tolerance,
                                    fringe_threshold=180, fringe_delta=20)


def normalize_source(
    source: Path,
    request: dict[str, object],
    *,
    chroma_tolerance: int,
    no_resize: bool,
    preserve_native: bool = False,
) -> tuple[Image.Image, list[str]]:
    with Image.open(source) as opened:
        image = opened.convert("RGBA")
    warnings: list[str] = []
    background = request.get("background") if isinstance(request.get("background"), dict) else {}
    if background.get("strategy") == "chroma-key":
        key = parse_hex_color(str(background.get("chroma_key", "#FF00FF")))
        image = remove_chroma_key(image, key, chroma_tolerance)

    if preserve_native:
        return image, warnings

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


def contact_anchor(image: Image.Image) -> tuple[float, int] | None:
    """Estimate the midpoint of the lowest opaque row, not the hair/body bbox."""
    pixels = image.load()
    for y in range(image.height - 1, -1, -1):
        xs = [x for x in range(image.width) if pixels[x, y][3] >= 128]
        if xs:
            return (xs[0] + xs[-1]) / 2, y
    return None


def trim_align_cell(image: Image.Image) -> tuple[Image.Image, dict[str, object]]:
    """Trim alpha-zero margins and translate onto the same canvas without rescaling."""
    bbox = image.getchannel("A").getbbox()
    anchor = contact_anchor(image)
    if bbox is None or anchor is None:
        raise SystemExit("trim-align requires a nonempty cell with an opaque contact anchor")
    left, top, right, bottom = bbox
    if left == 0 or top == 0 or right == image.width or bottom == image.height:
        raise SystemExit("trim-align refuses edge-touching content; check transparency or clipped poses first")
    target = ((image.width - 1) / 2, image.height - 2)
    dx = math.floor(target[0] - anchor[0] + 0.5)
    dy = target[1] - anchor[1]
    if left + dx < 0 or top + dy < 0 or right + dx > image.width or bottom + dy > image.height:
        raise SystemExit("trim-align would clip visible pixels; use a larger common cell or revise the source")
    result = Image.new("RGBA", image.size)
    result.paste(image.crop(bbox), (left + dx, top + dy))
    return result, {"alpha_bbox_before": bbox, "contact_anchor_before": anchor,
                    "translation": [dx, dy], "contact_anchor_after": [anchor[0] + dx, anchor[1] + dy]}


def pose_components(image: Image.Image, expected: int) -> list[list[dict[str, object]]]:
    """Find native-alpha poses conservatively; never discard detached components."""
    width, height = image.size
    remaining = bytearray(image.getchannel("A").point(lambda value: int(value > 0)).tobytes())
    components = []
    for seed in range(len(remaining)):
        if not remaining[seed]:
            continue
        remaining[seed] = 0
        stack = [seed]
        left = right = seed % width
        top = bottom = seed // width
        area = 0
        members = []
        while stack:
            current = stack.pop()
            x, y = current % width, current // width
            left, right, top, bottom = min(left, x), max(right, x), min(top, y), max(bottom, y)
            area += 1
            members.append(current)
            for ny in range(max(0, y - 1), min(height, y + 2)):
                for nx in range(max(0, x - 1), min(width, x + 2)):
                    neighbor = ny * width + nx
                    if remaining[neighbor]:
                        remaining[neighbor] = 0
                        stack.append(neighbor)
        if left == 0 or top == 0 or right == width - 1 or bottom == height - 1:
            raise SystemExit("components extraction refuses edge-touching content; repair clipped poses/background first")
        components.append({"bbox": (left, top, right + 1, bottom + 1), "pixels": area, "_members": members})
    components.sort(key=lambda part: part["pixels"], reverse=True)
    if len(components) < expected:
        raise SystemExit("components extraction found fewer separated poses than expected")
    # ponytail: similar-size pose cores plus much smaller detached parts only; ambiguous art needs regeneration or an explicit grid.
    cores = components[:expected]
    if (cores[-1]["pixels"] * 5 < cores[0]["pixels"]
            or (len(components) > expected and components[expected]["pixels"] * 4 >= cores[-1]["pixels"])):
        raise SystemExit("components extraction cannot distinguish the expected pose count from detached parts")
    groups = [[core] for core in cores]
    for part in components[expected:]:
        left, top, right, bottom = part["bbox"]
        distances = []
        for index, core in enumerate(cores):
            cl, ct, cr, cb = core["bbox"]
            dx, dy = max(cl - right, left - cr, 0), max(ct - bottom, top - cb, 0)
            distances.append((dx * dx + dy * dy, index))
        distances.sort()
        if len(distances) > 1 and distances[1][0] <= distances[0][0] * 2:
            raise SystemExit("components extraction cannot assign a detached part unambiguously")
        groups[distances[0][1]].append(part)
    groups.sort(key=lambda group: min(part["bbox"][0] for part in group))
    bounds = [group_bbox(group) for group in groups]
    if any(left[2] > right[0] for left, right in zip(bounds, bounds[1:])):
        raise SystemExit("components extraction refuses horizontally overlapping pose bounds")
    return groups


def group_bbox(group: list[dict[str, object]]) -> tuple[int, int, int, int]:
    bounds = [part["bbox"] for part in group]
    return min(b[0] for b in bounds), min(b[1] for b in bounds), max(b[2] for b in bounds), max(b[3] for b in bounds)


def pixel_lock_mask(size: tuple[int, int], config: dict) -> Image.Image:
    """Explicit final-cell rectangles only; no inferred anatomy or soft masks."""
    if not isinstance(config, dict) or set(config) != {"mutable_rects"}:
        raise SystemExit("pixel_lock requires only mutable_rects in final-cell coordinates")
    rects = config["mutable_rects"]
    if not isinstance(rects, list) or not rects:
        raise SystemExit("pixel_lock requires nonempty mutable_rects")
    mask = Image.new("L", size)
    draw = ImageDraw.Draw(mask)
    for rect in rects:
        if not isinstance(rect, list) or len(rect) != 4 or any(type(v) is not int for v in rect):
            raise SystemExit("pixel_lock rectangles must be four integers [left, top, right, bottom]")
        left, top, right, bottom = rect
        if not (0 <= left < right <= size[0] and 0 <= top < bottom <= size[1]):
            raise SystemExit("pixel_lock rectangle is empty or outside the final cell")
        draw.rectangle((left, top, right - 1, bottom - 1), fill=255)
    if mask.getextrema() == (255, 255):
        raise SystemExit("pixel_lock must retain a fixed region; mutable_rects cover the whole cell")
    return mask


def lock_frame_pixels(reference: Image.Image, frame: Image.Image, mask: Image.Image) -> tuple[Image.Image, dict]:
    """Keep cell 0 outside the mask and reuse its RGB palette inside it."""
    if reference.size != frame.size or mask.size != frame.size:
        raise SystemExit("pixel_lock requires equal final-cell sizes")
    alpha = frame.getchannel("A")
    if alpha.getbbox() is None or alpha.getextrema()[0] > 0:
        raise SystemExit("pixel_lock requires a nonempty full frame with transparent background; repair missing/opaque source frames first")
    base, source, selected = list(reference.get_flattened_data()), list(frame.get_flattened_data()), list(mask.get_flattened_data())
    palette = sorted({pixel[:3] for pixel in base if pixel[3]})
    if not palette:
        raise SystemExit("pixel_lock reference cell is empty")
    output, mapped = [], {}
    for original, candidate, mutable in zip(base, source, selected):
        if not mutable:
            output.append(original)
        elif candidate[3]:
            rgb = candidate[:3]
            if rgb not in mapped:
                mapped[rgb] = min(palette, key=lambda color: sum((a-b)**2 for a, b in zip(rgb, color)))
            output.append((*mapped[rgb], candidate[3]))
        else:
            output.append(candidate)  # Replace alpha too, so moving edges leave no trails.
    result = Image.new("RGBA", frame.size)
    result.putdata(output)
    return result, {
        "reference_cell": 0, "reference_rgba_sha256": hashlib.sha256(reference.tobytes()).hexdigest(),
        "source_rgba_sha256": hashlib.sha256(frame.tobytes()).hexdigest(),
        "palette": "reference-cell-rgb-nearest", "palette_colors": len(palette),
        "changed_outside_before": sum(a != b and not m for a, b, m in zip(base, source, selected)),
        "changed_outside_after": sum(a != b and not m for a, b, m in zip(base, output, selected)),
        "changed_inside_after": sum(a != b and bool(m) for a, b, m in zip(base, output, selected)),
    }


def extract_components(image: Image.Image, sheet: dict[str, object], registration: str,
                       *, no_resize: bool) -> list[tuple[Image.Image, dict[str, object]]]:
    count, cell_w, cell_h = sheet["used_cells"], sheet["cell_width"], sheet["cell_height"]
    if sheet.get("structure") != "sprite-row" or sheet["rows"] != 1 or count != sheet["columns"]:
        raise SystemExit("components extraction requires one sprite-row with every column used")
    if min(cell_w, cell_h) < 4:
        raise SystemExit("components extraction requires cells at least 4x4 for safe margins")
    if registration not in {"fixed", "free", "unspecified"}:
        raise SystemExit("components extraction requires fixed/free/unspecified registration")
    groups = pose_components(image, count)
    bounds = [group_bbox(group) for group in groups]
    crops = [image.crop(bbox) for bbox in bounds]
    anchors = [contact_anchor(crop) for crop in crops]
    scale = 1.0
    target_x, target_y = (cell_w - 1) / 2, cell_h - 2
    if registration == "fixed":
        if any(anchor is None for anchor in anchors):
            raise SystemExit("fixed component poses require opaque contact anchors")
        for crop, (ax, ay) in zip(crops, anchors):
            for available, extent in ((target_x - 1, ax), (cell_w - 2 - target_x, crop.width - 1 - ax),
                                      (target_y - 1, ay), (cell_h - 1 - target_y, crop.height - 1 - ay)):
                if extent > 0:
                    scale = min(scale, available / extent)
    else:
        slot = image.width / count
        horizontal_extent = max(max(abs(bbox[0] - (i + .5) * slot), abs(bbox[2] - (i + .5) * slot))
                                for i, bbox in enumerate(bounds))
        scale = min(scale, (cell_w - 2) / (2 * horizontal_extent), (cell_h - 2) / image.height)
    if no_resize and scale < 1:
        raise SystemExit("component poses require a smaller common scale; --no-resize forbids it")
    results = []
    for index, (crop, bbox, group) in enumerate(zip(crops, bounds, groups)):
        size = max(1, round(crop.width * scale)), max(1, round(crop.height * scale))
        resized = crop.resize(size, Image.Resampling.NEAREST) if size != crop.size else crop
        # Do not silently erase an entire detached part during downsampling.
        if size != crop.size:
            for part in group:
                mask = Image.new("L", crop.size)
                pixels = mask.load()
                for member in part["_members"]:
                    pixels[member % image.width - bbox[0], member // image.width - bbox[1]] = 255
                if not mask.resize(size, Image.Resampling.NEAREST).getbbox():
                    raise SystemExit("a component disappears at the common scale; use larger cells")
        if registration == "fixed":
            anchor = contact_anchor(resized)
            if anchor is None:
                raise SystemExit("common scale lost an opaque contact anchor; use larger cells")
            x, y = math.floor(target_x - anchor[0] + .5), target_y - anchor[1]
        else:
            x = round(cell_w / 2 + (bbox[0] - (index + .5) * image.width / count) * scale)
            y = round((cell_h - image.height * scale) / 2 + bbox[1] * scale)
        if x < 0 or y < 0 or x + resized.width > cell_w or y + resized.height > cell_h:
            raise SystemExit("component placement would clip visible content; use larger cells or revise poses")
        result = Image.new("RGBA", (cell_w, cell_h))
        result.paste(resized, (x, y))
        results.append((result, {"source_bbox": bbox,
                                 "source_components": [{"bbox": part["bbox"], "pixels": part["pixels"]} for part in group], "common_scale": scale,
                                 "scaled_size": size, "placement": [x, y], "registration": registration,
                                 "contact_anchor_after": contact_anchor(result)}))
    return results


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--source", default="")
    parser.add_argument("--output-dir", default="")
    parser.add_argument("--chroma-tolerance", type=int, default=96)
    parser.add_argument("--no-resize", action="store_true")
    parser.add_argument("--include-unused", action="store_true")
    parser.add_argument("--extraction", choices=("grid", "components"), default=None)
    parser.add_argument("--trim-align", action="store_true", help="After visual alpha/contact verification, trim and align fixed-contact animation cells")
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
    lock_config = request.get("animation", {}).get("pixel_lock")
    lock_mask = None
    if lock_config is not None:
        if (sheet.get("structure") != "sprite-row" or rows != 1 or used_cells < 2
                or request.get("animation", {}).get("registration") != "fixed"):
            raise SystemExit("pixel_lock requires a fixed sprite-row with at least two used cells")
        lock_mask = pixel_lock_mask((cell_w, cell_h), lock_config)
    extraction = args.extraction or sheet.get("extraction", "grid")
    if extraction not in {"grid", "components"}:
        raise SystemExit("unknown sheet extraction mode")
    if extraction == "components":
        fields = ("columns", "rows", "cell_width", "cell_height", "used_cells")
        if any(type(sheet.get(key)) is not int or sheet[key] <= 0 for key in fields):
            raise SystemExit("components extraction requires positive integer sheet dimensions/count")
        if args.trim_align:
            raise SystemExit("components extraction handles registration; do not combine it with --trim-align")
    if args.trim_align and (sheet.get("structure") not in {"sprite-row", "sprite-sheet"}
                            or request.get("animation", {}).get("registration") != "fixed"):
        raise SystemExit("--trim-align requires a fixed-contact animation contract; free/unspecified motion must retain its offsets")
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
        preserve_native=extraction == "components",
    )
    component_cells = (extract_components(image, sheet, request.get("animation", {}).get("registration", "unspecified"),
                                          no_resize=args.no_resize) if extraction == "components" else None)
    staged_dir = create_staged_directory(output_dir)
    normalized = output_dir / "source-normalized.png"
    manifest_path = output_dir / "cells-manifest.json"
    try:
        write_staged_image(staged_dir / normalized.name, image, image_format="PNG")

        cells: list[dict[str, object]] = []
        reference_cell = None
        for index in range(columns * rows):
            used = index < used_cells
            if not used and not args.include_unused:
                cells.append({"index": index, "used": False, "path": None})
                continue
            row = index // columns
            column = index % columns
            name = f"cell-{index:02d}.png"
            alignment = None
            component_metadata = None
            if component_cells is not None and used:
                crop, component_metadata = component_cells[index]
            else:
                crop = image.crop((column * cell_w, row * cell_h, (column + 1) * cell_w, (row + 1) * cell_h))
                if args.trim_align and used:
                    crop, alignment = trim_align_cell(crop)
            pixel_lock = None
            if lock_mask is not None and used:
                if reference_cell is None:
                    reference_cell = crop.copy()
                crop, pixel_lock = lock_frame_pixels(reference_cell, crop, lock_mask)
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
                    "alignment": alignment,
                    "component_extraction": component_metadata,
                    "pixel_lock": pixel_lock,
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
            "background": request.get("background", {}),
            "chroma_removal": ({"threshold": args.chroma_tolerance, "fringe_threshold": 180,
                                "fringe_delta": 20, "unmix_reach": 4}
                               if request.get("background", {}).get("strategy") == "chroma-key" else None),
            "animation": request.get("animation", {}),
            "trim_align": args.trim_align,
            "extraction": extraction,
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
