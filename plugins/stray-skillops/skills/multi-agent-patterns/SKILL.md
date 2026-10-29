---
name: "multi-agent-patterns"
description: "Use when designing or comparing multi-agent roles, dependencies, handoffs, shared state, and quality gates. Use subagent-creator to author .codex/agents/ files."
---

# Multi-Agent Patterns

Design multi-agent coordination that fits the task instead of defaulting to more agents. Keep an integrated agent-system design with `agent-system-designer`; contribute this coordination detail only when needed. Focus on routing, handoffs, context boundaries, and failure handling.

Use this skill when the user asks how to split a task across agents, how to coordinate specialists, or which multi-agent topology to use.

## Do Not Use For

- technical design of a single-agent system or an integrated context/tool/state/harness design; use `agent-system-designer`
- single-agent implementation or debugging
- creating or editing project subagents under `.codex/agents/`
- broad brainstorming that does not need an execution model
- ordinary work already settled as a single-agent task, without a coordination comparison
- deciding an AI feature's user behavior or workflow/agent boundaries before coordination is needed; use `product-designer`

## Workflow

1. Classify the task before proposing agents:
   - identify the goal, constraints, and why multiple agents would help
   - decide whether the problem is actually parallel, hierarchical, or sequential
   - separate autonomy from multiplicity: a workflow may use model calls and fixed parallel branches; an agent selects actions from observations; either can call the other without requiring multiple agents
   - compare against the smallest workflow or single-agent baseline; if it suffices, return that recommendation and its rationale instead of forcing a topology
   - evaluate task dependencies, tool/communication overhead, integration cost, correlated errors, and verification; do not infer benefit from agent count or role names
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
   - define each delegated outcome and its verifier before assigning work; split objectives further when they cannot be checked at that granularity
   - scope tools, data, authority, and re-delegation; keep downstream authorization and business invariants outside agent judgment
4. Specify coordination rules:
   - define handoff conditions and message format
   - decide what shared state lives in memory, files, or the coordinator
   - add quality gates for review, retry, or escalation
   - for each quality gate, name the verifier, observable pass/fail signal, hard execution limits, a reassessment point for repeated failures without progress, and escalation payload; continue evidence-based repairs within the hard limits instead of counting every new diagnosis as the same stalled retry
   - define the final completion condition before adding retries or parallel agents
   - express dependencies as a small DAG or ordered stage list and name the join condition
   - set a concurrency ceiling, token or cost posture, cancellation rule, and timeout owner
   - state which agent resolves conflicting results and which evidence wins
5. Call out failure modes explicitly:
   - note bottlenecks, duplicated work, and context drift
   - avoid majority voting when expertise is uneven
   - prefer direct handoff over repeated paraphrasing when fidelity matters
   - define what happens to partial work when a peer fails, times out, or is cancelled
   - keep recoverable progress separate from selected model context when work must survive interruption; preserve uncertain side effects for reconciliation instead of blindly replaying them
   - compare candidates under matched tasks, model/tool versions, and resource budgets; include repeated-run success, total cost per successful task, latency, and containment of errors
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
- Include role, input, output, dependency, write scope, verifier, hard execution limits, no-progress reassessment, and escalation fields for each agent. Hard limits remain binding even when progress continues.

## Guardrails

- Do not invent extra agents unless they reduce real complexity.
- Do not treat role names as the design; coordination rules matter more.
- Do not hide context boundaries or shared-state assumptions.
- Do not replace this with subagent file authoring.
- Do not allow multiple write-capable agents to own the same files without an explicit serialization or merge rule.
- Do not recommend parallelism without stating its expected latency, cost, and integration tradeoff.
- Do not launch agents or create agent files merely because this skill designs their coordination; use existing user authorization for execution and `subagent-creator` for requested reusable files.

## Evidence Basis

- [Towards a Science of Scaling Agent Systems](https://arxiv.org/abs/2512.08296), first published 2025-12-09 and revised 2026-04-08, reports task-dependent gains and regressions from coordination; benchmark results are not a universal topology rule.
- [Intelligent AI Delegation](https://arxiv.org/abs/2602.11865), published 2026-02-12, proposes verifiable task contracts and scoped delegation; treat it as a research framework rather than an established protocol requirement.
