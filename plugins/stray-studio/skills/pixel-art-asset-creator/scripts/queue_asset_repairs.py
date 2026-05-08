#!/usr/bin/env python3
"""Reopen a failed pixel-art asset generation job with targeted repair notes."""

from __future__ import annotations

import argparse
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path


def load_json(path: Path) -> dict[str, object]:
    if not path.exists():
        raise SystemExit(f"missing JSON file: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def jobs(manifest: dict[str, object]) -> list[dict[str, object]]:
    raw = manifest.get("jobs")
    if not isinstance(raw, list):
        raise SystemExit("invalid imagegen-jobs.json: jobs must be a list")
    return [job for job in raw if isinstance(job, dict)]


def find_job(manifest: dict[str, object], job_id: str) -> dict[str, object]:
    for job in jobs(manifest):
        if job.get("id") == job_id:
            return job
    raise SystemExit(f"unknown job id: {job_id}")


def repair_reasons(run_dir: Path, *, repair_on_warnings: bool) -> list[str]:
    reasons: list[str] = []
    review_path = run_dir / "qa" / "review.json"
    if review_path.exists():
        review = load_json(review_path)
        errors = review.get("errors") if isinstance(review.get("errors"), list) else []
        warnings = review.get("warnings") if isinstance(review.get("warnings"), list) else []
        reasons.extend(str(error) for error in errors)
        if repair_on_warnings:
            reasons.extend(str(warning) for warning in warnings)
    validation_path = run_dir / "final" / "validation.json"
    if validation_path.exists():
        validation = load_json(validation_path)
        errors = validation.get("errors") if isinstance(validation.get("errors"), list) else []
        warnings = validation.get("warnings") if isinstance(validation.get("warnings"), list) else []
        reasons.extend(str(error) for error in errors)
        if repair_on_warnings:
            reasons.extend(str(warning) for warning in warnings)
    return reasons or ["the asset did not pass visual or geometry QA"]


def append_repair_note(run_dir: Path, job: dict[str, object], attempt: int, reason: str) -> None:
    prompt_raw = job.get("prompt_file")
    if not isinstance(prompt_raw, str):
        raise SystemExit(f"job {job.get('id')} has no prompt_file")
    prompt_path = run_dir / prompt_raw
    if not prompt_path.exists():
        raise SystemExit(f"prompt file not found: {prompt_path}")
    existing = prompt_path.read_text(encoding="utf-8")
    note = f"""

Repair attempt {attempt}:
- The previous output failed QA: {reason}
- Regenerate the whole requested asset or sheet, not a partial crop.
- Preserve the canonical base identity, palette, outline weight, lighting direction, material, and silhouette language.
- Fill every requested used cell or frame with one complete centered asset.
- Keep unused cells empty with only transparent or chroma-key background.
- Avoid clipping, edge slivers, opaque background boxes, checkerboard backgrounds, visible grids, labels, frame numbers, shadows, glows, loose particles, and detached effects.
"""
    prompt_path.write_text(existing.rstrip() + note.rstrip() + "\n", encoding="utf-8")


def archive_output(run_dir: Path, job: dict[str, object], attempt: int) -> None:
    output_raw = job.get("output_path")
    if not isinstance(output_raw, str):
        return
    output = run_dir / output_raw
    if not output.exists():
        return
    archive_dir = run_dir / "repairs" / f"attempt-{attempt:02d}"
    archive_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(output, archive_dir / output.name)
    output.unlink()


def reopen_job(job: dict[str, object], reason: str) -> int:
    attempt = int(job.get("repair_attempt", 0)) + 1
    job["status"] = "pending"
    job["repair_attempt"] = attempt
    job["repair_reason"] = reason
    job["queued_at"] = datetime.now(timezone.utc).isoformat()
    for key in ["source_path", "source_provenance", "source_sha256", "output_sha256", "completed_at", "metadata"]:
        job.pop(key, None)
    return attempt


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--job-id", default="")
    parser.add_argument("--repair-on-warnings", action="store_true")
    args = parser.parse_args()

    run_dir = Path(args.run_dir).expanduser().resolve()
    request = load_json(run_dir / "asset_request.json")
    manifest_path = run_dir / "imagegen-jobs.json"
    manifest = load_json(manifest_path)
    structure = str(request.get("sheet", {}).get("structure", "standalone"))
    job_id = args.job_id or ("base" if structure == "standalone" else "asset-sheet")
    job = find_job(manifest, job_id)
    reason = "; ".join(repair_reasons(run_dir, repair_on_warnings=args.repair_on_warnings))
    attempt = reopen_job(job, reason)
    archive_output(run_dir, job, attempt)
    append_repair_note(run_dir, job, attempt, reason)
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"ok": True, "job_id": job_id, "repair_attempt": attempt, "reason": reason}, indent=2))


if __name__ == "__main__":
    main()
