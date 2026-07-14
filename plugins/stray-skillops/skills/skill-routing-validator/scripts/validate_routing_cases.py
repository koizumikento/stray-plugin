#!/usr/bin/env python3
"""Validate the local skill inventory and versioned routing cases."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import yaml
from yaml.constructor import ConstructorError
from yaml.nodes import MappingNode, ScalarNode, SequenceNode
from yaml.resolver import BaseResolver


FRONTMATTER_RE = re.compile(r"\A---\r?\n(?P<body>.*?)\r?\n---\r?\n", re.DOTALL)
LOCAL_REF_RE = re.compile(
    r"(?<![\w/])(?P<path>(?:(?:\.\.?/)+)?(?:references|scripts|assets)/[^`\s)]+)"
)
MARKDOWN_LINK_RE = re.compile(r"\]\((?P<target><[^>]+>|[^)\s]+)(?:\s+[^)]*)?\)")
OPENAI_YAML_TOP_LEVEL_KEYS = {"interface", "policy", "dependencies"}
INTERFACE_REQUIRED_KEYS = {"display_name", "short_description", "default_prompt"}
INTERFACE_OPTIONAL_KEYS = {"icon_small", "icon_large", "brand_color"}
INTERFACE_KEYS = INTERFACE_REQUIRED_KEYS | INTERFACE_OPTIONAL_KEYS
POLICY_KEYS = {"allow_implicit_invocation"}
DEPENDENCY_KEYS = {"tools"}
TOOL_DEPENDENCY_REQUIRED_KEYS = {"type", "value", "description"}
TOOL_DEPENDENCY_OPTIONAL_KEYS = {"transport", "url"}
CASE_KEYS = {"id", "prompt", "expect", "reject", "reason", "no_skill"}
ROUTING_CASES_VERSION = 2
SHORT_DESCRIPTION_MIN_CHARS = 25
SHORT_DESCRIPTION_MAX_CHARS = 64
HEX_COLOR_RE = re.compile(r"^#[0-9A-Fa-f]{6}$")


class UniqueKeyLoader(yaml.SafeLoader):
    """Safe YAML loader that rejects duplicate mapping keys."""


class DuplicateJsonKeyError(ValueError):
    """Raised when a JSON object repeats a mapping key."""


def construct_unique_json_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    mapping: dict[str, object] = {}
    for key, value in pairs:
        if key in mapping:
            raise DuplicateJsonKeyError(f"found duplicate key {key!r}")
        mapping[key] = value
    return mapping


def load_unique_json(text: str) -> object:
    return json.loads(text, object_pairs_hook=construct_unique_json_object)


def construct_unique_mapping(
    loader: UniqueKeyLoader,
    node: MappingNode,
    deep: bool = False,
) -> dict[object, object]:
    loader.flatten_mapping(node)
    mapping: dict[object, object] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        try:
            duplicate = key in mapping
        except TypeError:
            raise ConstructorError(
                "while constructing a mapping",
                node.start_mark,
                "found an unhashable mapping key",
                key_node.start_mark,
            ) from None
        if duplicate:
            raise ConstructorError(
                "while constructing a mapping",
                node.start_mark,
                f"found duplicate key {key!r}",
                key_node.start_mark,
            )
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueKeyLoader.add_constructor(BaseResolver.DEFAULT_MAPPING_TAG, construct_unique_mapping)


def load_unique_yaml(text: str) -> object:
    return yaml.load(text, Loader=UniqueKeyLoader)


def unquoted_string_value_paths(node: object, path: str = "$") -> list[str]:
    """Return YAML paths whose string values use implicit or block scalar style."""
    errors: list[str] = []
    if isinstance(node, MappingNode):
        for key_node, value_node in node.value:
            key = key_node.value if isinstance(key_node, ScalarNode) else "?"
            child_path = f"{path}.{key}"
            if (
                isinstance(value_node, ScalarNode)
                and value_node.tag == "tag:yaml.org,2002:str"
                and value_node.style not in {"'", '"'}
            ):
                errors.append(child_path)
            errors.extend(unquoted_string_value_paths(value_node, child_path))
    elif isinstance(node, SequenceNode):
        for index, child in enumerate(node.value):
            errors.extend(unquoted_string_value_paths(child, f"{path}[{index}]"))
    return errors


def repo_root() -> Path:
    return Path(__file__).resolve().parents[5]


def validate_json_files(root: Path) -> list[str]:
    errors: list[str] = []
    marketplace_path = root / ".agents" / "plugins" / "marketplace.json"
    manifest_paths = sorted(root.glob("plugins/*/.codex-plugin/plugin.json"))
    loaded: dict[Path, object] = {}
    for path in [marketplace_path, *manifest_paths]:
        try:
            data = load_unique_json(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError, DuplicateJsonKeyError) as exc:
            errors.append(f"{path}: invalid JSON: {exc}")
            continue
        loaded[path] = data
        if path.name == "plugin.json":
            if not isinstance(data, dict):
                errors.append(f"{path}: top level must be an object")
                continue
            expected_name = path.parents[1].name
            if data.get("name") != expected_name:
                errors.append(f"{path}: plugin name does not match directory {expected_name!r}")
            skills_path = data.get("skills")
            if not isinstance(skills_path, str):
                errors.append(f"{path}: skills path is missing or invalid: {skills_path!r}")
                continue
            plugin_root = path.parents[1].resolve()
            resolved_skills = (plugin_root / skills_path).resolve()
            try:
                resolved_skills.relative_to(plugin_root)
            except ValueError:
                errors.append(f"{path}: skills path escapes plugin root: {skills_path!r}")
                continue
            if not resolved_skills.is_dir():
                errors.append(f"{path}: skills path is missing or invalid: {skills_path!r}")

    manifest_names = {path.parents[1].name for path in manifest_paths}
    marketplace = loaded.get(marketplace_path)
    if marketplace is not None:
        if not isinstance(marketplace, dict):
            errors.append(f"{marketplace_path}: top level must be an object")
        else:
            entries = marketplace.get("plugins")
            if not isinstance(entries, list):
                errors.append(f"{marketplace_path}: plugins must be an array")
            else:
                marketplace_names: set[str] = set()
                for index, entry in enumerate(entries, 1):
                    location = f"{marketplace_path}: plugins[{index}]"
                    if not isinstance(entry, dict):
                        errors.append(f"{location} must be an object")
                        continue
                    name = entry.get("name")
                    if not isinstance(name, str) or not name.strip():
                        errors.append(f"{location}.name must be a non-empty string")
                        continue
                    if name in marketplace_names:
                        errors.append(f"{location}: duplicate plugin name {name!r}")
                    marketplace_names.add(name)

                    source = entry.get("source")
                    if not isinstance(source, dict) or source.get("source") != "local":
                        errors.append(f"{location}.source must declare source='local'")
                        continue
                    raw_path = source.get("path")
                    if not isinstance(raw_path, str) or not raw_path.strip():
                        errors.append(f"{location}.source.path must be a non-empty string")
                        continue
                    expected_root = (root / "plugins" / name).resolve()
                    resolved_root = (root / raw_path).resolve()
                    if resolved_root != expected_root:
                        errors.append(
                            f"{location}.source.path must resolve to plugins/{name}: {raw_path!r}"
                        )

                missing = sorted(manifest_names - marketplace_names)
                stale = sorted(marketplace_names - manifest_names)
                if missing:
                    errors.append(f"{marketplace_path}: missing plugin entries: {missing}")
                if stale:
                    errors.append(f"{marketplace_path}: stale plugin entries: {stale}")
    return errors


def validate_openai_yaml(path: Path) -> list[str]:
    """Parse and validate the local agents/openai.yaml schema."""
    errors: list[str] = []
    try:
        text = path.read_text(encoding="utf-8")
        data = load_unique_yaml(text)
        node = yaml.compose(text, Loader=UniqueKeyLoader)
    except (OSError, yaml.YAMLError) as exc:
        return [f"{path}: invalid YAML: {exc}"]

    if not isinstance(data, dict):
        return [f"{path}: top level must be a mapping"]
    if node is not None:
        for value_path in unquoted_string_value_paths(node):
            errors.append(f"{path}: string value at {value_path} must be quoted")

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
        for key in sorted(INTERFACE_REQUIRED_KEYS):
            value = interface.get(key)
            if not isinstance(value, str) or not value.strip():
                errors.append(f"{path}: interface.{key} must be a non-empty string")

        short_description = interface.get("short_description")
        if isinstance(short_description, str) and short_description.strip():
            length = len(short_description.strip())
            if not SHORT_DESCRIPTION_MIN_CHARS <= length <= SHORT_DESCRIPTION_MAX_CHARS:
                errors.append(
                    f"{path}: interface.short_description has {length} chars; "
                    f"expected {SHORT_DESCRIPTION_MIN_CHARS}-{SHORT_DESCRIPTION_MAX_CHARS}"
                )

        default_prompt = interface.get("default_prompt")
        skill_name = path.parents[1].name
        skill_token = re.compile(rf"(?<![\w-])\${re.escape(skill_name)}(?![\w-])")
        if (
            isinstance(default_prompt, str)
            and default_prompt.strip()
            and not skill_token.search(default_prompt)
        ):
            errors.append(
                f"{path}: interface.default_prompt must mention its own ${skill_name} token"
            )

        for key in ["icon_small", "icon_large"]:
            if key not in interface:
                continue
            value = interface[key]
            if not isinstance(value, str) or not value.strip():
                errors.append(f"{path}: interface.{key} must be a non-empty string when present")
                continue
            skill_dir = path.parents[1].resolve()
            assets_dir = (skill_dir / "assets").resolve()
            candidate = (skill_dir / value).resolve()
            try:
                relative_asset = candidate.relative_to(assets_dir)
            except ValueError:
                errors.append(f"{path}: interface.{key} must resolve inside the skill assets directory")
                continue
            if not relative_asset.parts or not candidate.is_file():
                errors.append(f"{path}: interface.{key} asset does not exist: {value!r}")

        if "brand_color" in interface:
            brand_color = interface["brand_color"]
            if not isinstance(brand_color, str) or not HEX_COLOR_RE.fullmatch(brand_color):
                errors.append(f"{path}: interface.brand_color must be a quoted #RRGGBB value")

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
                    if isinstance(tool.get("type"), str) and tool["type"] != "mcp":
                        errors.append(f"{location}.type must be 'mcp'")
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
            manifest = load_unique_json(manifest_path.read_text(encoding="utf-8"))
            display_name = manifest["interface"]["displayName"]
        except (OSError, json.JSONDecodeError, DuplicateJsonKeyError, KeyError, TypeError) as exc:
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


def inventory_skill_paths(root: Path) -> tuple[list[Path], list[str]]:
    """Inventory every immediate skill directory, including ones missing SKILL.md."""
    errors: list[str] = []
    skill_paths: list[Path] = []
    skills_roots = sorted(root.glob("plugins/*/skills"))
    if not skills_roots:
        return [], [f"{root}: no plugin skill roots found"]

    for skills_root in skills_roots:
        try:
            entries = sorted(skills_root.iterdir())
        except OSError as exc:
            errors.append(f"{skills_root}: cannot inventory skill directories: {exc}")
            continue
        for entry in entries:
            if not entry.is_dir():
                continue
            skill_path = entry / "SKILL.md"
            if not skill_path.is_file():
                errors.append(f"{entry}: skill directory is missing SKILL.md")
                continue
            skill_paths.append(skill_path)

        direct = set(skill_paths)
        for nested in sorted(skills_root.glob("**/SKILL.md")):
            if nested not in direct and nested.parent.parent != skills_root:
                errors.append(f"{nested}: SKILL.md must be directly under a skill directory")

    return sorted(skill_paths), errors


def local_references(text: str) -> list[str]:
    """Return one-hop repo-local artifact references from a SKILL.md body."""
    references = {match.group("path") for match in LOCAL_REF_RE.finditer(text)}
    for match in MARKDOWN_LINK_RE.finditer(text):
        target = match.group("target").strip("<>").split("#", 1)[0]
        local = LOCAL_REF_RE.fullmatch(target)
        if local:
            references.add(local.group("path"))
    return sorted(references)


def validate_local_references(path: Path, text: str, root: Path) -> list[str]:
    errors: list[str] = []
    resolved_root = root.resolve()
    for relative in local_references(text):
        candidate = (path.parent / Path(relative)).resolve()
        try:
            candidate.relative_to(resolved_root)
        except ValueError:
            errors.append(f"{path}: local reference escapes repository: {relative}")
            continue
        if not candidate.exists():
            errors.append(f"{path}: missing local reference {relative}")
    return errors


def parse_skill(
    path: Path,
    max_description_chars: int,
    root: Path,
) -> tuple[str | None, list[str]]:
    errors: list[str] = []
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        return None, [f"{path}: cannot read skill: {exc}"]
    frontmatter = FRONTMATTER_RE.match(text)
    if not frontmatter:
        return None, [f"{path}: missing or malformed frontmatter"]

    try:
        metadata = load_unique_yaml(frontmatter.group("body"))
    except yaml.YAMLError as exc:
        return None, [f"{path}: invalid frontmatter YAML: {exc}"]
    if not isinstance(metadata, dict):
        return None, [f"{path}: frontmatter must be a mapping"]

    raw_name = metadata.get("name")
    if not isinstance(raw_name, str) or not raw_name.strip():
        return None, [f"{path}: missing or invalid frontmatter name"]
    name = raw_name.strip()
    if name != path.parent.name:
        errors.append(f"{path}: name {name!r} does not match directory {path.parent.name!r}")

    raw_description = metadata.get("description")
    if not isinstance(raw_description, str) or not raw_description.strip():
        errors.append(f"{path}: missing or invalid frontmatter description")
    else:
        description = raw_description.strip()
        if not re.match(r"Use (?:only )?when\b", description):
            errors.append(f"{path}: description must start with 'Use when' or 'Use only when'")
        has_boundary = "Do not use" in description or "Do not trigger" in description or description.startswith("Use only when")
        if not has_boundary:
            errors.append(f"{path}: description must include an explicit non-trigger boundary")
        if len(description) > max_description_chars:
            errors.append(
                f"{path}: description has {len(description)} chars; limit is {max_description_chars}"
            )

    errors.extend(validate_local_references(path, text, root))

    return name, errors


def string_list(
    case: dict[object, object],
    field: str,
    case_id: str,
    errors: list[str],
    *,
    allow_empty: bool,
) -> list[str]:
    value = case.get(field)
    if not isinstance(value, list) or not all(
        isinstance(item, str) and item.strip() for item in value
    ):
        qualifier = "a string array" if allow_empty else "a non-empty string array"
        errors.append(f"case {case_id}: {field} must be {qualifier}")
        return []
    normalized = [item.strip() for item in value]
    if not allow_empty and not normalized:
        errors.append(f"case {case_id}: {field} must be a non-empty string array")
        return []
    duplicates = sorted({item for item in normalized if normalized.count(item) > 1})
    if duplicates:
        errors.append(f"case {case_id}: {field} must contain unique skills: {duplicates}")
    return normalized


def validate_routing_payload(
    payload: object,
    skills: set[str],
) -> tuple[list[str], dict[str, int]]:
    errors: list[str] = []
    stats = {"cases": 0, "multi_skill": 0, "no_skill": 0}
    if not isinstance(payload, dict):
        return ["routing cases: top level must be an object"], stats

    unknown_top_level = set(payload) - {"version", "cases"}
    if unknown_top_level:
        errors.append(f"routing cases: unknown top-level keys: {sorted(unknown_top_level)}")
    if payload.get("version") != ROUTING_CASES_VERSION:
        errors.append(
            f"routing cases: version must be {ROUTING_CASES_VERSION}, got {payload.get('version')!r}"
        )

    cases = payload.get("cases")
    if not isinstance(cases, list):
        errors.append("routing cases: top-level 'cases' must be an array")
        return errors, stats
    stats["cases"] = len(cases)

    ids: set[str] = set()
    positive: set[str] = set()
    rejected: set[str] = set()
    for index, case in enumerate(cases, 1):
        if not isinstance(case, dict):
            errors.append(f"case {index}: must be an object")
            continue
        case_id = case.get("id")
        if not isinstance(case_id, str) or not case_id.strip():
            case_id = f"index-{index}"
            errors.append(f"case {case_id}: missing non-empty id")
        else:
            case_id = case_id.strip()
            if case_id in ids:
                errors.append(f"case {case_id}: duplicate id")
        ids.add(case_id)

        unknown_case_keys = set(case) - CASE_KEYS
        if unknown_case_keys:
            errors.append(f"case {case_id}: unknown keys: {sorted(unknown_case_keys)}")

        prompt = case.get("prompt")
        reason = case.get("reason")
        if not isinstance(prompt, str) or not prompt.strip():
            errors.append(f"case {case_id}: prompt must be non-empty")
        if not isinstance(reason, str) or not reason.strip():
            errors.append(f"case {case_id}: reason must be non-empty")

        no_skill_raw = case.get("no_skill", False)
        if not isinstance(no_skill_raw, bool):
            errors.append(f"case {case_id}: no_skill must be a boolean when present")
            no_skill = False
        else:
            no_skill = no_skill_raw

        expected = string_list(
            case,
            "expect",
            case_id,
            errors,
            allow_empty=True,
        )
        reject = string_list(
            case,
            "reject",
            case_id,
            errors,
            allow_empty=False,
        )

        if no_skill:
            stats["no_skill"] += 1
            if expected:
                errors.append(f"case {case_id}: no_skill=true requires an empty ordered expect array")
        elif not expected:
            errors.append(
                f"case {case_id}: empty expect requires no_skill=true; otherwise list skills in handoff order"
            )
        elif len(expected) > 1:
            stats["multi_skill"] += 1

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
    return errors, stats


def main() -> int:
    default_cases = Path(__file__).resolve().parents[1] / "references" / "routing-cases.json"
    parser = argparse.ArgumentParser()
    parser.add_argument("--cases", type=Path, default=default_cases)
    parser.add_argument("--max-description-chars", type=int, default=300)
    args = parser.parse_args()

    root = repo_root()
    skill_paths, inventory_errors = inventory_skill_paths(root)
    errors: list[str] = [*validate_json_files(root), *inventory_errors]
    for metadata_path in sorted(root.glob("plugins/*/skills/*/agents/openai.yaml")):
        errors.extend(validate_openai_yaml(metadata_path))
    skills: set[str] = set()
    skills_by_plugin: dict[str, set[str]] = {}
    for path in skill_paths:
        name, skill_errors = parse_skill(path, args.max_description_chars, root)
        errors.extend(skill_errors)
        if name:
            if name in skills:
                errors.append(f"duplicate skill name: {name}")
            skills.add(name)
            skills_by_plugin.setdefault(path.parents[2].name, set()).add(name)

    try:
        payload = load_unique_json(args.cases.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError, DuplicateJsonKeyError) as exc:
        print(f"{args.cases}: cannot load routing cases: {exc}", file=sys.stderr)
        print("routing-cases-failed structural=failed runtime=not-run errors=1", file=sys.stderr)
        return 1

    case_errors, stats = validate_routing_payload(payload, skills)
    errors.extend(case_errors)

    errors.extend(validate_readme_inventory(root, skills_by_plugin))

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        print(
            f"routing-cases-failed structural=failed runtime=not-run errors={len(errors)}",
            file=sys.stderr,
        )
        return 1

    print(
        "routing-cases-ok "
        f"structural=passed runtime=not-run skills={len(skills)} "
        f"cases={stats['cases']} multi_skill={stats['multi_skill']} no_skill={stats['no_skill']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
