---
name: "multi-agent-patterns"
description: "Use when the user wants to design, route, or compare a multi-agent workflow for one task, such as choosing supervisor, swarm, pipeline, or hierarchical patterns, defining handoffs, or setting shared state and quality gates. Do not use for single-agent work, general brainstorming, or creating custom subagent files; use `subagent-creator` for `.codex/agents/` edits."
---

# Multi-Agent Patterns

Design a multi-agent architecture that fits the task instead of defaulting to more agents. Focus on routing, handoffs, context boundaries, and failure handling.

Use this skill when the user asks how to split a task across agents, how to coordinate specialists, or which multi-agent topology to use.

## Do Not Use For

- single-agent implementation or debugging
- creating or editing project subagents under `.codex/agents/`
- broad brainstorming that does not need an execution model
- cases where one focused agent can complete the work cleanly

## Workflow

1. Classify the task before proposing agents:
   - identify the goal, constraints, and why multiple agents would help
   - decide whether the problem is actually parallel, hierarchical, or sequential
   - stop if a single agent with better prompting is sufficient
2. Choose the smallest viable topology:
   - use `pipeline` for ordered stages with clear dependencies
   - use `supervisor` when one coordinator must assign and verify work
   - use `swarm` or peer routing when exploration benefits from flexible handoffs
   - use `hierarchical` when strategy, planning, and execution are distinct
3. Define each role narrowly:
   - give every agent one responsibility
   - state what each agent must not do
   - keep context shared only when the task truly needs it
4. Specify coordination rules:
   - define handoff conditions and message format
   - decide what shared state lives in memory, files, or the coordinator
   - add quality gates for review, retry, or escalation
5. Call out failure modes explicitly:
   - note bottlenecks, duplicated work, and context drift
   - avoid majority voting when expertise is uneven
   - prefer direct handoff over repeated paraphrasing when fidelity matters
6. Return a decision the user can act on:
   - recommended topology
   - agent roles and handoffs
   - shared state and quality gates
   - main risks and the simplest next step

## Output Expectations

- Lead with the recommended architecture and why it fits.
- Keep the answer concrete enough to implement or delegate.
- Include any assumptions that materially affect the design.
- State when the recommendation is to stay single-agent instead.

## Guardrails

- Do not invent extra agents unless they reduce real complexity.
- Do not treat role names as the design; coordination rules matter more.
- Do not hide context boundaries or shared-state assumptions.
- Do not replace this with subagent file authoring.
