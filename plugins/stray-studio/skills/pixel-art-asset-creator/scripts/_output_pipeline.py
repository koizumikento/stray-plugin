#!/usr/bin/env python3
"""Contained, staged output helpers for the pixel-art writer pipeline."""

from __future__ import annotations

import os
import shutil
import tempfile
from pathlib import Path
from typing import Any, Iterable

from PIL import Image

from _run_safety import (
    commit_staged_path,
    create_staging_path,
    resolve_run_mutation_path,
    resolve_run_output_path,
)


def run_relative_output(run_dir: Path, raw_path: str | Path, *, field: str) -> str:
    """Return a lexical run-relative path without resolving away symlinks."""
    root = run_dir.expanduser().resolve()
    supplied = Path(raw_path).expanduser()
    if supplied.is_absolute():
        try:
            supplied = supplied.relative_to(root)
        except ValueError:
            raise SystemExit(f"{field} must stay below the asset run: {raw_path!s}") from None
    return supplied.as_posix()


def resolve_output(
    run_dir: Path,
    raw_path: str | Path,
    *,
    field: str,
    force: bool,
) -> Path:
    """Resolve one output below a run and apply the overwrite gate."""
    relative = run_relative_output(run_dir, raw_path, field=field)
    return resolve_run_output_path(
        run_dir,
        relative,
        field=field,
        force=force,
    )


def resolve_output_directory(
    run_dir: Path,
    raw_path: str | Path,
    *,
    field: str,
) -> Path:
    """Resolve a contained directory target and reject symlink components."""
    relative = run_relative_output(run_dir, raw_path, field=field)
    directory = resolve_run_mutation_path(run_dir, relative, field=field)
    if directory.exists() and not directory.is_dir():
        raise SystemExit(f"{field} must be a directory: {directory}")
    return directory


def preflight_directory_outputs(
    run_dir: Path,
    output_dir: Path,
    names: Iterable[str],
    *,
    field: str,
    force: bool,
) -> list[Path]:
    """Preflight a replaceable multi-file directory and all known outputs."""
    root = run_dir.expanduser().resolve()
    relative_dir = output_dir.relative_to(root)
    if output_dir.exists() and any(output_dir.iterdir()) and not force:
        raise SystemExit(f"{output_dir} is not empty; pass --force to replace it")

    targets: list[Path] = []
    seen: set[Path] = set()
    for name in names:
        relative = relative_dir / name
        target = resolve_run_output_path(
            root,
            relative.as_posix(),
            field=f"{field} {name}",
            force=force,
        )
        if target in seen:
            raise SystemExit(f"duplicate {field} target: {target}")
        seen.add(target)
        targets.append(target)
    return targets


def create_staged_directory(target: Path) -> Path:
    """Create an invisible sibling directory for a complete output set."""
    target.parent.mkdir(parents=True, exist_ok=True)
    return Path(tempfile.mkdtemp(prefix=f".{target.name}.", suffix=".tmp", dir=target.parent))


def stage_image(
    target: Path,
    image: Image.Image,
    *,
    image_format: str,
    **save_options: Any,
) -> Path:
    """Write and fsync a complete Pillow image to a same-directory stage."""
    staged = create_staging_path(target)
    try:
        with staged.open("wb") as handle:
            image.save(handle, format=image_format, **save_options)
            handle.flush()
            os.fsync(handle.fileno())
    except BaseException:
        staged.unlink(missing_ok=True)
        raise
    return staged


def stage_text(target: Path, content: str) -> Path:
    """Write and fsync complete UTF-8 text to a same-directory stage."""
    staged = create_staging_path(target)
    try:
        with staged.open("wb") as handle:
            handle.write(content.encode("utf-8"))
            handle.flush()
            os.fsync(handle.fileno())
    except BaseException:
        staged.unlink(missing_ok=True)
        raise
    return staged


def write_staged_image(
    target: Path,
    image: Image.Image,
    *,
    image_format: str,
    **save_options: Any,
) -> None:
    """Atomically materialize an image inside an already-staged directory."""
    staged = stage_image(target, image, image_format=image_format, **save_options)
    try:
        commit_staged_path(staged, target, force=False)
    finally:
        staged.unlink(missing_ok=True)


def write_staged_text(target: Path, content: str) -> None:
    """Atomically materialize text inside an already-staged directory."""
    staged = stage_text(target, content)
    try:
        commit_staged_path(staged, target, force=False)
    finally:
        staged.unlink(missing_ok=True)


def commit_outputs(
    run_dir: Path,
    staged_outputs: list[tuple[Path, Path]],
    *,
    force: bool,
) -> None:
    """Revalidate and atomically commit staged files one by one."""
    root = run_dir.expanduser().resolve()
    seen: set[Path] = set()
    try:
        for _, target in staged_outputs:
            if target in seen:
                raise SystemExit(f"duplicate output target: {target}")
            seen.add(target)
            relative = target.relative_to(root).as_posix()
            resolve_run_output_path(
                root,
                relative,
                field="output",
                force=force,
            )
        for staged, target in staged_outputs:
            commit_staged_path(staged, target, force=force)
    finally:
        for staged, _ in staged_outputs:
            staged.unlink(missing_ok=True)


def commit_staged_directory(
    run_dir: Path,
    staged_dir: Path,
    output_dir: Path,
    names: Iterable[str],
    *,
    field: str,
    force: bool,
) -> None:
    """Swap a complete staged directory into place without retaining stale files."""
    root = run_dir.expanduser().resolve()
    relative_dir = output_dir.relative_to(root).as_posix()
    resolve_run_mutation_path(root, relative_dir, field=field)
    preflight_directory_outputs(root, output_dir, names, field=field, force=force)

    if not output_dir.exists():
        os.replace(staged_dir, output_dir)
        return

    backup = Path(tempfile.mkdtemp(prefix=f".{output_dir.name}.old.", dir=output_dir.parent))
    backup.rmdir()
    os.replace(output_dir, backup)
    try:
        os.replace(staged_dir, output_dir)
    except BaseException:
        os.replace(backup, output_dir)
        raise
    else:
        shutil.rmtree(backup)


def cleanup_staged_directory(path: Path) -> None:
    """Remove an uncommitted staging directory without following child symlinks."""
    if path.exists():
        shutil.rmtree(path)
