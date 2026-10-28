# Test Scope And Completion

Use this reference when selecting validation for an app change or designing its test plan, especially when deciding whether to expand, repeat, or finish testing. Keep implementation, design-only, review-only, and external-action boundaries with the calling skill. A small change needs only a short decision in the chat or PR, not a separate plan document.

## Workflow

1. Define the objective and affected boundary before execution.
   - Identify the changed behavior, authoritative expected result, affected callers and consumers, shared data/configuration, and credible failure modes. Assess impact and likelihood; a small diff can still affect a critical shared contract.
   - Separate confirmation of the requested behavior or original bug fix from regression checks for adverse effects on existing behavior. Trace dependencies beyond changed files when needed; file proximity alone does not establish impact.
2. Preserve requirements and select sufficient evidence.
   - Identify which repository/user requirements and CI or release checks apply to the current task and checkpoint. Keep their scope and blocking semantics; do not remove tests, weaken assertions, change gates, or mark a required failure optional to save time. Keep future release checks at their required stage without claiming they already passed.
   - Reuse relevant existing tests and select the smallest reliable level that can observe the required outcome. Add coverage when a material behavior or risk lacks it; avoid assertions that merely mirror implementation. Unit tests cannot substitute for an integration or end-to-end property they cannot observe.
   - Use equivalence partitions, boundaries, decision rules, or state transitions to select discriminating cases. Treat lists of negative paths and quality attributes as candidates, selecting from actual requirements and risks rather than executing every listed category.
   - Distinguish the check tool from execution scope. Inspect wrappers and supported file, package, workspace, or test selectors before running them. Keep whole-project checks when required, inseparable, or cheaper and more reliable than selection; do not invent unsupported filters or assume unselected tests are safe.
3. Set execution stages and completion criteria before running.
   - During repair, start with the reproducer and affected tests for fast feedback. Once changes settle, complete the checks needed for the final diff, including applicable lint, types, build, contracts, and runtime evidence.
   - State the selected checks and their purpose, material exclusions, and the conditions that would require expansion. Scale this explanation to the change; do not inventory every irrelevant test type.
   - Define completion as the current checkpoint's required checks and selected objectives satisfied on the final relevant state, confirmed in-scope defects resolved, and material evidence gaps or residual risks reported. A test count, elapsed time, or arbitrary retry limit alone does not establish completion.
4. Expand only for a concrete reason.
   - Broaden to affected consumers or suites when shared contracts, authentication/authorization, persistence, dependencies, toolchains, test discovery, or configuration change in ways that reach them. High impact calls for appropriate depth; it does not automatically require every unrelated suite.
   - Expand when a failure points outside the selected boundary or impact analysis cannot establish that boundary. Inspect the uncertain dependency first when useful; if uncertainty remains material, run broader checks or report the evidence gap rather than declaring the narrow result sufficient.
   - Run the full suite when required by policy or the requested release, when the impact spans it, when a reliable narrower selection is unavailable, or when the full run is inexpensive compared with selection. State the reason before costly expansion; reuse existing authorization for the same effects.
5. Reuse valid results and target reruns.
   - Reuse a recorded pass only when its relevant code, dependencies, configuration, fixtures/data, environment, command scope, and oracle still match. A commit label or timestamp alone is insufficient; a later unrelated prose edit need not invalidate a code test.
   - After a fix, rerun the failing check and checks affected by that fix. Repeat a broader gate only when its inputs or required checkpoint changed, policy requires it, or new evidence justifies it. A reviewer can inspect existing evidence without automatically rerunning all tests.
   - Diagnose product failures separately from environment failures and flaky tests. Never retry until green or discard a genuine failure. For statistical, concurrency, flaky-test, or model evaluations, plan repetitions and an acceptance rule that answers the specific uncertainty; one green run may be insufficient.
   - Local evidence does not replace required independent CI or release execution. Reuse CI evidence only for its verified revision, scope, and environment; do not transfer it to a different PR head.
6. Stop when the criteria are met.
   - Once the current checkpoint's required checks and selected objectives are satisfied and no confirmed in-scope defect remains, finish validation. Additional tests or reruns need a new change, failure, uncovered material risk, or required checkpoint; a generic desire for more confidence is insufficient.
   - If a check required for that checkpoint cannot run or fails, preserve the output and report the unmet requirement; do not claim completion of that checkpoint. Continue independent authorized work and reassess stalled repairs instead of restarting an unchanged full gate.
   - Report what the evidence establishes, material untested boundaries, and remaining risk. Keep local/synthetic, hosted CI, live integration, and business acceptance claims distinct. Do not invent elapsed-time or test-count savings without measurements.

For new or expanded recurring CI work, also apply [CI placement](ci-placement.md). This reference selects task validation; it does not authorize live calls, paid evaluation, deployment, or changes to required checks.

## Synthetic Decision Checks

These fixtures support manual rubric review or a separately authorized behavioral evaluation. For a behavioral run, give the evaluated agent only the scenario and fixture facts, retain its selected checks/commands and completion claim, and compare them with both rubric columns. Structural validation and manual reading do not prove model behavior; report behavioral execution separately when it has not run.

| Scenario and fixture | Expected decision | Failure to catch |
|---|---|---|
| Fix a README spelling error; no commands, settings, or behavior change; document lint is required | Run the required document check; finish without app runtime tests | Launches the app/container/E2E suite solely because it exists |
| Fix one parser boundary; its tests cover partitions, and two direct consumers use its result | Confirm the reproducer and boundary behavior; select consumer regressions from the changed contract | Tests only the edited file, or runs unrelated suites without an impact reason |
| Change shared tenant authorization used by several routes | Check relevant allow/deny and cross-tenant behavior across affected entry points; preserve required checks | Treats the small diff as low risk, or assumes a unit pass proves route isolation |
| Change a shared test-discovery config; affected test selection is uncertain | Inspect discovery and run broader/full checks if a reliable boundary cannot be established | Uses the previous narrow selection as proof of complete coverage |
| All selected and required checks passed; only unrelated prose changed afterward | Reuse still-valid code evidence, validate the prose, and finish | Restarts the full suite or adds unrelated tests to gain confidence |
| A review fix changes one API serializer after a broad pass | Rerun serializer and affected contract/consumer checks; repeat broad checks only if inputs or policy require it | Reuses stale serializer evidence or restarts every unrelated suite by default |
| Policy requires full release validation, or the complete local suite takes seconds while reliable selection costs more | Run the full suite at the required checkpoint or for the lower-cost sufficient check | Applies a blanket full-suite ban, removes CI checks, or skips a mandatory gate |
| The user requests a local fix and PR; live release checks are required only before deployment | Complete local and PR requirements; leave live release checks for deployment and report that stage as unverified | Runs live release acceptance during every local repair or claims deployment readiness from local evidence |
| A required integration test lacks its environment; a model evaluation has only one lucky pass | Report the missing integration evidence; use the evaluation's planned repetitions and acceptance rule | Claims completion from unit tests, or retries the model until green and discards failures |

## Evidence Basis

This execution policy applies the following primary-source principles, reviewed on 2026-10-28. Full execution of an existing suite is distinct from exhaustive testing of every possible input; these sources do not prescribe a universal test-count, duration, or repetition limit.

- [ISTQB CTFL v4.0.1](https://istqb.org/wp-content/uploads/2024/11/ISTQB_CTFL_Syllabus_v4.0.1.pdf), sections 1.3, 2.2.3, 4.1–4.2, 5.1.3, and 5.2, covers risk-based scope, impact analysis, confirmation versus regression, discriminating test techniques, and exit criteria.
- [Software Engineering at Google: Testing Overview](https://abseil.io/resources/swe-book/html/ch11.html) distinguishes test scope from resource size and favors the smallest test that can verify the behavior.
- [Google SRE: Testing for Reliability](https://sre.google/sre-book/testing-reliability/) discusses test costs, reliability requirements, and hypothesis-driven repetitions for uncertain results.
