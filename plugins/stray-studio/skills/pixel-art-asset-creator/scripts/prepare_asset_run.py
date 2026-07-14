#!/usr/bin/env python3
"""Create a pixel-art asset run folder, prompts, and imagegen job manifest."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import shutil
import sys
import tempfile
import uuid
from datetime import datetime, timezone
from pathlib import Path

from _image_input_safety import read_validated_image_input
from _run_safety import require_safe_managed_replacement, write_run_marker

DEFAULT_STYLE = (
    "Pixel-art-adjacent game asset style: compact readable silhouette, "
    "low-resolution sprite logic, visible stepped edges, limited palette, crisp dark "
    "outline when appropriate, flat cel-style shading, one clear light direction, "
    "minimal texture, no tiny detail that disappears at target size, and clean "
    "transparent-background readiness."
)

AVOID_STYLE = (
    "Avoid polished illustration, anime key art, 3D render, glossy app icon, vector "
    "mascot, painterly rendering, realistic fur or material texture, soft gradients, "
    "high-detail antialiasing, excessive tiny accessories, text, labels, scenery, "
    "visible grids, checkerboard transparency, shadows, glows, halos, blur, smears, "
    "watermarks, and unrelated props."
)


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-{2,}", "-", value)
    return value.strip("-")


def display_from_slug(value: str) -> str:
    words = [word for word in re.split(r"[^a-zA-Z0-9]+", value) if word]
    return " ".join(word.capitalize() for word in words)


def parse_size(value: str, *, field: str) -> tuple[int, int]:
    raw = value.lower().replace(" ", "")
    match = re.fullmatch(r"(\d+)x(\d+)", raw)
    if not match:
        raise SystemExit(f"{field} must use WIDTHxHEIGHT format, got {value!r}")
    width = int(match.group(1))
    height = int(match.group(2))
    if width <= 0 or height <= 0:
        raise SystemExit(f"{field} dimensions must be positive")
    return width, height


def parse_list(values: list[str] | None) -> list[str]:
    if not values:
        return []
    result: list[str] = []
    for value in values:
        for item in re.split(r"[,;\n]", value):
            item = item.strip()
            if item:
                result.append(item)
    return result


def infer_name(args: argparse.Namespace, references: list[Path]) -> str:
    if args.asset_name.strip():
        return args.asset_name.strip()
    if args.description.strip():
        words = [
            word
            for word in re.findall(r"[A-Za-z0-9]+", args.description)
            if word.lower()
            not in {
                "a",
                "an",
                "and",
                "asset",
                "for",
                "from",
                "icon",
                "pixel",
                "sprite",
                "style",
                "the",
                "with",
            }
        ]
        if words:
            return " ".join(words[:3])
    if references:
        return display_from_slug(references[0].stem)
    return "Pixel Asset"


def resolve_references(paths: list[str] | None) -> list[Path]:
    references: list[Path] = []
    seen_hashes: set[str] = set()
    for raw in paths or []:
        path = Path(raw).expanduser().resolve()
        if not path.is_file():
            raise SystemExit(f"reference image not found: {path}")
        _, payload = read_validated_image_input(path, field="reference image")
        digest = hashlib.sha256(payload).hexdigest()
        if digest in seen_hashes:
            raise SystemExit(f"duplicate reference image content is not allowed: {path}")
        seen_hashes.add(digest)
        references.append(path)
    return references


def resolve_output_destination(raw_path: str) -> Path:
    """Resolve an output directory only after rejecting every lexical symlink."""
    supplied = Path(raw_path).expanduser()
    if supplied.is_absolute():
        cursor = Path(supplied.anchor)
        parts = supplied.parts[1:]
    else:
        cursor = Path.cwd()
        parts = supplied.parts
    for part in parts:
        if part in {"", "."}:
            continue
        if part == "..":
            cursor = cursor.parent
            continue
        cursor /= part
        if cursor.is_symlink():
            raise SystemExit(
                f"--output-dir must not contain symlink components: {supplied}"
            )
    return supplied.resolve()


def choose_structure(args: argparse.Namespace, items: list[str], tiles: list[str]) -> str:
    if args.sheet_structure != "auto":
        return args.sheet_structure
    if args.frame_count and args.frame_count > 1:
        return "sprite-row"
    if items:
        return "item-set"
    if tiles or "tile" in args.asset_type.lower():
        return "tileset"
    if args.sheet_columns and args.sheet_rows and args.sheet_columns * args.sheet_rows > 1:
        return "sprite-sheet"
    return "standalone"


def sheet_contract(
    args: argparse.Namespace,
    structure: str,
    *,
    target_size: tuple[int, int],
    cell_size: tuple[int, int],
    items: list[str],
    tiles: list[str],
) -> dict[str, object]:
    if structure == "standalone":
        columns = 1
        rows = 1
        cell_w, cell_h = target_size
        used = 1
    elif structure == "sprite-row":
        used = args.frame_count or args.sheet_columns or 4
        columns = args.sheet_columns or used
        rows = args.sheet_rows or 1
        cell_w, cell_h = cell_size
    elif structure == "item-set":
        used = len(items) if items else args.frame_count or 4
        columns = args.sheet_columns or max(1, math.ceil(math.sqrt(used)))
        rows = args.sheet_rows or max(1, math.ceil(used / columns))
        cell_w, cell_h = cell_size
    elif structure == "tileset":
        used = len(tiles) if tiles else args.frame_count or None
        columns = args.sheet_columns or 4
        rows = args.sheet_rows or 4
        used = used or columns * rows
        tile_size = parse_size(args.tile_size, field="--tile-size") if args.tile_size else cell_size
        cell_w, cell_h = tile_size
    else:
        used = args.frame_count or args.sheet_columns or 4
        columns = args.sheet_columns or used
        rows = args.sheet_rows or 1
        cell_w, cell_h = cell_size

    if columns <= 0 or rows <= 0:
        raise SystemExit("sheet columns and rows must be positive")
    if used > columns * rows:
        raise SystemExit(
            f"used cells ({used}) exceed grid capacity ({columns}x{rows})"
        )

    return {
        "structure": structure,
        "columns": columns,
        "rows": rows,
        "cell_width": cell_w,
        "cell_height": cell_h,
        "width": columns * cell_w,
        "height": rows * cell_h,
        "used_cells": used,
    }


def background_text(args: argparse.Namespace) -> str:
    if args.background == "transparent":
        return "a clean transparent background"
    return f"a perfectly flat pure {args.chroma_key.upper()} chroma-key background"


def style_contract(args: argparse.Namespace) -> str:
    if not args.style_notes.strip():
        return DEFAULT_STYLE
    return f"{DEFAULT_STYLE} Additional user style notes: {args.style_notes.strip()}."


def base_prompt(args: argparse.Namespace, request: dict[str, object]) -> str:
    target = request["target_size"]
    return f"""Create a single clean pixel-art style base asset for {request["display_name"]}.

Asset: {request["description"]}.
Asset type: {request["asset_type"]}.
Target use: {request["target_use"]}.
Target size: {target["width"]}x{target["height"]}.
Style contract: {style_contract(args)}

Use this prompt as an authoritative production asset spec. Do not expand it into a polished illustration, anime key art, 3D render, glossy icon, vector mascot, painterly image, or marketing artwork.

Output one centered complete asset only, with safe padding, on {background_text(args)}. The asset must remain readable at {target["width"]}x{target["height"]}. {AVOID_STYLE} Do not include unrelated props or alternate variants."""


def sheet_prompt(
    args: argparse.Namespace,
    request: dict[str, object],
    *,
    items: list[str],
    tiles: list[str],
) -> str:
    sheet = request["sheet"]
    structure = str(sheet["structure"])
    base = f"""Create a production pixel-art asset sheet for {request["display_name"]}.

Use the attached reference image(s) for identity and the attached base asset as the canonical design. Do not redesign the asset family, palette, outline, material, lighting direction, or silhouette language. Simplify detailed references into the requested pixel-art style.

Grid: {sheet["columns"]} columns x {sheet["rows"]} rows.
Cell size: {sheet["cell_width"]}x{sheet["cell_height"]}.
Full sheet target: {sheet["width"]}x{sheet["height"]}.
Used cells: {sheet["used_cells"]}.
Asset type: {request["asset_type"]}.
Target use: {request["target_use"]}.
Style contract: {style_contract(args)}

Use this prompt as an authoritative production asset spec. Do not expand it into hero art, polished illustration, anime key art, 3D render, glossy icon, vector mascot, painterly image, or marketing artwork.
"""
    if structure == "sprite-row":
        beats = args.motion_beats.strip() or "clear readable motion beats from start to finish"
        body = f"""
Create exactly {sheet["used_cells"]} animation frames arranged left-to-right in one horizontal row. Treat the row as {sheet["used_cells"]} equal-width invisible frame slots. Fill every used slot with exactly one complete centered pose. No pose may be cropped, overlap another pose, or cross into a neighboring slot.

Animation action: {beats}.
"""
    elif structure == "tileset":
        tile_list = ", ".join(tiles) if tiles else "terrain center, edges, corners, transitions, and a few simple decoration tiles"
        body = f"""
Create a tileset. Tiles required: {tile_list}. Every tile must align to the same grid, use the same perspective and palette, and connect cleanly to neighboring tiles when it represents an edge, corner, or transition.
"""
    elif structure == "item-set":
        item_list = ", ".join(items) if items else f"{sheet['used_cells']} related item assets"
        body = f"""
Create an item or icon sheet. Items required: {item_list}. Each used cell must contain one centered complete asset with consistent scale, outline, lighting, palette discipline, and safe padding. Keep silhouettes distinct.
"""
    else:
        body = """
Create a consistent multi-cell sprite or asset sheet. Each used cell must contain one centered complete asset or pose with consistent scale, outline, lighting, palette discipline, and safe padding.
"""

    return (
        base
        + body
        + f"""
Background: {background_text(args)}.

Do not include visible grid lines, borders, labels, frame numbers, scenery, checkerboard transparency, speed lines, motion blur, floor shadows, glows, dust, loose particles, watermarks, or detached effects unless the brief explicitly requires an attached hard-edged sprite effect. Leave unused cells empty with only the background color."""
    )


def copy_references(references: list[Path], run_dir: Path) -> list[dict[str, object]]:
    entries: list[dict[str, object]] = []
    seen_hashes: set[str] = set()
    reference_dir = run_dir / "references" / "source-images"
    reference_dir.mkdir(parents=True, exist_ok=True)
    for index, source in enumerate(references, start=1):
        validated, payload = read_validated_image_input(source, field="reference image")
        digest = hashlib.sha256(payload).hexdigest()
        if digest in seen_hashes:
            raise SystemExit(f"duplicate reference image content is not allowed: {source}")
        seen_hashes.add(digest)
        suffix = validated.suffix
        target = reference_dir / f"reference-{index:02d}{suffix}"
        target.write_bytes(payload)
        entries.append(
            {
                "path": str(target.relative_to(run_dir)),
                "role": "source visual reference",
                "original_path": str(source),
                "sha256": digest,
            }
        )
    return entries


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def write_json(path: Path, data: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def install_staged_run(staging_dir: Path, run_dir: Path, *, replacing: bool) -> None:
    """Publish a complete sibling run, restoring the old run if publication fails."""
    if not replacing:
        os.replace(staging_dir, run_dir)
        return

    backup = run_dir.with_name(f".{run_dir.name}.replaced-{uuid.uuid4().hex}")
    os.replace(run_dir, backup)
    try:
        os.replace(staging_dir, run_dir)
    except Exception:
        os.replace(backup, run_dir)
        raise
    try:
        shutil.rmtree(backup)
    except OSError as exc:
        print(f"warning: new run installed but old backup remains at {backup}: {exc}", file=sys.stderr)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--asset-name", default="")
    parser.add_argument("--description", default="A clean pixel-art asset.")
    parser.add_argument("--asset-type", default="sprite")
    parser.add_argument("--target-use", default="game or app asset")
    parser.add_argument("--target-size", default="64x64")
    parser.add_argument("--sheet-structure", default="auto", choices=["auto", "standalone", "sprite-row", "sprite-sheet", "item-set", "tileset"])
    parser.add_argument("--cell-size", default="")
    parser.add_argument("--tile-size", default="")
    parser.add_argument("--sheet-columns", type=int)
    parser.add_argument("--sheet-rows", type=int)
    parser.add_argument("--frame-count", type=int)
    parser.add_argument("--item", action="append")
    parser.add_argument("--items", action="append")
    parser.add_argument("--tile", action="append")
    parser.add_argument("--tiles", action="append")
    parser.add_argument("--motion-beats", default="")
    parser.add_argument("--style-notes", default="")
    parser.add_argument("--reference", action="append")
    parser.add_argument("--background", default="chroma-key", choices=["chroma-key", "transparent"])
    parser.add_argument("--chroma-key", default="#FF00FF")
    parser.add_argument("--output-dir", default="")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    if not re.fullmatch(r"#[0-9A-Fa-f]{6}", args.chroma_key):
        raise SystemExit("--chroma-key must be a hex color like #FF00FF")

    references = resolve_references(args.reference)
    display_name = infer_name(args, references)
    asset_id = slugify(display_name)
    if not asset_id:
        raise SystemExit("asset name must contain at least one letter or digit")

    target_size = parse_size(args.target_size, field="--target-size")
    cell_size = parse_size(args.cell_size, field="--cell-size") if args.cell_size else target_size
    items = parse_list(args.items) + parse_list(args.item)
    tiles = parse_list(args.tiles) + parse_list(args.tile)
    structure = choose_structure(args, items, tiles)
    sheet = sheet_contract(
        args,
        structure,
        target_size=target_size,
        cell_size=cell_size,
        items=items,
        tiles=tiles,
    )

    if args.output_dir:
        run_dir = resolve_output_destination(args.output_dir)
    else:
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
        run_dir = resolve_output_destination(
            str(Path.cwd() / "tmp" / "pixel-art-assets" / f"{asset_id}-{timestamp}")
        )
    replacing = run_dir.exists()
    if replacing:
        if not args.force:
            raise SystemExit(f"{run_dir} already exists; pass --force to replace it")
        require_safe_managed_replacement(run_dir)
        for reference in references:
            try:
                reference.relative_to(run_dir)
            except ValueError:
                continue
            raise SystemExit(
                f"refusing to replace a run that contains its own reference image: {reference}"
            )

    run_dir.parent.mkdir(parents=True, exist_ok=True)
    staging_dir = Path(
        tempfile.mkdtemp(prefix=f".{run_dir.name}.staging-", dir=run_dir.parent)
    ).resolve()
    try:
        for directory in ["prompts", "decoded", "final", "qa", "references"]:
            (staging_dir / directory).mkdir(parents=True, exist_ok=True)
        write_run_marker(
            staging_dir,
            asset_id=asset_id,
            declared_run_dir=run_dir,
        )

        copied_references = copy_references(references, staging_dir)
        request = {
            "asset_id": asset_id,
            "display_name": display_name,
            "description": args.description.strip() or "A clean pixel-art asset.",
            "asset_type": args.asset_type,
            "target_use": args.target_use,
            "target_size": {"width": target_size[0], "height": target_size[1]},
            "sheet": sheet,
            "items": items,
            "tiles": tiles,
            "background": {"strategy": args.background, "chroma_key": args.chroma_key.upper()},
            "style_contract": style_contract(args),
            "references": copied_references,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        write_json(staging_dir / "asset_request.json", request)
        write_text(staging_dir / "prompts" / "base-asset.md", base_prompt(args, request))

        jobs: list[dict[str, object]] = [
            {
                "id": "base",
                "kind": "base-asset",
                "status": "pending",
                "prompt_file": "prompts/base-asset.md",
                "output_path": "decoded/base.png",
                "input_images": copied_references,
                "allow_prompt_only_generation": not copied_references,
                "generation_skill": "imagegen",
                "recording_owner": "parent",
            }
        ]

        if structure != "standalone":
            write_text(
                staging_dir / "prompts" / "asset-sheet.md",
                sheet_prompt(args, request, items=items, tiles=tiles),
            )
            jobs.append(
                {
                    "id": "asset-sheet",
                    "kind": structure,
                    "status": "pending",
                    "depends_on": ["base"],
                    "prompt_file": "prompts/asset-sheet.md",
                    "output_path": "decoded/asset-sheet.png",
                    "input_images": copied_references
                    + [{"path": "references/canonical-base.png", "role": "canonical base asset"}],
                    "allow_prompt_only_generation": False,
                    "requires_grounded_generation": True,
                    "generation_skill": "imagegen",
                    "recording_owner": "parent",
                }
            )

        manifest = {
            "asset_id": asset_id,
            "run_dir": str(run_dir),
            "created_at": datetime.now(timezone.utc).isoformat(),
            "jobs": jobs,
        }
        write_json(staging_dir / "imagegen-jobs.json", manifest)
        install_staged_run(staging_dir, run_dir, replacing=replacing)
    except BaseException:
        shutil.rmtree(staging_dir, ignore_errors=True)
        raise

    print(
        json.dumps(
            {
                "ok": True,
                "run_dir": str(run_dir),
                "asset_request": str(run_dir / "asset_request.json"),
                "job_manifest": str(run_dir / "imagegen-jobs.json"),
                "structure": structure,
                "sheet": sheet,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
