# MCP Application Contracts

Read this when an MCP server exposes existing application commands, supports writes, shares behavior with browser tools or an HTTP API, or needs deployment/discovery acceptance criteria. Produce a design contract only; do not execute tools, deploy, change registrations, or create an evaluation harness under this skill.

## Applicability And Authority

These are application design patterns, not additional MCP protocol requirements. Use the selected protocol revision and the target client's official documentation for wire behavior. Keep SDK, client, runtime, deployment, and contract versions explicit; mark unverified compatibility as provisional.

The patterns were independently synthesized from [KasaneNote at revision 1e0263e3fc12fd5b243b43978cbefdb259e0966c](https://github.com/koizumikento/kasanenote/tree/1e0263e3fc12fd5b243b43978cbefdb259e0966c) on 2026-10-10. Its entity names, tool count, size limits, credential restrictions, patch format, and hosting controls are example-specific. Its implementation advertises protocol revision `2025-03-26`; this is not evidence of compatibility with other revisions or clients.

## Workflow

1. Map actors, entry points, and ownership.
   - Identify browser tools, remote MCP, HTTP API, CLI, and worker paths that reach the same state. Choose only the surfaces the use case needs.
   - Reuse existing commands, validation, object authorization, and persistence invariants. Keep protocol encoding, credential validation, and UI effects in the appropriate adapters; do not add a common framework just to share rules.
   - Distinguish end-user authority, service authority, and any trusted hosting identity boundary. Browser login, remote OAuth, and a worker credential are separate flows whose permissions must be defined explicitly.
   - Treat a currently selected UI object as interaction context, not authorization. Define whether a tool requires that object to be open and whether it changes navigation, drafts, focus, or selection.
2. Specify each tool as a caller contract.
   - Record purpose, allowed actor and resource, input schema, required/optional fields, defaults, units, limits, result shape, effects, failures, retry safety, and the next useful read.
   - Describe what is committed, accepted for later work, proposed for review, or unavailable. Saving an external result does not imply fetching its source, scheduling work, running inference, or approving a conclusion.
   - Verify the advertised schema against runtime validation and domain rules. Document conditional constraints that the schema does not express; resolve discrepancies instead of copying one representation unchecked.
   - Declare annotations according to the selected revision; annotations are hints and do not grant authority or guarantee deduplication. Use `outputSchema` and `structuredContent` only with verified revision/client support, and retain any required compatibility representation.
   - Distinguish malformed protocol requests from tool execution failures according to that revision. Do not use HTTP success alone as tool success or copy an application's catch-all JSON-RPC error mapping as a general pattern.
3. Design writes and recovery where applicable.
   - Choose a deduplication identity with an explicit subject/resource/operation scope. It may be a caller request key or a provider event/execution ID. Define payload matching, retention, concurrent claims, and stored results.
   - Make the mutation and receipt atomic where supported. A lookup followed by an insert is insufficient against concurrent delivery; a local transaction cannot make an unrelated provider effect atomic.
   - For partial updates, define omitted fields, empty values, nulls, arrays, and immutable fields. Do not assume arrays merge, null clears, or every update is partial.
   - Match replays against the original caller intent, including any expected version. Do not hash a patch after merging it into mutable current state. Authenticate and reauthorize before returning a protected receipt.
   - After a lost response, preserve the same command identity and input for a supported replay or query the result. After a confirmed version conflict, read current state and reevaluate intent before issuing a new command. Never turn an unknown external outcome into a fresh execution by default.
   - State how no-op updates, older receipts, and changed schemas behave during rollout. Preserve history and review/approval boundaries required by the domain.
4. Design bounded reads and evidence.
   - Define search scope and exclusions, stable identifiers, ordering, page bounds, and terminal markers. Keep protocol discovery pagination separate from domain-tool pagination.
   - State whether offsets count records, characters, code units, or bytes. Preserve filters and scope across pages; concatenate serialized fragments before parsing when required, and handle byte/text encoding boundaries deliberately.
   - Distinguish a page with more data, a permanently shortened field, an unavailable original, and a partial capture. A next-page marker for one collection does not recover every truncated field in the result.
   - Carry source ID, saved revision, timestamps, hash where available, derivation, and missing-data reasons when evidence matters. A URL registration, an AI summary, and a saved original are different records with different evidentiary meaning.
   - Define cache/replay authorization and read-after-write behavior. Protected result retrieval must use the same effective ownership policy as the write.
5. Define evaluation tasks for the changed guarantees.
   - Reuse [the read-only evaluation contract](read-only-eval-contract.md) for multi-tool reads. Add relevant mutation cases below as a separate allowed-write set, not to its read-only tasks.
   - Name an isolated, resettable fixture, versions, allowed tools, forbidden effects, expected call dependencies, bounded calls, and cleanup. Prefer a disposable store when no deletion tool is exposed; do not require a production fixture.
   - Verify the first result, replayed receipt, and authoritative readback. Include allowed happy paths as well as denial, conflict, and incomplete outcomes.
   - Execution belongs to a separately authorized implementation/test workflow. This reference defines assertions; it does not authorize live writes, account creation, network changes, or recurring jobs.
6. Specify publication evidence for the intended environment.
   - Record source revision and artifact identity, deployed artifact/configuration, authenticated discovery, host registration where one exists, tool definitions visible to the target client, and an allowed call/result check.
   - When retrievable, inspect the exact deployable archive in isolation and compare its server/tool contract with the expected source. Match the saved version's source revision and archive identity. If a deduplicated save returns an existing version for the same source revision, that response does not prove that newly built bytes replaced the stored artifact; a version number is an identity marker, not a refresh mechanism.
   - Compare tool names, schemas, and behavior at each applicable boundary. Identify the first observed mismatch; do not infer a cache or archive defect merely from stale client definitions.
   - If an older published archive cannot be retrieved, label its contents unknown. Separate a failed build/save/deploy/refresh request from successful deployment with stale client discovery; do not attribute either outcome to versioning without evidence from that boundary.
   - A build, deploy, version bump, registration UI, or new conversation turn cannot alone prove usable tools in the current client. Use the host's supported refresh mechanism when needed; do not prescribe a vendor-specific UI action universally.
   - When registration refresh fails or the current client's definitions remain stale, retain the observed error and definition mismatch, then identify a supported next step. Do not promise that another user turn will refresh tools or repeat the same failed refresh without a new diagnosis; report the unresolved boundary while preserving existing connections and access controls.
   - Preserve target identity, storage, access policy, and credentials during an authorized rollout. If no mutation target is authorized, leave the deployed write success path unverified rather than weakening auth or writing fixtures to production.

## Mutation Evaluation Matrix

Select cases the server supports. The generic record below is a fixture entity, not a required domain model or tool name.

| Case | Call relationship | Required assertion |
|---|---|---|
| Create and read | create -> detail using returned ID | Correct actor/resource, committed data and version, no fabricated IDs |
| Replay after lost response | write -> same identity/input -> detail | One effect; receipt remains stable even if current data subsequently changes |
| Conflicting reuse | write -> same deduplication identity with changed input | Rejected mismatch; first result unchanged |
| Concurrent delivery | same command twice; then competing commands at one version | One effect for replay; conflict behavior matches declared concurrency guarantees |
| Partial update | read -> update one field -> detail | Omitted fields retained; arrays/null/empty values follow the declared contract |
| Stale version | read -> intervening update -> update old version | Explicit conflict; no overwrite or automatic fresh execution |
| Actor and object denial | attempt protected read/write/receipt from disallowed context | No protected data or effect; allowed context still succeeds |
| Evidence and review | save derived result -> read source and saved result | Provenance and source versions retained; save does not imply domain approval |

## Transfer Checks

- For a read-only catalogue server, apply search scope, identifiers, pagination, source freshness, errors, and discovery checks. Skip mutation receipts and approval workflows; do not invent a writable store merely to fit the example.
- For a ticketing server, map caller authority to ticket/project scope, define expected-version updates and provider deduplication support, and read back the saved ticket. An authorized service actor may write if that domain permits it; KasaneNote's worker-credential restriction is not a universal rule. When the provider cannot deduplicate, define bounded lookup/manual reconciliation rather than promising exactly-once delivery.

These are design examples, not executed compatibility tests.

## Deliverable

Return the entry-point/actor map, per-tool caller contracts, write/recovery and read-completeness decisions, selected evaluation cases, publication evidence requirements, and unresolved compatibility or authority gaps. Keep design decisions, implemented behavior, fixture results, and live acceptance separately labeled.

## Sources And Limits

- Implementation observations: [MCP adapter](https://github.com/koizumikento/kasanenote/blob/1e0263e3fc12fd5b243b43978cbefdb259e0966c/site/lib/mcp.ts), [shared commands](https://github.com/koizumikento/kasanenote/blob/1e0263e3fc12fd5b243b43978cbefdb259e0966c/site/lib/agent-tools.ts), [store](https://github.com/koizumikento/kasanenote/blob/1e0263e3fc12fd5b243b43978cbefdb259e0966c/site/lib/store.ts), [publication checks](https://github.com/koizumikento/kasanenote/blob/1e0263e3fc12fd5b243b43978cbefdb259e0966c/docs/connections.md), and [isolated research fixture](https://github.com/koizumikento/kasanenote/blob/1e0263e3fc12fd5b243b43978cbefdb259e0966c/site/scripts/test-mcp-research.mjs). Source review does not establish current production behavior.
- Protocol authorities checked 2026-10-10: MCP [2025-03-26 tools](https://modelcontextprotocol.io/specification/2025-03-26/server/tools), [transport](https://modelcontextprotocol.io/specification/2025-03-26/basic/transports), [authorization](https://modelcontextprotocol.io/specification/2025-03-26/basic/authorization), and [2026-07-28 tools](https://modelcontextprotocol.io/specification/2026-07-28/server/tools). Recheck the selected revision and SDK/client documentation before implementation; fields and lifecycle rules differ between revisions.
