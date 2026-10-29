# AI Feature Design

Read this when deciding an AI feature's behavior, human/AI responsibilities, or workflow/agent control. Keep user-visible feature behavior and product decisions in Product Designer; use `agent-system-designer` for requested technical allocation across model context, tools, state, harness, loops, and graphs; this reference does not authorize implementation, deployment, external evaluation calls, or agent execution. Use the decisions relevant to the requested artifact, not a compulsory document template.

## Workflow

1. Define the user outcome before choosing AI.
   - Map the current task, its pain point, and the smallest useful improvement. Compare ordinary code, rules, search, a single model call, and more involved AI only where they fit.
   - Decide whether the feature automates work or helps the user do it. Define success through task completion, correction effort, and user benefit as well as model quality; record a baseline and material latency/cost constraints.
2. Design for uncertainty and recovery.
   - Define what the system can do, known limits, and the user's ability to inspect evidence, edit, dismiss, undo, or resume work. Distinguish a proposed result from an applied change and make insufficient information visible.
   - Keep the AI's identity and role clear. Match intervention and tone to the task; do not imply human experience or stronger capability than evidence supports.
   - Identify consequential mistakes, affected people/data, and human handoff conditions. Do not use a model's self-reported confidence as the sole permission or completion signal.
3. Select control per operation using the table below.
   - Use workflow for predefined paths, agent control for adaptive action selection, and a combination when only some stages need exploration. A workflow can contain model calls, routing, loops, and parallel steps; tool use or repeated calls alone does not establish agent autonomy.
   - Treat unclear requirements as a design gap first. Many exceptions do not automatically justify an agent. Keep a simple baseline and require evidence that dynamic control improves the user outcome enough to justify its burden.
4. Define information and action boundaries.
   - Specify authoritative sources, access scope, freshness, provenance, and missing/conflicting-information behavior. Choose retrieval, tools, or memory for a demonstrated information need; RAG is one context-supply mechanism, not a correctness guarantee.
   - Check whether evidence covers the question before answering; bound additional retrieval and define clarification or stopping when information remains insufficient.
   - For each autonomous stage, identify its input, expected output/evidence, allowed tools/data/actions, time/cost/attempt budget, verifier, and exit or escalation condition. Keep business invariants and authorization enforced outside the model.
   - Plan durable progress and recovery when the task must survive interruption. Keep the recoverable record distinct from selected model context; do not require event sourcing or a memory service for a short stateless feature.
5. Choose multiplicity separately from autonomy.
   - Start with one agent where adaptive control is needed. Add workers only for separable work or an independently useful verification role, accounting for communication, integration, correlated errors, and total cost.
   - Use `multi-agent-patterns` for a requested topology/handoff design. A combined workflow/agent feature does not inherently need multiple agents.
6. Define validation before expanding complexity.
   - Compare candidates on the same representative normal, ambiguous, missing-evidence, failure, and out-of-scope cases. Measure actual task outcome, repeated-run reliability, correction effort, cost per successful task, and tail latency where relevant.
   - Separate deterministic checks of contracts, permissions, and side effects from semantic assessment. Calibrate model judging against human examples; distinguish quality failures from tool or infrastructure failures.
   - Specify a rollout, fallback, monitoring, and recovery approach proportionate to the feature. Revisit prompts, retrieval, and scaffolding on model/data changes; remove compensating components that no longer improve outcomes without removing required controls.
7. Deliver the decision in the requested format.
   - Explain the selected control boundaries, material alternatives, evidence, and unresolved assumptions when needed for the deliverable. Label the selection as a design synthesis rather than an industry-mandated score or universal standard.
   - Route settled app implementation to `fullstack-app-builder` when requested, evaluation strategy alone to `test-design-strategist`, and a requested repeatable AI quality gate to `ai-eval-ci`.

## Selection Criteria

Use these questions together; do not count answers into an invented threshold.

| Question | Workflow fits | Agent control may help | Combined boundary |
| --- | --- | --- | --- |
| Can the steps and exceptions be specified in advance? | Known transitions and bounded branches | Observations determine new steps, searches, or tools | Fixed outer lifecycle with an adaptive investigation stage |
| Does choosing the next action add value? | Classification or generation within a known process is sufficient | Hypotheses and plans must change with environmental feedback | Escalate only cases where fixed handling demonstrably falls short |
| Can success be checked? | Per-step contracts and final-state checks | The path is variable but evidence or outcome is inspectable | Verify the agent's result before consuming it; limit automation when verification is weak |
| What is the effect of a mistake? | Strict transitions and narrow operations fit | Exploration can stay within an enforceable permission scope | Separate investigation/proposal from consequential execution and check authority at execution |
| What latency/cost is acceptable? | Tight predictable budgets favor bounded paths | Additional work has measurable value | Bound exploration and provide a timeout/fallback path |
| How coupled are the steps? | Ordered stages or known independent branches | One agent maintains evolving context across observations | Add workers only for separable tasks with an explicit join/verifier |

## Worked Examples

These are illustrative designs, not measured claims about a specific product.

| Feature and requirement | Starting choice | Responsibility and completion boundary |
| --- | --- | --- |
| Extract invoice fields and register them | Workflow | Model extraction -> code checks required fields, arithmetic, and duplicates -> authorized registration or review queue. Variable document layout alone does not need adaptive control. |
| Diagnose an unfamiliar incident and return evidence | One bounded agent | Select read-only logs/docs, revise hypotheses, and return findings plus gaps. Restrict data access, budget, and stop conditions; remediation is a separate action. |
| Investigate a refund request and execute an eligible refund | Combination | Fixed identity/order checks -> adaptive investigation if needed -> proposed resolution -> server-side eligibility, amount, authority, and replay checks -> execution or escalation. |
| Compare named competitors on fixed fields | Workflow | Fetch known sources, extract fields, validate citations, and format the comparison. Missing data is an explicit outcome. |
| Discover competitors and refine comparison questions | Combination | Agent explores within scope/budget -> evidence and gap checks -> fixed report generation. The agent may also call a predefined data-gathering workflow as a tool. |

## Evidence And Freshness

Sources checked 2026-10-15. Recheck current capabilities before a concrete design decision. Distinguish original publication from later revisions; the criteria and examples above are a synthesis, not an adopted standard. Do not treat benchmark gains or vendor case studies as expected business improvements.

- [Google PAIR: User Needs + Defining Success](https://pair.withgoogle.com/guidebook-v2/chapter/user-needs/) grounds automation/augmentation and success in user benefit.
- [Microsoft Research: Guidelines for Human-AI Interaction](https://www.microsoft.com/en-us/research/articles/guidelines-for-human-ai-interaction-eighteen-best-practices-for-human-centered-ai-design/) (2019-03-05) covers expectations, correction, uncertainty, and change over time; it is research-backed design guidance.
- [Berkeley BAIR: Compound AI Systems](https://bair.berkeley.edu/blog/2024/02/18/compound-ai-systems/) (2024-02-18) frames composition of models, retrieval, and ordinary software as a system-design problem.
- [Anthropic: Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) (2024-12-19) provides practical control patterns; it is vendor engineering guidance, not a universal taxonomy.
- [Intelligent AI Delegation](https://arxiv.org/abs/2602.11865) (2026-02-12) proposes verifiable task contracts, boundaries, and delegation; treat it as a research framework.
- [Towards a Science of Scaling Agent Systems](https://arxiv.org/abs/2512.08296) (first published 2025-12-09; revised 2026-04-08) reports task-dependent architecture effects in controlled benchmarks, not a universal agent-count rule.
- [Google Research: Agentic RAG](https://research.google/blog/unlocking-dependable-responses-with-gemini-enterprise-agent-platforms-agentic-rag/) (2026-06-05) illustrates evidence-sufficiency checks and iterative retrieval in a vendor system.
- [NIST: Agent identity foundation](https://www.nist.gov/blogs/cybersecurity-insights/back-future-why-agentic-ai-needs-strong-identity-foundation) (2026-08-27) discusses scoped authority and approval fatigue; it is an expert explanation, not a finalized agent authorization standard.
