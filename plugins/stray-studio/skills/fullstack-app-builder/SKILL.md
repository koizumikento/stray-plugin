---
name: "fullstack-app-builder"
description: "Use when the user wants to build, modify, or debug a full-stack application in the current repository, including web, mobile, desktop, or hybrid user-facing surfaces, their screens or views, navigation, forms, local state, API endpoints, background work, authentication, authorization, sessions, database-backed flows, migrations, observability, and shipped features that should end in working code. Do not use for product strategy, pure visual theming, marketing assets, backend platform work with no shipped app flow, or standalone library work."
---

# Fullstack App Builder

Build or modify a full-stack application in the current repository and carry the work through implementation, validation, and a concise handoff. Focus on shipped code, not just advice. Treat an app feature as an end-to-end flow that spans the user surface, server behavior, data, security, and operational checks.

Use this skill when the user wants to:

- add or change screens, routes, views, layouts, or windows
- build client-side features, interactions, forms, navigation, or local state
- wire app UI to APIs, server actions, auth, background handlers, device or OS integrations, or data-fetching layers
- add or change backend behavior that directly serves the shipped app experience
- implement end-to-end flows that cross client, backend, and database boundaries
- fix app bugs in rendering, state, validation, auth, permissions, sync, offline behavior, responsiveness, accessibility, or performance
- scaffold a small full-stack app when the repository does not already contain one and the user explicitly wants implementation

## Do Not Use For

- product strategy, feature definition, or market-backed direction setting
- pure visual theming, screenshot creation, or marketing asset work
- browser-based research tasks
- read-only PR, branch, diff, staged-change, or specification reviews where the user explicitly asks for findings instead of implementation
- backend-only services, infra work, or protocol design with no shipped user-facing app flow
- standalone libraries, SDKs, or packages that are not part of a shipped app flow

## Core Principles

- Start from the user surface and user flow, not from the database table or endpoint list.
- Prefer the existing framework, architecture, and surface conventions over introducing a new stack shape.
- Keep trust boundaries and privileged operations on the secure side of the app boundary.
- Validate on both client and server: client validation for UX, server validation for correctness and security.
- Enforce authorization explicitly and deny by default.
- Treat auth, permissions, sessions, schema changes, background work, and observability as part of the shipped feature when the flow depends on them.
- Favor incremental, backward-compatible changes over broad rewrites.
- Verify user-visible behavior on the actual target surface before calling the work done.
- Treat unfinished UI, unconnected controls, no-op handlers, placeholder copy, and silent mutations as correctness problems, not cosmetic leftovers.
- Keep implementation and review modes separate: when the user asks for review only, route to the relevant review skill instead of editing.
- When the user's desired behavior is ambiguous, surface the decision points and choose a reversible default only when the change can safely proceed.
- Treat "first investigate", "first check", "first plan", and similar phrasing as an intent gate. Gather evidence and stop with findings or a plan until the user asks to implement.
- For business workflows, model domain states explicitly instead of testing only the happy path. Missing baseline data, one-item cases, locked records, archived records, stale selections, and read-only modes often change the correct behavior.

## Surface And Framework Policy

- Identify the primary surface first: web, mobile, desktop, or hybrid.
- If the repository already uses a framework on that surface, follow its conventions for navigation, rendering, state, data loading, packaging, auth integration, and testing.
- Do not introduce a new surface architecture, router, packaging model, or state model when the existing stack can satisfy the request.
- Do not perform framework or surface migration work unless the user explicitly asks for migration or re-platforming.
- When the request is greenfield and the surface is unspecified, choose the smallest credible surface and stack for the requested outcome instead of defaulting to a heavy or trendy setup.
- Prefer boring, well-supported primitives over clever surface-specific abstractions when the codebase does not already depend on them.
- When surface conventions conflict with generic best practices, prefer the framework or platform's safe default unless there is a concrete correctness, security, or maintainability reason to override it.

## Architecture Reference Policy

- Keep this skill implementation-first. When structure decisions matter, load `references/application-architecture.md` instead of expanding the main workflow into a long architecture discussion.
- Default to the repository's existing structure, or a layered modular monolith when the repo is greenfield and service boundaries are not yet proven.
- Name the chosen app shape before coding and keep UI, application, domain, and infrastructure boundaries explicit when they materially affect the change.

## Quality Tooling Policy

- Follow the repository's existing lint, type-check, and test commands first when they are already established and working.
- When the primary app implementation language is TypeScript or JavaScript, load `references/typescript-javascript.md` before choosing validation commands.
- For TypeScript or JavaScript work, explicitly check whether the repository uses `vp check` or `vp test` before falling back to package-manager scripts.
- When the primary app implementation language is Python, load `references/python.md` before choosing validation, runtime, or package-management commands.
- For Python work, explicitly check whether `uv`, `ruff`, `ty`, and `pytest` fit the repository before falling back to other established commands.
- When the primary app implementation language is Go, load `references/go.md` before choosing validation, runtime, or package-management commands.
- For Go work, explicitly check whether `gofmt`, `go test`, `go vet`, and `golangci-lint` fit the repository before falling back to other established commands.
- When the primary app implementation language is Rust, load `references/rust.md` before choosing validation, runtime, or package-management commands.
- For Rust work, explicitly check whether `cargo fmt`, `cargo clippy`, `cargo test`, pinned toolchains, and Nix fit the repository before falling back to other established commands.
- If the repository does not have a clear quality toolchain, prefer the language's de facto standard tools instead of inventing a custom stack.
- Do not force a tooling migration for a small feature or bug fix unless the user explicitly asks for it.
- Report which lint, type-check, and test gates were run, skipped, unavailable, or left unchanged.

## Runtime And Package Management Policy

- Follow the repository's existing runtime, package manager, lockfile, and local environment workflow first when it is already established.
- Do not assume bare executables such as `python`, `pytest`, `node`, framework CLIs, or deploy CLIs are available globally. Find the repository command, package-local binary, runtime manager, or workspace wrapper first.
- Do not introduce a package manager, version manager, or environment manager migration for a small feature or bug fix unless the user explicitly asks for it.
- For greenfield or unsettled repositories, prefer one clear package and environment workflow per language instead of mixing overlapping tools.
- Report which runtime, package manager, environment manager, packaging flow, or reproducibility layer the work assumed.
- When surface-specific or ecosystem-specific defaults matter, consult the smallest relevant reference instead of bloating this file with stack-specific policy.
- Do not let a reference override clear repository conventions.
- On Windows, account for `.cmd` shims, PowerShell command behavior, path quoting, and workspace-local tools before declaring a command unavailable.
- When local and CI or deploy environments differ, state which environment the command proves and which remains unverified.
- Check local secret/config conventions before running app, migration, or deploy commands. Distinguish tracked examples from ignored local secrets, and do not rename or expose secret files casually.

## Security And Data Expectations

- Never trust client input by itself. Re-validate on the server or privileged boundary.
- Keep authentication and authorization separate in the design and implementation.
- Prefer established auth protocols and libraries over hand-rolled auth flows.
- Apply least privilege and resource-level checks instead of relying only on coarse roles.
- Use secure session, token, cookie, keychain, or local secret handling when credentials are involved.
- Keep secrets and environment-specific config out of source-controlled code.
- Prefer committed, versioned, reviewable database migrations for non-trivial schema changes.
- Make write paths observable enough to debug failures and investigate incidents.

## Data Change Safety

- Treat schema, backfill, and persistence changes as operational events, not just code edits.
- Prefer additive, backward-compatible schema changes before destructive or shape-tightening ones.
- When tightening constraints, think through deploy order, existing data cleanup, and how old and new code will coexist during rollout.
- Surface any need for backfills, dual reads, dual writes, or one-time repair scripts instead of hiding them inside the feature work.
- For migrations, distinguish clearly between generating migration files, applying them locally, confirming pending or unapplied migrations, and applying them to remote or production-like environments.
- Check code and query contracts after schema work for stale fields, wildcard selection assumptions, generated types, fixture drift, and runtime-only failures that type-checking may not catch.
- When a schema change is intentionally not applied, say which behavior remains unproven and what command or environment would prove it.

## Release And Rollout Policy

- Prefer backward-compatible changes that can be rolled out safely without breaking existing clients, sessions, stored data, or local installations.
- When a change affects auth, schema, caching, device permissions, packaging, or a business-critical flow, think through rollout order, rollback path, and failure mode before shipping.
- Use feature flags, staged rollout patterns, or guarded code paths when the repository or product already supports them and the risk justifies the extra control.
- Do not hide release risk. Surface any change that requires coordination, sequencing, downtime planning, store review, installer updates, or data backfill.

## Caching And Idempotency

- When a flow depends on caches, revalidation, deduplication, retries, offline sync, or repeated submissions, treat those behaviors as part of correctness rather than as optional optimization.
- Make cache invalidation and freshness expectations explicit at the boundary where data is read and written.
- Design write paths and async triggers to be safe under retry or duplicate delivery when the surrounding system can replay them.
- Call out any operation that is not idempotent or that can leave the user-visible state inconsistent if retried midway.
- For idempotent command flows, verify that the first successful response and replayed response have the same contract shape and enough persisted data for the UI to render identically.
- Keep the side effect and the stored command result in the same transaction or equivalent atomic boundary when the platform supports it. If not, call out the partial-write failure mode.
- Check that failed, canceled, or partially completed writes cannot reserve an idempotency key forever, replay stale input as if it were saved output, or hide a retryable error from the user.

## Source Of Truth Policy

- Identify which local artifact is authoritative before implementing behavior: product spec, issue, AGENTS guidance, design-system doc, wireframe, migration, API contract, or existing production behavior.
- If docs, implementation, tests, and review instructions disagree, pause long enough to name the drift and choose the smallest alignment path before writing more code.
- Keep source-of-truth updates in the same change when the implementation intentionally changes behavior that docs, tests, design-system rules, or AGENTS guidance describe.
- Do not paper over drift with code comments. Update the artifact users and future agents will actually consult.
- For design-system or shared component work, verify export inventory, CSS ownership, app usage, tests, and documentation together instead of treating a passing build as proof of alignment.

## API And Contract Policy

- Treat contracts between UI, platform bridges, server handlers, APIs, jobs, and persistence layers as first-class design boundaries.
- Make input and output shapes explicit in code and keep validation close to the contract boundary.
- Prefer additive and backward-compatible contract changes over breaking ones.
- When a breaking contract change is unavoidable, call it out clearly and update all affected callers in the same change when feasible.

## Dependency Policy

- Prefer existing dependencies and platform primitives when they already solve the problem well enough.
- Add a new dependency only when it meaningfully improves correctness, safety, maintainability, or delivery speed.
- Avoid overlapping libraries that create competing ways to solve the same problem inside one repository.
- When introducing a dependency, consider maintenance health, ecosystem fit, security posture, and how hard it will be to remove later.

## Background Jobs And Async Work

- If the shipped flow depends on queues, emails, webhooks, scheduled work, sync engines, background tasks, or retries, treat that async behavior as part of the feature rather than an implementation detail.
- Make trigger conditions, retry behavior, idempotency expectations, and failure visibility explicit.
- Do not assume asynchronous work succeeded just because the synchronous request returned successfully.
- Verify the user-visible consequence of async work or state clearly what could not be verified.

## Workflow

1. Frame the user-facing change before editing.
   - Identify the primary surface, framework, runtime, navigation model, state model, styling approach, packaging flow, and test setup.
   - Confirm whether the user asked for implementation, planning, investigation, or review-only feedback. Stop with findings or a plan when the user says "first", "まずは", "investigate", "check", or "plan" and has not asked for implementation yet.
   - Stop and route to a review skill when the request is read-only review.
   - Load the smallest relevant surface reference and ecosystem reference when stack-specific defaults matter.
   - If the app is primarily TypeScript or JavaScript, load `references/typescript-javascript.md` even when the stack otherwise looks familiar.
   - If the app is primarily Python, load `references/python.md` even when the framework otherwise looks familiar.
   - If the app is primarily Go, load `references/go.md` even when the framework otherwise looks familiar.
   - If the app is primarily Rust, load `references/rust.md` even when the framework otherwise looks familiar.
   - Load the architecture reference when deciding layer shape, bounded contexts, BFF use, read versus write separation, async boundaries, or whether the repo should stay monolithic.
   - Load the observability reference when the changed flow needs new or revised logs, traces, metrics, crash signals, or audit events.
   - Find the entry points, affected flows, trust boundaries, data model boundaries, and any backend or platform assumptions.
   - Read the nearest `AGENTS.md`, app docs, product specs, design-system docs, and existing issue or PR context that define the behavior. Treat these as source-of-truth inputs, not optional background.
   - If the user explicitly asks for subagents or parallel review, split only independent read-only or disjoint implementation work, and keep ownership boundaries clear.
   - Stop if the request is design-only, research-only, or not actually about a shipped app flow.

2. Follow the existing app before inventing a new one.
   - Read the current structure for screens, routes, views, windows, components, server handlers, data access, styling, state, and platform glue.
   - Preserve established patterns unless the user asks for a deliberate change.
   - If the repo lacks an app, choose the smallest implementation shape that satisfies the request on the target surface.
   - Before implementation, search for related TODOs, placeholders, stubs, disabled controls, no-op handlers, dead routes, and existing partial implementations that could make the new flow appear complete while still being unusable.

3. Design the smallest coherent slice.
   - Name the intended app shape before coding: existing repo pattern, layered modular monolith, Clean Architecture slice, BFF-backed flow, or queue-worker split.
   - Define the UI states, navigation transitions, request flow, validation, auth rules, authorization rules, persistence, loading, error, empty, and offline states when relevant.
   - Build a small domain-state matrix for business-critical flows. Include zero/one/many records, missing baseline or active record, selected versus unselected item, locked/read-only/archived states, stale route or form state, permission denied, and retry after failure when those states can occur.
   - Decide which rules belong in UI, application orchestration, domain logic, infrastructure adapters, and background workers. Keep these boundaries explicit in code.
   - Decide whether a domain boundary or bounded context split is actually needed or whether a single module is enough for the change.
   - Prefer incremental end-to-end changes over broad rewrites.
   - Keep client, backend, database, and platform boundaries explicit when cross-layer changes are uncertain or out of scope.
   - Decide what must be observable in logs, traces, metrics, crash reports, or audit events for the changed flow.
   - If the requested behavior admits multiple credible UX or data interpretations, list the choice points briefly, state the assumption you will implement, and prefer the option that preserves existing data and user escape hatches.
   - For forms and write flows, decide when the input surface appears, how the user enters create, edit, bulk update, recovery, or settings intent, how they cancel, and how successful or failed mutations are acknowledged.

4. Implement the flow end to end.
   - Update screens, components, routes, windows, styles, types, request handlers, API wiring, persistence, and platform integrations as needed.
   - Keep semantics, copy, and interaction details intentional.
   - Add or update tests when the codebase already uses them or when the changed behavior is easy to lock down.
   - Treat schema changes, auth changes, session handling, authorization checks, deep links, IPC bridges, device permissions, and data migrations as part of the job when the shipped flow depends on them.
   - Do not leave a feature at "looks wired" if the primary action does not persist, navigate, invalidate data, surface errors, or update state as the user would expect.
   - Remove or replace scaffolding and placeholder UI that would confuse users or reviewers unless the user explicitly asked for a visible stub.

5. Validate with the right level of evidence.
   - Run targeted tests, lint, typecheck, build, migration checks, packaging checks, simulator or emulator checks, browser checks, or desktop runtime checks when they fit the stack.
   - For TypeScript or JavaScript work, include the `vp check` and `vp test` decision in the validation pass: run them when available and appropriate, or state the repository-specific reason for using different commands.
   - For Python work, include the `uv`, `ruff`, `ty`, and `pytest` decision in the validation pass: run the relevant tools when available and appropriate, or state the repository-specific reason for using different commands.
   - For Go work, include the `gofmt`, `go test`, `go vet`, and `golangci-lint` decision in the validation pass: run the relevant tools when available and appropriate, or state the repository-specific reason for using different commands.
   - For Rust work, include the `cargo fmt`, `cargo clippy`, `cargo test`, pinned toolchain, and Nix decision in the validation pass: run the relevant tools when available and appropriate, or state the repository-specific reason for using different commands.
   - Verify the main user path on the actual target surface, not just isolated functions.
   - Check that validation, auth, authorization, navigation, error handling, retry behavior, and rollback behavior match the intended flow.
   - Check user-visible accessibility, responsiveness, lifecycle, and platform-specific concerns when the changed surface area makes them relevant.
   - Exercise the domain-state matrix for the changed flow, especially missing baseline, single-record, read-only, archived, and stale-selection cases that often look fine in the default seeded path.
   - For UI changes, run or open the app on the real target surface when feasible and inspect the affected flow at the relevant desktop and mobile viewports.
   - When a dev server is needed, start it or reuse an existing one, visit the actual route, and report the local URL. If the server cannot run, report the exact blocker.
   - Check for overlapping text or controls, broken focus order, hidden primary actions, stale data after mutation, duplicate submission, silent success or failure, and empty or loading states that strand the user.
   - After implementation, repeat a focused unfinished-work scan for placeholders, TODOs, disabled actions, no-op handlers, and newly stale docs or specs in the touched area.
   - Report what was validated and what could not be validated.

6. Hand off clearly.
   - Summarize the user-visible result, key implementation decisions, and any residual risks.
   - Call out follow-up work only when it materially affects correctness, data safety, performance, observability, or maintainability.
   - Include the route, local URL, command, migration status, deployment status, and any reload or cache caveat that affects how the user can verify the result.
   - If the user requested a review loop, report whether subagent or reviewer findings remain, what was fixed, and what was intentionally deferred.
   - If the work expands into product framing, route to `product-designer` instead of stretching this skill.

## Validation Expectations

- Prefer tests that cover user-visible behavior and real flow boundaries.
- Keep tests isolated and avoid depending on flaky third-party systems when the codebase has a better seam.
- Include negative-path checks when changing auth, validation, permissions, persistence, or platform bridges.
- When migrations are involved, check both forward application and operational safety assumptions.
- For browser UI changes, prefer at least one real render check of the changed route or component state. Use screenshots, browser automation, or manual inspection through the app when the repository supports it.
- For responsive surfaces, verify the smallest relevant mobile width and a normal desktop width when the layout, density, navigation, or form surface changed.
- For write flows, verify pending, success, error, and duplicate-submit behavior whenever the affected code makes those states possible.
- For data-backed flows, verify the read-after-write path, cache invalidation or revalidation, and any generated types or query contracts touched by the change.
- For baseline-dependent, selection, approval, import, bulk edit, and review workflows, verify baseline-missing, one-item, many-item, no-difference, read-only, archived, and permission-denied states when those states exist in the domain.
- For source-of-truth changes, verify that docs, tests, shared exports, CSS boundaries, and implementation agree where the changed behavior crosses those artifacts.
- If the main path cannot be verified locally, say exactly what remains unproven.

## Documentation And Handoff

- Update local docs, runbooks, API notes, env var docs, setup instructions, or release notes when the change materially alters how the system is operated, configured, packaged, or extended.
- Keep handoff notes short but concrete: what changed, how it was verified, what remains risky, and what operators or reviewers should watch next.
- If the change introduces a new required dependency, environment variable, migration step, permission, packaging step, or rollout concern, include it in the handoff.
- Include the command and URL needed to inspect the changed app surface when a local app was run.
- If deployment, remote migration, external service verification, or production-like testing was not performed, say that directly and explain the practical impact.
- Separate "implemented", "reviewed", "merged", "deployed", and "migrated" status. Do not let a successful local build imply a remote deployment or database migration happened.
- Do not leave operationally important knowledge only in code comments or commit context.

## Output Expectations

- Working code changes or a concrete blocker report
- A short summary of what changed for the user
- The chosen architecture shape when it materially affected the implementation
- Validation results with any important cross-stack gaps
- Any source-of-truth drift found and how it was resolved or deferred
- The exact route, screen, command, or URL used for user-visible verification when applicable
- Explicit assumptions, risks, or follow-up items when relevant
- Notes on security, data, platform, or observability implications when the change touches them

## Guardrails

- Do not treat a broad product discussion as implementation work.
- Do not treat review-only prompts as permission to edit.
- Do not implement after a "first investigate/check/plan" request unless the user also clearly asks for code changes in the same turn.
- Do not rewrite the stack, surface architecture, or design system without a clear reason.
- Do not leave visible placeholder experiences, disabled primary actions, or no-op handlers unless the user explicitly asked for a staged stub.
- Do not ignore docs, design-system, AGENTS, migration, or test drift just because the code compiles.
- Do not skip loading, error, empty, responsive, accessibility, lifecycle, or platform states when the changed UI needs them.
- Do not make backend, schema, auth, or permission changes without checking how they affect the shipped user flow.
- Do not rely on client-only validation or client-only authorization.
- Do not add opaque data migrations or destructive production-only changes without surfacing the risk.
- Do not ship flows that cannot be debugged because no useful logs, traces, metrics, or crash signals exist.
- Do not absorb unrelated platform or infrastructure work unless the app change directly depends on it.
- Do not stop at code changes without checking whether the main end-to-end flow actually works.

## References

Use only the smallest relevant surface pack:

- `references/web.md`
- `references/mobile.md`
- `references/desktop.md`

Use only the smallest relevant ecosystem pack:

- `references/typescript-javascript.md`
- `references/python.md`
- `references/go.md`
- `references/rust.md`

Use this when the request needs structure decisions beyond surface conventions:

- `references/application-architecture.md`

Use this only when the change materially touches observability:

- `references/observability.md`
