# Implementation Policy Reference

Use this reference for non-trivial full-stack app changes where security, data, release, contract, dependency, async, source-of-truth, or validation policy matters. Keep `SKILL.md` focused on trigger, gates, workflow, validation, handoff, and guardrails.

## Surface And Framework Policy

- Identify the primary surface first: web, mobile, desktop, or hybrid.
- If the repository already uses a framework on that surface, follow its conventions for navigation, rendering, state, data loading, packaging, auth integration, and testing.
- Do not introduce a new surface architecture, router, packaging model, or state model when the existing stack can satisfy the request.
- Do not perform framework or surface migration work unless the user explicitly asks for migration or re-platforming.
- When the request is greenfield and the surface is unspecified, choose the smallest credible surface and stack for the requested outcome.
- Prefer boring, well-supported primitives over clever surface-specific abstractions when the codebase does not already depend on them.

## Runtime And Package Management

- Follow the repository's existing runtime, package manager, lockfile, and local environment workflow first.
- Do not assume bare executables such as `python`, `pytest`, `node`, framework CLIs, or deploy CLIs are globally available. Find the repository command, package-local binary, runtime manager, or workspace wrapper first.
- Do not introduce a package manager, version manager, or environment manager migration for a small feature or bug fix unless the user explicitly asks for it.
- For greenfield or unsettled repositories, prefer one clear package and environment workflow per language instead of mixing overlapping tools.
- On Windows, account for `.cmd` shims, PowerShell command behavior, path quoting, and workspace-local tools before declaring a command unavailable.
- Check local secret and config conventions before running app, migration, or deploy commands. Distinguish tracked examples from ignored local secrets.

## Security And Data

- Never trust client input by itself. Re-validate on the server or privileged boundary.
- Keep authentication and authorization separate in design and implementation.
- Prefer established auth protocols and libraries over hand-rolled auth flows.
- Apply least privilege and resource-level checks instead of relying only on coarse roles.
- Use secure session, token, cookie, keychain, or local secret handling when credentials are involved.
- Keep secrets and environment-specific config out of source-controlled code.
- Prefer committed, versioned, reviewable database migrations for non-trivial schema changes.
- Make write paths observable enough to debug failures and investigate incidents.

## Data Change Safety

- Treat schema, backfill, and persistence changes as operational events.
- Prefer additive, backward-compatible schema changes before destructive or shape-tightening ones.
- When tightening constraints, think through deploy order, existing data cleanup, and how old and new code coexist during rollout.
- Surface any need for backfills, dual reads, dual writes, or one-time repair scripts instead of hiding them inside feature work.
- For migrations, distinguish generating files, applying locally, confirming pending or unapplied migrations, and applying to remote or production-like environments.
- Check code and query contracts after schema work for stale fields, wildcard selection assumptions, generated types, fixture drift, and runtime-only failures that type-checking may not catch.

## Release And Rollout

- Prefer backward-compatible changes that can be rolled out without breaking existing clients, sessions, stored data, or local installations.
- When a change affects auth, schema, caching, device permissions, packaging, or a business-critical flow, think through rollout order, rollback path, and failure mode before shipping.
- Use feature flags, staged rollout patterns, or guarded code paths when the repository or product already supports them and the risk justifies the control.
- Surface changes that require coordination, sequencing, downtime planning, store review, installer updates, or data backfill.

## Caching And Idempotency

- Treat caches, revalidation, deduplication, retries, offline sync, and repeated submissions as correctness concerns when the flow depends on them.
- Make freshness expectations explicit at read and write boundaries.
- Design write paths and async triggers to be safe under retry or duplicate delivery when the surrounding system can replay them.
- Call out operations that are not idempotent or that can leave user-visible state inconsistent if retried midway.
- For idempotent command flows, verify that first success and replayed success have the same contract shape and enough persisted data for the UI to render identically.
- Keep the side effect and stored command result in the same transaction or equivalent atomic boundary when the platform supports it. If not, call out the partial-write failure mode.

## Source Of Truth

- Identify the authoritative local artifact before implementation: product spec, issue, AGENTS guidance, design-system doc, wireframe, migration, API contract, or existing behavior.
- If docs, implementation, tests, and review instructions disagree, pause long enough to name the drift and choose the smallest alignment path.
- Keep source-of-truth updates in the same change when implementation intentionally changes behavior described by docs, tests, design-system rules, or AGENTS guidance.
- Do not paper over drift with code comments. Update the artifact users and future agents will consult.
- For design-system or shared component work, verify export inventory, CSS ownership, app usage, tests, and documentation together.

## API And Contracts

- Treat contracts between UI, platform bridges, server handlers, APIs, jobs, and persistence layers as first-class boundaries.
- Make input and output shapes explicit in code and keep validation close to the boundary.
- Prefer additive and backward-compatible contract changes.
- When a breaking contract change is unavoidable, call it out clearly and update affected callers in the same change when feasible.

## Dependencies

- Prefer existing dependencies and platform primitives when they already solve the problem well enough.
- Add a dependency only when it meaningfully improves correctness, safety, maintainability, or delivery speed.
- Avoid overlapping libraries that create competing ways to solve the same problem inside one repository.
- When introducing a dependency, consider maintenance health, ecosystem fit, security posture, and how hard it will be to remove later.

## Background Jobs And Async Work

- If the shipped flow depends on queues, emails, webhooks, scheduled work, sync engines, background tasks, or retries, treat async behavior as part of the feature.
- Make trigger conditions, retry behavior, idempotency expectations, and failure visibility explicit.
- Do not assume async work succeeded just because the synchronous request returned successfully.
- Verify the user-visible consequence of async work or state clearly what could not be verified.

## Validation And Handoff Detail

- For TypeScript or JavaScript, include the `vp check` and `vp test` decision when those commands exist; otherwise use repository scripts or package-local commands.
- For Python, include the `uv`, `ruff`, `ty`, and `pytest` decision when they fit the repository.
- For Go, include `gofmt`, `go test`, `go vet`, and `golangci-lint` decisions when they fit.
- For Rust, include `cargo fmt`, `cargo clippy`, `cargo test`, pinned toolchain, and Nix decisions when they fit.
- When local and CI or deploy environments differ, state which environment was proven and which remains unverified.
- Update docs, runbooks, API notes, env var docs, setup instructions, or release notes when the change alters operation, configuration, packaging, or extension.
- Include new required dependencies, environment variables, migration steps, permissions, packaging steps, or rollout concerns in the handoff.
