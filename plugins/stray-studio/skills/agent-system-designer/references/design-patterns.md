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

## Control Context Growth

Distinguish runtime accumulation (history, retrieved data, tool results, repeated state) from development-time accretion (fixed rules, examples, and exceptions added after failures). They need different controls; compaction does not repair a bloated fixed prompt or an ambiguous tool contract.

1. Measure the actual model-bound request, including SDK-injected content. Attribute tokens to stable instructions, tool definitions, conversation, business state, retrieved evidence, and tool results; compare growth across turns and task stages. Where token measurement is unavailable, label size estimates and avoid treating character counts as billing tokens. Keep telemetry redacted; record counts and versions rather than private content by default.
2. Define the lifecycle of each information class using the table below. Reuse existing records and retrieval rather than adding a second memory store. Omission from a model request must not silently delete an authoritative record or bypass its access/retention policy.
3. Select compaction/trimming using the adopted SDK version's supported mechanisms before building a replacement. Choose a trigger and retained recent context against model capacity, output/tool-call headroom, and observed task quality, cost, and latency. Token volume catches unusually large messages that a turn-count window can miss; a window may fit predictable small chats. Do not copy sample thresholds or reset a session merely because a fixed number of turns elapsed.
4. Preserve active requirements, latest corrections and their provenance, unresolved questions, current authorization scope, and pending/unknown external effects across compaction. These may be compactly represented or referenced in authoritative state; they must remain available at the point of decision. Keep enough recent interaction to resolve references, preserve provider-required tool-call/result relationships, and retain an authorized route back to older evidence. A summary must not grant permission, turn uncertainty into fact, or outrank a newer correction.
5. Verify on conversations of different lengths, including a large tool result, topic return, a correction before and after compaction, and recovery of an older source. Compare input growth by component, task outcome, constraint adherence, latency, and cost under matched conditions. Shorter input alone is not success; retain unverified behavior as a gap when trials are not authorized or available.

| Information | Add or update | Omit, compact, or retrieve again |
|---|---|---|
| Stable instructions and tool contracts | Keep required responsibilities and rules; replace contradictory or superseded wording | Load specialized instructions/tools for the current need; do not accumulate one permanent rule per failed example |
| Current business state | Supply relevant current values, revision, provenance, and unresolved facts from the owner | Replace stale snapshots in the selected context; retain historical records under their policy and fetch them when relevant |
| Conversation events | Let the SDK manage history once; retain necessary recent exchanges | Compact or omit older exchanges while keeping active requirements and recoverable source references |
| Retrieved documents | Supply the necessary passage with source identity/version | Keep full documents in existing authorized storage; retrieve the needed passage again instead of resending the whole corpus |
| Tool outputs | Return relevant facts, outcome status, and result references | Offload bulky payloads through existing storage; preserve errors or uncertain effects needed for recovery and replay decisions |

For fixed-instruction changes, diagnose the trace first. Repair missing evidence, a schema mismatch, or faulty state handling in its owner. If wording is responsible, consolidate the existing rule and check consistency with examples instead of appending a stronger warning. Preserve representative failures as evaluation cases, keep development and confirmation sets distinct, and revisit model/SDK workarounds on upgrades. Runtime history summaries and instruction maintenance are separate jobs.

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
- [ADK: Context compression](https://adk.dev/context/compaction/) documents token-based and sliding-window session compaction. Verify support in the adopted SDK version; its sample configuration is not a universal retention policy or a guarantee that summaries preserve every requirement.
- [LangGraph: Thinking in LangGraph](https://docs.langchain.com/oss/python/langgraph/thinking-in-langgraph) describes nodes, shared state, on-demand prompt formatting, and distinct error-handling strategies.
- [Workflow optimization survey](https://arxiv.org/abs/2603.22386) (2026-03-23) distinguishes static scaffolds from per-run or runtime structure changes; it does not establish that dynamic graphs are universally better.
- [Anthropic: Managed Agents](https://www.anthropic.com/research/managed-agents) (2026-04-08) separates durable sessions, context selection, harness, and execution environment, and illustrates model workarounds becoming obsolete.
- [LangChain: Improving Deep Agents with harness engineering](https://www.langchain.com/blog/improving-deep-agents-with-harness-engineering) (2026-02-17) reports a fixed-model coding-benchmark experiment using traces and harness changes. Its gains and heuristics are not expected outcomes for arbitrary business agents.
