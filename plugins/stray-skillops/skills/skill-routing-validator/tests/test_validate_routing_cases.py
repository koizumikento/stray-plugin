from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "validate_routing_cases.py"
REPO_ROOT = Path(__file__).resolve().parents[5]
SPEC = importlib.util.spec_from_file_location("validate_routing_cases", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


def valid_case_payload() -> dict[str, object]:
    return {
        "version": 2,
        "cases": [
            {
                "id": "ordered",
                "prompt": "Do A, then B.",
                "expect": ["a", "b"],
                "reject": ["c"],
                "reason": "A precedes B.",
            },
            {
                "id": "single",
                "prompt": "Do C only.",
                "expect": ["c"],
                "reject": ["a", "b"],
                "reason": "C owns the request.",
            },
            {
                "id": "none",
                "prompt": "Answer a trivial question.",
                "expect": [],
                "reject": ["a"],
                "no_skill": True,
                "reason": "No specialist is needed.",
            },
        ],
    }


def write_skill(path: Path, *, reference: str = "") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    body = (
        "---\n"
        f'name: "{path.parent.name}"\n'
        'description: "Use when a focused fixture is needed. Do not use for neighboring work."\n'
        "---\n\n"
        "# Fixture\n"
    )
    if reference:
        body += f"\nLoad `{reference}`.\n"
    path.write_text(body, encoding="utf-8")


def write_openai_yaml(path: Path, *, short_description: str, default_prompt: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "interface:\n"
        '  display_name: "Fixture"\n'
        f'  short_description: "{short_description}"\n'
        f'  default_prompt: "{default_prompt}"\n',
        encoding="utf-8",
    )


def test_schema_v2_accepts_ordered_handoffs_and_explicit_no_skill() -> None:
    errors, stats = validator.validate_routing_payload(valid_case_payload(), {"a", "b", "c"})

    assert errors == []
    assert stats == {"cases": 3, "multi_skill": 1, "no_skill": 1}


def test_positive_trigger_needs_no_exclusion_but_still_requires_description(tmp_path: Path) -> None:
    skill = tmp_path / "fixture" / "SKILL.md"
    write_skill(skill)
    text = skill.read_text(encoding="utf-8").replace(" Do not use for neighboring work.", "")
    skill.write_text(text, encoding="utf-8")
    assert validator.parse_skill(skill, 300, tmp_path) == ("fixture", [])

    skill.write_text(text.replace("Use when a focused fixture is needed.", ""), encoding="utf-8")
    _, errors = validator.parse_skill(skill, 300, tmp_path)
    assert any("missing or invalid frontmatter description" in error for error in errors)


def test_schema_v2_rejects_duplicate_expectations_and_no_skill_contradictions() -> None:
    payload = valid_case_payload()
    ordered = payload["cases"][0]
    none = payload["cases"][2]
    ordered["expect"] = ["a", "a", "b"]
    none["expect"] = ["c"]

    errors, _ = validator.validate_routing_payload(payload, {"a", "b", "c"})

    assert any("expect must contain unique skills" in error for error in errors)
    assert any("no_skill=true requires an empty ordered expect array" in error for error in errors)


def test_schema_v2_requires_explicit_no_skill_and_current_version() -> None:
    payload = valid_case_payload()
    payload["version"] = 1
    none = payload["cases"][2]
    none.pop("no_skill")

    errors, _ = validator.validate_routing_payload(payload, {"a", "b", "c"})

    assert any("version must be 2" in error for error in errors)
    assert any("empty expect requires no_skill=true" in error for error in errors)


def test_inventory_reports_every_missing_or_nested_skill_entrypoint(tmp_path: Path) -> None:
    skills_root = tmp_path / "plugins" / "fixture" / "skills"
    write_skill(skills_root / "complete" / "SKILL.md")
    (skills_root / "missing").mkdir(parents=True)
    write_skill(skills_root / "nested" / "child" / "SKILL.md")

    paths, errors = validator.inventory_skill_paths(tmp_path)

    assert paths == [skills_root / "complete" / "SKILL.md"]
    assert any("missing: skill directory is missing SKILL.md" in error for error in errors)
    assert any("nested: skill directory is missing SKILL.md" in error for error in errors)
    nested_path = skills_root / "nested" / "child" / "SKILL.md"
    assert any(f"{nested_path}: SKILL.md must be directly" in error for error in errors)


def test_marketplace_must_match_plugin_manifests_and_local_paths(tmp_path: Path) -> None:
    for name in ["included", "missing"]:
        plugin_root = tmp_path / "plugins" / name
        (plugin_root / "skills").mkdir(parents=True)
        manifest = plugin_root / ".codex-plugin" / "plugin.json"
        manifest.parent.mkdir()
        manifest.write_text(
            json.dumps({"name": name, "skills": "./skills/"}) + "\n",
            encoding="utf-8",
        )

    marketplace = tmp_path / ".agents" / "plugins" / "marketplace.json"
    marketplace.parent.mkdir(parents=True)
    marketplace.write_text(
        json.dumps(
            {
                "plugins": [
                    {
                        "name": "included",
                        "source": {"source": "local", "path": "../../../outside"},
                    },
                    {
                        "name": "stale",
                        "source": {"source": "local", "path": "./plugins/stale"},
                    },
                ]
            }
        )
        + "\n",
        encoding="utf-8",
    )

    errors = validator.validate_json_files(tmp_path)

    assert any("must resolve to plugins/included" in error for error in errors)
    assert any("missing plugin entries: ['missing']" in error for error in errors)
    assert any("stale plugin entries: ['stale']" in error for error in errors)


def write_plugin_fixture(
    root: Path,
    *,
    manifest_extra: dict[str, object] | None = None,
) -> Path:
    plugin_root = root / "plugins" / "fixture"
    (plugin_root / "skills").mkdir(parents=True)
    manifest = {"name": "fixture", "skills": "./skills/", **(manifest_extra or {})}
    manifest_path = plugin_root / ".codex-plugin" / "plugin.json"
    manifest_path.parent.mkdir()
    manifest_path.write_text(json.dumps(manifest) + "\n", encoding="utf-8")
    marketplace = root / ".agents" / "plugins" / "marketplace.json"
    marketplace.parent.mkdir(parents=True)
    marketplace.write_text(
        json.dumps(
            {
                "plugins": [
                    {
                        "name": "fixture",
                        "source": {"source": "local", "path": "./plugins/fixture"},
                    }
                ]
            }
        )
        + "\n",
        encoding="utf-8",
    )
    return plugin_root


def test_plugin_mcp_servers_accepts_direct_and_wrapped_maps(tmp_path: Path) -> None:
    direct_root = tmp_path / "direct"
    direct = write_plugin_fixture(direct_root, manifest_extra={"mcpServers": "./.mcp.json"})
    (direct / "server").mkdir()
    (direct / ".mcp.json").write_text(
        json.dumps(
            {
                "local": {
                    "command": "uv",
                    "args": ["run", "server"],
                    "cwd": "./server",
                    "env": {"MODE": "readonly"},
                }
            }
        )
        + "\n",
        encoding="utf-8",
    )

    wrapped_root = tmp_path / "wrapped"
    wrapped = write_plugin_fixture(wrapped_root, manifest_extra={"mcpServers": "./mcp.json"})
    (wrapped / "mcp.json").write_text(
        json.dumps({"mcp_servers": {"remote": {"url": "https://example.test/mcp"}}}) + "\n",
        encoding="utf-8",
    )

    assert validator.validate_json_files(direct_root) == []
    assert validator.validate_json_files(wrapped_root) == []


def test_plugin_mcp_servers_rejects_escape_and_invalid_server_shape(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    plugin = write_plugin_fixture(root, manifest_extra={"mcpServers": "./.mcp.json"})
    (plugin / ".mcp.json").write_text(
        json.dumps(
            {
                "bad-local": {
                    "command": "uv",
                    "url": "http://example.test/mcp",
                    "args": "run server",
                    "cwd": "./../outside",
                },
                "bad-remote": {"url": "http://example.test/mcp", "env": {"PORT": 8000}},
            }
        )
        + "\n",
        encoding="utf-8",
    )

    errors = validator.validate_json_files(root)

    assert any("exactly one non-empty command or url" in error for error in errors)
    assert any(".args must be a string array" in error for error in errors)
    assert any(".cwd escapes plugin root" in error for error in errors)
    assert any(".url must use https://" in error for error in errors)
    assert any(".env must be a string-to-string object" in error for error in errors)

    manifest_path = plugin / ".codex-plugin" / "plugin.json"
    manifest_path.write_text(
        json.dumps({"name": "fixture", "skills": "./skills/", "mcpServers": "./../outside.json"})
        + "\n",
        encoding="utf-8",
    )
    errors = validator.validate_json_files(root)
    assert any("mcpServers path escapes plugin root" in error for error in errors)


def test_plugin_mcp_servers_rejects_duplicate_json_keys(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    plugin = write_plugin_fixture(root, manifest_extra={"mcpServers": "./.mcp.json"})
    (plugin / ".mcp.json").write_text(
        '{"local": {"command": "uv", "command": "python"}}\n',
        encoding="utf-8",
    )

    errors = validator.validate_json_files(root)

    assert any("invalid JSON" in error and "duplicate key 'command'" in error for error in errors)


def test_duplicate_yaml_keys_fail_for_metadata_and_skill_frontmatter(tmp_path: Path) -> None:
    metadata = tmp_path / "plugins" / "fixture" / "skills" / "duplicate" / "agents" / "openai.yaml"
    metadata.parent.mkdir(parents=True)
    metadata.write_text(
        "interface:\n"
        '  display_name: "One"\n'
        '  display_name: "Two"\n'
        '  short_description: "A sufficiently long fixture description."\n'
        '  default_prompt: "Use $duplicate for this fixture."\n',
        encoding="utf-8",
    )
    skill = metadata.parents[1] / "SKILL.md"
    skill.write_text(
        "---\n"
        'name: "duplicate"\n'
        'name: "duplicate-again"\n'
        'description: "Use when testing duplicates. Do not use otherwise."\n'
        "---\n",
        encoding="utf-8",
    )

    metadata_errors = validator.validate_openai_yaml(metadata)
    _, skill_errors = validator.parse_skill(skill, 300, tmp_path)

    assert any("found duplicate key 'display_name'" in error for error in metadata_errors)
    assert any("found duplicate key 'name'" in error for error in skill_errors)


def test_duplicate_json_keys_fail_for_marketplace_and_routing_payload(tmp_path: Path) -> None:
    marketplace = tmp_path / ".agents" / "plugins" / "marketplace.json"
    marketplace.parent.mkdir(parents=True)
    marketplace.write_text(
        '{"plugins": [], "plugins": [{"name": "shadowed"}]}\n',
        encoding="utf-8",
    )

    errors = validator.validate_json_files(tmp_path)

    assert any("found duplicate key 'plugins'" in error for error in errors)
    with pytest.raises(validator.DuplicateJsonKeyError, match="duplicate key 'expect'"):
        validator.load_unique_json(
            '{"version": 2, "cases": [{"expect": [], "expect": ["shadowed"]}]}'
        )


def test_broken_inline_and_markdown_one_hop_references_fail(tmp_path: Path) -> None:
    skill = tmp_path / "plugins" / "fixture" / "skills" / "broken" / "SKILL.md"
    write_skill(skill, reference="references/missing.md")
    with skill.open("a", encoding="utf-8") as handle:
        handle.write("Also load [the script](scripts/missing.py).\n")

    _, errors = validator.parse_skill(skill, 300, tmp_path)

    assert any("missing local reference references/missing.md" in error for error in errors)
    assert any("missing local reference scripts/missing.py" in error for error in errors)


def test_openai_metadata_constraints_and_quoted_values(tmp_path: Path) -> None:
    metadata = tmp_path / "plugins" / "fixture" / "skills" / "fixture" / "agents" / "openai.yaml"
    write_openai_yaml(
        metadata,
        short_description="short",
        default_prompt="Use $someone-else for this fixture.",
    )
    with metadata.open("a", encoding="utf-8") as handle:
        handle.write(
            "  icon_small: \"../outside.svg\"\n"
            "  brand_color: \"blue\"\n"
            "dependencies:\n"
            "  tools:\n"
            "    - type: \"cli\"\n"
            "      value: unquoted-cli\n"
            "      description: \"Fixture dependency.\"\n"
        )

    errors = validator.validate_openai_yaml(metadata)

    assert any("short_description has 5 chars" in error for error in errors)
    assert any("must mention its own $fixture token" in error for error in errors)
    assert any("icon_small must resolve inside" in error for error in errors)
    assert any("brand_color must be a quoted #RRGGBB" in error for error in errors)
    assert any("dependencies.tools[1].type must be 'mcp'" in error for error in errors)
    assert any("$.dependencies.tools[0].value must be quoted" in error for error in errors)


def test_openai_metadata_accepts_optional_contained_assets(tmp_path: Path) -> None:
    skill_dir = tmp_path / "plugins" / "fixture" / "skills" / "fixture"
    metadata = skill_dir / "agents" / "openai.yaml"
    icon = skill_dir / "assets" / "icon.svg"
    icon.parent.mkdir(parents=True)
    icon.write_text("<svg/>", encoding="utf-8")
    write_openai_yaml(
        metadata,
        short_description="Validate a correctly scoped fixture skill.",
        default_prompt="Use $fixture to validate this fixture.",
    )
    with metadata.open("a", encoding="utf-8") as handle:
        handle.write('  icon_small: "assets/icon.svg"\n  brand_color: "#12A0EF"\n')

    assert validator.validate_openai_yaml(metadata) == []


def test_repository_validator_reports_structural_only_runtime_status() -> None:
    result = subprocess.run(
        [sys.executable, str(SCRIPT)],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert "structural=passed runtime=not-run" in result.stdout
    assert "multi_skill=12 no_skill=8" in result.stdout
