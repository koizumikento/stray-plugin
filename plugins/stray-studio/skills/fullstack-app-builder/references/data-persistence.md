# Data And Persistence Reference

Read this when changing schema, queries, persistence, or migrations, or diagnosing concurrent writes, integrity, or database performance. Skip it when the change does not depend on persistence behavior. Use existing database and data-access conventions.

## Workflow

1. Trace the data and its writers.
   - Identify the authoritative store, keys, tenant/resource ownership, relationships, generated types, queries, caches, and every API, worker, or local-client path that writes the same state.
   - State the business invariant and which updates must succeed together. Distinguish stored facts from rebuildable caches, projections, search indexes, and derived UI values.
2. Enforce invariants at the storage boundary.
   - Prefer supported unique, foreign-key, check, or equivalent constraints over a read-then-write application check that can race.
   - Choose transaction scope, conditional updates, version checks, locks, or isolation according to the actual competing operations. Keep transaction duration bounded and avoid holding locks across remote calls.
   - Inspect the database's actual isolation guarantees. A transaction alone does not make a multi-step operation safe under all concurrent schedules. For example, PostgreSQL Read Committed can see different committed data on successive reads. See [PostgreSQL transaction isolation](https://www.postgresql.org/docs/18/transaction-iso.html).
   - When a serialization or deadlock retry is required, retry the appropriate transaction with a bounded policy; do not repeat an external side effect as though it rolled back with the database.
3. Persist safe command outcomes when replay is possible.
   - Scope idempotency records to the operation and authorized subject or tenant. Make concurrent claims atomic; reject reuse of a key with a different payload according to the API contract.
   - Store the local side effect and command result in the same transaction or equivalent atomic boundary where supported. Preserve enough result data for first and replayed success to satisfy the same application contract and render consistently.
   - Name partial-write failure modes when atomicity is unavailable. A database commit cannot make an unrelated remote write atomic; consult the API or async reference before choosing coordination or recovery.
4. Make migrations reviewable and compatible.
   - Use versioned migrations for non-trivial schema changes. Treat schema changes and backfills as operational events; prefer additive changes before destructive or shape-tightening ones.
   - Check existing data, constraint cleanup, old/new code coexistence, rollout order, and rollback feasibility. Surface backfills, dual reads/writes, or repair scripts instead of hiding them in feature code.
   - Distinguish generating a migration, applying it locally, pending migrations, and applying it remotely. Use only the environments and effects covered by the task's authorization.
   - Check stale fields, wildcard selections, generated types, queries, fixtures, and runtime contracts after schema changes; compilation alone may miss drift.
5. Preserve read correctness and freshness.
   - Define invalidation or refresh after writes, and which reads may lag. Verify derived totals, caches, and UI against persisted state.
   - For performance work, inspect representative query plans, data volumes, indexes, and connection-pool limits before adding caches or indexes.
   - For offline writes, identify durable local changes, versions, deletion markers, and the authoritative reconciliation outcome. Use the async reference when reconciliation or replay needs design.
6. Validate the changed guarantees.
   - Use the real database's behavior where feasible for concurrent updates, duplicate commands, rollback, and migrations. Mocks alone cannot establish isolation or constraint behavior.
   - Verify relevant read-after-write and replayed-result contracts, including the app's response to a rejected conflict. Exercise representative existing data when constraints tighten.
   - Report migration status, proven guarantees, and any environment or concurrency checks left unverified.
