---
name: "agent-skill-creater"
description: "Use when creating or updating a Codex SKILL.md in a plugin or repo .agents/skills/. Use separate skills for plugin scaffolding, custom subagents, or routing-only evaluation."
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
   - plugin-family skills may touch the selected plugin's `skills/` directory and its plugin manifest for required version bumps or discovery updates
   - project-scoped repo skills may touch only `.agents/skills/` in the target repo unless the user explicitly asks otherwise
   - include the selected skills' required routing cases, README inventory entries, version-linked metadata or test expectations, and associated validation updates in the same repository; these necessary companion changes do not require a second approval
4. Ask one short clarification if the target surface is still ambiguous after reading the repo and user request.

## Description Rules

- Start with `Use when...` and name the user intent, not the implementation detail.
- Say the one job the skill owns.
- Add a short exclusion only when the positive trigger leaves a likely collision unresolved; put detailed handoffs in the body.
- Keep it concrete enough for routing; avoid broad phrases like "helps with X" unless the owned workflow is named.
- Preserve user-requested skill names unless asked to normalize them.
- Put the decisive intent and nearest collision first because descriptions may be shortened in large skill sets.
- Define at least one intended prompt and one neighboring prompt that must not select the skill.

## Progressive Disclosure

Keep `SKILL.md` short enough to route and act from. Add one-hop references only when the detail would distract from routing.

Keep task-specific knowledge, completion evidence, and applicable safety boundaries. Delete repeated advice before moving detail to references; give each reference a loading condition. Reuse authorization for the same target and effects, continue while evidence supports progress, and stop only the blocked action when necessary input, capability, or authorization is missing.

- Use `references/authoring-guide.md` for detailed authoring rules and validation checklists.
- Use `references/execution-trust-contract.md` when a new or materially changed skill can mutate state, use credentials, incur cost, send data externally, or act on retrieved content.
- Add `scripts/` only for deterministic work that text instructions cannot reliably express.
- Do not add `agents/openai.yaml` to this plugin family. Put skill identity and routing in frontmatter, and document real tool dependencies and unavailable-tool behavior in the workflow.

## Compact `SKILL.md` Template

```markdown
---
name: "<skill-name>"
description: "Use when <specific user intent and owned job>."
---

# <Title>

<One short paragraph that states the skill's job and default posture.>

## Workflow

1. <First routing or scoping action.>
2. <Read the context needed for this task; name conditions for optional references.>
3. <Main execution step.>
4. <Define completion and collect the evidence needed for the requested result.>
5. <If repair stalls on the same failure without new evidence, reassess the approach; continue while making progress and report a blocker only when required input, authority, or execution capability is missing.>

## Output

- <Expected deliverable>
- <Important assumptions or paths touched>

## Boundaries

- <Applicable ownership, tool, trust, authorization, failure, and cleanup boundaries; omit inapplicable boilerplate.>
```

## Workflow

1. Read existing repo guidance and the nearest relevant skill examples.
2. Decide the skill's owned job, trigger, non-goals, and handoffs before writing.
3. Create or update `SKILL.md` using the compact template unless the existing local style requires a small variation.
4. For a side-effectful skill, apply `references/execution-trust-contract.md` and declare its dependencies, credentials, destinations, effects, authorization gates, outputs, failure and cleanup behavior, and untrusted-content boundary.
5. Move detailed guidance to `references/` instead of expanding the entry point.
6. For changed packaged skill content, update the containing plugin's version before final validation, using the versioning rules in `references/authoring-guide.md`. Count the change set once, respect explicit version instructions, and do not invent plugin metadata for project-scoped skills.
7. Validate placement, frontmatter, local references, absence of per-skill `agents/openai.yaml`, any edited JSON manifests, and affected version-linked checks.
8. When routing behavior changed, add or update cases owned by `skill-routing-validator` and check both intended and near-miss prompts.
9. Report changed paths, target surface, final trigger description, old and new plugin versions or why unchanged, validation evidence, and any added references, scripts, or metadata.

For detailed authoring rules, use `references/authoring-guide.md`.

## Stop Conditions

- Stop if the request is really plugin scaffolding rather than skill authoring.
- Stop and route to `subagent-creator` for custom subagents.
- Stop before unrelated changes outside the selected skills and their necessary manifest, routing, README inventory, and validation updates unless the user authorized the broader scope.
- Stop before broadening plugin discovery text unless the new or changed skill materially changes discoverability; required version bumps remain part of skill authoring.
- Stop and route to `skill-routing-validator` when the requested deliverable is an eval set rather than a skill artifact.
