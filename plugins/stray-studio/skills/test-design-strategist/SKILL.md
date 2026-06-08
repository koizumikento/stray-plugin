---
name: "test-design-strategist"
description: "Use when the user wants a software test strategy, test design, test viewpoints, test cases, QA plan, release test checklist, regression scope, test data plan, coverage criteria, or manual-versus-automation testing recommendations. Do not use for implementing test code, reviewing an existing artifact with findings-first feedback, adding AI evals to CI, or designing validation cases for Codex skills."
---

# Test Design Strategist

Design practical software test coverage from the target behavior, risks, quality attributes, and delivery constraints. Produce a test design artifact that a team can execute, refine, or turn into automated tests.

Use this skill when the user wants to plan what to test and why before implementation, release, QA handoff, or automation work.

## Preferred Scope

- Test strategy for a feature, app, API, service, workflow, release, migration, integration, or regression area
- Test viewpoints, test scenarios, test cases, test matrices, QA checklists, or acceptance test design
- Risk-based testing plans that prioritize limited time or environments
- Test data, test oracle, coverage, exit criteria, and manual-versus-automation recommendations
- Non-functional test planning for security, accessibility, performance, reliability, compatibility, usability, or maintainability when relevant

## Do Not Use For

- Writing, modifying, or running test code or production code
- Findings-first review of an existing PR, codebase, test plan, document, UI, plugin, prompt, or artifact; use `reviewer`
- End-to-end app implementation that includes adding executable tests; use `fullstack-app-builder`
- LLM or agent eval setup in CI; use `ai-eval-ci`
- Codex skill trigger-boundary validation or near-miss prompt tests; use the skillops validation skill when available
- Broad QA organization design, staffing plans, or vendor process audits

## Decision Gates

1. Confirm the request is for test design rather than implementation or review.
2. Identify the test target: feature, workflow, API, data path, integration, release, migration, UI, model behavior, or operational process.
3. Identify the available test basis: requirements, acceptance criteria, spec, diff, code, user story, incident, risk note, design, API contract, or observed behavior.
4. If the test basis is thin, state assumptions and missing inputs before designing detailed cases.
5. Choose the smallest useful artifact for the user's decision: strategy, matrix, checklist, cases, charters, automation candidates, or release gate.

## Workflow

1. Frame the test target.
   - Name the behavior, user flow, data boundary, system boundary, external dependencies, environments, and release context.
   - Separate confirmed facts from assumptions.
   - Identify what is intentionally out of scope.

2. Define the test objective and quality risks.
   - Ask what failure would be costly, unsafe, embarrassing, irreversible, hard to detect, or likely to regress.
   - Map relevant quality attributes such as functional suitability, performance, compatibility, usability, accessibility, reliability, security, maintainability, portability, flexibility, and safety.
   - Rank risk by impact and likelihood, then use that ranking to decide test depth.

3. Select the test levels and test types.
   - Choose from unit, component, integration, contract, system, end-to-end, acceptance, regression, exploratory, smoke, migration, data-quality, and non-functional tests.
   - Prefer a balanced test portfolio over a single large end-to-end suite.
   - Explain why omitted levels or types are not worth the cost for the current scope.

4. Choose test design techniques.
   - Use equivalence partitioning and boundary value analysis for input ranges, validation rules, numeric limits, dates, quantities, sizes, and lifecycle thresholds.
   - Use decision tables or pairwise/combinatorial coverage when behavior depends on multiple conditions.
   - Use state transition testing when valid behavior depends on status, lifecycle, permissions, retries, locking, payment, publishing, or workflow stage.
   - Use scenario or use-case testing for user journeys and acceptance flows.
   - Use contract tests for service boundaries, API compatibility, event schemas, or third-party integrations.
   - Use property-based or metamorphic tests when specific expected values are hard to enumerate but invariants or relations are clear.
   - Use exploratory testing, error guessing, and checklist-based testing for ambiguity, unfamiliar domains, or high-change surfaces.

5. Design the cases or viewpoints.
   - Cover happy path, negative path, edge cases, empty/null/zero/one/many, duplicates, malformed input, permission denied, stale data, concurrency, timeout, retry, partial failure, rollback, and observability when they can occur.
   - For each material case, include objective, preconditions, input or action, expected result, priority, level/type, design technique, automation fit, and risk covered.
   - Keep cases discriminating; avoid many near-duplicates that do not increase risk coverage.

6. Define data, oracle, and environment needs.
   - Specify required fixtures, personas, roles, permissions, records, external service states, clocks, locales, devices, browsers, network conditions, and production-like data constraints.
   - Identify the test oracle: exact expected output, invariant, schema, business rule, audit event, metric, log, visual state, or human judgment.
   - Mark data that must be synthetic, anonymized, resettable, or protected.

7. Decide execution and automation strategy.
   - Mark each area as automate now, automate later, manual scripted, exploratory, monitor-only, or out of scope.
   - Prefer automation for deterministic, repeated, high-risk, regression-prone behavior.
   - Prefer manual or exploratory testing for ambiguous UX, one-off migration rehearsal, visual judgment, early discovery, or unstable requirements.

8. Define coverage and exit criteria.
   - Tie coverage to risks, requirements, states, branches, APIs, roles, data partitions, devices, or quality attributes.
   - State release gates, smoke criteria, regression minimums, known gaps, and residual risks.
   - Call out when specialist security, accessibility, performance, legal, safety, or domain review is still required.

9. Produce the artifact.
   - Use a compact matrix, checklist, cases table, risk map, release gate, or exploratory charter according to the user's need.
   - Lead with the highest-risk coverage and the decisions needed next.
   - Include assumptions and unresolved questions at the end.

## Output Expectations

Choose the smallest useful shape:

- Test strategy
- Test viewpoint list
- Test case table
- Risk-based test matrix
- Release or regression checklist
- Automation candidate list
- Manual exploratory test charter

For detailed cases, prefer these fields:

- ID
- Objective
- Target or condition
- Input or action
- Expected result or oracle
- Priority
- Test level/type
- Design technique
- Automation fit
- Risk or coverage rationale
- Notes, assumptions, or residual risk

## Guardrails

- Do not implement code or test code unless the user explicitly asks for implementation in the same turn.
- Do not claim exhaustive coverage; state the selected boundary and residual risk.
- Do not create a generic QA checklist detached from the user's target, risks, and quality attributes.
- Do not stop at happy paths.
- Do not treat all tests as equal priority.
- Do not invent facts about requirements, systems, data, or environments; mark assumptions clearly.
- Do not over-prescribe tooling before understanding the stack and repository conventions.
- Do not hide the need for specialist review in security, privacy, accessibility, regulated, safety-critical, medical, legal, or financial contexts.
