#!/usr/bin/env python3
"""Finalize a pixel-art asset run after image generation jobs are complete."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

from _output_pipeline import (
    commit_outputs,
    preflight_directory_outputs,
    resolve_output,
    resolve_output_directory,
    stage_text,
)
from _run_safety import resolve_run_path


def load_json(path: Path) -> dict[str, object]:
    if not path.exists():
        raise SystemExit(f"missing JSON file: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def run(command: list[str], *, check: bool = True) -> subprocess.CompletedProcess[str]:
    print("+ " + " ".join(command))
    return subprocess.run(command, check=check, text=True)


def jobs(manifest: dict[str, object]) -> list[dict[str, object]]:
    raw = manifest.get("jobs")
    if not isinstance(raw, list):
        raise SystemExit("invalid imagegen-jobs.json: jobs must be a list")
    return [job for job in raw if isinstance(job, dict)]


def require_complete_jobs(manifest: dict[str, object]) -> None:
    incomplete = [
        str(job.get("id"))
        for job in jobs(manifest)
        if job.get("status", "pending") != "complete"
    ]
    if incomplete:
        raise SystemExit("image generation jobs are not complete: " + ", ".join(incomplete))


def append_force(command: list[str], *, force: bool) -> None:
    if force:
        command.append("--force")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--chroma-tolerance", type=int, default=8)
    parser.add_argument("--no-resize", action="store_true")
    parser.add_argument("--skip-preview", action="store_true")
    parser.add_argument("--allow-unused-content", action="store_true")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    scripts_dir = Path(__file__).resolve().parent
    run_dir = Path(args.run_dir).expanduser().resolve()
    request = load_json(resolve_run_path(run_dir, "asset_request.json", field="asset request"))
    manifest = load_json(resolve_run_path(run_dir, "imagegen-jobs.json", field="job manifest"))
    require_complete_jobs(manifest)

    cells_dir = resolve_output_directory(run_dir, "cells", field="cells directory")
    final_dir = resolve_output_directory(run_dir, "final", field="final directory")
    qa_dir = resolve_output_directory(run_dir, "qa", field="QA directory")

    sheet = request.get("sheet")
    if not isinstance(sheet, dict):
        raise SystemExit("asset_request.json is missing sheet contract")
    capacity = int(sheet["columns"]) * int(sheet["rows"])
    used_cells = int(sheet["used_cells"])
    cell_output_names = ["source-normalized.png"]
    cell_output_names.extend(
        f"cell-{index:02d}.png"
        for index in range(capacity)
        if index < used_cells
    )
    cell_output_names.append("cells-manifest.json")
    preflight_directory_outputs(
        run_dir,
        cells_dir,
        cell_output_names,
        field="extracted cell output",
        force=args.force,
    )

    known_outputs = {
        "review": resolve_output(
            run_dir,
            "qa/review.json",
            field="cell review output",
            force=args.force,
        ),
        "asset_png": resolve_output(
            run_dir,
            "final/asset.png",
            field="composed PNG output",
            force=args.force,
        ),
        "asset_webp": resolve_output(
            run_dir,
            "final/asset.webp",
            field="composed WebP output",
            force=args.force,
        ),
        "compose_summary": resolve_output(
            run_dir,
            "final/compose-summary.json",
            field="compose summary output",
            force=args.force,
        ),
        "asset_manifest": resolve_output(
            run_dir,
            "final/asset-manifest.json",
            field="asset manifest output",
            force=args.force,
        ),
        "validation": resolve_output(
            run_dir,
            "final/validation.json",
            field="validation JSON output",
            force=args.force,
        ),
        "contact_sheet": resolve_output(
            run_dir,
            "qa/contact-sheet.png",
            field="contact sheet output",
            force=args.force,
        ),
        "run_summary": resolve_output(
            run_dir,
            "qa/run-summary.json",
            field="run summary output",
            force=args.force,
        ),
    }
    if not args.skip_preview and sheet.get("structure") == "sprite-row":
        known_outputs["preview"] = resolve_output(
            run_dir,
            "qa/previews/animation.gif",
            field="animation preview output",
            force=args.force,
        )

    extract_command = [
        sys.executable,
        str(scripts_dir / "extract_sheet_cells.py"),
        "--run-dir",
        str(run_dir),
        "--output-dir",
        str(cells_dir),
        "--chroma-tolerance",
        str(args.chroma_tolerance),
    ]
    append_force(extract_command, force=args.force)
    if args.no_resize:
        extract_command.append("--no-resize")
    run(extract_command)

    review_path = known_outputs["review"]
    review_command = [
        sys.executable,
        str(scripts_dir / "inspect_asset_cells.py"),
        "--cells-dir",
        str(cells_dir),
        "--run-dir",
        str(run_dir),
        "--json-out",
        str(review_path),
    ]
    append_force(review_command, force=args.force)
    review_result = run(review_command, check=False)
    if review_result.returncode != 0:
        print(
            json.dumps(
                {
                    "ok": False,
                    "review": str(review_path),
                    "repair_hint": "Run queue_asset_repairs.py, regenerate the reopened job with image generation, then finalize again.",
                },
                indent=2,
            )
        )
        raise SystemExit(review_result.returncode)

    compose_command = [
        sys.executable,
        str(scripts_dir / "compose_asset_sheet.py"),
        "--cells-dir",
        str(cells_dir),
        "--run-dir",
        str(run_dir),
        "--output",
        str(known_outputs["asset_png"]),
        "--webp-output",
        str(known_outputs["asset_webp"]),
    ]
    append_force(compose_command, force=args.force)
    run(compose_command)

    validation_path = known_outputs["validation"]
    validate_command = [
        sys.executable,
        str(scripts_dir / "validate_asset_sheet.py"),
        "--run-dir",
        str(run_dir),
        "--json-out",
        str(validation_path),
    ]
    if args.allow_unused_content:
        validate_command.append("--allow-unused-content")
    append_force(validate_command, force=args.force)
    run(validate_command)

    contact_command = [
        sys.executable,
        str(scripts_dir / "make_contact_sheet.py"),
        "--run-dir",
        str(run_dir),
        "--output",
        str(known_outputs["contact_sheet"]),
    ]
    append_force(contact_command, force=args.force)
    run(contact_command)

    preview = None
    if not args.skip_preview:
        preview_command = [
            sys.executable,
            str(scripts_dir / "render_animation_preview.py"),
            "--run-dir",
            str(run_dir),
        ]
        append_force(preview_command, force=args.force)
        preview_result = run(preview_command, check=False)
        if preview_result.returncode == 0 and request.get("sheet", {}).get("structure") == "sprite-row":
            preview = str(known_outputs["preview"])

    summary = {
        "ok": True,
        "run_dir": str(run_dir),
        "asset_png": str(known_outputs["asset_png"]),
        "asset_webp": str(known_outputs["asset_webp"]),
        "validation": str(validation_path),
        "review": str(review_path),
        "contact_sheet": str(known_outputs["contact_sheet"]),
        "preview": preview,
    }
    summary_path = known_outputs["run_summary"]
    staged_summary = stage_text(summary_path, json.dumps(summary, indent=2) + "\n")
    commit_outputs(run_dir, [(staged_summary, summary_path)], force=args.force)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
