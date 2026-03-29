---
name: "fullstack-web-app-builder"
description: "Use when the user wants to build, modify, or debug a full-stack web application in the current repository, including pages, routes, components, forms, state, API endpoints, server actions, authentication, authorization, sessions, database-backed flows, migrations, observability, and user-facing features that should end in working code. Do not use for product strategy, pure visual theming, marketing assets, native apps, or backend platform work that has no direct web-app flow to ship."
---

# Fullstack Web App Builder

Build or modify a full-stack web application in the current repository and carry the work through implementation, validation, and a concise handoff. Focus on shipped code, not just advice. Treat a web app feature as an end-to-end flow that spans UI, server behavior, data, security, and operational checks.

Use this skill when the user wants to:

- add or change pages, routes, or layouts
- build frontend features, flows, and interactions
- wire UI to APIs, server actions, auth, background handlers, or data-fetching layers
- add or change backend behavior that directly serves the web app, such as validation, persistence, sessions, permissions, or request handlers
- implement end-to-end flows that cross frontend, backend, and database boundaries
- fix web app bugs in rendering, state, validation, auth, data integrity, responsiveness, accessibility, or performance
- scaffold a small web app when the repository does not already contain one and the user explicitly wants implementation

## Do Not Use For

- product strategy, feature definition, or market-backed direction setting
- pure visual theming, screenshot creation, or marketing asset work
- browser-based research tasks
- native mobile, desktop, or non-web application development
- backend-only services, infra work, or protocol design with no web-app flow to ship

## Core Principles

- Start from the user flow, not from the database table or endpoint list.
- Prefer the existing framework, architecture, and conventions over introducing a new stack shape.
- Keep the server as the source of truth for security-critical decisions.
- Validate on both client and server: client validation for UX, server validation for correctness and security.
- Enforce authorization explicitly and deny by default.
- Treat auth, sessions, schema changes, and observability as part of the shipped feature when the flow depends on them.
- Favor incremental, backward-compatible changes over broad rewrites.
- Verify user-visible behavior across the stack before calling the work done.

## Framework Policy

- If the repository already uses a web framework, follow that framework's conventions for routing, rendering, data loading, mutations, auth integration, and testing.
- Do not introduce a new framework or router when the existing stack can satisfy the request.
- Do not perform framework migration work unless the user explicitly asks for migration or re-platforming.
- When the request is greenfield and the framework is unspecified, choose the smallest credible stack for the requested outcome instead of defaulting to a heavy or trendy setup.
- Prefer boring, well-supported primitives over clever framework-specific abstractions when the codebase does not already depend on them.
- When framework conventions conflict with generic best practices, prefer the framework's safe default unless there is a concrete correctness, security, or maintainability reason to override it.

## Quality Tooling Policy

- Follow the repository's existing lint, type-check, and test commands first when they are already established and working.
- If the repository does not have a clear quality toolchain, prefer the language's de facto standard tools instead of inventing a custom stack.
- Do not force a tooling migration for a small feature or bug fix unless the user explicitly asks for it.
- Report which lint, type-check, and test gates were run, skipped, unavailable, or left unchanged.

### Language Defaults

- Go: prefer `gofmt` for formatting, `go test` for tests, and `go vet` for built-in static checks. If the repository already uses `golangci-lint`, follow it rather than introducing a parallel lint stack.
- Python: prefer `ruff` for linting and formatting checks, `ty` for static type checking, and `pytest` for tests.
- Rust: prefer `cargo fmt` for formatting, `cargo clippy` for linting and static checks, and `cargo test` for tests.
- TypeScript and JavaScript: prefer `Vite+` as the default quality baseline when the repo is greenfield or the toolchain is still unsettled.
- TypeScript and JavaScript: in practice, prefer `vp check` for formatting, linting, and type checking, and `vp test` for tests.
- TypeScript and JavaScript: if the repository already has an established stack, do not replace it with `Vite+` unless the user explicitly wants that migration.

## Runtime And Package Management Policy

- Follow the repository's existing runtime, package manager, lockfile, and local environment workflow first when it is already established.
- Do not introduce a package manager, version manager, or environment manager migration for a small feature or bug fix unless the user explicitly asks for it.
- For greenfield or unsettled repositories, prefer one clear package and environment workflow per language instead of mixing overlapping tools.
- Report which runtime, package manager, environment manager, or reproducibility layer the work assumed.

### Environment And Dependency Defaults

- Python: prefer `uv` for both environment and package management, including `uv sync`, `uv lock`, and `uv run`, unless the repository already uses a different established workflow.
- TypeScript and JavaScript: if `Vite+` is the chosen baseline for a greenfield or unsettled repository, keep the package and quality workflow consistent with that toolchain instead of mixing ad hoc alternatives.
- Go: prefer the standard Go toolchain and module system already defined by the repository.
- Rust: prefer the standard Cargo toolchain already defined by the repository.
- Nix: if the repository already uses Nix, follow it for shell, toolchain, and reproducible environment setup.
- Nix: consider it for greenfield or multi-language repositories only when reproducibility and cross-machine consistency are important enough to justify the added operational weight.
- Nix: do not introduce it for a small change unless the user explicitly asks for it or the repository already depends on it.

## Security And Data Expectations

- Never trust client input by itself. Re-validate on the server.
- Keep authentication and authorization separate in the design and implementation.
- Prefer established auth protocols and libraries over hand-rolled auth flows.
- Apply least privilege and resource-level checks instead of relying only on coarse roles.
- Use secure session and cookie handling when sessions are involved.
- Keep secrets and environment-specific config out of source-controlled code.
- Prefer committed, versioned, reviewable database migrations for non-trivial schema changes.
- Make write paths observable enough to debug failures and investigate incidents.

## Data Change Safety

- Treat schema, backfill, and persistence changes as operational events, not just code edits.
- Prefer additive, backward-compatible schema changes before destructive or shape-tightening ones.
- When tightening constraints, think through deploy order, existing data cleanup, and how old and new code will coexist during rollout.
- Surface any need for backfills, dual reads, dual writes, or one-time repair scripts instead of hiding them inside the feature work.

## Release And Rollout Policy

- Prefer backward-compatible changes that can be rolled out safely without breaking existing clients, sessions, or stored data.
- When a change affects auth, schema, caching, or a business-critical flow, think through rollout order, rollback path, and failure mode before shipping.
- Use feature flags, staged rollout patterns, or guarded code paths when the repository or product already supports them and the risk justifies the extra control.
- Do not hide release risk. Surface any change that requires coordination, sequencing, downtime planning, or data backfill.

## Caching And Idempotency

- When a flow depends on caches, revalidation, deduplication, retries, or repeated submissions, treat those behaviors as part of correctness rather than as optional optimization.
- Make cache invalidation and freshness expectations explicit at the boundary where data is read and written.
- Design write paths and async triggers to be safe under retry or duplicate delivery when the surrounding system can replay them.
- Call out any operation that is not idempotent or that can leave the user-visible state inconsistent if retried midway.

## API And Contract Policy

- Treat contracts between UI, server handlers, APIs, jobs, and persistence layers as first-class design boundaries.
- Make input and output shapes explicit in code and keep validation close to the contract boundary.
- Prefer additive and backward-compatible contract changes over breaking ones.
- When a breaking contract change is unavoidable, call it out clearly and update all affected callers in the same change when feasible.

## Dependency Policy

- Prefer existing dependencies and platform primitives when they already solve the problem well enough.
- Add a new dependency only when it meaningfully improves correctness, safety, maintainability, or delivery speed.
- Avoid overlapping libraries that create competing ways to solve the same problem inside one repository.
- When introducing a dependency, consider maintenance health, ecosystem fit, security posture, and how hard it will be to remove later.

## Background Jobs And Async Work

- If the shipped flow depends on queues, emails, webhooks, scheduled work, or retries, treat that async behavior as part of the feature rather than an implementation detail.
- Make trigger conditions, retry behavior, idempotency expectations, and failure visibility explicit.
- Do not assume asynchronous work succeeded just because the synchronous request returned successfully.
- Verify the user-visible consequence of async work or state clearly what could not be verified.

## Workflow

1. Frame the user-facing change before editing.
   - Identify the framework, runtime, routing model, styling approach, and test setup.
   - Find the entry points, affected flows, trust boundaries, data model boundaries, and any backend or API assumptions.
   - Stop if the request is design-only, research-only, or not actually about a web app.

2. Follow the existing app before inventing a new one.
   - Read the current structure for routes, components, server handlers, data access, styling, and state.
   - Preserve established patterns unless the user asks for a deliberate change.
   - If the repo lacks a web app, choose the smallest implementation shape that satisfies the request.

3. Design the smallest coherent slice.
   - Define the UI states, request flow, validation, auth rules, authorization rules, persistence, loading, error, and empty states.
   - Prefer incremental end-to-end changes over broad rewrites.
   - Keep frontend, backend, and database boundaries explicit when cross-layer changes are uncertain or out of scope.
   - Decide what must be observable in logs, traces, metrics, or audit events for the changed flow.

4. Implement the flow end to end.
   - Update components, routes, styles, types, request handlers, API wiring, and persistence as needed.
   - Keep semantics, copy, and interaction details intentional.
   - Add or update tests when the codebase already uses them or when the changed behavior is easy to lock down.
   - Treat schema changes, auth changes, session handling, authorization checks, and data migrations as part of the job when the shipped flow depends on them.

5. Validate with the right level of evidence.
   - Run targeted tests, lint, typecheck, build, migration checks, API checks, or browser checks when they fit the stack.
   - Verify the main user path across the stack, not just isolated functions.
   - Check that validation, auth, authorization, error handling, and rollback behavior match the intended flow.
   - Check user-visible accessibility and performance concerns when the changed surface area makes them relevant.
   - Report what was validated and what could not be validated.

6. Hand off clearly.
   - Summarize the user-visible result, key implementation decisions, and any residual risks.
   - Call out follow-up work only when it materially affects correctness, data safety, performance, observability, or maintainability.
   - If the work expands into product framing, route to `product-designer` instead of stretching this skill.

## Validation Expectations

- Prefer tests that cover user-visible behavior and real flow boundaries.
- Keep tests isolated and avoid depending on flaky third-party systems when the codebase has a better seam.
- Include negative-path checks when changing auth, validation, permissions, or persistence.
- When migrations are involved, check both forward application and operational safety assumptions.
- If the main path cannot be verified locally, say exactly what remains unproven.

## Documentation And Handoff

- Update local docs, runbooks, API notes, env var docs, or setup instructions when the change materially alters how the system is operated, configured, or extended.
- Keep handoff notes short but concrete: what changed, how it was verified, what remains risky, and what operators or reviewers should watch next.
- If the change introduces a new required dependency, environment variable, migration step, or rollout concern, include it in the handoff.
- Do not leave operationally important knowledge only in code comments or commit context.

## Output Expectations

- Working code changes or a concrete blocker report
- A short summary of what changed for the user
- Validation results with any important cross-stack gaps
- Explicit assumptions, risks, or follow-up items when relevant
- Notes on security, data, or observability implications when the change touches them

## Guardrails

- Do not treat a broad product discussion as implementation work.
- Do not rewrite the stack or design system without a clear reason.
- Do not skip loading, error, empty, responsive, or accessibility states when the changed UI needs them.
- Do not make backend, schema, or auth changes without checking how they affect the shipped user flow.
- Do not rely on client-only validation or client-only authorization.
- Do not add opaque data migrations or destructive production-only changes without surfacing the risk.
- Do not ship flows that cannot be debugged because no useful logs, traces, or metrics exist.
- Do not absorb unrelated platform or infrastructure work unless the web app change directly depends on it.
- Do not stop at code changes without checking whether the main end-to-end flow actually works.
