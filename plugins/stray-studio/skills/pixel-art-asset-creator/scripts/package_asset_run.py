#!/usr/bin/env python3
"""Normalize and package a completed pixel-art asset run."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image

from _output_pipeline import (
    commit_outputs,
    resolve_output,
    resolve_output_directory,
    stage_image,
    stage_text,
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


def require_complete(manifest: dict[str, object]) -> None:
    incomplete = [
        str(job.get("id"))
        for job in jobs(manifest)
        if job.get("status", "pending") != "complete"
    ]
    if incomplete:
        raise SystemExit("image generation jobs are not complete: " + ", ".join(incomplete))


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


def expected_size(request: dict[str, object]) -> tuple[int, int]:
    sheet = request.get("sheet")
    if not isinstance(sheet, dict):
        raise SystemExit("asset_request.json is missing sheet contract")
    return int(sheet["width"]), int(sheet["height"])


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


def normalize_image(
    source: Path,
    *,
    request: dict[str, object],
    no_resize: bool,
    chroma_tolerance: int,
) -> tuple[Image.Image, list[str]]:
    warnings: list[str] = []
    with Image.open(source) as opened:
        image = opened.convert("RGBA")

    background = request.get("background") if isinstance(request.get("background"), dict) else {}
    if background.get("strategy") == "chroma-key":
        key = parse_hex_color(str(background.get("chroma_key", "#FF00FF")))
        image = remove_chroma_key(image, key, chroma_tolerance)

    expected = expected_size(request)
    if image.size != expected:
        message = f"resized from {image.width}x{image.height} to {expected[0]}x{expected[1]}"
        if no_resize:
            raise SystemExit(message)
        image = image.resize(expected, Image.Resampling.NEAREST)
        warnings.append(message)
    return image, warnings


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--output-dir", default="")
    parser.add_argument("--no-resize", action="store_true")
    parser.add_argument("--chroma-tolerance", type=int, default=8)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    run_dir = Path(args.run_dir).expanduser().resolve()
    request = load_json(resolve_run_path(run_dir, "asset_request.json", field="asset request"))
    manifest = load_json(resolve_run_path(run_dir, "imagegen-jobs.json", field="job manifest"))
    require_complete(manifest)
    source = selected_output(run_dir, request, manifest)

    output_dir = resolve_output_directory(
        run_dir,
        args.output_dir or "final",
        field="package output directory",
    )
    png_path = resolve_output(
        run_dir,
        output_dir / "asset.png",
        field="packaged PNG output",
        force=args.force,
    )
    webp_path = resolve_output(
        run_dir,
        output_dir / "asset.webp",
        field="packaged WebP output",
        force=args.force,
    )
    manifest_path = resolve_output(
        run_dir,
        output_dir / "asset-manifest.json",
        field="package manifest output",
        force=args.force,
    )
    summary_path = resolve_output(
        run_dir,
        "qa/package-summary.json",
        field="package summary output",
        force=args.force,
    )

    image, warnings = normalize_image(
        source,
        request=request,
        no_resize=args.no_resize,
        chroma_tolerance=args.chroma_tolerance,
    )
    package = {
        "asset_id": request.get("asset_id"),
        "display_name": request.get("display_name"),
        "description": request.get("description"),
        "asset_type": request.get("asset_type"),
        "target_use": request.get("target_use"),
        "sheet": request.get("sheet"),
        "items": request.get("items", []),
        "tiles": request.get("tiles", []),
        "source_job_output": str(source),
        "files": {"png": png_path.name, "webp": webp_path.name},
        "warnings": warnings,
    }

    summary = {
        "ok": True,
        "output_dir": str(output_dir),
        "asset_png": str(png_path),
        "asset_webp": str(webp_path),
        "asset_manifest": str(manifest_path),
        "warnings": warnings,
    }
    staged_outputs: list[tuple[Path, Path]] = []
    try:
        staged_outputs.append((stage_image(png_path, image, image_format="PNG"), png_path))
        staged_outputs.append(
            (
                stage_image(
                    webp_path,
                    image,
                    image_format="WEBP",
                    lossless=True,
                    quality=100,
                    method=6,
                ),
                webp_path,
            )
        )
        staged_outputs.append(
            (
                stage_text(manifest_path, json.dumps(package, indent=2) + "\n"),
                manifest_path,
            )
        )
        staged_outputs.append(
            (
                stage_text(summary_path, json.dumps(summary, indent=2) + "\n"),
                summary_path,
            )
        )
        commit_outputs(run_dir, staged_outputs, force=args.force)
    finally:
        for staged, _ in staged_outputs:
            staged.unlink(missing_ok=True)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
