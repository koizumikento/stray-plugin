#!/usr/bin/env python3
"""Finalize a pixel-art asset run after image generation jobs are complete."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


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
    request = load_json(run_dir / "asset_request.json")
    manifest = load_json(run_dir / "imagegen-jobs.json")
    require_complete_jobs(manifest)

    cells_dir = run_dir / "cells"
    final_dir = run_dir / "final"
    qa_dir = run_dir / "qa"
    final_dir.mkdir(parents=True, exist_ok=True)
    qa_dir.mkdir(parents=True, exist_ok=True)

    extract_command = [
        sys.executable,
        str(scripts_dir / "extract_sheet_cells.py"),
        "--run-dir",
        str(run_dir),
        "--output-dir",
        str(cells_dir),
        "--chroma-tolerance",
        str(args.chroma_tolerance),
        "--force",
    ]
    if args.no_resize:
        extract_command.append("--no-resize")
    run(extract_command)

    review_path = qa_dir / "review.json"
    review_command = [
        sys.executable,
        str(scripts_dir / "inspect_asset_cells.py"),
        "--cells-dir",
        str(cells_dir),
        "--json-out",
        str(review_path),
    ]
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

    run(
        [
            sys.executable,
            str(scripts_dir / "compose_asset_sheet.py"),
            "--cells-dir",
            str(cells_dir),
            "--output",
            str(final_dir / "asset.png"),
            "--webp-output",
            str(final_dir / "asset.webp"),
        ]
    )

    validation_path = final_dir / "validation.json"
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
    run(validate_command)

    run(
        [
            sys.executable,
            str(scripts_dir / "make_contact_sheet.py"),
            "--run-dir",
            str(run_dir),
            "--output",
            str(qa_dir / "contact-sheet.png"),
        ]
    )

    preview = None
    if not args.skip_preview:
        preview_command = [
            sys.executable,
            str(scripts_dir / "render_animation_preview.py"),
            "--run-dir",
            str(run_dir),
        ]
        preview_result = run(preview_command, check=False)
        if preview_result.returncode == 0 and request.get("sheet", {}).get("structure") == "sprite-row":
            preview = str(qa_dir / "previews" / "animation.gif")

    summary = {
        "ok": True,
        "run_dir": str(run_dir),
        "asset_png": str(final_dir / "asset.png"),
        "asset_webp": str(final_dir / "asset.webp"),
        "validation": str(validation_path),
        "review": str(review_path),
        "contact_sheet": str(qa_dir / "contact-sheet.png"),
        "preview": preview,
    }
    (qa_dir / "run-summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
