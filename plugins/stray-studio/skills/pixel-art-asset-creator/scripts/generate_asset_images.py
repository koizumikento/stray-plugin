#!/usr/bin/env python3
"""Explicit, user-authorized direct Image API path for pixel-art asset jobs."""

from __future__ import annotations

import argparse
import base64
import binascii
import hashlib
import json
import os
import re
import secrets
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import BinaryIO
from urllib.error import HTTPError, URLError
from urllib.request import HTTPRedirectHandler, Request, build_opener

from _image_input_safety import read_validated_image_input, validate_image_input
from _run_safety import (
    atomic_write_bytes,
    commit_staged_path,
    create_staging_path,
    resolve_run_mutation_path,
    resolve_run_path,
)

CANONICAL_BASE_PATH = "references/canonical-base.png"
MAX_API_RESPONSE_BYTES = 64 * 1024 * 1024
RESPONSE_READ_CHUNK_BYTES = 1024 * 1024
MAX_PROMPT_BYTES = 1024 * 1024
MAX_INPUT_IMAGES = 8
MAX_TOTAL_INPUT_IMAGE_BYTES = 60 * 1024 * 1024
MAX_REQUEST_BODY_BYTES = 64 * 1024 * 1024
SAFE_ERROR_LABEL_RE = re.compile(r"\A[A-Za-z0-9][A-Za-z0-9._:/-]{0,79}\Z")


@dataclass(frozen=True)
class AuthorizedImageInput:
    path: Path
    payload: bytes
    mime_type: str
    suffix: str
    sha256: str


class RejectRedirects(HTTPRedirectHandler):
    """Never forward the authorization header to a redirected origin."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):  # noqa: ANN001
        return None


class ResponseTooLarge(Exception):
    """Carry a bounded response prefix so failure evidence can still be retained."""

    def __init__(self, evidence: bytes, limit: int) -> None:
        super().__init__(f"Image API response exceeds the {limit}-byte safety limit")
        self.evidence = evidence
        self.limit = limit


def load_manifest(run_dir: Path) -> dict[str, object]:
    path = resolve_run_path(run_dir, "imagegen-jobs.json", field="job manifest")
    if not path.exists():
        raise SystemExit(f"job manifest not found: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def manifest_jobs(manifest: dict[str, object]) -> list[dict[str, object]]:
    jobs = manifest.get("jobs")
    if not isinstance(jobs, list):
        raise SystemExit("invalid imagegen-jobs.json: jobs must be a list")
    return [job for job in jobs if isinstance(job, dict)]


def select_jobs(manifest: dict[str, object], job_ids: list[str]) -> list[dict[str, object]]:
    jobs = manifest_jobs(manifest)
    if job_ids:
        selected_ids = set(job_ids)
        selected = [job for job in jobs if job.get("id") in selected_ids]
    else:
        selected = [job for job in jobs if job.get("status", "pending") != "complete"]
        selected_ids = {
            str(job.get("id"))
            for job in selected
            if isinstance(job.get("id"), str)
        }
    missing = selected_ids - {str(job.get("id")) for job in selected}
    if missing:
        raise SystemExit(f"unknown job id(s): {', '.join(sorted(missing))}")
    completed = [
        str(job.get("id"))
        for job in selected
        if job.get("status", "pending") == "complete"
    ]
    if completed:
        raise SystemExit(
            "refusing to regenerate completed job(s): "
            f"{', '.join(completed)}; queue an authorized repair first"
        )
    return selected


def completed_ids(manifest: dict[str, object]) -> set[str]:
    return {
        str(job["id"])
        for job in manifest_jobs(manifest)
        if job.get("status") == "complete" and isinstance(job.get("id"), str)
    }


def missing_deps(job: dict[str, object], completed: set[str]) -> list[str]:
    deps = job.get("depends_on", [])
    if not isinstance(deps, list):
        return []
    return [dep for dep in deps if isinstance(dep, str) and dep not in completed]


def response_relative_path(job: dict[str, object]) -> str:
    """Keep each authorized repair response without replacing earlier evidence."""
    job_id = job.get("id")
    if not isinstance(job_id, str) or not job_id:
        raise SystemExit("job id must be a non-empty string")
    try:
        repair_attempt = int(job.get("repair_attempt", 0))
    except (TypeError, ValueError):
        raise SystemExit(f"job {job_id} has an invalid repair_attempt") from None
    if repair_attempt < 0:
        raise SystemExit(f"job {job_id} has an invalid repair_attempt")
    suffix = "" if repair_attempt == 0 else f".repair-{repair_attempt:02d}"
    return f"raw/{job_id}{suffix}.response.json"


def run_image_edit(
    *,
    model: str,
    prompt_file: Path,
    image_paths: list[AuthorizedImageInput],
    output_json: Path,
    size: str,
    api_key: str,
) -> dict[str, object]:
    body, content_type = multipart_body(
        fields={
            "model": model,
            "prompt": read_prompt_text(prompt_file),
            "size": size,
            "output_format": "png",
        },
        image_paths=image_paths,
    )
    return post_image_request(
        url="https://api.openai.com/v1/images/edits",
        body=body,
        content_type=content_type,
        output_json=output_json,
        api_key=api_key,
    )


def run_image_generation(
    *,
    model: str,
    prompt_file: Path,
    output_json: Path,
    size: str,
    api_key: str,
) -> dict[str, object]:
    body = json.dumps(
        {
            "model": model,
            "prompt": read_prompt_text(prompt_file),
            "size": size,
            "output_format": "png",
        }
    ).encode("utf-8")
    if len(body) > MAX_REQUEST_BODY_BYTES:
        raise SystemExit(
            f"Image API request body exceeds the {MAX_REQUEST_BODY_BYTES // (1024 * 1024)} MiB safety limit"
        )
    return post_image_request(
        url="https://api.openai.com/v1/images/generations",
        body=body,
        content_type="application/json",
        output_json=output_json,
        api_key=api_key,
    )


def multipart_body(
    *,
    fields: dict[str, str],
    image_paths: list[AuthorizedImageInput],
) -> tuple[bytes, str]:
    if len(image_paths) > MAX_INPUT_IMAGES:
        raise SystemExit(f"direct Image API jobs may include at most {MAX_INPUT_IMAGES} input images")
    boundary = f"----stray-pixel-{secrets.token_hex(16)}"
    chunks: list[bytes] = []
    for name, value in fields.items():
        chunks.extend(
            [
                f"--{boundary}\r\n".encode("ascii"),
                f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode("ascii"),
                value.encode("utf-8"),
                b"\r\n",
            ]
        )
    for index, image in enumerate(image_paths, start=1):
        chunks.extend(
            [
                f"--{boundary}\r\n".encode("ascii"),
                (
                    'Content-Disposition: form-data; name="image[]"; '
                    f'filename="image-{index:02d}{image.suffix}"\r\n'
                ).encode("ascii"),
                f"Content-Type: {image.mime_type}\r\n\r\n".encode("ascii"),
                image.payload,
                b"\r\n",
            ]
        )
    chunks.append(f"--{boundary}--\r\n".encode("ascii"))
    body = b"".join(chunks)
    if len(body) > MAX_REQUEST_BODY_BYTES:
        raise SystemExit(
            f"Image API request body exceeds the {MAX_REQUEST_BODY_BYTES // (1024 * 1024)} MiB safety limit"
        )
    return body, f"multipart/form-data; boundary={boundary}"


def read_prompt_text(prompt_file: Path) -> str:
    """Read a bounded UTF-8 prompt before constructing an external request."""
    try:
        size = prompt_file.stat().st_size
    except OSError as exc:
        raise SystemExit(f"cannot inspect prompt file {prompt_file}: {exc}") from None
    if size > MAX_PROMPT_BYTES:
        raise SystemExit(
            f"prompt exceeds the {MAX_PROMPT_BYTES // 1024} KiB direct API safety limit: {prompt_file}"
        )
    try:
        payload = prompt_file.read_bytes()
        if len(payload) > MAX_PROMPT_BYTES:
            raise SystemExit(
                f"prompt exceeds the {MAX_PROMPT_BYTES // 1024} KiB direct API safety limit: {prompt_file}"
            )
        return payload.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise SystemExit(f"prompt file must be valid UTF-8: {prompt_file}: {exc}") from None


def post_image_request(
    *,
    url: str,
    body: bytes,
    content_type: str,
    output_json: Path,
    api_key: str,
) -> dict[str, object]:
    request = Request(
        url,
        data=body,
        method="POST",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": content_type,
        },
    )
    try:
        opener = build_opener(RejectRedirects())
        # Fixed OpenAI endpoint; redirects are rejected by the opener.
        with opener.open(request, timeout=180) as response:
            payload = read_bounded_response(response)
    except ResponseTooLarge as exc:
        write_exclusive(output_json, exc.evidence, field="bounded Image API response evidence")
        raise SystemExit(
            f"Image API response exceeds the {exc.limit // (1024 * 1024)} MiB safety limit; "
            f"saved the first {len(exc.evidence)} bytes as failure evidence"
        ) from None
    except HTTPError as exc:
        try:
            payload = read_bounded_response(exc)
        except ResponseTooLarge as oversized:
            write_exclusive(
                output_json,
                oversized.evidence,
                field="bounded Image API error response evidence",
            )
            raise SystemExit(
                f"Image API HTTP {exc.code} response exceeds the "
                f"{oversized.limit // (1024 * 1024)} MiB safety limit; saved the first "
                f"{len(oversized.evidence)} bytes as failure evidence"
            ) from None
        write_exclusive(output_json, payload, field="Image API response")
        raise SystemExit(
            f"Image API request failed with HTTP {exc.code}; response evidence saved locally to {output_json}"
        ) from None
    except URLError as exc:
        raise SystemExit(f"Image API request failed: {exc.reason}") from None

    write_exclusive(output_json, payload, field="Image API response")
    try:
        parsed = json.loads(payload)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Image API returned invalid JSON: {exc}") from None
    if not isinstance(parsed, dict):
        raise SystemExit("Image API response must be a JSON object")
    if parsed.get("error"):
        error = parsed["error"]
        labels = []
        if isinstance(error, dict):
            for key in ("type", "code"):
                value = error.get(key)
                if isinstance(value, str) and SAFE_ERROR_LABEL_RE.fullmatch(value):
                    labels.append(f"{key}={value}")
        suffix = f" ({', '.join(labels)})" if labels else ""
        raise SystemExit(f"Image API returned an error{suffix}; details remain in {output_json}")
    return parsed


def read_bounded_response(
    response: BinaryIO,
    *,
    max_bytes: int | None = None,
) -> bytes:
    """Read at most ``max_bytes + 1`` bytes and retain a bounded failure prefix."""
    if max_bytes is None:
        max_bytes = MAX_API_RESPONSE_BYTES
    if max_bytes <= 0:
        raise ValueError("max_bytes must be positive")
    payload = bytearray()
    while len(payload) <= max_bytes:
        remaining = max_bytes + 1 - len(payload)
        chunk = response.read(min(RESPONSE_READ_CHUNK_BYTES, remaining))
        if not chunk:
            return bytes(payload)
        payload.extend(chunk[:remaining])
    raise ResponseTooLarge(bytes(payload[:max_bytes]), max_bytes)


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


def response_image_bytes(response: dict[str, object]) -> bytes:
    """Strictly decode the first base64 image from an Image API response."""
    data = response.get("data")
    if not isinstance(data, list) or not data:
        raise SystemExit("image API response did not contain data[0]")
    first = data[0]
    if not isinstance(first, dict) or not isinstance(first.get("b64_json"), str):
        raise SystemExit("image API response did not contain data[0].b64_json")
    try:
        return base64.b64decode(first["b64_json"], validate=True)
    except (binascii.Error, ValueError) as exc:
        raise SystemExit(f"image API response contains invalid base64 image data: {exc}") from None


def stage_decoded_response(response: dict[str, object], output_image: Path) -> Path:
    """Stage a strictly decoded, fully verified PNG without publishing it."""
    staged = stage_bytes(output_image, response_image_bytes(response))
    try:
        validated = validate_image_input(staged, field="decoded Image API output")
        if validated.format != "PNG":
            raise SystemExit(
                f"decoded Image API output must be PNG, received {validated.format!r}"
            )
    except BaseException:
        staged.unlink(missing_ok=True)
        raise
    return staged


def decode_response(response: dict[str, object], output_image: Path) -> None:
    """Verify and atomically publish a decoded output without overwriting."""
    staged = stage_decoded_response(response, output_image)
    try:
        commit_staged_path(staged, output_image, force=False)
    finally:
        staged.unlink(missing_ok=True)


def write_exclusive(path: Path, payload: bytes, *, field: str) -> None:
    """Atomically create evidence without replacing an existing artifact."""
    if path.exists() or path.is_symlink():
        raise SystemExit(f"refusing to overwrite existing {field}: {path}") from None
    atomic_write_bytes(path, payload, force=False, mode=0o600)


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def complete_job(
    job: dict[str, object],
    output_path: Path,
    *,
    hash_path: Path | None = None,
) -> None:
    content_path = hash_path or output_path
    job["status"] = "complete"
    job["source_path"] = str(output_path)
    job["source_provenance"] = "explicit-direct-image-api"
    job["source_sha256"] = file_sha256(content_path)
    job["output_sha256"] = file_sha256(content_path)
    job["completed_at"] = datetime.now(timezone.utc).isoformat()
    job["direct_image_api"] = True
    job.pop("secondary_fallback", None)
    for key in ["last_error", "repair_reason", "queued_at"]:
        job.pop(key, None)


def prepare_canonical_base(
    run_dir: Path,
    manifest: dict[str, object],
    job: dict[str, object],
    staged_image: Path,
) -> tuple[Path, bytes, Path | None, bytes | None]:
    """Prepare derived base artifacts without mutating their published paths."""
    canonical = resolve_run_mutation_path(
        run_dir,
        CANONICAL_BASE_PATH,
        field="canonical base path",
        allowed_roots=("references",),
    )
    reference = {
        "path": CANONICAL_BASE_PATH,
        "source_job": "base",
        "sha256": file_sha256(staged_image),
    }
    job["canonical_reference_path"] = CANONICAL_BASE_PATH
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
    return canonical, staged_image.read_bytes(), request_path, request_payload


def commit_generated_transaction(
    artifacts: list[tuple[Path, Path, bool]],
    *,
    manifest_staged: Path,
    manifest_path: Path,
) -> None:
    """Publish artifacts atomically one-by-one and make the manifest the commit point."""
    for staged, target, force in artifacts:
        commit_staged_path(staged, target, force=force)
    commit_staged_path(manifest_staged, manifest_path, force=True)


def authorized_input_inventory(run_dir: Path, job: dict[str, object]) -> dict[str, str]:
    """Load the prepared reference paths and hashes authorized for this job."""
    request_path = resolve_run_path(run_dir, "asset_request.json", field="asset request")
    try:
        request = json.loads(request_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"cannot load authorized reference inventory: {exc}") from None
    if not isinstance(request, dict):
        raise SystemExit("asset_request.json must contain a JSON object")

    entries = request.get("references", [])
    if not isinstance(entries, list):
        raise SystemExit("asset_request.json references must be an array")
    candidates = [entry for entry in entries if isinstance(entry, dict)]
    if job.get("id") != "base":
        canonical = request.get("canonical_identity_reference")
        if isinstance(canonical, dict):
            candidates.append(canonical)

    inventory: dict[str, str] = {}
    root = run_dir.expanduser().resolve()
    for entry in candidates:
        raw_path = entry.get("path")
        expected_hash = entry.get("sha256")
        if not isinstance(raw_path, str) or not isinstance(expected_hash, str):
            raise SystemExit(
                "authorized reference inventory requires path and sha256 for every input"
            )
        path = resolve_run_path(
            run_dir,
            raw_path,
            field="authorized reference path",
            allowed_roots=("references",),
        )
        relative = path.relative_to(root).as_posix()
        if relative in inventory:
            raise SystemExit(f"duplicate authorized reference path: {relative}")
        inventory[relative] = expected_hash
    return inventory


def path_list(run_dir: Path, job: dict[str, object]) -> list[AuthorizedImageInput]:
    inputs = job.get("input_images")
    if not isinstance(inputs, list):
        return []
    if len(inputs) > MAX_INPUT_IMAGES:
        raise SystemExit(f"direct Image API jobs may include at most {MAX_INPUT_IMAGES} input images")
    inventory = authorized_input_inventory(run_dir, job) if inputs else {}
    root = run_dir.expanduser().resolve()
    seen: set[str] = set()
    seen_hashes: set[str] = set()
    total_bytes = 0
    paths: list[AuthorizedImageInput] = []
    for item in inputs:
        if not isinstance(item, dict) or not isinstance(item.get("path"), str):
            raise SystemExit(f"job {job.get('id')} has invalid input image entry")
        path = resolve_run_path(
            run_dir,
            item["path"],
            field=f"job {job.get('id')} input image path",
            allowed_roots=("references",),
        )
        if not path.is_file():
            raise SystemExit(f"input image for job {job.get('id')} not found: {path}")
        validated, payload = read_validated_image_input(
            path,
            field=f"job {job.get('id')} input image",
        )
        relative = path.relative_to(root).as_posix()
        if relative in seen:
            raise SystemExit(f"job {job.get('id')} repeats input image: {relative}")
        seen.add(relative)
        expected_hash = inventory.get(relative)
        if expected_hash is None:
            raise SystemExit(
                f"job {job.get('id')} input image was not authorized during run preparation: {relative}"
            )
        actual_hash = hashlib.sha256(payload).hexdigest()
        if not secrets.compare_digest(actual_hash, expected_hash):
            raise SystemExit(
                f"job {job.get('id')} input image no longer matches its prepared sha256: {relative}"
            )
        if actual_hash in seen_hashes:
            raise SystemExit(
                f"job {job.get('id')} repeats input image content: {relative}"
            )
        seen_hashes.add(actual_hash)
        total_bytes += len(payload)
        if total_bytes > MAX_TOTAL_INPUT_IMAGE_BYTES:
            raise SystemExit(
                "job input images exceed the "
                f"{MAX_TOTAL_INPUT_IMAGE_BYTES // (1024 * 1024)} MiB aggregate safety limit"
            )
        paths.append(
            AuthorizedImageInput(
                path=path,
                payload=payload,
                mime_type=validated.mime_type,
                suffix=validated.suffix,
                sha256=actual_hash,
            )
        )
    return paths


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--model", default="gpt-image-2")
    parser.add_argument("--size", default="1024x1024")
    parser.add_argument("--job-id", action="append", default=[])
    parser.add_argument(
        "--confirm-direct-api",
        action="store_true",
        help=(
            "confirm that prompts and input images may be sent to the separately billed "
            "OpenAI Image API"
        ),
    )
    args = parser.parse_args()

    if not args.confirm_direct_api:
        raise SystemExit(
            "direct Image API use requires explicit user authorization and --confirm-direct-api"
        )
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise SystemExit("OPENAI_API_KEY is not set")

    run_dir = Path(args.run_dir).expanduser().resolve()
    manifest_path = resolve_run_mutation_path(
        run_dir,
        "imagegen-jobs.json",
        field="job manifest",
    )
    manifest = load_manifest(run_dir)

    completed = []
    for job in select_jobs(manifest, args.job_id):
        job_id = str(job.get("id"))
        deps = missing_deps(job, completed_ids(manifest))
        if deps:
            raise SystemExit(
                f"job {job_id} is not ready; missing dependency result(s): "
                f"{', '.join(deps)}"
            )
        prompt_raw = job.get("prompt_file")
        output_raw = job.get("output_path")
        if not isinstance(prompt_raw, str) or not isinstance(output_raw, str):
            raise SystemExit(f"job {job_id} is missing prompt_file or output_path")
        prompt_file = resolve_run_path(
            run_dir,
            prompt_raw,
            field=f"job {job_id} prompt_file",
            allowed_roots=("prompts",),
        )
        if not prompt_file.is_file():
            raise SystemExit(f"prompt file for job {job_id} not found: {prompt_file}")
        output_image = resolve_run_mutation_path(
            run_dir,
            output_raw,
            field=f"job {job_id} output_path",
            allowed_roots=("decoded",),
        )
        response_json = resolve_run_mutation_path(
            run_dir,
            response_relative_path(job),
            field=f"job {job_id} response path",
            allowed_roots=("raw",),
        )
        for path, field in [
            (output_image, "decoded image"),
            (response_json, "Image API response"),
        ]:
            if path.exists() or path.is_symlink():
                raise SystemExit(f"refusing to overwrite existing {field}: {path}")
        print(f"Generating {job_id} through the explicitly authorized direct Image API path")
        image_paths = path_list(run_dir, job)
        if image_paths:
            response = run_image_edit(
                model=args.model,
                prompt_file=prompt_file,
                image_paths=image_paths,
                output_json=response_json,
                size=args.size,
                api_key=api_key,
            )
        else:
            response = run_image_generation(
                model=args.model,
                prompt_file=prompt_file,
                output_json=response_json,
                size=args.size,
                api_key=api_key,
            )
        staged_paths: list[Path] = []
        try:
            output_staged = stage_decoded_response(response, output_image)
            staged_paths.append(output_staged)
            complete_job(job, output_image, hash_path=output_staged)

            artifact_commits: list[tuple[Path, Path, bool]] = [
                (output_staged, output_image, False)
            ]
            if job_id == "base":
                canonical, canonical_payload, request_path, request_payload = (
                    prepare_canonical_base(run_dir, manifest, job, output_staged)
                )
                canonical_staged = stage_bytes(canonical, canonical_payload)
                staged_paths.append(canonical_staged)
                artifact_commits.append((canonical_staged, canonical, True))
                if request_path is not None and request_payload is not None:
                    request_staged = stage_bytes(request_path, request_payload)
                    staged_paths.append(request_staged)
                    artifact_commits.append((request_staged, request_path, True))

            manifest_payload = (json.dumps(manifest, indent=2) + "\n").encode("utf-8")
            manifest_staged = stage_bytes(manifest_path, manifest_payload)
            staged_paths.append(manifest_staged)
            commit_generated_transaction(
                artifact_commits,
                manifest_staged=manifest_staged,
                manifest_path=manifest_path,
            )
        finally:
            for staged in staged_paths:
                staged.unlink(missing_ok=True)
        completed.append({"job_id": job_id, "output": str(output_image)})

    print(json.dumps({"ok": True, "completed": completed}, indent=2))


if __name__ == "__main__":
    main()
