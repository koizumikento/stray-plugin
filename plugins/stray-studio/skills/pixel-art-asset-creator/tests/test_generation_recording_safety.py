from __future__ import annotations

import base64
import io
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

import generate_asset_images as generate  # noqa: E402
import record_imagegen_result as record  # noqa: E402


class FakeResponse(io.BytesIO):
    def __enter__(self) -> FakeResponse:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()


class FakeOpener:
    def __init__(self, payload: bytes) -> None:
        self.payload = payload

    def open(self, request: object, timeout: int) -> FakeResponse:
        return FakeResponse(self.payload)


def write_png(path: Path, color: tuple[int, int, int, int]) -> bytes:
    path.parent.mkdir(parents=True, exist_ok=True)
    Image.new("RGBA", (3, 2), color).save(path, format="PNG")
    return path.read_bytes()


def png_bytes(color: tuple[int, int, int, int] = (255, 0, 0, 255)) -> bytes:
    buffer = io.BytesIO()
    Image.new("RGBA", (3, 2), color).save(buffer, format="PNG")
    return buffer.getvalue()


def make_run(tmp_path: Path) -> tuple[Path, Path, Path]:
    run_dir = tmp_path / "run"
    (run_dir / "decoded").mkdir(parents=True)
    (run_dir / "references").mkdir()
    manifest_path = run_dir / "imagegen-jobs.json"
    request_path = run_dir / "asset_request.json"
    manifest_path.write_text(
        json.dumps(
            {
                "jobs": [
                    {
                        "id": "base",
                        "status": "pending",
                        "depends_on": [],
                        "allow_prompt_only_generation": True,
                        "output_path": "decoded/base.png",
                    }
                ]
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    request_path.write_text('{"asset_id": "safety-test"}\n', encoding="utf-8")
    return run_dir, manifest_path, request_path


def run_record(
    run_dir: Path,
    source: Path,
    *extra: str,
) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    return subprocess.run(
        [
            sys.executable,
            str(SCRIPTS_DIR / "record_imagegen_result.py"),
            "--run-dir",
            str(run_dir),
            "--job-id",
            "base",
            "--source",
            str(source),
            *extra,
        ],
        capture_output=True,
        text=True,
        env=env,
        check=False,
    )


def assert_no_staging_files(run_dir: Path) -> None:
    assert not [path for path in run_dir.rglob(".*.tmp") if path.is_file()]


def test_api_response_limit_keeps_only_bounded_raw_evidence(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    payload = b"0123456789abcdef-should-not-be-read-as-evidence"
    monkeypatch.setattr(generate, "MAX_API_RESPONSE_BYTES", 16)
    monkeypatch.setattr(generate, "build_opener", lambda *args: FakeOpener(payload))
    evidence = tmp_path / "raw" / "base.response.json"

    with pytest.raises(SystemExit, match="response exceeds"):
        generate.post_image_request(
            url="https://api.openai.com/v1/images/generations",
            body=b"{}",
            content_type="application/json",
            output_json=evidence,
            api_key="not-a-real-key",
        )

    assert evidence.read_bytes() == payload[:16]
    assert not list(evidence.parent.glob(f".{evidence.name}.*.tmp"))


def test_invalid_api_json_is_preserved_as_raw_evidence(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    payload = b'{"data": [not-json]}'
    monkeypatch.setattr(generate, "build_opener", lambda *args: FakeOpener(payload))
    evidence = tmp_path / "raw" / "base.response.json"

    with pytest.raises(SystemExit, match="invalid JSON"):
        generate.post_image_request(
            url="https://api.openai.com/v1/images/generations",
            body=b"{}",
            content_type="application/json",
            output_json=evidence,
            api_key="not-a-real-key",
        )

    assert evidence.read_bytes() == payload
    assert evidence.stat().st_mode & 0o777 == 0o600
    assert not list(evidence.parent.glob(f".{evidence.name}.*.tmp"))


def test_api_error_labels_cannot_inject_terminal_controls(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    payload = json.dumps(
        {"error": {"type": "bad\nINJECTED", "code": "\u001b[31mred"}}
    ).encode("utf-8")
    monkeypatch.setattr(generate, "build_opener", lambda *args: FakeOpener(payload))
    evidence = tmp_path / "raw" / "base.response.json"

    with pytest.raises(SystemExit) as raised:
        generate.post_image_request(
            url="https://api.openai.com/v1/images/generations",
            body=b"{}",
            content_type="application/json",
            output_json=evidence,
            api_key="not-a-real-key",
        )

    message = str(raised.value)
    assert "INJECTED" not in message
    assert "\x1b" not in message
    assert evidence.read_bytes() == payload


def test_prompt_and_aggregate_input_limits_apply_before_request_building(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    prompt = tmp_path / "prompt.md"
    prompt.write_text("four", encoding="utf-8")
    monkeypatch.setattr(generate, "MAX_PROMPT_BYTES", 3)
    with pytest.raises(SystemExit, match="prompt exceeds"):
        generate.read_prompt_text(prompt)

    run_dir, _, request_path = make_run(tmp_path)
    reference = run_dir / "references" / "source.png"
    payload = write_png(reference, (255, 0, 0, 255))
    digest = generate.file_sha256(reference)
    request_path.write_text(
        json.dumps(
            {
                "references": [
                    {
                        "path": "references/source.png",
                        "sha256": digest,
                    }
                ]
            }
        )
        + "\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(generate, "MAX_TOTAL_INPUT_IMAGE_BYTES", len(payload) - 1)
    with pytest.raises(SystemExit, match="aggregate safety limit"):
        generate.path_list(
            run_dir,
            {
                "id": "base",
                "input_images": [{"path": "references/source.png"}],
            },
        )


def test_multipart_uses_the_exact_verified_image_snapshot(tmp_path: Path) -> None:
    run_dir, _, request_path = make_run(tmp_path)
    reference = run_dir / "references" / "source.png"
    original = write_png(reference, (255, 0, 0, 255))
    digest = generate.file_sha256(reference)
    request_path.write_text(
        json.dumps(
            {
                "references": [
                    {
                        "path": "references/source.png",
                        "sha256": digest,
                    }
                ]
            }
        )
        + "\n",
        encoding="utf-8",
    )
    snapshots = generate.path_list(
        run_dir,
        {"id": "base", "input_images": [{"path": "references/source.png"}]},
    )
    replacement = write_png(reference, (0, 0, 255, 255))
    assert replacement != original

    body, _ = generate.multipart_body(fields={"prompt": "fixture"}, image_paths=snapshots)

    assert original in body
    assert replacement not in body


def test_strict_base64_failure_never_publishes_output(tmp_path: Path) -> None:
    output = tmp_path / "decoded" / "base.png"

    with pytest.raises(SystemExit, match="invalid base64"):
        generate.decode_response({"data": [{"b64_json": "not base64***"}]}, output)

    assert not output.exists()
    assert not output.parent.exists()


def test_decoded_non_image_is_removed_before_publish(tmp_path: Path) -> None:
    output = tmp_path / "decoded" / "base.png"
    response = {
        "data": [{"b64_json": base64.b64encode(b"not an image").decode("ascii")}]
    }

    with pytest.raises(SystemExit, match="not a valid supported image"):
        generate.decode_response(response, output)

    assert not output.exists()
    assert not list(output.parent.glob(f".{output.name}.*.tmp"))


def test_verified_png_is_atomically_published(tmp_path: Path) -> None:
    output = tmp_path / "decoded" / "base.png"
    response = {
        "data": [{"b64_json": base64.b64encode(png_bytes()).decode("ascii")}]
    }

    generate.decode_response(response, output)

    with Image.open(output) as image:
        image.verify()
    assert not list(output.parent.glob(f".{output.name}.*.tmp"))


def test_generate_manifest_remains_pending_if_final_commit_fails(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    run_dir, manifest_path, _ = make_run(tmp_path)
    output = run_dir / "decoded" / "base.png"
    output_staged = generate.stage_bytes(output, png_bytes())
    final = {"jobs": [{"id": "base", "status": "complete"}]}
    manifest_staged = generate.stage_bytes(
        manifest_path,
        (json.dumps(final) + "\n").encode("utf-8"),
    )
    real_commit = generate.commit_staged_path

    def fail_manifest(staged: Path, target: Path, *, force: bool) -> None:
        if target == manifest_path:
            raise OSError("simulated manifest commit failure")
        real_commit(staged, target, force=force)

    monkeypatch.setattr(generate, "commit_staged_path", fail_manifest)
    try:
        with pytest.raises(OSError, match="simulated manifest"):
            generate.commit_generated_transaction(
                [(output_staged, output, False)],
                manifest_staged=manifest_staged,
                manifest_path=manifest_path,
            )
        assert output.read_bytes() == png_bytes()
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        assert manifest["jobs"][0]["status"] == "pending"
    finally:
        output_staged.unlink(missing_ok=True)
        manifest_staged.unlink(missing_ok=True)


def test_invalid_source_cannot_replace_any_artifact_with_force(tmp_path: Path) -> None:
    run_dir, manifest_path, request_path = make_run(tmp_path)
    output = run_dir / "decoded" / "base.png"
    canonical = run_dir / "references" / "canonical-base.png"
    output_before = write_png(output, (20, 30, 40, 255))
    canonical_before = write_png(canonical, (40, 30, 20, 255))
    manifest_before = manifest_path.read_bytes()
    request_before = request_path.read_bytes()
    source = tmp_path / "corrupt.png"
    source.write_bytes(b"not really a PNG")

    result = run_record(run_dir, source, "--force")

    assert result.returncode != 0
    assert "not a valid supported image" in result.stderr
    assert output.read_bytes() == output_before
    assert canonical.read_bytes() == canonical_before
    assert manifest_path.read_bytes() == manifest_before
    assert request_path.read_bytes() == request_before
    assert_no_staging_files(run_dir)


def test_force_rejects_symlink_output_without_touching_target(tmp_path: Path) -> None:
    run_dir, manifest_path, _ = make_run(tmp_path)
    victim = run_dir / "decoded" / "victim.png"
    victim_before = write_png(victim, (10, 20, 30, 255))
    output = run_dir / "decoded" / "base.png"
    output.symlink_to(victim.name)
    source = tmp_path / "source.png"
    write_png(source, (200, 100, 50, 255))
    manifest_before = manifest_path.read_bytes()

    result = run_record(run_dir, source, "--force")

    assert result.returncode != 0
    assert "symlink path" in result.stderr
    assert output.is_symlink()
    assert victim.read_bytes() == victim_before
    assert manifest_path.read_bytes() == manifest_before
    assert_no_staging_files(run_dir)


def test_force_rejects_symlink_canonical_before_replacing_output(tmp_path: Path) -> None:
    run_dir, manifest_path, _ = make_run(tmp_path)
    output = run_dir / "decoded" / "base.png"
    output_before = write_png(output, (10, 20, 30, 255))
    victim = run_dir / "references" / "victim.png"
    victim_before = write_png(victim, (40, 50, 60, 255))
    canonical = run_dir / "references" / "canonical-base.png"
    canonical.symlink_to(victim.name)
    source = tmp_path / "source.png"
    write_png(source, (200, 100, 50, 255))
    manifest_before = manifest_path.read_bytes()

    result = run_record(run_dir, source, "--force")

    assert result.returncode != 0
    assert "symlink path" in result.stderr
    assert output.read_bytes() == output_before
    assert canonical.is_symlink()
    assert victim.read_bytes() == victim_before
    assert manifest_path.read_bytes() == manifest_before
    assert_no_staging_files(run_dir)


def test_request_parse_failure_happens_before_any_replacement(tmp_path: Path) -> None:
    run_dir, manifest_path, request_path = make_run(tmp_path)
    output = run_dir / "decoded" / "base.png"
    output_before = write_png(output, (5, 10, 15, 255))
    source = tmp_path / "source.png"
    write_png(source, (200, 210, 220, 255))
    request_path.write_text("{not-json", encoding="utf-8")
    manifest_before = manifest_path.read_bytes()

    result = run_record(run_dir, source, "--force")

    assert result.returncode != 0
    assert output.read_bytes() == output_before
    assert manifest_path.read_bytes() == manifest_before
    assert not (run_dir / "references" / "canonical-base.png").exists()
    assert_no_staging_files(run_dir)


def test_mid_publish_failure_leaves_manifest_explicitly_recording(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    run_dir, manifest_path, _ = make_run(tmp_path)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    recording_payload = record.recording_manifest_payload(
        manifest,
        "base",
        "2026-07-14T00:00:00+00:00",
    )
    output = run_dir / "decoded" / "base.png"
    canonical = run_dir / "references" / "canonical-base.png"
    canonical_before = write_png(canonical, (1, 2, 3, 255))
    output_staged = record.stage_bytes(output, png_bytes((4, 5, 6, 255)))
    canonical_staged = record.stage_bytes(canonical, png_bytes((7, 8, 9, 255)))
    final_manifest = {"jobs": [{"id": "base", "status": "complete"}]}
    final_manifest_staged = record.stage_bytes(
        manifest_path,
        (json.dumps(final_manifest) + "\n").encode("utf-8"),
    )
    real_commit = record.commit_staged_path

    def fail_canonical(staged: Path, target: Path, *, force: bool) -> None:
        if target == canonical:
            raise OSError("simulated canonical commit failure")
        real_commit(staged, target, force=force)

    monkeypatch.setattr(record, "commit_staged_path", fail_canonical)
    try:
        with pytest.raises(OSError, match="simulated canonical"):
            record.commit_recording_transaction(
                manifest_path=manifest_path,
                recording_payload=recording_payload,
                artifacts=[
                    (output_staged, output, False),
                    (canonical_staged, canonical, True),
                ],
                final_manifest_staged=final_manifest_staged,
            )
        state = json.loads(manifest_path.read_text(encoding="utf-8"))
        assert state["jobs"][0]["status"] == "recording"
        assert output.read_bytes() == png_bytes((4, 5, 6, 255))
        assert canonical.read_bytes() == canonical_before
    finally:
        output_staged.unlink(missing_ok=True)
        canonical_staged.unlink(missing_ok=True)
        final_manifest_staged.unlink(missing_ok=True)


def test_success_updates_output_canonical_request_then_complete_manifest(tmp_path: Path) -> None:
    run_dir, manifest_path, request_path = make_run(tmp_path)
    source = tmp_path / "source.png"
    source_bytes = write_png(source, (100, 110, 120, 255))

    result = run_record(run_dir, source)

    assert result.returncode == 0, result.stderr
    assert (run_dir / "decoded" / "base.png").read_bytes() == source_bytes
    assert (run_dir / "references" / "canonical-base.png").read_bytes() == source_bytes
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    request = json.loads(request_path.read_text(encoding="utf-8"))
    assert manifest["jobs"][0]["status"] == "complete"
    assert "recording_started_at" not in manifest["jobs"][0]
    assert request["canonical_identity_reference"] == manifest["canonical_identity_reference"]
    assert_no_staging_files(run_dir)
