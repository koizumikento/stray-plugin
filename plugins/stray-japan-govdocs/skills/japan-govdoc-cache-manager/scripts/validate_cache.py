#!/usr/bin/env python3
"""Validate tmp/japan-govdocs cache metadata.

Checks manifest JSONL required fields, local path existence, bytes, sha256, and
the broad whitepaper source-index shape described in download-cache-policy.md.
"""

from __future__ import annotations

import argparse
import hashlib
import json
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

SOURCE_INDEX_RECORD_FIELDS = {
    "document_id",
    "title",
    "ministry",
    "year",
    "landing_page",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_jsonl(path: Path) -> tuple[list[dict], list[str]]:
    records: list[dict] = []
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
        records.append(record)
    return records, errors


def resolve_local_path(cache_root: Path, raw_path: str) -> Path:
    path = Path(raw_path)
    if path.is_absolute():
        return path
    if path.parts[:2] == ("tmp", "japan-govdocs"):
        return cache_root.parent.parent / path
    return cache_root / path


def validate_manifest(cache_root: Path) -> list[str]:
    manifest_path = cache_root / "manifest.jsonl"
    if not manifest_path.exists():
        return [f"{manifest_path}: missing manifest.jsonl"]

    records, errors = load_jsonl(manifest_path)
    for index, record in enumerate(records, 1):
        missing = sorted(REQUIRED_MANIFEST_FIELDS - record.keys())
        if missing:
            errors.append(f"{manifest_path}:{index}: missing fields: {', '.join(missing)}")

        local_path_value = record.get("local_path")
        if isinstance(local_path_value, str) and local_path_value:
            local_path = resolve_local_path(cache_root, local_path_value)
            if not local_path.exists():
                errors.append(f"{manifest_path}:{index}: local_path does not exist: {local_path}")
                continue

            expected_bytes = record.get("bytes")
            actual_bytes = local_path.stat().st_size
            if expected_bytes != actual_bytes:
                errors.append(
                    f"{manifest_path}:{index}: bytes mismatch for {local_path}: "
                    f"manifest={expected_bytes!r} actual={actual_bytes}"
                )

            expected_hash = record.get("sha256")
            if isinstance(expected_hash, str) and expected_hash:
                actual_hash = sha256(local_path)
                if expected_hash.lower() != actual_hash:
                    errors.append(
                        f"{manifest_path}:{index}: sha256 mismatch for {local_path}: "
                        f"manifest={expected_hash} actual={actual_hash}"
                    )
        else:
            errors.append(f"{manifest_path}:{index}: local_path must be a non-empty string")

    return errors


def iter_source_records(data: object) -> list[dict]:
    if isinstance(data, list):
        return [item for item in data if isinstance(item, dict)]
    if isinstance(data, dict):
        if isinstance(data.get("records"), list):
            return [item for item in data["records"] if isinstance(item, dict)]
        if isinstance(data.get("whitepapers"), list):
            return [item for item in data["whitepapers"] if isinstance(item, dict)]
        return [data]
    return []


def validate_source_index(cache_root: Path) -> list[str]:
    index_path = cache_root / "sources" / "whitepaper-index.json"
    if not index_path.exists():
        return []

    try:
        data = json.loads(index_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"{index_path}: invalid JSON: {exc}"]

    records = iter_source_records(data)
    if not records:
        return [f"{index_path}: expected an object, records array, or whitepapers array"]

    errors: list[str] = []
    for index, record in enumerate(records, 1):
        missing = sorted(SOURCE_INDEX_RECORD_FIELDS - record.keys())
        if missing:
            errors.append(f"{index_path}:record {index}: missing recommended fields: {', '.join(missing)}")
        if "editions" in record and not isinstance(record["editions"], list):
            errors.append(f"{index_path}:record {index}: editions must be an array when present")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("cache_root", nargs="?", default="tmp/japan-govdocs")
    args = parser.parse_args()

    cache_root = Path(args.cache_root).resolve()
    if not cache_root.exists():
        print(f"{cache_root}: cache root does not exist", file=sys.stderr)
        return 1

    errors = validate_manifest(cache_root) + validate_source_index(cache_root)
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    print("cache-ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
