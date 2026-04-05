# Repository Guidance

This repository manages a repo-local Codex plugin. Keep this file short and use it as a map. If repo-specific guidance grows, move the detail into `docs/` and link to it from here.

## Repository Map

- Marketplace file: `.agents/plugins/marketplace.json`
- Skill ops plugin root: `plugins/stray-skillops/`
- Research plugin root: `plugins/stray-research/`
- Studio plugin root: `plugins/stray-studio/`
- Skill ops manifest: `plugins/stray-skillops/.codex-plugin/plugin.json`
- Research manifest: `plugins/stray-research/.codex-plugin/plugin.json`
- Studio manifest: `plugins/stray-studio/.codex-plugin/plugin.json`
- Existing skill authoring helper: `plugins/stray-skillops/skills/agent-skill-creater/`

## Working Rules

- Treat the repository as a small plugin family:
  `plugins/stray-skillops/` for skill authoring, review, eval, and subagent operations,
  `plugins/stray-research/` for research and analysis,
  `plugins/stray-studio/` for delivery and artifact production.
- Do not add `-local` suffixes to marketplace or plugin names unless explicitly requested.
- Keep changes repo-local and versioned. Do not rely on undocumented external context as the source of truth.
- Put new skills under the matching plugin root as `plugins/<plugin-name>/skills/<skill-name>/`.
- Preserve user-requested skill names unless asked to normalize them.
- When adding or materially broadening user-facing skills, review the matching plugin's `plugin.json` and update `interface.longDescription` or `interface.defaultPrompt` if discovery would otherwise lag behind the actual skill set.

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
json.load(open('plugins/stray-skillops/.codex-plugin/plugin.json'))
json.load(open('plugins/stray-research/.codex-plugin/plugin.json'))
json.load(open('plugins/stray-studio/.codex-plugin/plugin.json'))
print('json-ok')
PY`
- Confirm any new skill is placed under `plugins/*/skills/` and not inside `.codex-plugin/`.
- When a new skill changes the practical surface area of a plugin, confirm whether that plugin's `plugin.json` discovery text still matches the current skill set.

## Nested Guidance

- If a subdirectory grows its own workflow or constraints, add a nearer `AGENTS.md` there instead of expanding this file indefinitely.
- The closest `AGENTS.md` to the changed files should carry the most specific instructions.
