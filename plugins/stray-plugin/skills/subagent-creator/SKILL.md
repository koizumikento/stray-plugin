---
name: "subagent-creator"
description: "Use when the user wants to create or update a Codex custom subagent under .codex/agents/, including task-specific TOML, optional .codex/config.toml agent limits, and clear delegation guidance for when that subagent should or should not be used."
---

# Subagent Creator

Create or update focused Codex custom subagents for the current project. Default to small, opinionated agent definitions that complement the built-in `default`, `worker`, and `explorer` agents instead of replacing them broadly.

Use this skill for project-scoped agent files under `.codex/agents/` and only touch `.codex/config.toml` when the workflow genuinely needs custom `[agents]` limits.

## Preferred Scope

- New custom agent creation in `.codex/agents/<agent-name>.toml`
- Existing custom agent cleanup or narrowing
- Adding or tuning `[agents]` settings in `.codex/config.toml`
- Creating a small set of cooperating agents for a repeatable workflow such as review, research, or debugging

## Do Not Use For

- General skill authoring under `skills/`
- Prompt-only task decomposition that does not need reusable agent files
- Replacing built-in agents with a broad catch-all custom agent
- Deep multi-level delegation plans unless the user explicitly needs recursive fan-out

## Workflow

1. Locate the project root and inspect existing `.codex/agents/` and `.codex/config.toml` files before writing anything.
2. Define the agent boundary in one sentence:
   - the single job it owns
   - the work it must avoid
   - whether it should read only or write code
3. Prefer built-in agents first:
   - keep `explorer` for read-heavy mapping
   - keep `worker` for implementation
   - create a custom agent only when the workflow benefits from narrower instructions, model choice, sandboxing, or tool access
4. Write the minimal TOML first. Every custom agent file must include:
   - `name`
   - `description`
   - `developer_instructions`
5. Add optional fields only when they materially improve reliability:
   - `model` and `model_reasoning_effort` when the task needs a different cost, speed, or depth profile
   - `sandbox_mode` when the agent should be stricter than the parent workflow, especially `read-only` for reviewers, researchers, and explorers
   - `nickname_candidates` when many instances of the same agent will run and clearer UI labels help
   - `mcp_servers` or `skills.config` only when the agent truly depends on them
6. Keep delegation predictable:
   - default `[agents].max_depth` to `1`
   - only raise `max_depth` when recursive delegation is explicitly needed
   - set `max_threads` only when the workflow needs a different concurrency cap than the default
7. When designing multiple agents, split by responsibility and write access:
   - read-only exploration or evidence gathering
   - read-only review or verification
   - targeted implementation
8. In `developer_instructions`, tell the agent:
   - what evidence to gather or what output to produce
   - what it must not do
   - how narrowly it should operate
9. For write-capable agents, make ownership explicit in `developer_instructions`:
   - name the files, modules, or responsibility boundary they own
   - state that they are not alone in the codebase
   - tell them not to revert edits made by other agents or the user
10. Avoid name collisions with built-in agents unless the user explicitly wants to override one. If a custom agent uses the same `name` as `explorer`, `worker`, or another built-in, the custom definition wins.
11. Report the created or updated paths, the final agent boundaries, and any assumptions about model choice, sandboxing, or thread limits.

## Authoring Rules

- Keep each custom agent narrow and opinionated.
- Prefer read-only agents for exploration, review, and docs verification.
- Use write-capable agents only for implementation tasks that truly need edits.
- For write-capable agents, assign a disjoint write scope whenever practical.
- Match the model to the task:
  - smaller or faster models for mapping and repeated exploration
  - stronger models or higher reasoning for correctness-sensitive review
- Keep `developer_instructions` operational, not generic. They should constrain behavior, not restate the agent name.
- Omit optional config that simply copies the parent session without changing behavior.
- Match the filename to the agent name when practical, even though `name` is the source of truth.

## Guardrails

- Do not create a "do everything" custom agent.
- Do not raise `max_depth` above `1` unless the user asks for nested delegation or the workflow cannot work without it.
- Do not grant write access to research or review agents by default.
- Do not add MCP servers or skills to an agent that can do its job without them.
- Do not overwrite unrelated `.codex/config.toml` or `.codex/agents/*.toml` settings.
- Do not assume a custom agent should exist when a one-off prompt to a built-in agent is enough.

## Output

When you finish, report:

- created or updated file paths
- the final trigger description for each custom agent
- any `[agents]` settings added or intentionally left unchanged
- assumptions about model, reasoning effort, sandbox, and tool dependencies
- any risks kept open, such as a deliberate built-in override or a workflow that needs user confirmation before deeper delegation

## Reference

If you need the current rationale for these defaults, use `references/subagent-best-practices.md`.
