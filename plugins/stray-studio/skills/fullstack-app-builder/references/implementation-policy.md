# Implementation Policy Reference

Use this reference when security/session handling, rollout, runtime/dependency choices, or source-of-truth alignment needs a decision. Select data, API, and asynchronous implementation details through the Reference Loading table in `SKILL.md`; this file is not required reading for every edit.

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
- Make write paths observable enough to debug failures and investigate incidents.

## Release And Rollout

- Prefer backward-compatible changes that can be rolled out without breaking existing clients, sessions, stored data, or local installations.
- When a change affects auth, schema, caching, device permissions, packaging, or a business-critical flow, think through rollout order, rollback path, and failure mode before shipping.
- Use feature flags, staged rollout patterns, or guarded code paths when the repository or product already supports them and the risk justifies the control.
- Surface changes that require coordination, sequencing, downtime planning, store review, installer updates, or data backfill.

## Cross-Boundary Correctness

- Treat caches, revalidation, deduplication, retries, offline sync, and repeated submissions as correctness concerns when the flow depends on them.
- Identify authoritative state and freshness expectations at read and write boundaries.
- Keep success, acceptance, replay, and partial-failure semantics consistent across UI, APIs, persistence, and jobs. Record any unresolved gap instead of treating one successful boundary as proof of the whole flow.

## Source Of Truth

- Identify the authoritative local artifact before implementation: product spec, issue, AGENTS guidance, design-system doc, wireframe, migration, API contract, or existing behavior.
- If docs, implementation, tests, and review instructions disagree, pause long enough to name the drift and choose the smallest alignment path.
- Keep source-of-truth updates in the same change when implementation intentionally changes behavior described by docs, tests, design-system rules, or AGENTS guidance.
- Do not paper over drift with code comments. Update the artifact users and future agents will consult.
- When the same missing context, setup step, validation command, or reproduction path blocks repeated work, prefer updating the durable source of truth such as `AGENTS.md`, docs, scripts, tests, fixtures, or CI instead of relying on another one-off explanation.
- For design-system or shared component work, verify export inventory, CSS ownership, app usage, tests, and documentation together.

## Dependencies

- Prefer existing dependencies and platform primitives when they already solve the problem well enough.
- Add a dependency only when it meaningfully improves correctness, safety, maintainability, or delivery speed.
- Avoid overlapping libraries that create competing ways to solve the same problem inside one repository.
- When introducing a dependency, consider maintenance health, ecosystem fit, security posture, and how hard it will be to remove later.

## Validation And Handoff Detail

- For TypeScript or JavaScript, include the `vp check` and `vp test` decision when those commands exist; otherwise use repository scripts or package-local commands.
- For Python, include the `uv`, `ruff`, `ty`, and `pytest` decision when they fit the repository.
- For Go, include `gofmt`, `go test`, `go vet`, and `golangci-lint` decisions when they fit.
- For Rust, include `cargo fmt`, `cargo clippy`, `cargo test`, pinned toolchain, and Nix decisions when they fit.
- When local and CI or deploy environments differ, state which environment was proven and which remains unverified.
- Update docs, runbooks, API notes, env var docs, setup instructions, or release notes when the change alters operation, configuration, packaging, or extension.
- Include new required dependencies, environment variables, migration steps, permissions, packaging steps, or rollout concerns in the handoff.

## Repair And Review Checks

- Four successive, distinct failures with evidence of progress: continue the targeted repairs; do not stop solely at the third attempt.
- The same failure twice with no new hypothesis or progress: reassess diagnostics before retrying; if no safe next step exists, report the unresolved failure rather than success.
- Independent review finds an in-scope defect: fix and validate it, then request one focused correction check. Add another pass only for a new material change or unresolved confirmed finding.
- Subagents unavailable: self-review and run feasible checks, disclose the missing independent review, and preserve any unresolved requirements. If the user required independent review, report completion as blocked on that requirement.
