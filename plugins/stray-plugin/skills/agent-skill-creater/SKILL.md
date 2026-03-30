---
name: "agent-skill-creater"
description: "Use when the user wants to create or update a Codex agent skill inside the current plugin, including drafting SKILL.md, optional agents/openai.yaml metadata, and any lightweight references needed for repeatable use. Do not use for general plugin scaffolding or unrelated documentation work."
---

# Agent Skill Creater

Create or update Codex agent skills inside the current plugin. Default to instruction-first skills and only add scripts, references, or metadata when they materially improve reliability or usability.

## Preferred Scope

- New skill creation under `skills/<skill-name>/`
- Existing skill cleanup or refactoring
- Trigger description improvements
- Optional `agents/openai.yaml` metadata when UI polish, dependency declaration, or invocation policy is needed

## Do Not Use For

- General plugin scaffolding or manifest bootstrapping
- Broad plugin-wide overlap audits that belong in `skill-overlap-auditor`
- Focused review-only requests that belong in `skill-reviewer`
- Test planning or validation design that belongs in `test-strategist`
- Unrelated documentation work that does not create or refine a skill artifact

## Inputs

- The target skill name or existing skill path
- The job the skill should own
- Trigger boundaries, including when it should not be used
- Any repo-specific constraints that must be preserved

## Assumptions

- The target is a repo-local skill under `plugins/stray-plugin/skills/`
- `SKILL.md` is the required entry point for the skill
- Instruction-first packaging is preferred unless determinism or heavy reference material justifies extra files

## Workflow

1. Locate the plugin root by finding `.codex-plugin/plugin.json`.
2. Choose the target skill folder under `<plugin-root>/skills/`.
3. Define the skill boundary before writing files:
   - what the skill does
   - when it should trigger
   - when it should not trigger
4. Write `SKILL.md` with:
   - frontmatter `name`
   - frontmatter `description`
   - concise overview
   - imperative workflow steps
   - output expectations
   - guardrails
5. Default to instruction-only. Add `scripts/` only when deterministic execution or external tooling is required.
6. Add `references/` only for material that is too large or too specialized to keep in `SKILL.md`.
7. Add `agents/openai.yaml` only when at least one of these is true:
   - the skill needs user-facing branding or starter prompts
   - the skill should disable implicit invocation
   - the skill depends on specific MCP tools or apps
8. Validate that the plugin manifest still points to `./skills/` and that the new skill sits at the plugin root, not inside `.codex-plugin/`.
9. If the new or materially broadened skill changes the practical surface area of the plugin, review `plugins/stray-plugin/.codex-plugin/plugin.json` and update `interface.longDescription` or `interface.defaultPrompt` when discovery text would otherwise lag behind reality.

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
- Do not add scripts just to restate text instructions.
- Do not leave trigger boundaries vague.
- Do not duplicate the same guidance across `SKILL.md` and `references/`.
- Do not store skills inside `.codex-plugin/`.

## Stop Conditions

- Stop if the request is actually for plugin scaffolding rather than a skill.
- Stop if another existing skill already owns the job and the user only asked for review.
- Stop if the target location falls outside `plugins/stray-plugin/skills/` without explicit user instruction.

## Output

When you finish, report:

- created or updated file paths
- the final trigger description
- any assumptions kept in the skill
- whether `agents/openai.yaml`, `references/`, or `scripts/` were added and why
