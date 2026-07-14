#!/usr/bin/env python3
"""Record a selected image generation output for a pixel-art asset job."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import shutil
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image

from _image_input_safety import validate_image_input
from _run_safety import (
    atomic_write_bytes,
    commit_staged_path,
    create_staging_path,
    resolve_run_mutation_path,
    resolve_run_output_path,
    resolve_run_path,
)

CANONICAL_BASE_PATH = "references/canonical-base.png"


def load_jobs(path: Path) -> dict[str, object]:
    if not path.exists():
        raise SystemExit(f"job manifest not found: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def job_list(manifest: dict[str, object]) -> list[dict[str, object]]:
    jobs = manifest.get("jobs")
    if not isinstance(jobs, list):
        raise SystemExit("invalid imagegen-jobs.json: jobs must be a list")
    return [job for job in jobs if isinstance(job, dict)]


def find_job(manifest: dict[str, object], job_id: str) -> dict[str, object]:
    for job in job_list(manifest):
        if job.get("id") == job_id:
            return job
    raise SystemExit(f"unknown job id: {job_id}")


def image_metadata(path: Path) -> dict[str, object]:
    with Image.open(path) as image:
        image.verify()
    with Image.open(path) as image:
        return {
            "width": image.width,
            "height": image.height,
            "mode": image.mode,
            "format": image.format,
        }


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def stage_bytes(target: Path, payload: bytes) -> Path:
    """Fully write and sync a same-directory staging file."""
    staged = create_staging_path(target)
    try:
        with staged.open("wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
    except BaseException:
        staged.unlink(missing_ok=True)
        raise
    return staged


def stage_image_copy(source: Path, target: Path) -> Path:
    """Copy and revalidate an image before exposing it at the target path."""
    staged = create_staging_path(target)
    try:
        with source.open("rb") as source_handle, staged.open("wb") as staged_handle:
            shutil.copyfileobj(source_handle, staged_handle)
            staged_handle.flush()
            os.fsync(staged_handle.fileno())
        validate_image_input(staged, field="staged source image")
        image_metadata(staged)
    except BaseException:
        staged.unlink(missing_ok=True)
        raise
    return staged


def is_relative_to(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
    except ValueError:
        return False
    return True


def default_generated_images_root() -> Path:
    codex_home = Path(os.environ.get("CODEX_HOME") or "~/.codex").expanduser().resolve()
    return codex_home / "generated_images"


def source_provenance(source: Path, run_dir: Path, *, allow_run_source: bool) -> str:
    if is_relative_to(source, run_dir) and not allow_run_source:
        raise SystemExit(
            "source image is inside the asset run directory; record the original image "
            "generation output instead"
        )
    generated_root = default_generated_images_root()
    if is_relative_to(source, generated_root) and source.name.startswith("ig_"):
        return "built-in-imagegen"
    return "external-image"


def completed_job_ids(manifest: dict[str, object]) -> set[str]:
    return {
        str(job["id"])
        for job in job_list(manifest)
        if job.get("status") == "complete" and isinstance(job.get("id"), str)
    }


def validate_required_grounding(job: dict[str, object], run_dir: Path) -> None:
    if job.get("allow_prompt_only_generation") is not False:
        return
    inputs = job.get("input_images")
    if not isinstance(inputs, list) or not inputs:
        raise SystemExit(f"job {job.get('id')} requires input images but lists none")
    missing = []
    for item in inputs:
        if not isinstance(item, dict) or not isinstance(item.get("path"), str):
            raise SystemExit(f"job {job.get('id')} has an invalid input image entry")
        path = resolve_run_path(
            run_dir,
            item["path"],
            field=f"job {job.get('id')} input image path",
            allowed_roots=("references",),
        )
        if not path.is_file():
            missing.append(str(path))
    if missing:
        raise SystemExit(
            f"job {job.get('id')} is missing required grounding image(s): "
            + ", ".join(missing)
        )


def manifest_relative(path: Path, run_dir: Path) -> str:
    return str(path.resolve().relative_to(run_dir.resolve()))


def prepare_base_reference(
    *,
    run_dir: Path,
    staged_output: Path,
    manifest: dict[str, object],
    job: dict[str, object],
    metadata: dict[str, object],
) -> tuple[Path, bytes, Path | None, bytes | None] | None:
    """Prepare canonical and request updates without publishing either file."""
    if job.get("id") != "base":
        return None
    canonical = resolve_run_mutation_path(
        run_dir,
        CANONICAL_BASE_PATH,
        field="canonical base path",
        allowed_roots=("references",),
    )
    reference = {
        "path": manifest_relative(canonical, run_dir),
        "source_job": "base",
        "sha256": file_sha256(staged_output),
        "metadata": metadata,
    }
    job["canonical_reference_path"] = reference["path"]
    manifest["canonical_identity_reference"] = reference

    request_path = resolve_run_mutation_path(run_dir, "asset_request.json", field="asset request")
    request_payload = None
    if request_path.exists():
        request = json.loads(request_path.read_text(encoding="utf-8"))
        if not isinstance(request, dict):
            raise SystemExit("asset_request.json must contain a JSON object")
        request["canonical_identity_reference"] = reference
        request_payload = (json.dumps(request, indent=2) + "\n").encode("utf-8")
    else:
        request_path = None
    return canonical, staged_output.read_bytes(), request_path, request_payload


def recording_manifest_payload(manifest: dict[str, object], job_id: str, timestamp: str) -> bytes:
    """Create a non-complete transaction marker before replacing published artifacts."""
    recording_manifest = copy.deepcopy(manifest)
    recording_job = find_job(recording_manifest, job_id)
    recording_job["status"] = "recording"
    recording_job["recording_started_at"] = timestamp
    for key in [
        "source_path",
        "source_provenance",
        "source_sha256",
        "output_sha256",
        "completed_at",
        "metadata",
    ]:
        recording_job.pop(key, None)
    return (json.dumps(recording_manifest, indent=2) + "\n").encode("utf-8")


def commit_recording_transaction(
    *,
    manifest_path: Path,
    recording_payload: bytes,
    artifacts: list[tuple[Path, Path, bool]],
    final_manifest_staged: Path,
) -> None:
    """Mark incomplete, publish artifacts, then atomically publish complete state."""
    atomic_write_bytes(manifest_path, recording_payload, force=True)
    for staged, target, force in artifacts:
        commit_staged_path(staged, target, force=force)
    commit_staged_path(final_manifest_staged, manifest_path, force=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--job-id", required=True)
    parser.add_argument("--source", required=True)
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--allow-run-source", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args()

    run_dir = Path(args.run_dir).expanduser().resolve()
    source = Path(args.source).expanduser().resolve()
    if not source.is_file():
        raise SystemExit(f"source image not found: {source}")
    validate_image_input(source, field="source image")
    image_metadata(source)
    provenance = source_provenance(source, run_dir, allow_run_source=args.allow_run_source)

    manifest_path = resolve_run_mutation_path(
        run_dir,
        "imagegen-jobs.json",
        field="job manifest",
    )
    manifest = load_jobs(manifest_path)
    job = find_job(manifest, args.job_id)

    missing_deps = [
        dep
        for dep in job.get("depends_on", [])
        if isinstance(dep, str) and dep not in completed_job_ids(manifest)
    ]
    if missing_deps:
        raise SystemExit(
            f"job {args.job_id} is not ready; missing dependency result(s): "
            f"{', '.join(missing_deps)}"
        )
    validate_required_grounding(job, run_dir)

    output_raw = job.get("output_path")
    if not isinstance(output_raw, str):
        raise SystemExit(f"job {args.job_id} has no output_path")
    output = resolve_run_output_path(
        run_dir,
        output_raw,
        field=f"job {args.job_id} output_path",
        allowed_roots=("decoded",),
        force=args.force,
    )
    timestamp = datetime.now(timezone.utc).isoformat()
    recording_payload = recording_manifest_payload(manifest, args.job_id, timestamp)

    staged_paths: list[Path] = []
    try:
        output_staged = stage_image_copy(source, output)
        staged_paths.append(output_staged)
        metadata = image_metadata(output_staged)
        output_sha256 = file_sha256(output_staged)

        job["status"] = "complete"
        job["source_path"] = str(source)
        job["source_provenance"] = provenance
        job["source_sha256"] = output_sha256
        job["output_sha256"] = output_sha256
        job["completed_at"] = timestamp
        job["metadata"] = metadata
        job.pop("recording_started_at", None)
        for key in ["last_error", "repair_reason", "queued_at"]:
            job.pop(key, None)

        artifacts: list[tuple[Path, Path, bool]] = [
            (output_staged, output, args.force)
        ]
        base_update = prepare_base_reference(
            run_dir=run_dir,
            staged_output=output_staged,
            manifest=manifest,
            job=job,
            metadata=metadata,
        )
        if base_update is not None:
            canonical, canonical_payload, request_path, request_payload = base_update
            canonical_staged = stage_bytes(canonical, canonical_payload)
            staged_paths.append(canonical_staged)
            artifacts.append((canonical_staged, canonical, True))
            if request_path is not None and request_payload is not None:
                request_staged = stage_bytes(request_path, request_payload)
                staged_paths.append(request_staged)
                artifacts.append((request_staged, request_path, True))

        final_manifest_payload = (json.dumps(manifest, indent=2) + "\n").encode("utf-8")
        final_manifest_staged = stage_bytes(manifest_path, final_manifest_payload)
        staged_paths.append(final_manifest_staged)
        commit_recording_transaction(
            manifest_path=manifest_path,
            recording_payload=recording_payload,
            artifacts=artifacts,
            final_manifest_staged=final_manifest_staged,
        )
    finally:
        for staged in staged_paths:
            staged.unlink(missing_ok=True)
    print(
        json.dumps(
            {
                "ok": True,
                "job_id": args.job_id,
                "output": str(output),
                "source_provenance": provenance,
                "metadata": metadata,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
