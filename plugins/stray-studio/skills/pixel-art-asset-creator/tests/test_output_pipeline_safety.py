from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

from PIL import Image

SKILL_DIR = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = SKILL_DIR / "scripts"


def run_script(name: str, *args: object) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    return subprocess.run(
        [sys.executable, str(SCRIPTS_DIR / name), *(str(arg) for arg in args)],
        capture_output=True,
        text=True,
        env=env,
        check=False,
    )


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def make_complete_run(tmp_path: Path) -> Path:
    run_dir = tmp_path / "run"
    decoded = run_dir / "decoded"
    decoded.mkdir(parents=True)
    request = {
        "asset_id": "output-safety",
        "display_name": "Output Safety",
        "description": "Pipeline safety fixture",
        "asset_type": "sprite",
        "target_use": "test",
        "background": {"strategy": "transparent"},
        "items": ["idle"],
        "tiles": [],
        "sheet": {
            "structure": "standalone",
            "columns": 1,
            "rows": 1,
            "cell_width": 4,
            "cell_height": 4,
            "width": 4,
            "height": 4,
            "used_cells": 1,
        },
    }
    manifest = {
        "jobs": [
            {
                "id": "base",
                "status": "complete",
                "output_path": "decoded/base.png",
            }
        ]
    }
    write_json(run_dir / "asset_request.json", request)
    write_json(run_dir / "imagegen-jobs.json", manifest)
    Image.new("RGBA", (4, 4), (255, 0, 0, 128)).save(decoded / "base.png")
    return run_dir


def test_writer_rejects_broken_intermediate_symlink_escape(tmp_path: Path) -> None:
    run_dir = make_complete_run(tmp_path)
    qa_dir = run_dir / "qa"
    qa_dir.mkdir()
    broken = qa_dir / "broken"
    broken.symlink_to(tmp_path / "outside" / "missing", target_is_directory=True)

    result = run_script(
        "make_contact_sheet.py",
        "--run-dir",
        run_dir,
        "--output",
        "qa/broken/contact-sheet.png",
    )

    assert result.returncode != 0
    assert "escapes the asset run" in result.stderr
    assert not (tmp_path / "outside").exists()


def test_force_still_refuses_final_output_symlink(tmp_path: Path) -> None:
    run_dir = make_complete_run(tmp_path)
    qa_dir = run_dir / "qa"
    qa_dir.mkdir()
    victim = qa_dir / "victim.png"
    victim.write_bytes(b"do-not-replace")
    output = qa_dir / "contact-sheet.png"
    output.symlink_to(victim.name)

    result = run_script(
        "make_contact_sheet.py",
        "--run-dir",
        run_dir,
        "--force",
    )

    assert result.returncode != 0
    assert "must not use a symlink path" in result.stderr
    assert output.is_symlink()
    assert victim.read_bytes() == b"do-not-replace"


def test_finalize_without_force_rejects_existing_output_before_writes(tmp_path: Path) -> None:
    run_dir = make_complete_run(tmp_path)
    final_dir = run_dir / "final"
    final_dir.mkdir()
    existing = final_dir / "asset.png"
    existing.write_bytes(b"existing-asset")

    result = run_script("finalize_asset_run.py", "--run-dir", run_dir)

    assert result.returncode != 0
    assert "already exists; pass --force" in result.stderr
    assert existing.read_bytes() == b"existing-asset"
    assert not (run_dir / "cells").exists()
    assert not (run_dir / "qa").exists()


def test_extract_force_replaces_cell_directory_without_stale_files(tmp_path: Path) -> None:
    run_dir = make_complete_run(tmp_path)
    cells_dir = run_dir / "cells"
    cells_dir.mkdir()
    stale = cells_dir / "stale-cell.png"
    stale.write_bytes(b"stale")

    refused = run_script("extract_sheet_cells.py", "--run-dir", run_dir)
    assert refused.returncode != 0
    assert "is not empty; pass --force" in refused.stderr
    assert stale.read_bytes() == b"stale"

    replaced = run_script(
        "extract_sheet_cells.py",
        "--run-dir",
        run_dir,
        "--force",
    )
    assert replaced.returncode == 0, replaced.stderr
    assert not stale.exists()
    assert (cells_dir / "source-normalized.png").is_file()
    assert (cells_dir / "cell-00.png").is_file()
    assert (cells_dir / "cells-manifest.json").is_file()
