---
name: "agent-skill-creater"
description: "Use when the user wants to create or update a Codex agent skill and the main work is authoring the skill itself, whether it belongs in this plugin family under `plugins/*/skills/` or in a target repository under `.agents/skills/`. Do not use for general plugin scaffolding, `.codex/agents/` subagents, or unrelated documentation work."
---

# Agent Skill Creater

Create or update Codex agent skills. Start by classifying the target surface correctly: plugin-family skill, project-scoped repo skill, or something that is not a skill at all. Default to instruction-first skills and only add scripts, references, or metadata when they materially improve reliability or usability.

## Preferred Scope

- New plugin-family skill creation under `plugins/<plugin-name>/skills/<skill-name>/`
- New project-scoped repo skill creation under `<target-repo>/.agents/skills/<skill-name>/`
- Existing skill cleanup or refactoring
- Trigger description improvements
- Optional `agents/openai.yaml` metadata when UI polish, dependency declaration, or invocation policy is needed

## Do Not Use For

- General plugin scaffolding or manifest bootstrapping
- Creating or updating `.codex/agents/*.toml` custom subagents that belong in `subagent-creator`
- Broad plugin-wide overlap audits that belong in `skill-overlap-auditor`
- Focused review-only requests that belong in `skill-reviewer`
- Test planning or validation design that belongs in `test-strategist`
- Unrelated documentation work that does not create or refine a skill artifact

## Inputs

- The target surface:
  - plugin family under `plugins/*/skills/`
  - project-scoped repo under `.agents/skills/`
- The target skill name or existing skill path
- The job the skill should own
- Trigger boundaries, including when it should not be used
- Any repo-specific constraints that must be preserved

## Assumptions

- `SKILL.md` is the required entry point for the skill
- Instruction-first packaging is preferred unless determinism or heavy reference material justifies extra files
- Strong target signals should be honored:
  - `plugins/stray-skillops/skills/`, `plugins/stray-research/skills/`, `plugins/stray-studio/skills/`, plugin manifests, marketplace files, or plugin naming imply a plugin-family skill
  - `.agents/skills/`, "repo-specific", "project-only", "このリポジトリ専用", or an application/service repository imply a project-scoped repo skill
- `.codex/agents/` or custom agent TOML requests imply a subagent, not a skill

## Workflow

1. Classify the target before writing anything:
   - plugin-family skill under `plugins/*/skills/`
   - project-scoped repo skill under `.agents/skills/`
   - custom subagent under `.codex/agents/`
   - If the user says the skill should be repository-specific or project-only, default to `.agents/skills/`, not plugin scaffolding.
   - If the target is still ambiguous after checking the repo and the user message, ask one short clarification before editing.
2. Route by target surface:
   - For a plugin-family skill, locate the plugin root by finding `.codex-plugin/plugin.json` and choose `<plugin-root>/skills/<skill-name>/`.
   - For a project-scoped repo skill, choose `<target-repo>/.agents/skills/<skill-name>/`.
   - For a custom subagent request, stop and route to `subagent-creator`.
3. Lock the storage boundary before writing:
   - plugin-family skills may touch `plugins/*/skills/` and, if needed, the matching plugin manifest
   - project-scoped repo skills may touch `.agents/skills/` in the target repo
   - project-scoped repo skills must not create or edit `.agents/plugins/marketplace.json`, `plugins/*`, or `.codex-plugin/plugin.json`
4. Define the skill boundary before writing files:
   - what the skill does
   - when it should trigger
   - when it should not trigger
5. Write `SKILL.md` with:
   - frontmatter `name`
   - frontmatter `description`
   - concise overview
   - imperative workflow steps
   - output expectations
   - guardrails
6. Default to instruction-only. Add `scripts/` only when deterministic execution or external tooling is required.
7. Add `references/` only for material that is too large or too specialized to keep in `SKILL.md`.
8. Add `agents/openai.yaml` only when at least one of these is true:
   - the skill needs user-facing branding or starter prompts
   - the skill should disable implicit invocation
   - the skill depends on specific MCP tools or apps
9. Validate the placement:
   - plugin-family skills must sit under the chosen plugin's `skills/` directory, not inside `.codex-plugin/`
   - project-scoped repo skills must sit under `.agents/skills/` in the target repo
10. If a plugin-family skill is new or materially broadened, review that plugin's `.codex-plugin/plugin.json` and update `interface.longDescription` or `interface.defaultPrompt` when discovery text would otherwise lag behind reality.

## SKILL.md Rules

- Keep the skill focused on one job.
- Make the `description` explicit enough for implicit invocation.
- Prefer instructions over scripts.
- Use numbered steps for the main workflow.
- State inputs, outputs, and stop conditions.
- Put heavy detail in `references/` instead of bloating the main file.

## `agents/openai.yaml` Rules

Use `agents/openai.yaml` sparingly. Keep it small and purposeful.

- `interface`: add only useful display metadata
- `policy.allow_implicit_invocation`: set to `false` only when explicit invocation is safer
- `dependencies.tools`: declare only tools the skill genuinely relies on

## Guardrails

- Do not turn a broad domain into a single overloaded skill.
- Do not confuse project-scoped repo skills with plugin-family skills.
- Do not treat "repo-specific" or "project-only" as permission to scaffold a plugin.
- Do not create `.agents/plugins/marketplace.json`, `plugins/*`, or `.codex-plugin/plugin.json` for a project-scoped repo skill.
- Do not store a plugin-family skill under `.agents/skills/` unless the user explicitly asks for that structure.
- Do not add scripts just to restate text instructions.
- Do not leave trigger boundaries vague.
- Do not duplicate the same guidance across `SKILL.md` and `references/`.
- Do not store skills inside `.codex-plugin/`.

## Stop Conditions

- Stop if the request is actually for plugin scaffolding rather than a skill.
- Stop and route to `subagent-creator` if the request is really for `.codex/agents/` or a custom subagent.
- Stop if another existing skill already owns the job and the user only asked for review.
- Stop if the target location falls outside the plugin family under `plugins/*/skills/` or the target repo's `.agents/skills/` without explicit user instruction.

## Output

When you finish, report:

- created or updated file paths
- the chosen target surface and why
- the final trigger description
- any assumptions kept in the skill
- whether `agents/openai.yaml`, `references/`, or `scripts/` were added and why
