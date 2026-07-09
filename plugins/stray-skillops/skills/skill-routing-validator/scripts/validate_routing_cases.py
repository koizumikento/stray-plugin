#!/usr/bin/env python3
"""Validate the local skill inventory and versioned routing cases."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import yaml


FRONTMATTER_RE = re.compile(r"\A---\r?\n(?P<body>.*?)\r?\n---\r?\n", re.DOTALL)
NAME_RE = re.compile(r'^name:\s*["\']?([^"\'\r\n]+)', re.MULTILINE)
DESCRIPTION_RE = re.compile(r'^description:\s*["\']?(.*)$', re.MULTILINE)
LOCAL_REF_RE = re.compile(r"`((?:(?:\.\./)+)?(?:references|scripts|assets)/[^`\s]+)`")
OPENAI_YAML_TOP_LEVEL_KEYS = {"interface", "policy", "dependencies"}
INTERFACE_KEYS = {"display_name", "short_description", "default_prompt"}
POLICY_KEYS = {"allow_implicit_invocation"}
DEPENDENCY_KEYS = {"tools"}
TOOL_DEPENDENCY_REQUIRED_KEYS = {"type", "value", "description"}
TOOL_DEPENDENCY_OPTIONAL_KEYS = {"transport", "url"}


def repo_root() -> Path:
    return Path(__file__).resolve().parents[5]


def validate_json_files(root: Path) -> list[str]:
    errors: list[str] = []
    paths = [root / ".agents" / "plugins" / "marketplace.json"]
    paths.extend(sorted(root.glob("plugins/*/.codex-plugin/plugin.json")))
    for path in paths:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"{path}: invalid JSON: {exc}")
            continue
        if path.name == "plugin.json":
            expected_name = path.parents[1].name
            if data.get("name") != expected_name:
                errors.append(f"{path}: plugin name does not match directory {expected_name!r}")
            skills_path = data.get("skills")
            if not isinstance(skills_path, str) or not (path.parents[1] / skills_path).is_dir():
                errors.append(f"{path}: skills path is missing or invalid: {skills_path!r}")
    return errors


def validate_openai_yaml(path: Path) -> list[str]:
    """Parse and validate the local agents/openai.yaml schema."""
    errors: list[str] = []
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        return [f"{path}: invalid YAML: {exc}"]

    if not isinstance(data, dict):
        return [f"{path}: top level must be a mapping"]

    unknown = set(data) - OPENAI_YAML_TOP_LEVEL_KEYS
    if unknown:
        errors.append(f"{path}: unknown top-level keys: {sorted(unknown)}")

    interface = data.get("interface")
    if not isinstance(interface, dict):
        errors.append(f"{path}: interface must be a mapping")
    else:
        unknown_interface = set(interface) - INTERFACE_KEYS
        if unknown_interface:
            errors.append(f"{path}: unknown interface keys: {sorted(unknown_interface)}")
        for key in sorted(INTERFACE_KEYS):
            value = interface.get(key)
            if not isinstance(value, str) or not value.strip():
                errors.append(f"{path}: interface.{key} must be a non-empty string")

    if "policy" in data:
        policy = data["policy"]
        if not isinstance(policy, dict):
            errors.append(f"{path}: policy must be a mapping")
        else:
            unknown_policy = set(policy) - POLICY_KEYS
            if unknown_policy:
                errors.append(f"{path}: unknown policy keys: {sorted(unknown_policy)}")
            if not isinstance(policy.get("allow_implicit_invocation"), bool):
                errors.append(f"{path}: policy.allow_implicit_invocation must be a boolean")

    if "dependencies" in data:
        dependencies = data["dependencies"]
        if not isinstance(dependencies, dict):
            errors.append(f"{path}: dependencies must be a mapping")
        else:
            unknown_dependencies = set(dependencies) - DEPENDENCY_KEYS
            if unknown_dependencies:
                errors.append(f"{path}: unknown dependencies keys: {sorted(unknown_dependencies)}")
            tools = dependencies.get("tools")
            if not isinstance(tools, list) or not tools:
                errors.append(f"{path}: dependencies.tools must be a non-empty array")
            else:
                allowed_tool_keys = TOOL_DEPENDENCY_REQUIRED_KEYS | TOOL_DEPENDENCY_OPTIONAL_KEYS
                for index, tool in enumerate(tools, 1):
                    location = f"{path}: dependencies.tools[{index}]"
                    if not isinstance(tool, dict):
                        errors.append(f"{location} must be a mapping")
                        continue
                    unknown_tool_keys = set(tool) - allowed_tool_keys
                    if unknown_tool_keys:
                        errors.append(f"{location} has unknown keys: {sorted(unknown_tool_keys)}")
                    for key in sorted(TOOL_DEPENDENCY_REQUIRED_KEYS):
                        value = tool.get(key)
                        if not isinstance(value, str) or not value.strip():
                            errors.append(f"{location}.{key} must be a non-empty string")
                    for key in sorted(TOOL_DEPENDENCY_OPTIONAL_KEYS):
                        if key in tool and (not isinstance(tool[key], str) or not tool[key].strip()):
                            errors.append(f"{location}.{key} must be a non-empty string when present")
                    if ("transport" in tool) != ("url" in tool):
                        errors.append(f"{location}: transport and url must be supplied together")
    return errors


def validate_readme_inventory(root: Path, skills_by_plugin: dict[str, set[str]]) -> list[str]:
    """Compare each README plugin table exactly with its skill directories."""
    errors: list[str] = []
    readme_path = root / "README.md"
    try:
        readme = readme_path.read_text(encoding="utf-8")
    except OSError as exc:
        return [f"{readme_path}: cannot read README: {exc}"]

    for plugin_name, expected in sorted(skills_by_plugin.items()):
        manifest_path = root / "plugins" / plugin_name / ".codex-plugin" / "plugin.json"
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            display_name = manifest["interface"]["displayName"]
        except (OSError, json.JSONDecodeError, KeyError, TypeError) as exc:
            errors.append(f"{manifest_path}: cannot resolve interface.displayName for README validation: {exc}")
            continue
        if not isinstance(display_name, str) or not display_name.strip():
            errors.append(f"{manifest_path}: interface.displayName must be a non-empty string")
            continue

        section_re = re.compile(
            rf"^###\s+{re.escape(display_name)}\s*\r?\n(?P<body>.*?)(?=^###\s+|^##\s+|\Z)",
            re.MULTILINE | re.DOTALL,
        )
        sections = list(section_re.finditer(readme))
        if len(sections) != 1:
            errors.append(
                f"{readme_path}: expected exactly one '### {display_name}' section; found {len(sections)}"
            )
            continue

        rows = re.findall(r"^\|\s*`([^`]+)`\s*\|", sections[0].group("body"), re.MULTILINE)
        actual = set(rows)
        duplicates = sorted({name for name in rows if rows.count(name) > 1})
        if duplicates:
            errors.append(f"{readme_path}: duplicate rows in {display_name}: {duplicates}")
        missing = sorted(expected - actual)
        stale = sorted(actual - expected)
        if missing:
            errors.append(f"{readme_path}: missing rows in {display_name}: {missing}")
        if stale:
            errors.append(f"{readme_path}: stale or misplaced rows in {display_name}: {stale}")

    return errors


def parse_skill(path: Path, max_description_chars: int) -> tuple[str | None, list[str]]:
    errors: list[str] = []
    text = path.read_text(encoding="utf-8")
    frontmatter = FRONTMATTER_RE.match(text)
    if not frontmatter:
        return None, [f"{path}: missing or malformed frontmatter"]

    body = frontmatter.group("body")
    name_match = NAME_RE.search(body)
    description_match = DESCRIPTION_RE.search(body)
    if not name_match:
        return None, [f"{path}: missing frontmatter name"]

    name = name_match.group(1).strip()
    if name != path.parent.name:
        errors.append(f"{path}: name {name!r} does not match directory {path.parent.name!r}")

    if not description_match:
        errors.append(f"{path}: missing frontmatter description")
    else:
        description = description_match.group(1).strip().strip('"\'')
        if not re.match(r"Use (?:only )?when\b", description):
            errors.append(f"{path}: description must start with 'Use when' or 'Use only when'")
        has_boundary = "Do not use" in description or "Do not trigger" in description or description.startswith("Use only when")
        if not has_boundary:
            errors.append(f"{path}: description must include an explicit non-trigger boundary")
        if len(description) > max_description_chars:
            errors.append(
                f"{path}: description has {len(description)} chars; limit is {max_description_chars}"
            )

    for relative in LOCAL_REF_RE.findall(text):
        candidate = path.parent / Path(relative)
        if not candidate.exists():
            errors.append(f"{path}: missing local reference {relative}")

    return name, errors


def string_list(case: dict, field: str, case_id: str, errors: list[str]) -> list[str]:
    value = case.get(field)
    if not isinstance(value, list) or not value or not all(isinstance(item, str) and item for item in value):
        errors.append(f"case {case_id}: {field} must be a non-empty string array")
        return []
    return value


def main() -> int:
    default_cases = Path(__file__).resolve().parents[1] / "references" / "routing-cases.json"
    parser = argparse.ArgumentParser()
    parser.add_argument("--cases", type=Path, default=default_cases)
    parser.add_argument("--max-description-chars", type=int, default=300)
    args = parser.parse_args()

    root = repo_root()
    skill_paths = sorted(root.glob("plugins/*/skills/*/SKILL.md"))
    errors: list[str] = validate_json_files(root)
    for metadata_path in sorted(root.glob("plugins/*/skills/*/agents/openai.yaml")):
        errors.extend(validate_openai_yaml(metadata_path))
    skills: set[str] = set()
    skills_by_plugin: dict[str, set[str]] = {}
    for path in skill_paths:
        name, skill_errors = parse_skill(path, args.max_description_chars)
        errors.extend(skill_errors)
        if name:
            if name in skills:
                errors.append(f"duplicate skill name: {name}")
            skills.add(name)
            skills_by_plugin.setdefault(path.parents[2].name, set()).add(name)

    try:
        payload = json.loads(args.cases.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"{args.cases}: cannot load routing cases: {exc}", file=sys.stderr)
        return 1

    cases = payload.get("cases") if isinstance(payload, dict) else None
    if not isinstance(cases, list):
        print(f"{args.cases}: top-level 'cases' must be an array", file=sys.stderr)
        return 1

    ids: set[str] = set()
    positive: set[str] = set()
    rejected: set[str] = set()
    for index, case in enumerate(cases, 1):
        if not isinstance(case, dict):
            errors.append(f"case {index}: must be an object")
            continue
        case_id = case.get("id")
        if not isinstance(case_id, str) or not case_id:
            case_id = f"index-{index}"
            errors.append(f"case {case_id}: missing non-empty id")
        elif case_id in ids:
            errors.append(f"case {case_id}: duplicate id")
        ids.add(case_id)

        prompt = case.get("prompt")
        reason = case.get("reason")
        if not isinstance(prompt, str) or not prompt.strip():
            errors.append(f"case {case_id}: prompt must be non-empty")
        if not isinstance(reason, str) or not reason.strip():
            errors.append(f"case {case_id}: reason must be non-empty")

        expected = string_list(case, "expect", case_id, errors)
        reject = string_list(case, "reject", case_id, errors)
        overlap = sorted(set(expected) & set(reject))
        if overlap:
            errors.append(f"case {case_id}: skills cannot be both expected and rejected: {overlap}")
        for name in expected + reject:
            if name not in skills:
                errors.append(f"case {case_id}: unknown skill {name!r}")
        positive.update(expected)
        rejected.update(reject)

    for name in sorted(skills - positive):
        errors.append(f"skill {name}: missing positive routing coverage")
    for name in sorted(skills - rejected):
        errors.append(f"skill {name}: missing near-miss reject coverage")

    errors.extend(validate_readme_inventory(root, skills_by_plugin))

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    print(f"routing-cases-ok skills={len(skills)} cases={len(cases)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
