#!/usr/bin/env python3
"""Validate reference images before copying or external transmission."""

from __future__ import annotations

import io
import warnings
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, UnidentifiedImageError

MAX_REFERENCE_BYTES = 20 * 1024 * 1024
ALLOWED_FORMATS = {
    "JPEG": ("image/jpeg", ".jpg"),
    "PNG": ("image/png", ".png"),
    "WEBP": ("image/webp", ".webp"),
}


@dataclass(frozen=True)
class ValidatedImage:
    format: str
    mime_type: str
    suffix: str
    size_bytes: int


def read_validated_image_input(
    path: Path,
    *,
    field: str,
) -> tuple[ValidatedImage, bytes]:
    """Read one bounded snapshot and validate the exact bytes returned."""
    try:
        size = path.stat().st_size
    except OSError as exc:
        raise SystemExit(f"cannot inspect {field}: {path}: {exc}") from None
    if size <= 0:
        raise SystemExit(f"{field} is empty: {path}")
    if size > MAX_REFERENCE_BYTES:
        raise SystemExit(
            f"{field} exceeds the {MAX_REFERENCE_BYTES // (1024 * 1024)} MiB local safety limit: {path}"
        )

    try:
        with path.open("rb") as handle:
            payload = handle.read(MAX_REFERENCE_BYTES + 1)
    except OSError as exc:
        raise SystemExit(f"cannot read {field}: {path}: {exc}") from None
    if len(payload) > MAX_REFERENCE_BYTES:
        raise SystemExit(
            f"{field} exceeds the {MAX_REFERENCE_BYTES // (1024 * 1024)} MiB local safety limit: {path}"
        )
    if not payload:
        raise SystemExit(f"{field} is empty: {path}")

    validated = validate_image_bytes(payload, field=field, source=str(path))
    return validated, payload


def validate_image_bytes(payload: bytes, *, field: str, source: str) -> ValidatedImage:
    """Validate a bounded immutable PNG, JPEG, or WebP byte snapshot."""
    if not payload:
        raise SystemExit(f"{field} is empty: {source}")
    if len(payload) > MAX_REFERENCE_BYTES:
        raise SystemExit(
            f"{field} exceeds the {MAX_REFERENCE_BYTES // (1024 * 1024)} MiB local safety limit: {source}"
        )
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("error", Image.DecompressionBombWarning)
            with Image.open(io.BytesIO(payload)) as image:
                image_format = image.format
                image.verify()
    except (Image.DecompressionBombError, Image.DecompressionBombWarning) as exc:
        raise SystemExit(f"{field} exceeds Pillow's safe pixel limit: {source}: {exc}") from None
    except (UnidentifiedImageError, OSError, SyntaxError) as exc:
        raise SystemExit(f"{field} is not a valid supported image: {source}: {exc}") from None

    if image_format not in ALLOWED_FORMATS:
        allowed = ", ".join(sorted(ALLOWED_FORMATS))
        raise SystemExit(
            f"{field} uses unsupported image format {image_format!r}; allowed formats: {allowed}"
        )
    mime_type, suffix = ALLOWED_FORMATS[image_format]
    return ValidatedImage(image_format, mime_type, suffix, len(payload))


def validate_image_input(path: Path, *, field: str) -> ValidatedImage:
    """Require a bounded, decodable PNG, JPEG, or WebP input image."""
    validated, _ = read_validated_image_input(path, field=field)
    return validated
