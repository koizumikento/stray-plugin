from __future__ import annotations

import base64
import io
import json
import os
import re
import subprocess
import sys
from pathlib import Path

import pytest
from PIL import Image

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/render_animation_preview.py"


def make_run(tmp_path: Path, *, multirow: bool = False) -> Path:
    run = tmp_path / "run"
    (run / "final").mkdir(parents=True)
    rows = 2 if multirow else 1
    sheet = dict(structure="grid" if multirow else "sprite-row", columns=2, rows=rows,
                 cell_width=4, cell_height=6, width=8, height=rows * 6, used_cells=rows * 2 - 1)
    (run / "asset_request.json").write_text(json.dumps({"sheet": sheet, "display_name": "</script><script>bad()</script>"}))
    source = Image.new("RGBA", (8, rows * 6))
    for index, color in enumerate(("red", "blue", "yellow", "green")[:rows * 2]):
        source.paste(color, ((index % 2) * 4 + 1, (index // 2) * 6 + 1,
                            (index % 2) * 4 + 3, (index // 2) * 6 + 5))
    source.save(run / "final/asset.png")
    return run


def render(run: Path, *args: object) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, str(SCRIPT), "--run-dir", str(run), *map(str, args)],
                          capture_output=True, text=True, check=False,
                          env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})


@pytest.mark.parametrize("multirow", [False, True])
def test_portable_preview_uses_manifest_and_preserves_sheet(tmp_path: Path, multirow: bool) -> None:
    run = make_run(tmp_path, multirow=multirow)
    result = render(run, "--scale", 2, *(["--force-non-row"] if multirow else []))
    assert result.returncode == 0, result.stderr
    html_path = run / "qa/previews/animation.html"
    assert json.loads(result.stdout)["html_preview"] == str(html_path)
    html = html_path.read_text(encoding="utf-8")
    config = json.loads(re.search(r"const config = (.*);", html)[1])
    assert (config["columns"], config["rows"], config["count"]) == (2, 2 if multirow else 1, 3 if multirow else 1)
    assert (config["width"], config["height"], config["duration"], config["scale"]) == (4, 6, 140, 2)
    assert "bad()" not in html and "fetch(" not in html
    with Image.open(io.BytesIO(base64.b64decode(config["image"].split(",", 1)[1]))) as embedded:
        with Image.open(run / "final/asset.png") as source:
            assert embedded.tobytes() == source.tobytes()
    with Image.open(run / "qa/previews/animation.gif") as gif:
        assert gif.n_frames == config["count"] and gif.size == (8, 12)
    assert not list(run.rglob("*.tmp"))


def test_html_overwrite_gate_preflights_gif_and_force_replaces(tmp_path: Path) -> None:
    run = make_run(tmp_path)
    html = run / "qa/previews/animation.html"
    html.parent.mkdir(parents=True)
    html.write_text("keep")
    result = render(run)
    assert result.returncode != 0 and "--force" in result.stderr
    assert html.read_text() == "keep"
    assert not (html.parent / "animation.gif").exists()
    result = render(run, "--force")
    assert result.returncode == 0, result.stderr
    assert "<html" in html.read_text(encoding="utf-8")


@pytest.mark.parametrize("target", ["../escaped.html", "qa/../../escaped.html"])
def test_html_traversal_rejected_before_writes(tmp_path: Path, target: str) -> None:
    run = make_run(tmp_path)
    result = render(run, "--html-output", target)
    assert result.returncode != 0
    assert not (run / "qa").exists() and not (tmp_path / "escaped.html").exists()


def test_html_absolute_escape_and_duplicate_output_rejected(tmp_path: Path) -> None:
    run = make_run(tmp_path)
    for target in (str(tmp_path / "escape.html"), "qa/previews/animation.gif"):
        result = render(run, "--html-output", target)
        assert result.returncode != 0
    assert not (run / "qa").exists() and not (tmp_path / "escape.html").exists()


def test_html_symlink_rejected_before_writes(tmp_path: Path) -> None:
    run = make_run(tmp_path)
    outside = tmp_path / "outside"
    outside.mkdir()
    try:
        (run / "alias").symlink_to(outside, target_is_directory=True)
    except OSError as error:
        if getattr(error, "winerror", None) == 1314:
            pytest.skip("Windows symlink privilege unavailable")
        raise
    result = render(run, "--html-output", "alias/animation.html", "--force")
    assert result.returncode != 0
    assert not list(outside.iterdir()) and not (run / "qa").exists()


@pytest.mark.parametrize("change", ["count", "dimensions", "image", "type", "duration", "scale"])
def test_invalid_contract_fails_before_writes(tmp_path: Path, change: str) -> None:
    run = make_run(tmp_path)
    request = json.loads((run / "asset_request.json").read_text())
    args = []
    if change == "count": request["sheet"]["used_cells"] = 3
    if change == "dimensions": request["sheet"]["width"] = 9
    if change == "type": request["sheet"]["cell_width"] = 4.5
    if change == "image": Image.new("RGBA", (7, 6)).save(run / "final/asset.png")
    if change == "duration": args = ["--duration", 0]
    if change == "scale": args = ["--scale", 0]
    (run / "asset_request.json").write_text(json.dumps(request))
    result = render(run, *args)
    assert result.returncode != 0
    assert not (run / "qa").exists()


def test_non_row_remains_opt_in(tmp_path: Path) -> None:
    run = make_run(tmp_path, multirow=True)
    result = render(run)
    assert result.returncode == 0 and json.loads(result.stdout)["skipped"]
    assert not (run / "qa").exists()
