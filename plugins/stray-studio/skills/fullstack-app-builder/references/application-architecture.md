# Application Architecture Reference

Use this reference when the task depends on choosing or refining app structure, not just editing code inside an already-settled shape.

## Good Defaults

- Start with a layered modular monolith unless the repository already has proven service boundaries.
- Keep dependencies pointing inward: UI and infrastructure depend on application and domain code, not the reverse.
- Separate orchestration from business rules. Use the application layer for workflow coordination and the domain layer for invariants and rules that must survive framework changes.

## Boundary Heuristics

- Use bounded contexts when two areas of the product use different terms, rules, actors, or release cadence.
- Keep one source of truth per business concept. Derived read models, caches, and projections should be rebuildable.
- Make trust boundaries explicit: browser or device, server edge, app core, background worker, and external systems.

## Pattern Selection

- Layered modular monolith: default for most greenfield or evolving products.
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
| Layered modular monolith | The product is still evolving, one deployable unit is acceptable, and you mainly need clear module boundaries. | You already have multiple clients or teams that truly need separate contracts or release cadence. | Discipline is required to keep modules from collapsing into a big ball of mud. |
| Clean Architecture | Core business rules are non-trivial, reused across flows, or need strong isolation from frameworks and data access. | The app is mostly thin CRUD around framework primitives and extra indirection would dominate the work. | More abstraction, more files, and more upfront design pressure. |
| BFF | Different clients need different payloads, auth handling, caching, or orchestration. | One UI can call the existing backend shape directly without awkward adapters. | Extra API surface and another boundary to maintain. |
| CQRS | Reads and writes have materially different shapes, performance goals, or task-based workflows. | The domain is simple and a single model remains understandable. | More moving parts, eventual consistency concerns, and projection maintenance. |
| Event sourcing | Event history itself is a product requirement and replay or reconstruction is valuable. | Current state storage is enough and historical replay is not central. | Highest complexity, especially when combined with CQRS and projections. |

## Decision Order

Escalate only when the current level is demonstrably hurting correctness, maintainability, or delivery speed.

1. Start with a layered modular monolith.
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
