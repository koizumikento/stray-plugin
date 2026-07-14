#!/usr/bin/env python3
"""Audit and optionally optimize corporate-site assets.

Default behavior is read-only. Use --optimize-dir to write optimized image
derivatives without overwriting source files.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
from typing import Any


IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".avif"}
OPTIMIZABLE_EXTS = {".jpg", ".jpeg", ".png", ".webp"}
VIDEO_EXTS = {".mp4", ".mov", ".webm", ".avi", ".mkv"}
DOCUMENT_EXTS = {".pdf"}
SOURCE_EXTS = {
    ".psd",
    ".ai",
    ".fig",
    ".sketch",
    ".raw",
    ".cr2",
    ".nef",
    ".arw",
    ".zip",
    ".7z",
}


def kb(size: int) -> float:
    return round(size / 1024, 1)


def rel(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def source_path(row_path: str, project_root: Path) -> Path:
    """Resolve a reported asset path without trusting it as an output path."""
    path = Path(row_path)
    if not path.is_absolute():
        path = project_root / path
    return path.resolve()


def derivative_path(src: Path, project_root: Path, out_dir: Path) -> Path:
    """Return a contained derivative path for project and external sources."""
    try:
        relative = src.relative_to(project_root)
    except ValueError:
        digest = hashlib.sha256(os.fsencode(src)).hexdigest()[:12]
        relative = Path("_external") / digest / src.name

    target = out_dir / relative.with_suffix(".webp")
    resolved_target = target.resolve()
    try:
        resolved_target.relative_to(out_dir)
    except ValueError as exc:
        raise OSError(f"output path escapes optimize directory: {target}") from exc
    return resolved_target


def image_size(path: Path) -> tuple[int | None, int | None]:
    ext = path.suffix.lower()
    try:
        with path.open("rb") as f:
            if ext == ".png":
                sig = f.read(24)
                if sig[:8] == b"\x89PNG\r\n\x1a\n":
                    return int.from_bytes(sig[16:20], "big"), int.from_bytes(sig[20:24], "big")
            if ext in {".jpg", ".jpeg"}:
                f.read(2)
                while True:
                    marker = f.read(2)
                    if len(marker) < 2:
                        break
                    while marker[0] != 0xFF:
                        marker = marker[1:] + f.read(1)
                        if len(marker) < 2:
                            return None, None
                    code = marker[1]
                    size_bytes = f.read(2)
                    if len(size_bytes) < 2:
                        break
                    segment_size = int.from_bytes(size_bytes, "big")
                    if code in {0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF}:
                        data = f.read(5)
                        if len(data) == 5:
                            return int.from_bytes(data[3:5], "big"), int.from_bytes(data[1:3], "big")
                        break
                    f.seek(segment_size - 2, os.SEEK_CUR)
            if ext == ".gif":
                sig = f.read(10)
                if sig[:3] == b"GIF":
                    return int.from_bytes(sig[6:8], "little"), int.from_bytes(sig[8:10], "little")
            if ext == ".webp":
                data = f.read(40)
                if data[:4] == b"RIFF" and data[8:12] == b"WEBP":
                    if data[12:16] == b"VP8X" and len(data) >= 30:
                        return int.from_bytes(data[24:27], "little") + 1, int.from_bytes(data[27:30], "little") + 1
                    if data[12:16] == b"VP8 " and len(data) >= 30:
                        return int.from_bytes(data[26:28], "little") & 0x3FFF, int.from_bytes(data[28:30], "little") & 0x3FFF
    except OSError:
        pass
    return None, None


def default_scan_roots(project_root: Path) -> list[Path]:
    candidates = [
        project_root / "src" / "assets",
        project_root / "public",
        project_root / "assets",
    ]
    found = [p for p in candidates if p.exists()]
    return found or [project_root]


def should_skip(path: Path) -> bool:
    parts = set(path.parts)
    return bool(parts & {".git", "node_modules", "dist", "build", ".astro", ".next", "out"})


def scan(paths: list[Path], project_root: Path, args: argparse.Namespace) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for base in paths:
        if not base.exists():
            continue
        files = [base] if base.is_file() else [p for p in base.rglob("*") if p.is_file()]
        for path in files:
            if should_skip(path):
                continue
            ext = path.suffix.lower()
            if ext not in IMAGE_EXTS | VIDEO_EXTS | DOCUMENT_EXTS | SOURCE_EXTS:
                continue
            size = path.stat().st_size
            width, height = image_size(path) if ext in IMAGE_EXTS else (None, None)
            kind = "other"
            warnings: list[str] = []
            if ext in IMAGE_EXTS:
                kind = "image"
                if size > args.max_image_kb * 1024:
                    warnings.append(f"image over {args.max_image_kb} KB")
                if width and width > args.max_width:
                    warnings.append(f"image width over {args.max_width}px")
            elif ext in DOCUMENT_EXTS:
                kind = "document"
                if size > args.max_pdf_kb * 1024:
                    warnings.append(f"PDF over {args.max_pdf_kb} KB")
            elif ext in VIDEO_EXTS:
                kind = "video"
                if size > args.max_video_kb * 1024:
                    warnings.append(f"video over {args.max_video_kb} KB")
            elif ext in SOURCE_EXTS:
                kind = "source"
                warnings.append("source/original asset; keep outside shipped asset folders unless required")
            rows.append(
                {
                    "path": rel(path, project_root),
                    "kind": kind,
                    "extension": ext,
                    "size_kb": kb(size),
                    "width": width,
                    "height": height,
                    "warnings": warnings,
                }
            )
    return sorted(rows, key=lambda item: (-len(item["warnings"]), -item["size_kb"], item["path"]))


def optimize_images(rows: list[dict[str, Any]], project_root: Path, out_dir: Path, args: argparse.Namespace) -> list[dict[str, Any]]:
    try:
        from PIL import Image
    except ImportError as exc:
        raise SystemExit("Pillow is required for --optimize-dir. Run with: uv run --with pillow python asset_audit.py ...") from exc

    project_root = project_root.resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    out_dir = out_dir.resolve()
    source_paths = {source_path(row["path"], project_root) for row in rows}
    written: list[dict[str, Any]] = []
    for row in rows:
        src = source_path(row["path"], project_root)
        ext = src.suffix.lower()
        if row["kind"] != "image" or ext not in OPTIMIZABLE_EXTS:
            continue
        try:
            with Image.open(src) as im:
                im = im.convert("RGBA") if im.mode in {"P", "LA"} else im
                width, height = im.size
                if width > args.max_width:
                    ratio = args.max_width / width
                    im = im.resize((args.max_width, int(height * ratio)), Image.LANCZOS)
                target = derivative_path(src, project_root, out_dir)
                if target in source_paths:
                    raise OSError(f"refusing to overwrite source asset: {target}")
                if target.exists() or target.is_symlink():
                    raise OSError(f"refusing to overwrite existing output: {target}")
                target.parent.mkdir(parents=True, exist_ok=True)
                if target.parent.resolve() != target.parent:
                    raise OSError(f"output parent escapes optimize directory: {target.parent}")
                save_im = im.convert("RGB") if im.mode == "RGBA" and not has_alpha(im) else im
                try:
                    output = target.open("xb")
                except FileExistsError as exc:
                    raise OSError(f"refusing to overwrite existing output: {target}") from exc
                try:
                    with output:
                        save_im.save(output, "WEBP", quality=args.quality, method=6)
                except Exception:
                    target.unlink(missing_ok=True)
                    raise
                written.append(
                    {
                        "source": row["path"],
                        "output": rel(target, project_root),
                        "source_kb": row["size_kb"],
                        "output_kb": kb(target.stat().st_size),
                    }
                )
        except OSError as exc:
            written.append({"source": row["path"], "error": str(exc)})
    return written


def has_alpha(image: Any) -> bool:
    if image.mode != "RGBA":
        return False
    alpha = image.getchannel("A")
    return alpha.getextrema() != (255, 255)


def print_markdown(rows: list[dict[str, Any]], optimized: list[dict[str, Any]]) -> None:
    warned = [r for r in rows if r["warnings"]]
    print(f"Scanned assets: {len(rows)}")
    print(f"Assets with warnings: {len(warned)}")
    if warned:
        print()
        print("| Path | Type | Size KB | Dimensions | Warnings |")
        print("| --- | --- | ---: | --- | --- |")
        for row in warned:
            dims = f"{row['width']}x{row['height']}" if row["width"] and row["height"] else ""
            print(f"| {row['path']} | {row['kind']} | {row['size_kb']} | {dims} | {'; '.join(row['warnings'])} |")
    if optimized:
        print()
        print("Optimized derivatives:")
        print()
        print("| Source | Output | Before KB | After KB |")
        print("| --- | --- | ---: | ---: |")
        for item in optimized:
            if "error" in item:
                print(f"| {item['source']} | ERROR: {item['error']} |  |  |")
            else:
                print(f"| {item['source']} | {item['output']} | {item['source_kb']} | {item['output_kb']} |")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit corporate-site assets and optionally write optimized WebP derivatives.")
    parser.add_argument("paths", nargs="*", help="Files or directories to scan. Defaults to src/assets, public, or assets.")
    parser.add_argument("--project-root", default=".", help="Project root used for relative paths.")
    parser.add_argument("--max-image-kb", type=int, default=800, help="Warn when an image exceeds this size.")
    parser.add_argument("--max-pdf-kb", type=int, default=5000, help="Warn when a PDF exceeds this size.")
    parser.add_argument("--max-video-kb", type=int, default=8000, help="Warn when a video exceeds this size.")
    parser.add_argument("--max-width", type=int, default=2400, help="Warn/resize when image width exceeds this size.")
    parser.add_argument("--optimize-dir", help="Write optimized WebP derivatives to this directory. Never overwrites sources.")
    parser.add_argument("--quality", type=int, default=82, help="WebP quality for optimized derivatives.")
    parser.add_argument("--json", action="store_true", help="Print JSON instead of Markdown.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    project_root = Path(args.project_root).resolve()
    scan_paths = [Path(p).resolve() for p in args.paths] if args.paths else default_scan_roots(project_root)
    rows = scan(scan_paths, project_root, args)
    optimized: list[dict[str, Any]] = []
    if args.optimize_dir:
        optimized = optimize_images(rows, project_root, Path(args.optimize_dir).resolve(), args)
    if args.json:
        print(json.dumps({"assets": rows, "optimized": optimized}, indent=2))
    else:
        print_markdown(rows, optimized)


if __name__ == "__main__":
    main()
