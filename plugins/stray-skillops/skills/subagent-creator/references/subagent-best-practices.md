# Subagent Best Practices

This note distills the current guidance used by the `subagent-creator` skill.

## Official Defaults

- Custom subagents live in `.codex/agents/` for project scope or `~/.codex/agents/` for personal scope.
- Every custom agent file must define `name`, `description`, and `developer_instructions`.
- Optional fields such as `model`, `model_reasoning_effort`, `sandbox_mode`, `nickname_candidates`, `mcp_servers`, and `skills.config` inherit from the parent session when omitted.
- Global limits live under `[agents]` in `.codex/config.toml`.
- `agents.max_threads` defaults to `6`.
- `agents.max_depth` defaults to `1` and should usually stay there.

## Practical Defaults

- Start with built-ins before adding a custom agent:
  - `default` for general work
  - `worker` for implementation
  - `explorer` for read-heavy analysis
- Add a custom agent only when a narrower role, different sandbox, different model, or dedicated tool surface materially improves the workflow.
- Keep each agent single-purpose and opinionated.
- Split read-only and write-capable work into separate agents.
- Prefer `sandbox_mode = "read-only"` for reviewers, researchers, docs verifiers, and code mappers.
- Use stronger models or higher reasoning effort for correctness-heavy review; use faster models for mapping and repeated exploration.
- Add `nickname_candidates` only when many same-type agents will run and UI readability matters.
- Avoid overriding built-in names unless that override is intentional and documented.
- For write-capable agents, assign a clear file or module ownership boundary and tell them not to revert unrelated edits.
- For read-only explorer-style agents, keep the prompt narrowly scoped to specific questions instead of broad open-ended exploration.

## Instruction Design

`description` should answer when Codex should use the agent.

`developer_instructions` should answer:

- what the agent owns
- what evidence or output it should return
- what it must avoid
- how narrow or conservative it should be

Good instructions reduce drift. Weak instructions create agents that overlap and compete with each other.

## Delegation Safety

- Keep `max_depth = 1` unless recursive delegation is a real requirement.
- More depth increases token use, latency, and unpredictability even when `max_threads` still caps open threads.
- If you need multiple agents, assign disjoint responsibilities and keep the write scope narrow.
- Do not make urgent blocking work a delegated recursive workflow unless the parent can keep making progress in parallel.
- Subagents inherit parent approvals and sandbox behavior unless specifically overridden.

## Sources

- OpenAI Developers, "Subagents": https://developers.openai.com/codex/subagents
- OpenAI Developers, "Agent Skills": https://developers.openai.com/codex/skills
