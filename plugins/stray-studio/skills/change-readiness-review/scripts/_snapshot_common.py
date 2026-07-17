from __future__ import annotations

import hashlib
import json
import os
import re
import stat
import subprocess
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any


_ARTIFACT_NAME_RE = re.compile(r"[a-z0-9][a-z0-9_-]{0,63}")
_EXTENSION_RE = re.compile(r"[a-z0-9]{1,12}")


class CaptureError(Exception):
    """A concise state-capture failure that is safe to report."""


def canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=True,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("ascii")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def seal_state(state: Mapping[str, Any], *, domain: str) -> dict[str, Any]:
    sealed = dict(state)
    hasher = hashlib.sha256()
    hasher.update(domain.encode("ascii"))
    hasher.update(b"\0")
    hasher.update(canonical_json_bytes(sealed))
    sealed["snapshot_sha256"] = hasher.hexdigest()
    return sealed


def command_environment() -> dict[str, str]:
    environment = os.environ.copy()
    environment["GIT_OPTIONAL_LOCKS"] = "0"
    environment["GIT_PAGER"] = "cat"
    environment["GH_PAGER"] = "cat"
    environment["LC_ALL"] = "C"
    return environment


def run_result(
    command: Sequence[str],
    *,
    cwd: Path | None = None,
    input_bytes: bytes | None = None,
) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        list(command),
        cwd=cwd,
        input=input_bytes,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=command_environment(),
    )


def one_line(raw: bytes, *, limit: int = 500) -> str:
    text = " ".join(
        part.strip()
        for part in raw.decode("utf-8", "backslashreplace").splitlines()
        if part.strip()
    )
    if not text:
        return "command failed without an error message"
    return text if len(text) <= limit else f"{text[: limit - 3]}..."


def run_checked(
    command: Sequence[str],
    *,
    cwd: Path | None = None,
    input_bytes: bytes | None = None,
    label: str | None = None,
) -> bytes:
    result = run_result(command, cwd=cwd, input_bytes=input_bytes)
    if result.returncode != 0:
        raise CaptureError(f"{label or command[0]} failed: {one_line(result.stderr)}")
    return result.stdout


def _is_relative_to(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
    except ValueError:
        return False
    return True


def _artifact_root(
    root_argument: str,
    *,
    forbidden_roots: Sequence[Path],
) -> Path:
    raw_root = Path(root_argument).expanduser()
    try:
        metadata = raw_root.lstat()
    except OSError as error:
        raise CaptureError(f"cannot inspect --snapshot-dir: {error}") from error
    if stat.S_ISLNK(metadata.st_mode):
        raise CaptureError("--snapshot-dir must not be a symlink")
    if not stat.S_ISDIR(metadata.st_mode):
        raise CaptureError("--snapshot-dir must be an existing directory")

    root = raw_root.resolve(strict=True)
    for forbidden in forbidden_roots:
        resolved = forbidden.resolve(strict=True)
        if root == resolved or _is_relative_to(root, resolved):
            raise CaptureError(
                f"--snapshot-dir must be outside the protected root: {resolved}"
            )
    return root


def write_artifact_set(
    snapshot_dir: str,
    name: str,
    payloads: Mapping[str, bytes],
    *,
    forbidden_roots: Sequence[Path],
) -> dict[str, str]:
    if not _ARTIFACT_NAME_RE.fullmatch(name):
        raise CaptureError(
            "--name must contain only lowercase letters, digits, underscores, or hyphens"
        )
    if not payloads:
        raise CaptureError("at least one artifact payload is required")

    root = _artifact_root(snapshot_dir, forbidden_roots=forbidden_roots)
    targets: dict[str, Path] = {}
    for extension in payloads:
        if not _EXTENSION_RE.fullmatch(extension):
            raise CaptureError(f"invalid artifact extension: {extension!r}")
        target = root / f"{name}.{extension}"
        if target.parent.resolve(strict=True) != root:
            raise CaptureError("artifact path escapes --snapshot-dir")
        try:
            target.lstat()
        except FileNotFoundError:
            pass
        except OSError as error:
            raise CaptureError(f"cannot inspect artifact target: {error}") from error
        else:
            raise CaptureError(
                f"refusing to overwrite existing artifact: {target.name}"
            )
        targets[extension] = target

    created: list[Path] = []
    try:
        for extension, target in targets.items():
            flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
            if hasattr(os, "O_CLOEXEC"):
                flags |= os.O_CLOEXEC
            if hasattr(os, "O_NOFOLLOW"):
                flags |= os.O_NOFOLLOW
            descriptor = os.open(target, flags, 0o600)
            created.append(target)
            try:
                view = memoryview(payloads[extension])
                while view:
                    written = os.write(descriptor, view)
                    if written <= 0:
                        raise OSError("artifact write made no progress")
                    view = view[written:]
                os.fchmod(descriptor, 0o600)
                os.fsync(descriptor)
            finally:
                os.close(descriptor)
    except BaseException:
        for target in reversed(created):
            try:
                target.unlink()
            except FileNotFoundError:
                pass
        raise

    return {extension: str(path) for extension, path in targets.items()}
