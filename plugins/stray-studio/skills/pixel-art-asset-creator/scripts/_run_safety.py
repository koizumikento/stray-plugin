#!/usr/bin/env python3
"""Shared filesystem guards for pixel-art asset run scripts."""

from __future__ import annotations

import json
import os
import stat
import tempfile
from datetime import datetime, timezone
from pathlib import Path

RUN_MARKER_NAME = ".pixel-art-asset-run.json"
RUN_MARKER_KIND = "stray-pixel-art-asset-run"
RUN_MARKER_VERSION = 1


def resolve_run_path(
    run_dir: Path,
    raw_path: str,
    *,
    field: str,
    allowed_roots: tuple[str, ...] = (),
) -> Path:
    """Resolve a manifest path and require it to stay below ``run_dir``."""
    if not isinstance(raw_path, str) or not raw_path.strip():
        raise SystemExit(f"{field} must be a non-empty relative path")

    relative = Path(raw_path)
    if relative.is_absolute():
        raise SystemExit(f"{field} must be relative to the asset run: {raw_path!r}")
    if ".." in relative.parts:
        raise SystemExit(f"{field} must not contain parent traversal: {raw_path!r}")

    root = run_dir.expanduser().resolve()
    candidate = (root / relative).resolve()
    try:
        candidate.relative_to(root)
    except ValueError:
        raise SystemExit(f"{field} escapes the asset run: {raw_path!r}") from None
    if candidate == root:
        raise SystemExit(f"{field} must name a file below the asset run")

    if allowed_roots:
        allowed = []
        for raw_root in allowed_roots:
            relative_root = Path(raw_root)
            if relative_root.is_absolute() or ".." in relative_root.parts:
                raise ValueError(f"invalid allowed run root: {raw_root!r}")
            allowed.append((root / relative_root).resolve())
        if not any(_is_below(candidate, allowed_root) for allowed_root in allowed):
            expected = ", ".join(f"{value.rstrip('/')}/" for value in allowed_roots)
            raise SystemExit(f"{field} must stay below one of: {expected}")
    return candidate


def _is_below(candidate: Path, root: Path) -> bool:
    try:
        candidate.relative_to(root)
    except ValueError:
        return False
    return candidate != root


def resolve_run_mutation_path(
    run_dir: Path,
    raw_path: str,
    *,
    field: str,
    allowed_roots: tuple[str, ...] = (),
) -> Path:
    """Resolve a mutation target and reject every symlink component."""
    candidate = resolve_run_path(
        run_dir,
        raw_path,
        field=field,
        allowed_roots=allowed_roots,
    )
    root = run_dir.expanduser().resolve()
    cursor = root
    for part in Path(raw_path).parts:
        cursor /= part
        if cursor.is_symlink():
            raise SystemExit(f"{field} must not use a symlink path: {raw_path!r}")
    return candidate


def resolve_run_output_path(
    run_dir: Path,
    raw_path: str,
    *,
    field: str,
    allowed_roots: tuple[str, ...] = (),
    force: bool = False,
) -> Path:
    """Resolve a contained non-symlink output and enforce its overwrite gate."""
    candidate = resolve_run_mutation_path(
        run_dir,
        raw_path,
        field=field,
        allowed_roots=allowed_roots,
    )
    if candidate.exists():
        if candidate.is_dir():
            raise SystemExit(f"{field} must be a file path: {candidate}")
        if not force:
            raise SystemExit(f"{field} already exists; pass --force to replace it: {candidate}")
    return candidate


def create_staging_path(target: Path, *, mode: int | None = None) -> Path:
    """Create a same-directory staging file for a fully formed output."""
    target.parent.mkdir(parents=True, exist_ok=True)
    fd, raw_path = tempfile.mkstemp(
        prefix=f".{target.name}.",
        suffix=".tmp",
        dir=target.parent,
    )
    os.close(fd)
    staged = Path(raw_path)
    if mode is None:
        current_umask = os.umask(0)
        os.umask(current_umask)
        mode = 0o666 & ~current_umask
    staged.chmod(mode)
    return staged


def commit_staged_path(staged: Path, target: Path, *, force: bool) -> None:
    """Commit a staged file atomically, without following an output symlink."""
    if staged.parent != target.parent:
        raise ValueError("staged output must share the target directory")
    if force:
        if target.is_file() and not target.is_symlink():
            staged.chmod(stat.S_IMODE(target.stat().st_mode))
        os.replace(staged, target)
        return
    try:
        os.link(staged, target)
    except FileExistsError:
        raise SystemExit(f"refusing to overwrite existing output: {target}") from None
    else:
        staged.unlink()


def atomic_write_bytes(
    target: Path,
    payload: bytes,
    *,
    force: bool,
    mode: int | None = None,
) -> None:
    """Write complete bytes through a same-directory staging file."""
    staged = create_staging_path(target, mode=mode)
    try:
        with staged.open("wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        commit_staged_path(staged, target, force=force)
    finally:
        staged.unlink(missing_ok=True)


def atomic_write_text(target: Path, content: str, *, force: bool) -> None:
    atomic_write_bytes(target, content.encode("utf-8"), force=force)


def write_run_marker(
    run_dir: Path,
    *,
    asset_id: str,
    declared_run_dir: Path | None = None,
) -> Path:
    """Mark a newly-created directory as owned by this workflow."""
    root = run_dir.expanduser().resolve()
    declared_root = (
        declared_run_dir.expanduser().resolve()
        if declared_run_dir is not None
        else root
    )
    marker = root / RUN_MARKER_NAME
    marker.write_text(
        json.dumps(
            {
                "kind": RUN_MARKER_KIND,
                "version": RUN_MARKER_VERSION,
                "run_dir": str(declared_root),
                "asset_id": asset_id,
                "created_at": datetime.now(timezone.utc).isoformat(),
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return marker


def require_safe_managed_replacement(run_dir: Path) -> None:
    """Refuse recursive deletion unless ``run_dir`` is a marked workflow directory."""
    root = run_dir.expanduser().resolve()
    cwd = Path.cwd().resolve()
    home = Path.home().resolve()
    protected = {Path("/").resolve(), home, cwd, *home.parents, *cwd.parents}
    if root in protected:
        raise SystemExit(f"refusing to replace protected directory: {root}")
    if not root.is_dir():
        raise SystemExit(f"refusing to replace non-directory path: {root}")

    marker = root / RUN_MARKER_NAME
    if marker.is_symlink() or not marker.is_file():
        raise SystemExit(
            f"refusing to replace unmarked directory: {root}; expected {RUN_MARKER_NAME}"
        )
    try:
        data = json.loads(marker.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"refusing to replace directory with invalid run marker: {exc}") from None

    if not isinstance(data, dict):
        raise SystemExit("refusing to replace directory with invalid run marker")
    if data.get("kind") != RUN_MARKER_KIND or data.get("version") != RUN_MARKER_VERSION:
        raise SystemExit("refusing to replace directory with unrecognized run marker")
    marker_root = data.get("run_dir")
    if not isinstance(marker_root, str) or Path(marker_root).expanduser().resolve() != root:
        raise SystemExit("refusing to replace directory whose run marker path does not match")
