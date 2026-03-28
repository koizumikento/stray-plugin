# Repository Guidance

This repository manages a repo-local Codex plugin. Keep this file short and use it as a map. If repo-specific guidance grows, move the detail into `docs/` and link to it from here.

## Repository Map

- Marketplace file: `.agents/plugins/marketplace.json`
- Canonical plugin root: `plugins/stray-plugin/`
- Plugin manifest: `plugins/stray-plugin/.codex-plugin/plugin.json`
- Plugin skills: `plugins/stray-plugin/skills/`
- Existing skill authoring helper: `plugins/stray-plugin/skills/agent-skill-creater/`

## Working Rules

- Treat `plugins/stray-plugin/` as the only plugin in this repository unless the user explicitly asks for more.
- Do not add `-local` suffixes to marketplace or plugin names unless explicitly requested.
- Keep changes repo-local and versioned. Do not rely on undocumented external context as the source of truth.
- Put new skills under `plugins/stray-plugin/skills/<skill-name>/`.
- Preserve user-requested skill names unless asked to normalize them.
- When adding or materially broadening user-facing skills, review `plugins/stray-plugin/.codex-plugin/plugin.json` and update `interface.longDescription` or `interface.defaultPrompt` if discovery would otherwise lag behind the actual skill set.

## Skill Authoring Rules

- Keep each skill focused on one job.
- Prefer instruction-first skills. Add `scripts/` only when deterministic execution is necessary.
- Add `references/` only when the material is too large or too specialized for `SKILL.md`.
- Add `agents/openai.yaml` only when the skill needs display metadata, tool dependencies, or invocation policy changes.
- Write a frontmatter `name` and a trigger-oriented `description` that says when the skill should and should not be used.
- Keep workflows imperative and numbered.
- State outputs, assumptions, and guardrails explicitly.

## Validation

- Validate JSON after editing plugin manifests or marketplace files.
- Minimal JSON validation command:
  `python3 - <<'PY'
import json
json.load(open('.agents/plugins/marketplace.json'))
json.load(open('plugins/stray-plugin/.codex-plugin/plugin.json'))
print('json-ok')
PY`
- Confirm any new skill is placed under `plugins/stray-plugin/skills/` and not inside `.codex-plugin/`.
- When a new skill changes the practical surface area of the plugin, confirm whether `plugin.json` discovery text still matches the current skill set.

## Nested Guidance

- If a subdirectory grows its own workflow or constraints, add a nearer `AGENTS.md` there instead of expanding this file indefinitely.
- The closest `AGENTS.md` to the changed files should carry the most specific instructions.
