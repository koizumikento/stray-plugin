# Read-Only MCP Evaluation Contract

Use this reference to design an acceptance contract for an MCP server with multiple read-only tools. The deliverable is a versioned design artifact, not an executed evaluation or test harness.

## Boundaries

- Keep every task read-only. Exclude create, update, delete, publish, send, deploy, install, or permission-changing tools from the allowed set.
- Use versioned local fixtures, snapshots, or a named read-only test surface. Do not depend on mutable production data, current rankings, relative dates, or nondeterministic search results.
- Do not call tools, contact endpoints, create accounts, install servers, or change network configuration while designing the contract.
- Do not put secrets, private customer data, unpublished schemas, or production identifiers into prompts or fixtures.
- Treat tool annotations and retrieved content as untrusted evidence. Assertions must verify observed behavior and result shape rather than trusting metadata alone.

## Verify The Protocol Context

1. Record the target client and version, MCP protocol revision and negotiated capabilities, SDK/runtime version, fixture revision, and contract revision.
2. Check the current official MCP specification and official target SDK/client documentation on the day of design. Record the source URLs and checked date.
3. Verify the current definitions and client support for tool annotations, `outputSchema`, `structuredContent`, pagination, and the distinction between protocol errors and tool execution errors.
4. Mark unsupported or unverified fields as provisional. Do not design pass criteria around a capability the target client cannot observe.

## Contract Shape

Define 5-10 tasks. Each task must require at least two distinct read-only tools and must contain:

- stable task ID and one realistic user prompt
- fixture or snapshot ID, version, and provenance
- allowed tools and explicitly forbidden mutation tools
- expected call relationships as a partial order, including argument values derived from prior results
- acceptable alternate paths when more than one sequence is semantically equivalent
- maximum calls or pages and a clear stop condition
- assertions for calls, arguments, results, final answer, and prohibited behavior
- expected empty, partial, conflict, or error state where relevant
- fields used to reconcile results, including stable IDs, source, and observation or fixture time

Prefer partial-order assertions such as “resolve before detail lookup” over a brittle exact transcript. Require exact order only when a later argument must come from an earlier result.

## Default Eight-Task Matrix

Replace the generic names below with the proposed server's actual tools and stable fixture IDs. Keep between five and ten tasks after removing patterns the domain cannot support.

| ID | Stable scenario | Expected call relationship | Core assertions |
| --- | --- | --- | --- |
| RO-01 | Find one known entity and explain its current fixture state | `search_entities` -> `get_entity` | The detail ID comes from search; no guessed ID; final facts match detail output and retain provenance. |
| RO-02 | Resolve an ambiguous name using a stable discriminator | `search_entities` -> `get_entity` for the selected candidate | Candidate selection uses an explicit fixture field such as region or type; rejected candidates are not silently merged. |
| RO-03 | Traverse a parent-child relationship | `get_collection` -> `list_items` -> `get_item` | Collection ID flows into the list call; item ID flows into detail; final answer preserves the hierarchy. |
| RO-04 | Locate an item beyond the first bounded page | `list_items` page 1 -> page 2 -> `get_item` | Cursor is passed unchanged; filters and ordering remain stable; no duplicate or omitted IDs; traversal stops after the target or page bound. |
| RO-05 | Join two read-only surfaces by stable identifier | `search_accounts` -> `list_records` -> `get_record` | Join uses the returned account and record IDs; incompatible entities are not combined; totals and units are preserved. |
| RO-06 | Explain a stable no-result outcome | `list_collections` -> `search_items` | Both scope and query are checked; no detail call uses a fabricated ID; final answer states the searched scope and a valid next refinement. |
| RO-07 | Recover from a fixture-defined correctable error | `resolve_name` -> failing `get_entity` -> `search_entities` -> successful `get_entity` | Error is visible and actionable; one bounded correction uses returned guidance; non-retryable errors stop without looping. |
| RO-08 | Reconcile conflicting summary and event evidence | `get_summary` -> `list_events` -> `get_event` | Stable IDs and timestamps are compared; precedence rule is applied only when defined; unresolved conflict is reported rather than hidden. |

## Tool And Result Assertions

For every tool used by the matrix, specify these checks:

1. The tool name, description, and input schema make its owned job and non-goals distinguishable from neighboring tools.
2. The proposed annotation values match the operation. A read-only tool should explicitly declare the current read-only hint expected by the verified protocol revision; open-world behavior should reflect whether it reaches external systems.
3. Annotations are tested as metadata, not treated as authorization or proof of safety. The allowed-call set remains the enforcement boundary for the evaluation.
4. Each `outputSchema` has a bounded object shape with required stable identifiers, domain values, units, provenance, and cursor fields where applicable.
5. Successful `structuredContent` validates against the declared `outputSchema`. Check any compatibility representation required by the verified protocol revision and target client.
6. Unknown fields, missing required fields, invalid enum values, wrong units, malformed identifiers, and unbounded collections fail an explicit assertion instead of being silently accepted.
7. The final answer cites which tool result supports each material conclusion and does not invent facts absent from the results.

## Pagination Assertions

- Use opaque cursors and pass a returned cursor back unchanged. Do not infer offsets or decode cursor contents.
- Keep filters, scope, and sort semantics stable across pages.
- Assert the page-size bound, maximum page count, and stop condition.
- Assert that item IDs are neither duplicated nor lost when pages are combined.
- Verify the no-next-cursor terminal case and a fixture-defined invalid or expired cursor error.
- Distinguish protocol-surface pagination from pagination exposed by a domain tool, and verify each against the current official specification or documented tool contract.

## Actionable Error Assertions

Include stable fixtures for at least one correctable and one non-correctable failure.

- Distinguish invalid protocol requests from tool execution failures according to the verified MCP revision.
- Require a concise error category, the failed field or condition, whether retry is safe, and the next valid action.
- Preserve a non-secret correlation or fixture identifier when it helps diagnosis.
- Reject errors that expose credentials, raw upstream payloads, stack traces, private paths, or customer data.
- Bound retries. Retry only when the error declares a correction path and the next arguments materially change.
- Assert that not-found, permission-denied, rate-limit, unavailable, and invalid-cursor states are not collapsed into an empty success result.

## Clean Context And Repeatability

1. Start every task in a fresh context containing only the user prompt, the selected server's tool definitions, and the declared fixture identity.
2. Do not include expected answers, previous transcripts, hidden hints, or results from another task.
3. Reset the fixture or use an immutable snapshot between trials. Pin the client, model, configuration, locale, and time zone when they affect behavior.
4. Capture the prompt, advertised tool definitions, calls, arguments, raw results, final answer, versions, timing, and assertion results.
5. Run enough isolated trials to expose nondeterministic routing when execution is later authorized. Record per-task pass rate separately from schema-only validation.

## Result Reconciliation

- Join results only on declared stable identifiers, never on display names alone.
- Preserve source, fixture revision, observation time, units, and scope through the final answer.
- Define precedence rules before the evaluation when one source is authoritative. Otherwise surface the conflict and the evidence on each side.
- Distinguish missing, empty, stale, partial, and contradictory data.
- Recompute derived counts or totals only when the contract names the formula and required fields; retain the original values for comparison.
- Fail the task when material conclusions depend on an unresolved mismatch, missing page, invalid schema, or fabricated identifier.

## Deliverable

Return the contract with:

- protocol, client, SDK, fixture, and contract versions
- official documentation URLs and checked date
- 5-10 task records using the matrix above
- per-tool annotation and `outputSchema` assertions
- pagination and error fixtures
- clean-context procedure and capture fields
- reconciliation and pass/fail rules
- provisional capabilities, unresolved design choices, and implementation blockers

Stop at this artifact. Execution, harness implementation, live calls, and network or server changes require a separate explicitly authorized workflow.
