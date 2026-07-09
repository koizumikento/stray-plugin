---
name: "multi-agent-patterns"
description: "Use when the user wants to design or compare a multi-agent execution model with roles, dependencies, handoffs, shared state, and quality gates. Do not use for single-agent work or authoring `.codex/agents/` files."
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
   - assign disjoint write ownership or a single merge owner whenever agents can modify files
4. Specify coordination rules:
   - define handoff conditions and message format
   - decide what shared state lives in memory, files, or the coordinator
   - add quality gates for review, retry, or escalation
   - for each quality gate, name the verifier, observable pass/fail signal, maximum repair attempts, and escalation payload
   - define the final completion condition before adding retries or parallel agents
   - express dependencies as a small DAG or ordered stage list and name the join condition
   - set a concurrency ceiling, token or cost posture, cancellation rule, and timeout owner
   - state which agent resolves conflicting results and which evidence wins
5. Call out failure modes explicitly:
   - note bottlenecks, duplicated work, and context drift
   - avoid majority voting when expertise is uneven
   - prefer direct handoff over repeated paraphrasing when fidelity matters
   - define what happens to partial work when a peer fails, times out, or is cancelled
6. Return a decision the user can act on:
   - recommended topology
   - agent roles and handoffs
   - shared state and quality gates
   - main risks and the simplest next step
   - a handoff packet that `subagent-creator` can turn into reusable agent files when requested

## Output Expectations

- Lead with the recommended architecture and why it fits.
- Keep the answer concrete enough to implement or delegate.
- Include any assumptions that materially affect the design.
- State when the recommendation is to stay single-agent instead.
- Include role, input, output, dependency, write scope, verifier, retry limit, and escalation fields for each agent.

## Guardrails

- Do not invent extra agents unless they reduce real complexity.
- Do not treat role names as the design; coordination rules matter more.
- Do not hide context boundaries or shared-state assumptions.
- Do not replace this with subagent file authoring.
- Do not allow multiple write-capable agents to own the same files without an explicit serialization or merge rule.
- Do not recommend parallelism without stating its expected latency, cost, and integration tradeoff.
