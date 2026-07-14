from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest
from PIL import Image

SKILL_DIR = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = SKILL_DIR / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import _run_safety as run_safety  # noqa: E402
from _run_safety import RUN_MARKER_NAME, resolve_run_path  # noqa: E402
from generate_asset_images import (  # noqa: E402
    RejectRedirects,
    response_relative_path,
    write_exclusive,
)


def run_script(name: str, *args: object, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    command = [sys.executable, str(SCRIPTS_DIR / name), *(str(arg) for arg in args)]
    child_env = os.environ.copy()
    if env:
        child_env.update(env)
    return subprocess.run(command, capture_output=True, text=True, env=child_env, check=False)


def prepare_run(tmp_path: Path, name: str = "run") -> Path:
    run_dir = tmp_path / name
    result = run_script(
        "prepare_asset_run.py",
        "--asset-name",
        "Safety Test",
        "--output-dir",
        run_dir,
    )
    assert result.returncode == 0, result.stderr
    return run_dir


def load_manifest(run_dir: Path) -> dict[str, object]:
    return json.loads((run_dir / "imagegen-jobs.json").read_text(encoding="utf-8"))


def write_manifest(run_dir: Path, manifest: dict[str, object]) -> None:
    (run_dir / "imagegen-jobs.json").write_text(
        json.dumps(manifest, indent=2) + "\n",
        encoding="utf-8",
    )


def first_job(manifest: dict[str, object]) -> dict[str, object]:
    jobs = manifest["jobs"]
    assert isinstance(jobs, list) and isinstance(jobs[0], dict)
    return jobs[0]


def test_resolve_run_path_rejects_traversal_absolute_and_symlink_escape(tmp_path: Path) -> None:
    run_dir = tmp_path / "run"
    run_dir.mkdir()
    (run_dir / "decoded").mkdir()

    assert resolve_run_path(
        run_dir,
        "decoded/output.png",
        field="output",
        allowed_roots=("decoded",),
    ) == run_dir / "decoded" / "output.png"

    with pytest.raises(SystemExit, match="parent traversal"):
        resolve_run_path(run_dir, "../outside.png", field="output")
    with pytest.raises(SystemExit, match="must be relative"):
        resolve_run_path(run_dir, str(tmp_path / "outside.png"), field="output")
    with pytest.raises(SystemExit, match="must stay below"):
        resolve_run_path(
            run_dir,
            "imagegen-jobs.json",
            field="job output",
            allowed_roots=("decoded",),
        )

    outside = tmp_path / "outside"
    outside.mkdir()
    (run_dir / "decoded" / "link").symlink_to(outside, target_is_directory=True)
    with pytest.raises(SystemExit, match="escapes the asset run"):
        resolve_run_path(
            run_dir,
            "decoded/link/stolen.png",
            field="output",
            allowed_roots=("decoded",),
        )


def test_force_replacement_requires_matching_run_marker(tmp_path: Path) -> None:
    victim = tmp_path / "victim"
    victim.mkdir()
    keep = victim / "keep.txt"
    keep.write_text("keep", encoding="utf-8")

    refused = run_script(
        "prepare_asset_run.py",
        "--asset-name",
        "Safety Test",
        "--output-dir",
        victim,
        "--force",
    )
    assert refused.returncode != 0
    assert "unmarked directory" in refused.stderr
    assert keep.read_text(encoding="utf-8") == "keep"

    run_dir = prepare_run(tmp_path, "managed")
    stale = run_dir / "stale.txt"
    stale.write_text("old", encoding="utf-8")
    replaced = run_script(
        "prepare_asset_run.py",
        "--asset-name",
        "Safety Test",
        "--output-dir",
        run_dir,
        "--force",
    )
    assert replaced.returncode == 0, replaced.stderr
    assert not stale.exists()
    assert (run_dir / RUN_MARKER_NAME).is_file()


def test_prepare_rejects_non_image_reference(tmp_path: Path) -> None:
    secret = tmp_path / "secret.png"
    secret.write_text("not actually an image", encoding="utf-8")

    result = run_script(
        "prepare_asset_run.py",
        "--asset-name",
        "Safety Test",
        "--output-dir",
        tmp_path / "run",
        "--reference",
        secret,
    )

    assert result.returncode != 0
    assert "not a valid supported image" in result.stderr
    assert not (tmp_path / "run").exists()


def test_prepare_rejects_duplicate_reference_content(tmp_path: Path) -> None:
    source = tmp_path / "source.png"
    Image.new("RGBA", (4, 4), "red").save(source)

    result = run_script(
        "prepare_asset_run.py",
        "--asset-name",
        "Safety Test",
        "--output-dir",
        tmp_path / "run",
        "--reference",
        source,
        "--reference",
        source,
    )

    assert result.returncode != 0
    assert "duplicate reference image content" in result.stderr
    assert not (tmp_path / "run").exists()


def test_repair_job_cannot_target_control_files(tmp_path: Path) -> None:
    run_dir = prepare_run(tmp_path)
    manifest_path = run_dir / "imagegen-jobs.json"
    manifest = load_manifest(run_dir)
    first_job(manifest)["output_path"] = "imagegen-jobs.json"
    write_manifest(run_dir, manifest)
    before = manifest_path.read_bytes()

    result = run_script("queue_asset_repairs.py", "--run-dir", run_dir)

    assert result.returncode != 0
    assert "must stay below one of: decoded/" in result.stderr
    assert manifest_path.read_bytes() == before


def test_record_result_cannot_write_outside_run(tmp_path: Path) -> None:
    run_dir = prepare_run(tmp_path)
    manifest = load_manifest(run_dir)
    first_job(manifest)["output_path"] = "../escaped.png"
    write_manifest(run_dir, manifest)
    source = tmp_path / "source.png"
    Image.new("RGBA", (2, 2), (255, 0, 0, 255)).save(source)

    result = run_script(
        "record_imagegen_result.py",
        "--run-dir",
        run_dir,
        "--job-id",
        "base",
        "--source",
        source,
    )

    assert result.returncode != 0
    assert "parent traversal" in result.stderr
    assert not (tmp_path / "escaped.png").exists()


def test_direct_api_rejects_control_file_upload_before_network(tmp_path: Path) -> None:
    run_dir = prepare_run(tmp_path)
    manifest = load_manifest(run_dir)
    job = first_job(manifest)
    job["input_images"] = [{"path": "asset_request.json", "role": "malicious"}]
    write_manifest(run_dir, manifest)

    result = run_script(
        "generate_asset_images.py",
        "--run-dir",
        run_dir,
        "--confirm-direct-api",
        env={"OPENAI_API_KEY": "test-key-never-sent"},
    )

    assert result.returncode != 0
    assert "must stay below one of: references/" in result.stderr
    assert not (run_dir / "raw").exists()


def test_direct_api_rejects_disguised_non_image_before_network(tmp_path: Path) -> None:
    run_dir = prepare_run(tmp_path)
    disguised = run_dir / "references" / "secret.png"
    disguised.write_text("not actually an image", encoding="utf-8")
    manifest = load_manifest(run_dir)
    first_job(manifest)["input_images"] = [{"path": "references/secret.png"}]
    write_manifest(run_dir, manifest)

    result = run_script(
        "generate_asset_images.py",
        "--run-dir",
        run_dir,
        "--confirm-direct-api",
        env={"OPENAI_API_KEY": "test-key-never-sent"},
    )

    assert result.returncode != 0
    assert "not a valid supported image" in result.stderr
    assert not (run_dir / "raw").exists()


def test_direct_api_rejects_reference_changed_after_preparation(tmp_path: Path) -> None:
    source = tmp_path / "source.png"
    Image.new("RGBA", (4, 4), "red").save(source)
    run_dir = tmp_path / "run"
    prepared = run_script(
        "prepare_asset_run.py",
        "--asset-name",
        "Safety Test",
        "--output-dir",
        run_dir,
        "--reference",
        source,
    )
    assert prepared.returncode == 0, prepared.stderr
    request = json.loads((run_dir / "asset_request.json").read_text(encoding="utf-8"))
    reference = request["references"][0]
    assert len(reference["sha256"]) == 64
    copied = run_dir / reference["path"]
    Image.new("RGBA", (4, 4), "blue").save(copied)

    result = run_script(
        "generate_asset_images.py",
        "--run-dir",
        run_dir,
        "--confirm-direct-api",
        env={"OPENAI_API_KEY": "test-key-never-sent"},
    )

    assert result.returncode != 0
    assert "no longer matches its prepared sha256" in result.stderr
    assert not (run_dir / "raw").exists()


def test_direct_api_rejects_excessive_input_count_before_network(tmp_path: Path) -> None:
    source = tmp_path / "source.png"
    Image.new("RGBA", (4, 4), "red").save(source)
    run_dir = tmp_path / "run"
    prepared = run_script(
        "prepare_asset_run.py",
        "--asset-name",
        "Safety Test",
        "--output-dir",
        run_dir,
        "--reference",
        source,
    )
    assert prepared.returncode == 0, prepared.stderr
    manifest = load_manifest(run_dir)
    entry = first_job(manifest)["input_images"][0]
    first_job(manifest)["input_images"] = [entry] * 9
    write_manifest(run_dir, manifest)

    result = run_script(
        "generate_asset_images.py",
        "--run-dir",
        run_dir,
        "--confirm-direct-api",
        env={"OPENAI_API_KEY": "test-key-never-sent"},
    )

    assert result.returncode != 0
    assert "at most 8 input images" in result.stderr
    assert not (run_dir / "raw").exists()


def test_direct_api_requires_explicit_confirmation_and_never_uses_curl_argv(tmp_path: Path) -> None:
    run_dir = prepare_run(tmp_path)
    result = run_script("generate_asset_images.py", "--run-dir", run_dir)
    source = (SCRIPTS_DIR / "generate_asset_images.py").read_text(encoding="utf-8")

    assert result.returncode != 0
    assert "--confirm-direct-api" in result.stderr
    assert "import subprocess" not in source
    assert '"curl"' not in source


def test_direct_api_redirects_are_rejected() -> None:
    assert RejectRedirects().redirect_request(None, None, 302, "Found", {}, "https://example.com") is None


def test_direct_api_refuses_existing_output_before_network(tmp_path: Path) -> None:
    run_dir = prepare_run(tmp_path)
    output = run_dir / "decoded" / "base.png"
    output.write_bytes(b"existing-output")

    result = run_script(
        "generate_asset_images.py",
        "--run-dir",
        run_dir,
        "--confirm-direct-api",
        env={"OPENAI_API_KEY": "test-key-never-sent"},
    )

    assert result.returncode != 0
    assert "refusing to overwrite existing decoded image" in result.stderr
    assert output.read_bytes() == b"existing-output"
    assert not (run_dir / "raw").exists()


def test_direct_api_preserves_each_repair_response(tmp_path: Path) -> None:
    assert response_relative_path({"id": "base"}) == "raw/base.response.json"
    assert (
        response_relative_path({"id": "base", "repair_attempt": 2})
        == "raw/base.repair-02.response.json"
    )

    response = tmp_path / "base.response.json"
    write_exclusive(response, b"first", field="Image API response")
    with pytest.raises(SystemExit, match="refusing to overwrite"):
        write_exclusive(response, b"second", field="Image API response")
    assert response.read_bytes() == b"first"


def test_direct_api_response_is_private_before_publish(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    observed_modes: list[int] = []
    original_commit = run_safety.commit_staged_path

    def inspect_commit(staged: Path, target: Path, *, force: bool) -> None:
        observed_modes.append(staged.stat().st_mode & 0o777)
        original_commit(staged, target, force=force)

    monkeypatch.setattr(run_safety, "commit_staged_path", inspect_commit)
    response = tmp_path / "base.response.json"
    write_exclusive(response, b"private", field="Image API response")

    assert observed_modes == [0o600]
    assert response.stat().st_mode & 0o777 == 0o600


def test_repair_limit_preserves_third_attempt_output(tmp_path: Path) -> None:
    run_dir = prepare_run(tmp_path)
    output = run_dir / "decoded" / "base.png"
    output.write_bytes(b"third-attempt-result")
    manifest = load_manifest(run_dir)
    job = first_job(manifest)
    job["status"] = "complete"
    job["repair_attempt"] = 3
    write_manifest(run_dir, manifest)
    before = (run_dir / "imagegen-jobs.json").read_bytes()

    result = run_script("queue_asset_repairs.py", "--run-dir", run_dir)

    assert result.returncode != 0
    assert "reached the 3-attempt repair limit" in result.stderr
    assert output.read_bytes() == b"third-attempt-result"
    assert (run_dir / "imagegen-jobs.json").read_bytes() == before
