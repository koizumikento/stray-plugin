---
name: "fullstack-app-builder"
description: "Use when the user wants working code for an end-to-end web, mobile, or desktop app flow spanning UI and its API, data, auth, or background behavior. Do not use for Slack apps, static corporate sites, landing pages, reviews, test-design-only work, product strategy, or visual assets."
---

# Fullstack App Builder

Build or modify a full-stack application in the current repository and carry the work through implementation, validation, and handoff. Treat an app feature as an end-to-end user flow spanning the surface, server behavior, data, security, and operational checks.

Use this skill when the user wants to:

- add or change screens, routes, views, layouts, windows, forms, navigation, local state, or app interactions
- wire UI to APIs, server actions, auth, background handlers, platform integrations, or data-fetching layers
- change backend behavior that directly serves the shipped app experience
- implement flows that cross client, backend, and database boundaries
- fix app bugs in rendering, state, validation, auth, permissions, sync, offline behavior, responsiveness, accessibility, or performance
- scaffold a small full-stack app when the repository does not already contain one and the user explicitly wants implementation

## Do Not Use For

- product strategy, feature definition, or market-backed direction setting
- pure visual theming, screenshot creation, or marketing asset work
- browser-based research tasks
- read-only PR, branch, diff, staged-change, or specification reviews where the user asks for findings instead of implementation
- backend-only services, infra work, or protocol design with no shipped user-facing app flow
- standalone libraries, SDKs, or packages that are not part of a shipped app flow

## Decision Gates

1. Route named specialist surfaces before treating the request as general app work.
   - Use `slack-app-builder` when Slack commands, events, workflows, manifests, scopes, Slack CLI, or workspace behavior are the primary surface.
   - Use `corporate-site-builder` for a static, repository-managed corporate information site without CMS, approval, preview-dashboard, auth, or data-backed product flows.
   - Use `landing-page-builder` for a conversion-focused page whose primary job is message hierarchy, proof, CTA flow, and search posture.
   - Use `test-design-strategist` when the deliverable is a test strategy, matrix, cases, or QA plan rather than executable tests.
   - Use `security-preflight` for a security-focused review and `reviewer` for other findings-first reviews; neither review request authorizes implementation here.
   - Use `artifact-theme-applier`, `marketing-screenshot-creator`, or `brand-designer` when the owned output is respectively restyling an existing artifact, producing captures, or defining identity direction.
   - Return here only when the specialist surface is embedded in a broader authenticated, data-backed, or cross-layer app flow and the user asked to implement that broader flow.
2. Confirm the user asked for implementation, debugging, or end-to-end app change.
   - If the user says "first investigate", "first check", "first plan", "まずは", or similar, gather evidence and stop with findings or a plan until they ask to implement.
   - If the request is review-only, route to the relevant review skill.
3. Identify the primary surface: web, Android, iOS, mobile, desktop, or hybrid.
   - For Android work, distinguish existing-project maintenance from new-app scaffolding before choosing tools or architecture.
   - For new Android apps, research the current ecosystem before selecting the stack; do not rely on stale hardcoded Android tool, SDK, or library versions.
4. Identify the existing framework, runtime, package manager, navigation model, state model, styling approach, persistence layer, auth/session model, and validation/test setup.
5. Read the nearest `AGENTS.md`, app docs, specs, design-system docs, issues, or PR context that define the behavior.
6. Stop or route elsewhere if the task is design-only, research-only, product strategy, marketing-only, or not about a shipped app flow.

## Reference Loading

Load only the smallest reference needed for the task:

- `references/implementation-policy.md`: security, data, rollout, caching, source-of-truth, dependency, async, validation, and handoff policies for non-trivial app changes.
- `references/web.md`, `references/mobile.md`, or `references/desktop.md`: surface-specific defaults.
- `references/android.md`: Android-specific defaults, ecosystem research gates, native versus cross-platform selection, Gradle and release checks, emulator/device validation, and Play quality concerns.
- `references/typescript-javascript.md`, `references/python.md`, `references/go.md`, or `references/rust.md`: ecosystem-specific validation and runtime defaults.
- `references/application-architecture.md`: structure decisions such as layered modular monolith, Clean Architecture, BFF, CQRS, async boundaries, or bounded contexts.
- `references/observability.md`: logs, traces, metrics, crash signals, analytics, or audit events.
- `references/logging.md`: application logs, audit logs, background-job logs, integration logs, correlation fields, log levels, sensitive-data handling, cardinality, or incident diagnostics.

Do not let a reference override clear repository conventions.

## Workflow

1. Frame the user-facing change before editing.
   - Name the user flow, affected entry points, trust boundaries, data model boundaries, and backend or platform assumptions.
   - Load the relevant surface and ecosystem references when stack-specific defaults matter.
   - Load the Android reference when the primary surface is Android, when adding an Android target to a cross-platform app, or when Android platform behavior affects the shipped flow.
   - Load the architecture reference when deciding layer shape, BFF use, async boundaries, read versus write separation, or monolith boundaries.
   - Load the observability reference when the flow needs new or revised logs, traces, metrics, crash signals, or audit events.
   - Load the logging reference when the flow needs new or revised application logs, audit logs, retry or background-job logs, external integration logs, or incident diagnostics.

2. Follow the existing app before inventing a new one.
   - Read current screens, routes, components, handlers, data access, styling, state, platform glue, tests, and docs.
   - Preserve established patterns unless the user requested a deliberate change.
   - Search for related TODOs, placeholders, stubs, disabled controls, no-op handlers, dead routes, and partial implementations.
   - If the repo lacks an app, choose the smallest credible implementation shape for the requested outcome.

3. Design the smallest coherent slice.
   - Name the app shape before coding: existing repo pattern, layered modular monolith, Clean Architecture slice, BFF-backed flow, or queue-worker split.
   - Define UI states, navigation transitions, request flow, validation, auth, authorization, persistence, loading, error, empty, offline, and retry states when relevant.
   - For business-critical flows, build a small domain-state matrix covering zero/one/many records, missing baseline data, selected versus unselected item, locked/read-only/archived states, stale route or form state, permission denied, and retry after failure when those states can occur.
   - Decide what belongs in UI, application orchestration, domain logic, infrastructure adapters, and background workers.
   - If behavior admits multiple credible interpretations, state the assumption and choose the option that preserves data and user escape hatches.

4. Implement the flow end to end.
   - Update screens, components, routes, windows, styles, types, request handlers, API wiring, persistence, platform integrations, and docs as needed.
   - Treat schema changes, auth changes, session handling, authorization checks, deep links, IPC bridges, device permissions, background work, and migrations as part of the job when the flow depends on them.
   - Do not leave a feature at "looks wired" if the primary action does not persist, navigate, invalidate data, surface errors, or update state as users expect.
   - Remove or replace scaffolding and placeholder UI that would confuse users or reviewers unless the user explicitly asked for a visible stub.

5. Validate with the right level of evidence.
   - Run targeted lint, typecheck, tests, build, migration checks, packaging checks, simulator or emulator checks, browser checks, or desktop runtime checks when they fit the stack.
   - Verify the main user path on the actual target surface when feasible.
   - Check validation, auth, authorization, navigation, error handling, retry behavior, rollback behavior, accessibility, responsiveness, lifecycle, and platform-specific concerns when relevant.
   - For UI work, open the app on the real target surface when feasible and inspect the affected flow at relevant desktop and mobile viewports.
   - Repeat a focused unfinished-work scan for placeholders, TODOs, disabled actions, no-op handlers, and newly stale docs or specs.

6. Run a bounded repair loop when validation fails.
   - Read the failing output before editing again and name the current failure hypothesis.
   - Change one clear thing at a time, then rerun the smallest relevant check that can prove or disprove the hypothesis.
   - Do not rerun the same failing command without new evidence, a code/config change, or a narrower diagnostic command.
   - Stop with a blocker report after three failed repair attempts, or when the same failure repeats twice without a new hypothesis.
   - Classify the likely missing layer as prompt ambiguity, missing context, missing harness, loop limit, or external blocker.

7. Hand off clearly.
   - Summarize the user-visible result, key implementation decisions, and residual risks.
   - Include validation run, skipped, unavailable, or unverified.
   - Include the route, local URL, command, migration status, deployment status, and any reload or cache caveat that affects verification.
   - Separate implemented, reviewed, merged, deployed, and migrated status.

## Validation Expectations

- Prefer tests that cover user-visible behavior and real flow boundaries.
- Include negative-path checks when changing auth, validation, permissions, persistence, or platform bridges.
- For browser UI changes, prefer at least one real render check of the changed route or component state.
- For responsive surfaces, verify the smallest relevant mobile width and a normal desktop width when layout, density, navigation, or forms changed.
- For write flows, verify pending, success, error, duplicate-submit, read-after-write, cache invalidation, and generated type or query-contract effects when applicable.
- If the main path cannot be verified locally, say exactly what remains unproven.

## Output Expectations

- Working code changes or a concrete blocker report.
- Short summary of what changed for the user.
- Chosen architecture shape when it materially affected implementation.
- Validation results with important cross-stack gaps.
- Source-of-truth drift found and how it was resolved or deferred.
- Exact route, screen, command, or URL used for user-visible verification when applicable.
- Explicit assumptions, risks, or follow-up items when relevant.
- Blocker classification when work could not be completed: prompt ambiguity, missing context, missing harness, loop limit, or external blocker.
- Security, data, platform, or observability notes when the change touches them.

## Guardrails

- Do not treat a broad product discussion as implementation work.
- Do not treat review-only prompts as permission to edit.
- Do not implement after a "first investigate/check/plan" request unless the user also clearly asks for code changes in the same turn.
- Do not rewrite the stack, surface architecture, or design system without a clear reason.
- Do not leave visible placeholder experiences, disabled primary actions, or no-op handlers unless explicitly requested.
- Do not ignore docs, design-system, AGENTS, migration, or test drift just because the code compiles.
- Do not make backend, schema, auth, or permission changes without checking the shipped user flow.
- Do not rely on client-only validation or client-only authorization.
- Do not add opaque migrations or destructive production-only changes without surfacing the risk.
- Do not stop at code changes without checking whether the main end-to-end flow actually works.
