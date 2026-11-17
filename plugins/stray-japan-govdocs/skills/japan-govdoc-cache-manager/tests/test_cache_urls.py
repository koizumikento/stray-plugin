import hashlib
import json
from pathlib import Path
import subprocess
import sys


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "validate_cache.py"


def validate(cache):
    return subprocess.run([sys.executable, str(SCRIPT), str(cache)], capture_output=True, text=True)


def test_index_requires_http_urls_in_scalar_and_array_fields(tmp_path):
    sources = tmp_path / "sources"
    sources.mkdir()
    index = sources / "whitepaper-index.json"
    record = dict(document_id="demo", title="Demo", ministry="Example", year=2026,
                  landing_page="TBD", pdf_url="file:///tmp/test", chapter_urls=["https:///chapter"],
                  data_urls=["https://[broken"])
    index.write_text(json.dumps({"records": [record]}))
    result = validate(tmp_path)
    assert result.returncode == 1
    for field in ["landing_page", "pdf_url", "chapter_urls[1]", "data_urls[1]"]:
        assert field in result.stderr

    record.update(landing_page="http://example.org", pdf_url="https://example.org/file.pdf",
                  chapter_urls=["https://example.org/章?a=1#top"], data_urls=[])
    index.write_text(json.dumps({"records": [record]}))
    assert validate(tmp_path).returncode == 0


def test_manifest_validates_provenance_urls(tmp_path):
    (tmp_path / "downloads").mkdir()
    (tmp_path / "downloads" / "demo.txt").write_bytes(b"example")
    manifest = tmp_path / "manifest.jsonl"
    record = dict(document_id="demo", title="Demo", ministry="Example", year=2026,
                  landing_page="https://example.org", source_url="https://example.org/demo",
                  local_path="downloads/demo.txt", content_type="text/plain", bytes=7,
                  sha256=hashlib.sha256(b"example").hexdigest(), fetched_at="2026-01-01", reason="test")
    manifest.write_text(json.dumps(record))
    assert validate(tmp_path).returncode == 0
    record.update(landing_page="/relative", source_url="TBD", license_or_terms_url="https://")
    manifest.write_text(json.dumps(record))
    result = validate(tmp_path)
    assert result.returncode == 1
    for field in ["landing_page", "source_url", "license_or_terms_url"]:
        assert field in result.stderr
