# Application Architecture Reference

Use this reference when changing business invariants, business permission rules, state transitions, orchestration, or app structure; adding or reorganizing modules, packages, shared code, or execution boundaries; or when rules disagree across entry points. Use [identity-access.md](identity-access.md) when enforcing access, establishing identity, or managing sessions needs a decision. A routine edit inside a settled shape with unchanged rules does not need this reference.

## Business Rules And Use Cases

1. Trace the operation through UI actions, API or platform handlers, and workers. Identify the authoritative rule and every caller that can change the same business state.
2. Separate business meaning from execution: keep calculations, allowed transitions, and invariants in the existing domain code; use application orchestration for sequencing, authorization enforcement, transaction boundaries, and external side effects. Translate failures into API or UI outcomes at those boundaries. A rule may also need a database constraint to hold under concurrency.
3. Define the affected states and allowed transitions before editing. For business-critical flows, cover zero/one/many records, missing baseline, selection, locked/read-only/archived state, stale route or form state, permission denial, and retry after failure when applicable. Distinguish durable business state from transient UI state.
4. Reuse established functions and modules. Do not introduce domain classes, repositories, services, or a new process merely to reflect these conceptual responsibilities. Apply stronger structure only when the rules or reuse warrant it.
5. Verify the invariant through relevant entry points, including direct requests that bypass UI controls and workers that replay an operation. Use the data, communication, or async reference if those boundaries need further decisions.

## Good Defaults

- Preserve the existing layout and framework conventions. For greenfield work, prefer a modular monolith when one deployable unit meets the requirements; group features under their business owner and add internal layers only where rules, orchestration, or external implementations need separation.
- Keep dependencies pointing inward: UI and infrastructure depend on application and domain code, not the reverse.
- Separate orchestration from business rules. Use the application layer for workflow coordination and the domain layer for invariants and rules that must survive framework changes.

## Boundary Heuristics

- Use bounded contexts when two areas of the product use different terms, rules, actors, or release cadence.
- Keep one source of truth per business concept. Derived read models, caches, and projections should be rebuildable.
- Make trust boundaries explicit: browser or device, server edge, app core, background worker, and external systems.

## Placement And Change Boundaries

1. Inspect existing modules, actual callers and data flows, public exports, dependency rules, and build/test units before adding or moving code. Choose placement from responsibility and runtime use, not names alone. Keep folder layout, responsibility boundaries, and build or distribution units distinct; a feature does not automatically need its own package.
2. Assign each changed rule, feature, and external integration to an owning module. Group feature behavior with its focused tests; keep cross-feature invariants under their business owner. When a feature accumulates complex rules or rules recur across features, reassess ownership and consolidate the same invariant without merging merely similar behavior. Use public entry points across modules, but also inspect the actual dependency graph for new cycles or forbidden dependencies; an entry point alone does not make a dependency appropriate. Preserve runtime boundaries.
3. Add a module, package, shared component, or execution boundary only when an existing location cannot reasonably own the responsibility. State its public surface, allowed dependencies, and reason for the boundary in existing guidance or the change description; do not require a new design document for routine additions. Share code when consumers agree on its meaning and reasons for change, not merely because implementations look alike.
4. When splitting work, define each outcome, boundary contract, acceptance evidence, and dependency order. Do not equate code layers with task ownership. Settle shared-rule and contract changes before dependent feature work; separate agents are not required.
5. For replacement or removal, trace callers, registrations, configuration, tests, contracts, and persisted data. Localize replaceable implementation details without treating compatibility or migration history as disposable.
6. Run existing dependency, export, runtime-boundary, and affected-consumer checks when relevant, and verify cross-feature behavior; structural checks cannot establish semantic ownership or invariant correctness. Do not force every feature into a uniform internal pattern or introduce a monorepo tool, package split, interface, or folder solely to express these concepts.

## Pattern Selection

- Modular monolith: use the Good Defaults above when one deployable unit meets the requirements; preserve established structure in evolving products.
- Clean Architecture or ports-and-adapters: use when business logic is substantial, shared across entry points, or needs strong test seams away from infrastructure.
- Backend for Frontend: use when web, mobile, desktop, or partner clients need different aggregation, caching, auth handling, payload shape, or release cadence. Do not add a BFF just because there is a frontend.
- CQRS: use when read and write concerns genuinely diverge in workflow, consistency, scaling, or data shape. Skip it for straightforward CRUD.
- Event sourcing: use only when replayable history, auditability, temporal reconstruction, or projection rebuilds are first-class requirements. Do not combine it with CQRS by default.
- Queue-worker split: use when work is long-running, retry-heavy, rate-limited, or depends on external side effects.

## Consistency And Source Of Truth

- Prefer one clear source of truth per business concept.
- Treat caches, materialized views, search indexes, and read models as derived views with explicit freshness and rebuild expectations.
- Keep idempotency, retry safety, and failure visibility explicit whenever sync and async paths can both affect the same user-visible state.

## Quick Comparison

Use this table top to bottom and stop at the first option that fits without obvious strain.

| Option | Use when | Avoid when | Main cost |
| --- | --- | --- | --- |
| Modular monolith | The product is still evolving, one deployable unit is acceptable, and you mainly need clear module boundaries. | Independent deployment is a demonstrated requirement. | Discipline is required to keep modules from collapsing into a big ball of mud. |
| Clean Architecture | Core business rules are non-trivial, reused across flows, or need strong isolation from frameworks and data access. | The app is mostly thin CRUD around framework primitives and extra indirection would dominate the work. | More abstraction, more files, and more upfront design pressure. |
| BFF | Different clients need different payloads, auth handling, caching, or orchestration. | One UI can call the existing backend shape directly without awkward adapters. | Extra API surface and another boundary to maintain. |
| CQRS | Reads and writes have materially different shapes, performance goals, or task-based workflows. | The domain is simple and a single model remains understandable. | More moving parts, eventual consistency concerns, and projection maintenance. |
| Event sourcing | Event history itself is a product requirement and replay or reconstruction is valuable. | Current state storage is enough and historical replay is not central. | Highest complexity, especially when combined with CQRS and projections. |

## Decision Order

Escalate only when the current level is demonstrably hurting correctness, maintainability, or delivery speed.

1. Preserve established structure; for greenfield work, apply the modular-monolith defaults above when one deployable unit meets the requirements.
2. Add stronger internal boundaries only if domain rules or reuse pressure justify them.
3. Add BFF only if client-specific backend behavior is real.
4. Add CQRS only if read and write concerns truly diverge.
5. Add event sourcing only if the event log itself is a core requirement.
6. Split into services only after module boundaries and operational maturity are already proven.

## Common Failure Modes

- Jumping to Clean Architecture before there is enough domain complexity to justify the indirection.
- Adding BFF, CQRS, or event sourcing because they sound advanced instead of because the current shape is failing.
- Splitting services before the monolith has stable module boundaries, ownership, observability, and deployment maturity.
- Treating caches or projections as the source of truth instead of derived views.

## Framework-Specific Implications

- Next.js App Router: prefer one clear data access approach per codebase. For new projects, a server-only data access layer is usually cleaner than mixing ad hoc fetches, direct database calls, and public endpoints everywhere.
- Android: default to UI and data layers, and add the domain layer only when logic is complex or reused. Keep unidirectional data flow and state holders explicit.
- Service-backed web apps: keep processes stateless, keep session and durable state outside process memory, and avoid designs that rely on sticky sessions.

## Escalation Triggers

- Stay monolithic when boundaries are still being discovered.
- Consider service extraction only after module boundaries are stable, operational maturity exists, and independent deployment creates real value.
- If the design discussion dominates the task and no shipped app change is ready, route to `product-designer` or another design-focused skill instead of stretching implementation work.
