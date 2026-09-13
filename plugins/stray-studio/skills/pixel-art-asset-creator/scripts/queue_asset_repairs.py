#!/usr/bin/env python3
"""Reopen a failed pixel-art asset generation job with targeted repair notes."""

from __future__ import annotations

import argparse
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

from _run_safety import (
    atomic_write_text,
    commit_staged_path,
    create_staging_path,
    resolve_run_mutation_path,
    resolve_run_output_path,
    resolve_run_path,
)

MAX_REPAIR_ATTEMPTS = 3


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
    review_path = resolve_run_path(run_dir, "qa/review.json", field="QA review")
    if review_path.exists():
        review = load_json(review_path)
        errors = review.get("errors") if isinstance(review.get("errors"), list) else []
        warnings = review.get("warnings") if isinstance(review.get("warnings"), list) else []
        reasons.extend(str(error) for error in errors)
        if repair_on_warnings:
            reasons.extend(str(warning) for warning in warnings)
    validation_path = resolve_run_path(run_dir, "final/validation.json", field="validation report")
    if validation_path.exists():
        validation = load_json(validation_path)
        errors = validation.get("errors") if isinstance(validation.get("errors"), list) else []
        warnings = validation.get("warnings") if isinstance(validation.get("warnings"), list) else []
        reasons.extend(str(error) for error in errors)
        if repair_on_warnings:
            reasons.extend(str(warning) for warning in warnings)
    return reasons or ["the asset did not pass visual or geometry QA"]


def repair_prompt_update(
    run_dir: Path,
    job: dict[str, object],
    attempt: int,
    reason: str,
    registration: str,
) -> tuple[Path, str, str]:
    """Preflight the prompt path and return its old and proposed contents."""
    prompt_raw = job.get("prompt_file")
    if not isinstance(prompt_raw, str):
        raise SystemExit(f"job {job.get('id')} has no prompt_file")
    prompt_path = resolve_run_mutation_path(
        run_dir,
        prompt_raw,
        field=f"job {job.get('id')} prompt_file",
        allowed_roots=("prompts",),
    )
    if not prompt_path.exists():
        raise SystemExit(f"prompt file not found: {prompt_path}")
    existing = prompt_path.read_text(encoding="utf-8")
    motion_note = (
        "Preserve planned weight transfer, torso motion, sway and intentional travel; do not freeze the upper body or flatten the motion during repair."
        if registration == "free" else
        "For stationary idle/blink, keep torso, clothing and planted feet fixed; change only named animated parts. Preserve intentional travel and whole-body motion in other actions."
    )
    note = f"""

Repair attempt {attempt}:
- The previous output failed QA: {reason}
- Regenerate the whole requested asset or sheet, not a partial crop.
- Preserve the canonical base identity, palette, outline weight, lighting direction, material, and silhouette language.
- Preserve only verified pose and placement features. Reopen defective geometry, strip-spacing drift and loop transitions; do not lock an unreviewed previous result wholesale. Use approved contact/passing keys and the declared reference roles rather than inheriting defects from an edit chain.
- For articulated characters, preserve limb lengths and footwear proportions through joint motion and justified foreshortening; do not shrink or fuse feet to fit a pose. For skin, carry the accepted base/shadow colors across face, hands and limbs, preserving justified near/far shading.
- For inconsistent paint, use shared material base/shadow/highlight roles and coherent color regions; remove accidental speckles without erasing essential details. Let shading follow pose and occlusion under the same lighting. Preserve accepted pose geometry and motion during a paint-only repair; palette mapping alone does not fix shading flicker.
- Honor the declared material plan: if it omits shadows/highlights for a flat-color diagnostic, do not restore them implicitly. Distinguish near/far limbs by overlap and outlines without changing the declared skin base color.
- {motion_note}
- Remove colored background fringes without erasing thin outlines or changing subject colors. Follow the background strategy declared in this prompt; do not switch it implicitly during this repair.
- Fill every requested used cell or frame with one complete asset. Use the cell center as the default placement reference; honor the action's specified position changes within each slot.
- Keep unused cells empty with only transparent or chroma-key background.
- Avoid clipping, edge slivers, opaque background boxes, checkerboard backgrounds, visible grids, labels, frame numbers, detached or floor shadows, glows, loose particles, and detached effects.
"""
    updated = existing.rstrip() + note.rstrip() + "\n"
    return prompt_path, existing, updated


def archive_plan(
    run_dir: Path,
    job: dict[str, object],
    attempt: int,
) -> tuple[Path, Path] | None:
    """Preflight the decoded source and a new contained archive target."""
    output_raw = job.get("output_path")
    if not isinstance(output_raw, str):
        return None
    output = resolve_run_mutation_path(
        run_dir,
        output_raw,
        field=f"job {job.get('id')} output_path",
        allowed_roots=("decoded",),
    )
    if not output.exists():
        return None
    if not output.is_file():
        raise SystemExit(f"job {job.get('id')} output must be a file: {output}")
    archive = resolve_run_output_path(
        run_dir,
        f"repairs/attempt-{attempt:02d}/{output.name}",
        field=f"job {job.get('id')} repair archive",
        allowed_roots=("repairs",),
    )
    return output, archive


def create_archive(output: Path, archive: Path) -> None:
    """Copy a complete archive without replacing an existing path."""
    staged = create_staging_path(archive)
    try:
        shutil.copy2(output, staged)
        commit_staged_path(staged, archive, force=False)
    finally:
        staged.unlink(missing_ok=True)


def next_repair_attempt(job: dict[str, object]) -> int:
    try:
        completed_attempts = int(job.get("repair_attempt", 0))
    except (TypeError, ValueError):
        raise SystemExit(f"job {job.get('id')} has an invalid repair_attempt") from None
    if completed_attempts < 0:
        raise SystemExit(f"job {job.get('id')} has an invalid repair_attempt")
    if completed_attempts >= MAX_REPAIR_ATTEMPTS:
        raise SystemExit(
            f"job {job.get('id')} reached the {MAX_REPAIR_ATTEMPTS}-attempt repair limit"
        )
    return completed_attempts + 1


def reopen_job(job: dict[str, object], reason: str) -> int:
    attempt = next_repair_attempt(job)
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
    parser.add_argument("--visual-defect", action="append", default=[], help="Observed visual defect to include in the repair prompt; repeat for multiple defects")
    args = parser.parse_args()

    run_dir = Path(args.run_dir).expanduser().resolve()
    request = load_json(resolve_run_path(run_dir, "asset_request.json", field="asset request"))
    manifest_path = resolve_run_mutation_path(
        run_dir,
        "imagegen-jobs.json",
        field="job manifest",
    )
    manifest = load_json(manifest_path)
    structure = str(request.get("sheet", {}).get("structure", "standalone"))
    job_id = args.job_id or ("base" if structure == "standalone" else "asset-sheet")
    job = find_job(manifest, job_id)
    reason = "; ".join(repair_reasons(run_dir, repair_on_warnings=args.repair_on_warnings) + args.visual_defect)
    attempt = next_repair_attempt(job)
    prompt_path, old_prompt, updated_prompt = repair_prompt_update(
        run_dir,
        job,
        attempt,
        reason,
        str(request.get("animation", {}).get("registration", "unspecified")),
    )
    planned_archive = archive_plan(run_dir, job, attempt)

    archive: Path | None = None
    if planned_archive is not None:
        output, archive = planned_archive
        create_archive(output, archive)
    else:
        output = None

    prompt_updated = False
    manifest_updated = False
    try:
        actual_attempt = reopen_job(job, reason)
        if actual_attempt != attempt:
            raise RuntimeError("repair attempt changed after preflight")
        atomic_write_text(prompt_path, updated_prompt, force=True)
        prompt_updated = True
        atomic_write_text(
            manifest_path,
            json.dumps(manifest, indent=2) + "\n",
            force=True,
        )
        manifest_updated = True
    except BaseException:
        if prompt_updated and not manifest_updated:
            atomic_write_text(prompt_path, old_prompt, force=True)
        if archive is not None:
            archive.unlink(missing_ok=True)
        raise

    if output is not None:
        try:
            output.unlink()
        except OSError as exc:
            raise SystemExit(
                f"repair was queued and archived, but the decoded output could not be removed: {output}: {exc}"
            ) from None
    print(json.dumps({"ok": True, "job_id": job_id, "repair_attempt": attempt, "reason": reason}, indent=2))


if __name__ == "__main__":
    main()
