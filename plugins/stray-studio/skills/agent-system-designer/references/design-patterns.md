# Agent System Design Patterns

Read when choosing context/state boundaries, a control structure, or harness responsibilities. These are design aids, not a compulsory architecture or document template. Use only the parts relevant to the current decision.

## Terms And Boundaries

| Term | Design question | Common mistake |
|---|---|---|
| Prompt | What should this model operation accomplish, under which rules? | Writing a persona without required information or completion evidence |
| Context | What information and tools should this call see, and how are they updated? | Sending every stored record or duplicating the framework's history |
| Loop | What new observation justifies another action, and when does iteration end? | Repeating the same failure or treating another critique as verification |
| Graph | Which operations depend on each other, branch, join, or cycle? | Making each conversational turn a fixed stage or assuming every graph is a DAG |
| Harness | Which surrounding mechanisms make model behavior executable, observable, and recoverable? | Rebuilding SDK features or retaining obsolete model workarounds |

These terms overlap and vendors draw their boundaries differently. A graph can contain an agent loop; a loop can call a fixed workflow. Neither multiple calls nor a graph implies multiple agents. A checkpoint, durable session, model context, and business database are distinct responsibilities even when one platform implements several.

## Select Control From The Required Behavior

| Need | Smallest starting point | Add structure when |
|---|---|---|
| Transform supplied text into a checked record | One model call plus deterministic validation | A separately verifiable stage or necessary recovery boundary appears |
| Ask useful questions and update a draft | One conversational agent with task-oriented tools | Business transitions require explicit guards; keep question order flexible |
| Investigate an unfamiliar cause using observations | One tool-action loop | Independent work or a separate verification role justifies coordination |
| Run known processing stages with review and submission | Existing workflow/state machine | Branching, joins, interruption, or replay needs explicit graph boundaries |
| Refine an artifact against an observable criterion | Generate, verify, then repair an identified defect | Feedback supports another change; stop on success or a real execution boundary |

Do not adopt a graph library to draw a diagram. Do not assume a simple extraction task needs an adaptive controller because input documents vary. Conversely, do not encode a genuinely exploratory task as a brittle list of prompt-level if/else instructions.

## Separate Records From Model Inputs

Keep the responsibilities explicit, using the existing storage/runtime rather than requiring new infrastructure:

1. Preserve conversation events with speaker and event boundaries where continuity or source attribution requires them.
2. Keep current business facts and operation status in their authoritative owner. Track revisions when later actions depend on a particular version.
3. Assemble the model context from the relevant current facts, unresolved questions, necessary history, evidence, and tools. Formatting a prompt does not define the storage schema.
4. Keep enough provenance to revisit omitted or summarized evidence. Apply access and retention rules; durable does not mean retain everything forever.
5. When a fact changes, identify which derived plans, checks, or confirmations become stale. Do not require users to repeat facts already available in authoritative state.

For example, a museum caption assistant may converse freely about wording while the app enforces draft -> review -> publication transitions. A corrected attribution updates the current record and invalidates its prior review. It does not require a second classifier agent or deletion of the conversation history.

## Separate Iteration And Failure Types

| Mechanism | Feedback and progress | Exit or recovery |
|---|---|---|
| Action/observation loop | A tool result changes what to inspect or do next | Required result/evidence obtained, cancellation, unavailable prerequisite, or applicable execution limit |
| Semantic repair | A check names a concrete discrepancy and a supported correction | Check passes, evidence is insufficient, progress stalls, or an applicable limit is reached |
| Transport retry | A transient failure with safe replay or reconciliation | Existing retry policy, terminal error, or uncertain effect requiring reconciliation |
| Development improvement | Traces reveal a recurring failure; a candidate changes its responsible component | Compare on separate improvement/confirmation cases; reject regressions and unsupported extra machinery |

Distinguish a stopped stage from a stopped task. Preserve useful partial work and continue independent authorized work. Do not infer new action permission from a plan, model output, or successful earlier tool call. Use the caller/platform's existing constraints; if a material operating limit is unknown, state the gap rather than manufacturing a deadline or universal retry count.

## Design The Model's Interface

- Prefer an operation such as updating an exhibit's attribution with source evidence over exposing storage offsets, parallel arrays, and internal bookkeeping fields.
- Make tool descriptions, input schemas, actual validation, and error messages consistent. An accepted natural answer such as an unknown measurement needs a representable domain state when the feature permits unknowns.
- Return enough evidence to distinguish saved, rejected, pending, and unknown outcomes. Do not turn a tool contract failure into a new business requirement.
- Keep permissions, conditional updates, side-effect replay protection, and approval binding in the execution layer. Prompts and tool filtering help interpretation and selection, not enforcement.
- Instrument actual model inputs, tool results, state transitions, and outcome evidence with appropriate redaction. Debug the failing boundary before adding instructions, agents, or model compute.

## Evidence And Freshness

Sources checked 2026-10-29. The tables and example are a synthesis, not a standard or measured performance claim. Framework documentation describes that framework; research and vendor experiments support only their tested conditions. Recheck relevant official contracts when changing SDKs/models, relying on provider-specific features, or investigating contradictory behavior; routine local design work does not require opening every source.

- [Anthropic: Building effective agents](https://www.anthropic.com/research/building-effective-agents) (2024-12-19) distinguishes predefined workflows from model-directed control and favors simple composable patterns.
- [Anthropic: Context engineering](https://www.anthropic.com/research/effective-context-engineering-for-ai-agents) (2025-09-29) covers instructions, tools, history, retrieval, and selective context management; minimal context must still be sufficient.
- [Anthropic: Writing effective tools](https://www.anthropic.com/research/writing-tools-for-agents) (2025-09-11) covers model-facing contracts and outcome evaluation without requiring one exact valid tool path.
- [ReAct, ICLR 2023](https://arxiv.org/abs/2210.03629) (2023-03-10 revision) studies interleaved reasoning and actions on earlier models and tasks; it does not require exposing private model reasoning or using a particular current SDK.
- [ADK: Loop workflow](https://adk.dev/agents/workflow-agents/loop-agents/) documents iteration and termination mechanisms; its sample counts are examples, not universal execution budgets.
- [LangGraph: Thinking in LangGraph](https://docs.langchain.com/oss/python/langgraph/thinking-in-langgraph) describes nodes, shared state, on-demand prompt formatting, and distinct error-handling strategies.
- [Workflow optimization survey](https://arxiv.org/abs/2603.22386) (2026-03-23) distinguishes static scaffolds from per-run or runtime structure changes; it does not establish that dynamic graphs are universally better.
- [Anthropic: Managed Agents](https://www.anthropic.com/research/managed-agents) (2026-04-08) separates durable sessions, context selection, harness, and execution environment, and illustrates model workarounds becoming obsolete.
- [LangChain: Improving Deep Agents with harness engineering](https://www.langchain.com/blog/improving-deep-agents-with-harness-engineering) (2026-02-17) reports a fixed-model coding-benchmark experiment using traces and harness changes. Its gains and heuristics are not expected outcomes for arbitrary business agents.
