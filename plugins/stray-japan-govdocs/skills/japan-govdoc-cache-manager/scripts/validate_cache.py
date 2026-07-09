#!/usr/bin/env python3
"""Validate tmp/japan-govdocs cache metadata and file traceability.

Index-only caches may omit or empty manifest.jsonl when downloads/ and
extracted/ contain no files. Download caches require one manifest record per
cached file. The source index uses the canonical {"records": [...]} shape.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path


REQUIRED_MANIFEST_FIELDS = {
    "document_id",
    "title",
    "ministry",
    "year",
    "landing_page",
    "source_url",
    "local_path",
    "content_type",
    "bytes",
    "sha256",
    "fetched_at",
    "reason",
}

REQUIRED_SOURCE_INDEX_FIELDS = {
    "document_id",
    "title",
    "ministry",
    "year",
    "landing_page",
}

OPTIONAL_SOURCE_INDEX_STRING_FIELDS = {
    "ministry_slug",
    "document_slug",
    "series",
    "edition",
    "egov_index_url",
    "series_landing_page",
    "edition_landing_page",
    "html_url",
    "pdf_index_url",
    "pdf_url",
    "summary_url",
    "archive_url",
    "publication_date",
    "last_checked_at",
    "notes",
}

OPTIONAL_SOURCE_INDEX_ARRAY_FIELDS = {
    "chapter_urls",
    "data_urls",
}

ALLOWED_SOURCE_INDEX_FIELDS = (
    REQUIRED_SOURCE_INDEX_FIELDS
    | OPTIONAL_SOURCE_INDEX_STRING_FIELDS
    | OPTIONAL_SOURCE_INDEX_ARRAY_FIELDS
)

SHA256_RE = re.compile(r"^[0-9a-fA-F]{64}$")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_jsonl(path: Path) -> tuple[list[tuple[int, dict]], list[str]]:
    records: list[tuple[int, dict]] = []
    errors: list[str] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append(f"{path}:{line_number}: invalid JSON: {exc}")
            continue
        if not isinstance(record, dict):
            errors.append(f"{path}:{line_number}: record must be a JSON object")
            continue
        records.append((line_number, record))
    return records, errors


def resolve_local_path(cache_root: Path, raw_path: str) -> Path:
    path = Path(raw_path)
    if path.is_absolute():
        return path.resolve()
    if path.parts[:2] == ("tmp", "japan-govdocs"):
        return (cache_root.parent.parent / path).resolve()
    return (cache_root / path).resolve()


def cached_files(cache_root: Path) -> set[Path]:
    files: set[Path] = set()
    for directory_name in ("downloads", "extracted"):
        directory = cache_root / directory_name
        if directory.exists():
            files.update(path.resolve() for path in directory.rglob("*") if path.is_file())
    return files


def validate_manifest(cache_root: Path) -> tuple[list[str], int]:
    manifest_path = cache_root / "manifest.jsonl"
    files = cached_files(cache_root)
    if not manifest_path.exists():
        if files:
            return [f"{manifest_path}: required because cached files exist"], 0
        return [], 0

    records, errors = load_jsonl(manifest_path)
    tracked_paths: set[Path] = set()

    for line_number, record in records:
        location = f"{manifest_path}:{line_number}"
        missing = sorted(REQUIRED_MANIFEST_FIELDS - record.keys())
        if missing:
            errors.append(f"{location}: missing fields: {', '.join(missing)}")

        for field in ("document_id", "title", "ministry", "landing_page", "source_url", "content_type", "fetched_at", "reason"):
            if field in record and (not isinstance(record[field], str) or not record[field].strip()):
                errors.append(f"{location}: {field} must be a non-empty string")

        year = record.get("year")
        if "year" in record and (
            isinstance(year, bool)
            or not isinstance(year, (str, int))
            or (isinstance(year, str) and not year.strip())
        ):
            errors.append(f"{location}: year must be a non-empty string or integer")

        expected_bytes = record.get("bytes")
        if "bytes" in record and (not isinstance(expected_bytes, int) or isinstance(expected_bytes, bool) or expected_bytes < 0):
            errors.append(f"{location}: bytes must be a non-negative integer")

        expected_hash = record.get("sha256")
        if "sha256" in record and (not isinstance(expected_hash, str) or not SHA256_RE.fullmatch(expected_hash)):
            errors.append(f"{location}: sha256 must be 64 hexadecimal characters")

        local_path_value = record.get("local_path")
        if not isinstance(local_path_value, str) or not local_path_value:
            errors.append(f"{location}: local_path must be a non-empty string")
            continue

        local_path = resolve_local_path(cache_root, local_path_value)
        try:
            relative_path = local_path.relative_to(cache_root)
        except ValueError:
            errors.append(f"{location}: local_path escapes cache root: {local_path}")
            continue
        if not relative_path.parts or relative_path.parts[0] not in {"downloads", "extracted"}:
            errors.append(f"{location}: local_path must be under downloads/ or extracted/: {local_path}")
            continue

        if local_path in tracked_paths:
            errors.append(f"{location}: duplicate local_path: {local_path}")
        tracked_paths.add(local_path)

        if not local_path.exists():
            errors.append(f"{location}: local_path does not exist: {local_path}")
            continue
        if not local_path.is_file():
            errors.append(f"{location}: local_path is not a file: {local_path}")
            continue

        actual_bytes = local_path.stat().st_size
        if isinstance(expected_bytes, int) and not isinstance(expected_bytes, bool) and expected_bytes != actual_bytes:
            errors.append(
                f"{location}: bytes mismatch for {local_path}: "
                f"manifest={expected_bytes!r} actual={actual_bytes}"
            )

        if isinstance(expected_hash, str) and SHA256_RE.fullmatch(expected_hash):
            actual_hash = sha256(local_path)
            if expected_hash.lower() != actual_hash:
                errors.append(
                    f"{location}: sha256 mismatch for {local_path}: "
                    f"manifest={expected_hash} actual={actual_hash}"
                )

    for untracked in sorted(files - tracked_paths):
        errors.append(f"{manifest_path}: cached file has no manifest record: {untracked}")

    return errors, len(records)


def validate_source_index(cache_root: Path) -> tuple[list[str], int, bool]:
    index_path = cache_root / "sources" / "whitepaper-index.json"
    if not index_path.exists():
        return [], 0, False

    try:
        data = json.loads(index_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"{index_path}: invalid JSON: {exc}"], 0, True

    if not isinstance(data, dict) or set(data) != {"records"} or not isinstance(data.get("records"), list):
        return [f'{index_path}: expected canonical object {{"records": [...]}}'], 0, True

    records = data["records"]
    errors: list[str] = []
    for index, record in enumerate(records, 1):
        location = f"{index_path}:record {index}"
        if not isinstance(record, dict):
            errors.append(f"{location}: record must be a JSON object")
            continue
        missing = sorted(REQUIRED_SOURCE_INDEX_FIELDS - record.keys())
        if missing:
            errors.append(f"{location}: missing fields: {', '.join(missing)}")
        unknown = sorted(record.keys() - ALLOWED_SOURCE_INDEX_FIELDS)
        if unknown:
            errors.append(f"{location}: unknown fields: {', '.join(unknown)}")
        for field in ("document_id", "title", "ministry", "landing_page"):
            if field in record and (not isinstance(record[field], str) or not record[field].strip()):
                errors.append(f"{location}: {field} must be a non-empty string")
        year = record.get("year")
        if "year" in record and (
            isinstance(year, bool)
            or not isinstance(year, (str, int))
            or (isinstance(year, str) and not year.strip())
        ):
            errors.append(f"{location}: year must be a non-empty string or integer")
        for field in sorted(OPTIONAL_SOURCE_INDEX_STRING_FIELDS):
            if field in record and (not isinstance(record[field], str) or not record[field].strip()):
                errors.append(f"{location}: {field} must be a non-empty string when present")
        for field in sorted(OPTIONAL_SOURCE_INDEX_ARRAY_FIELDS):
            if field not in record:
                continue
            value = record[field]
            if not isinstance(value, list):
                errors.append(f"{location}: {field} must be an array when present")
                continue
            for item_index, item in enumerate(value, 1):
                if not isinstance(item, str) or not item.strip():
                    errors.append(
                        f"{location}: {field}[{item_index}] must be a non-empty string"
                    )
    return errors, len(records), True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("cache_root", nargs="?", default="tmp/japan-govdocs")
    args = parser.parse_args()

    cache_root = Path(args.cache_root).resolve()
    if not cache_root.exists():
        print(f"{cache_root}: cache root does not exist", file=sys.stderr)
        return 1

    manifest_errors, manifest_count = validate_manifest(cache_root)
    index_errors, index_count, index_exists = validate_source_index(cache_root)
    errors = manifest_errors + index_errors

    if not index_exists and not (cache_root / "manifest.jsonl").exists() and not cached_files(cache_root):
        errors.append(f"{cache_root}: no manifest or source index to validate")

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    mode = "download-cache" if cached_files(cache_root) else "index-only"
    print(f"cache-ok mode={mode} manifest_records={manifest_count} source_records={index_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
