# AI Feature Implementation

Read this when implementing or diagnosing model calls, retrieval, agent tools, adaptive control, context, or AI-specific verification in an app flow. Preserve settled product decisions and the repository's stack. Route an unresolved product decision to `product-designer`; do not start a market-research exercise for an already specified implementation.

## Workflow

1. Trace the outcome and control boundaries.
   - Identify the user-visible result, existing baseline, affected callers, authoritative state, and human/AI responsibilities. Separate a generated suggestion from an executed action.
   - Keep predefined paths, routing, and bounded loops as workflows. Use a single bounded agent when observations must determine the next action; combine control only at stages that need it. If selection is still an implementation choice, compare the smallest viable alternatives against the task instead of silently expanding scope.
   - Make the division concrete: invoice extraction can feed fixed validation/registration; an incident investigator can adapt read-only searches; a refund investigator can propose a resolution while fixed server-side rules control execution. Tool calls and multiple LLM calls alone do not require agent autonomy or multiple agents.
2. Enforce contracts and authority outside model output.
   - Validate model and tool outputs at trust boundaries. Treat retrieved documents, tool responses, model plans, and summaries as untrusted data, never as authorization to change scope or permissions.
   - Use the app's existing commands and domain rules across UI/API/worker/agent entry points. Enforce actor, tenant/resource access, business conditions, and input validation at execution, even when a plan was previously approved.
   - Give each adaptive stage an input, expected output/evidence, narrow tools/data/actions, verifier, and exit/escalation conditions. Scope credentials to the actor and task and keep secret values out of model context, tool output, and logs.
   - Reuse authorization covering the same target and effects. For consequential effects outside it, prepare a concrete reviewable proposal and request only the missing approval; do not turn every intermediate tool call into a confirmation prompt.
3. Define the prompt contract for each model-backed operation.
   - Reuse the settled feature behavior to specify the operation's purpose, required inputs, output shape, observable success criteria, and missing-information or invalid-output behavior. Resolve conflicting requirements and distinguish mandatory constraints from preferences; do not reopen product decisions merely to fill a template.
   - Separate stable application instructions from user input, retrieved documents, examples, and tool results using the provider's supported message roles and consistent delimiters. Do not interpolate untrusted content into privileged instructions. Delimiters help interpretation but do not replace the execution controls in step 2.
   - Keep prompt templates or builders with the owning feature and version them through the existing code-review and deployment process. Avoid a new prompt service, framework, or version registry unless the app needs it.
   - Choose examples to clarify an observed format, style, or classification boundary; include relevant boundary and insufficient-information cases and keep them consistent with the rules. Check guidance for the selected model rather than requiring examples, role personas, or step-by-step reasoning for every call.
   - Split model calls where intermediate results need validation, branching, or persistence. Give review stages an explicit criterion and source, computed result, or test where applicable; a request to reconsider alone is not proof of correctness. Keep repair within the execution limits below.
   - Define when the app should request clarification, use a permitted default, or return an explicit gap/failure. Tie clarification to missing information that changes the result or execution target; do not fabricate facts or infer action authorization.
4. Supply enough relevant information.
   - Preserve source identity, freshness, and access filtering for retrieval and caches. Check missing/conflicting evidence before answering; bound further retrieval and return gaps or request clarification rather than fabricating facts.
   - Keep a recoverable operation record distinct from the context selected for a model call. Store only the state the promised recovery needs; a stateless request does not require durable sessions or long-term memory.
   - When persistence is needed, define retention, access, deletion, and stale-information handling. Keep sensitive data out of general-purpose memory and telemetry by default.
5. Bound execution and recover uncertain effects.
   - Set task-wide time, model/tool request, token/cost, retry, and concurrency limits appropriate to the existing workload. Account for nested loops and workers; reaching a limit must yield a visible partial, failed, or escalated result rather than a false success.
   - End or escalate the adaptive stage on completion, cancellation, exhausted budget, or repeated lack of progress after reassessing the approach. Stop only the affected action on permission denial and continue independent authorized work. Distinguish semantic repair from retries of transient transport errors; do not create an unbounded self-correction loop.
   - For operations that survive the request, use [async-workflows.md](async-workflows.md) for durable acceptance, replay, cancellation, and recovery. A timeout after a side effect is an unknown outcome until reconciled; use idempotency/result checks before retrying.
6. Verify behavior at the appropriate layers.
   - Test deterministic validation, domain rules, authorization, and replay separately from semantic quality. Check final persisted/provider state or the produced artifact, not only the agent's completion text.
   - Use representative success, ambiguous-input, missing-evidence, invalid-output, injected-instruction, unauthorized-action, tool-failure, and budget-exhaustion cases as relevant to the changed flow. For durable work, include interruption and cancellation.
   - Compare candidates using fixed fixtures and recorded model/prompt/retrieval/tool/config revisions. Repeat stochastic trials where reliability is uncertain; measure task success, correction effort, cost per successful task, and tail latency. Calibrate semantic judges with human examples and separate environment failures from quality failures.
   - For prompt changes, keep improvement and candidate-selection cases separate from untouched final-check cases. Hold model, reasoning settings, tools, retrieval data, runtime limits, and retry conditions constant when isolating the prompt's effect; record intentional differences for whole-system comparisons. Treat final-check cases as development data if they guide another revision, and obtain fresh confirmation cases.
   - Keep lightweight evaluation in the existing harness. Use `ai-eval-ci` only when a repeatable CI gate is requested; do not silently add external model calls, providers, or paid evaluations.
7. Operate and simplify based on evidence.
   - Trace model/tool steps and final outcomes with redacted correlation data; record versions, latency, resource use, and failure categories without storing raw private prompts by default. Use existing observability and logging guidance when changing telemetry.
   - Roll out proportionately, retain a fallback or stop path, and recheck affected cases when model, prompt, data, retrieval, or tool behavior changes.
   - On model upgrades, remove one compensating component at a time and compare outcomes. Do not remove authorization, validation, recovery, or audit controls merely because a model appears more capable.
   - Report implemented behavior, verification results, remaining quality uncertainty, and unverified provider/runtime effects through the existing app handoff; no extra design document is required.

## Prompt Failure Diagnosis

Use these as hypotheses for the observed failure; inspect the actual input, evidence, tool result, and output before choosing a repair. Change the responsible component and recheck the affected behavior rather than appending stronger instructions to every prompt.

| Observed failure | Inspect first | Candidate repair |
|---|---|---|
| Wrong task or excessive scope | Operation purpose, conflicting requirements, completion criteria | Clarify the required result and scope |
| Wrong extracted fact or number | Source readability, retrieval coverage, definitions, calculation | Supply sufficient evidence, clarify field meaning, or use a calculation tool |
| Invalid format or inconsistent classification | Output contract and ambiguous decision boundaries | Use supported structured output plus validation, or representative examples |
| Missing work or repeated tool errors | Dependencies, tool contract, actual error, retry behavior | Add the missing check or repair the tool/integration; distinguish semantic repair from transport retry |
| Unnecessary questions or unsupported assumptions | Missing-information policy and available evidence | Clarify the app's question/default/gap behavior |
| Review leaves or introduces errors | Review criterion and independent verification signal | Compare with sources, computed results, tests, or actual final state; correct identified discrepancies |
| High cost, latency, or persistent quality failure | Repeated context, unnecessary calls, retrieval/tool performance, model capability | Measure the trajectory and compare the smallest viable prompt, context, model, or control change |

For example, an incorrect invoice total may come from unreadable input, a net/gross ambiguity, or missing arithmetic. Inspect those causes before adding an instruction to be more accurate. A successful retrieval may still provide insufficient evidence for the requested conclusion.

## Design Basis

Original sources checked 2026-10-15; prompting additions checked 2026-10-28. Recheck capability-specific decisions against current official documentation. These are engineering practices and bounded empirical findings, not performance guarantees; the diagnosis table is implementation guidance, not a measured universal mapping.

- [Anthropic: Harness design](https://www.anthropic.com/engineering/harness-design-long-running-apps) (2026-03-24) describes evaluator feedback and removing scaffolding when model capabilities change.
- [Anthropic: Scaling Managed Agents](https://www.anthropic.com/engineering/managed-agents) (2026-04-08) separates durable session records, orchestration, and sandbox execution; it does not require this service or a distributed architecture for every app.
- [Anthropic: Demystifying evals](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) (2026-01-09) distinguishes outcomes, traces, semantic grading, and repeated-trial reliability.
- [Anthropic: Infrastructure noise](https://www.anthropic.com/engineering/infrastructure-noise) (2026-02-05) shows why resource and runtime conditions belong in evaluation evidence.
- [OWASP: Excessive Agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/) gives least-privilege and downstream authorization guidance.
- [NIST: Agent identity foundation](https://www.nist.gov/blogs/cybersecurity-insights/back-future-why-agentic-ai-needs-strong-identity-foundation) (2026-08-27) discusses delegated authority, credential handling, and approval fatigue.
- [OpenAI: Prompt engineering](https://developers.openai.com/api/docs/guides/prompt-engineering) covers instruction/data structure, code-managed prompts, and regression evaluation; [reasoning guidance](https://developers.openai.com/api/docs/guides/reasoning-best-practices) recommends trying zero-shot first and cautions against unnecessary step-by-step prompting for its reasoning models.
- [Google: Prompt design](https://ai.google.dev/gemini-api/docs/prompting-strategies) strongly recommends examples, while [Claude: Prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices) describes examples and inspectable prompt chains. Provider recommendations differ; evaluate the selected technique on the target model and feature.
- [Sufficient Context](https://arxiv.org/abs/2411.06037v3) (2025-04-23 revision) separates insufficient retrieved evidence from failures to use available evidence on its tested RAG tasks and models; it does not validate every current model or a universal retrieval threshold.
- [Intrinsic self-correction, ICLR 2024](https://arxiv.org/abs/2310.01798v2) reports reasoning failures and degradation without external feedback in its tested models. It motivates explicit verification rather than assuming that a review prompt guarantees accuracy; it does not establish that all current models fail at revision.
