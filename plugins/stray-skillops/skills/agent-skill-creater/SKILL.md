---
name: "agent-skill-creater"
description: "Use when the user wants to create or update a Codex `SKILL.md` in a plugin or repo `.agents/skills/` directory. Do not use for plugin scaffolding, custom subagents, review-only audits, or routing-eval-only work."
---

# Agent Skill Creater

Create or update focused Codex agent skills. Route the request first, then write the smallest useful skill entry point. Keep this compatibility name, including the misspelling.

## Route First

1. Classify the target surface before editing:
   - plugin-family skill: `plugins/<plugin-name>/skills/<skill-name>/`
   - project-scoped repo skill: `<target-repo>/.agents/skills/<skill-name>/`
   - custom subagent: `.codex/agents/*.toml`
   - not a skill: plugin scaffolding, generic docs, tests, or app code
2. Hand off when another skill owns the request:
   - use `subagent-creator` for `.codex/agents/` custom subagents
   - use `skill-routing-validator` for trigger cases, near-miss prompts, or routing-eval maintenance
   - use `reviewer` for findings-first skill or plugin audits when no authoring is requested
3. Lock the storage boundary:
   - plugin-family skills may touch the selected plugin's `skills/` directory and, only if discoverability changes, its plugin manifest
   - project-scoped repo skills may touch only `.agents/skills/` in the target repo unless the user explicitly asks otherwise
4. Ask one short clarification if the target surface is still ambiguous after reading the repo and user request.

## Description Rules

- Start with `Use when...` and name the user intent, not the implementation detail.
- Say the one job the skill owns.
- Add `Do not use...` boundaries for the nearest likely collisions.
- Keep it concrete enough for routing; avoid broad phrases like "helps with X" unless the owned workflow is named.
- Preserve user-requested skill names unless asked to normalize them.
- Put the decisive intent and nearest collision first because descriptions may be shortened in large skill sets.
- Define at least one intended prompt and one neighboring prompt that must not select the skill.

## Progressive Disclosure

Keep `SKILL.md` short enough to route and act from. Add one-hop references only when the detail would distract from routing.

- Use `references/authoring-guide.md` for detailed authoring rules, metadata guidance, and validation checklists.
- Add `scripts/` only for deterministic work that text instructions cannot reliably express.
- Add `agents/openai.yaml` only for display metadata, invocation policy, or real tool dependencies.

## Compact `SKILL.md` Template

```markdown
---
name: "<skill-name>"
description: "Use when <specific user intent and owned job>. Do not use for <nearest non-goals or neighboring skills>."
---

# <Title>

<One short paragraph that states the skill's job and default posture.>

## Do Not Use For

- <neighboring skill or non-goal>
- <out-of-scope workflow>

## Workflow

1. <First routing or scoping action.>
2. <Gather the required context explicitly: files, docs, tools, repo guidance, or external sources to inspect before acting.>
3. <Main execution step.>
4. <Run or name the harness validation: commands, checks, scripts, review rubric, or tool result that proves the work.>
5. <If repair is needed, retry only N focused times; stop and report the failure artifact or escalation condition.>

## Output

- <Expected deliverable>
- <Important assumptions or paths touched>

## Guardrails

- <Safety or ownership boundary>
- <Stop condition>
```

## Workflow

1. Read existing repo guidance and the nearest relevant skill examples.
2. Decide the skill's owned job, trigger, non-goals, and handoffs before writing.
3. Create or update `SKILL.md` using the compact template unless the existing local style requires a small variation.
4. Move detailed guidance to `references/` instead of expanding the entry point.
5. Validate placement, frontmatter, local references, companion metadata, and any edited JSON manifests.
6. When routing behavior changed, add or update cases owned by `skill-routing-validator` and check both intended and near-miss prompts.
7. Report changed paths, target surface, final trigger description, validation evidence, and any added references, scripts, or metadata.

For detailed authoring rules, use `references/authoring-guide.md`.

## Stop Conditions

- Stop if the request is really plugin scaffolding rather than skill authoring.
- Stop and route to `subagent-creator` for custom subagents.
- Stop if the target path falls outside the selected plugin's `skills/` directory or the target repo's `.agents/skills/` without explicit instruction.
- Stop before broadening a plugin manifest unless the new or changed skill materially changes discoverability.
- Stop and route to `skill-routing-validator` when the requested deliverable is an eval set rather than a skill artifact.
