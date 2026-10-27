# CI Placement Decisions

Read this reference before adding or expanding CI work, including jobs, steps, triggers, schedules, matrices, required checks, or work hidden behind an existing script, test discovery rule, generator, or configuration. Apply it while planning and before editing the behavior that increases CI work. During review, apply it only to the affected execution and merge/release contracts. Routine local validation or an unrelated edit needs no placement report.

Keep the current skill as owner. This reference supplies placement criteria; it does not authorize new effects, require another skill or agent, or make every check a CI gate.

## Workflow

1. Name the purpose and authoritative basis.
   - Identify the defect, contract violation, artifact, or operational outcome the work addresses. Trace it to a requirement, supported risk, incident, or existing repository policy.
   - Separate a temporary diagnostic, hypothesis check, or task-completion check from a recurring requirement. A command used once successfully is not by itself a reason to run it for every change.
   - For tests, check behavior or an authoritative contract. Do not freeze incidental source text, internal call order, or the current implementation merely to detect edits. Structural assertions are appropriate when the structure itself is a required contract.
2. Inspect existing coverage and entry points.
   - Read the relevant workflows, repository guidance, scripts/task targets, test discovery, fixtures, generators, and required-check expectations. Follow what the workflow actually invokes, not only changes under `.github/workflows/`.
   - Reuse the existing command and configuration where they fit. Avoid independently maintaining local and CI versions of the same rule.
   - Local and CI execution can intentionally overlap: local runs shorten feedback, while CI independently verifies shared state and can enforce repository requirements. Local success alone is not grounds to remove an important CI check.
3. Choose execution place and frequency separately from automation.
   - Decide whether automation is useful, where it should run, what changes should trigger it, and how often it is needed. Then choose whether failure should block a merge or release.
   - Compare local/development execution, PR CI, post-merge CI, scheduled execution, manual dispatch, and release validation. Combine them where the assurance requires it.
   - Keep frequent feedback fast. Move necessary slower work to an appropriate stage only when delayed detection is acceptable; otherwise retain the required gate and improve its execution. Do not treat a suggested duration as a universal cutoff.
4. Check reproducibility, resources, and effects.
   - Identify declared inputs, tool/dependency versions, fixtures, environment assumptions, external services, credential names, and expected result. State any CI-only environment that prevents an equivalent local run.
   - Estimate runtime, execution frequency, runner/matrix growth, API/model requests, retries, cost, and artifact retention to the precision the decision needs. Do not require a benchmark project for a small bounded check.
   - Separate product/quality failures from infrastructure, rate-limit, availability, or evaluator-variance failures. Retries must not turn a real failure into a pass.
   - Preserve least privilege, secret/data boundaries, isolation, and existing deployment/publishing/paid-call authorization. Reuse authorization for the same scope and effects; do not add a permission round for every CI edit.
5. Decide blocking behavior and ownership.
   - For a required check, state what failure means, what must be fixed, and who responds. A delayed/manual check still needs a completion and response path when it protects a required outcome.
   - Verify that filters, conditional jobs, dependencies, and skipped runs preserve the intended required-check behavior. Workflow-level skipping can leave a required check pending; a skipped job can report success. Neither proves the affected verification ran.
   - Do not remove, weaken, or silently make an existing required check optional to reduce CI work. Preserve the intended assurance or report the policy decision needed.
6. Record the smallest sufficient decision and validate it.
   - Put the purpose, placement/trigger, blocking behavior, command, material resource/dependency assumptions, and failure response in the existing PR description or owning documentation. Create no per-check report or template unless requested or required by the repository.
   - Run the relevant existing local checks; verify changed workflow syntax and invocation paths where applicable. Distinguish local validation from actual hosted execution and required-check enforcement.
   - If the basis for permanent CI is missing, continue authorized diagnostics and implementation without inventing a gate. Resolve only material missing decisions with the user; retain important existing checks and report unverified requirements.

## Placement Examples

These are starting points, not universal requirements. Apply the repository's constraints and the consequences of delayed detection.

| Work | Usual placement | Reason or condition |
|---|---|---|
| Temporary debugging, data inspection, or exploratory hypothesis | Local/development environment | Keep investigation separate from a recurring acceptance condition |
| Personal setup, uncommitted working-tree state, attached device | Local or dedicated environment | The input is specific to the developer or device; it is not shared-source verification |
| Formatting fixes or generated-file updates | Local update; CI check when the output is a repository contract | Separate producing the change from checking committed consistency |
| Build, types, important regression tests, public schema/contract checks | Local and relevant PR CI | Fast feedback plus independent verification; share definitions where possible |
| Broad compatibility, long integration suite, performance evaluation | Relevant PR, later stage, schedule, manual, or release gate | Choose from risk and acceptable detection delay, not runtime alone |
| Live API, paid model, hardware, exploratory visual judgment | Controlled environment, manual/scheduled execution, or a justified gate | Bound cost, credentials, isolation, variance, and response; use deterministic fixtures for suitable routine checks |
| Publish, deploy, migrate, or another operational write | Dedicated authorized delivery/operations workflow | Distinguish a real operation from validation and preserve its target/effect controls |

For example: "Verify public-schema compatibility with the existing command in relevant PR CI; failure blocks merging. Use synthetic inputs and no live API. Regenerate fixtures locally, then check the committed diff."

## Synthetic Decision Checks

Use these examples for manual or available behavioral evaluation. They are not an executable test suite, and structural reference/routing validation does not prove that an agent follows them.

| Scenario | Expected decision | Failure to catch |
|---|---|---|
| A developer used a one-off API probe to diagnose a timeout | Keep the probe as a diagnostic unless a recurring requirement is established | Adds authenticated live calls to every PR merely because the probe helped once |
| An existing CI test target discovers a newly added paid model benchmark | Apply placement checks before adding the benchmark, even though workflow YAML is unchanged | Misses the CI expansion because only the test/config file changed |
| A deterministic authorization regression test also runs locally | Keep relevant shared CI verification and reuse the same test definition | Removes CI coverage solely because the local test passed |
| A long compatibility test protects a mandatory release requirement | Select a justified gate/stage and require completion before release | Makes it advisory or nightly without accounting for a release before that run |
| A PR adds a source-text checksum with no structural contract | Replace with a behavior/contract assertion or omit unsupported coverage | Treats any implementation edit as a defect |
| A copy-only change leaves CI execution unchanged | Use relevant existing checks without a new placement document | Loads a broad CI audit or adds process requirements for every edit |
| A required workflow gains a path filter | Verify required-check and skip semantics before adopting it | Claims unaffected PRs can merge without checking the pending-status consequence |

## Evidence Basis

The placement workflow above is this plugin's policy synthesized from the following primary sources, reviewed on 2026-10-27. The sources do not establish that AI-written CI is generally excessive, and their examples are not universal runtime limits.

- [Martin Fowler: Continuous Integration](https://martinfowler.com/articles/continuousIntegration.html) explains rapid feedback, local verification, and staged builds with slower downstream tests.
- [pre-commit: Usage in continuous integration](https://pre-commit.com/#usage-in-continuous-integration) documents reusing checks in local and CI execution.
- [Git: pre-commit hook](https://git-scm.com/docs/githooks#_pre_commit) documents that the local hook can be bypassed; it is not independent shared enforcement.
- [Google Testing Blog: Change-Detector Tests Considered Harmful](https://testing.googleblog.com/2015/01/testing-on-toilet-change-detector-tests.html) distinguishes behavioral verification from tests that mirror implementation.
- [Google Testing Blog: Test Sizes](https://testing.googleblog.com/2010/12/test-sizes.html) classifies tests by environment and external-system dependencies.
- [Bazel: Hermeticity](https://bazel.build/basics/hermeticity) explains declared inputs, isolation, and reproducible execution.
- [GitHub: Manually running a workflow](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/manually-run-a-workflow) documents manual dispatch as an execution option.
- [GitHub: Troubleshooting required status checks](https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/troubleshooting-required-status-checks) explains required-check and skipped-workflow/job behavior.
- [GitHub: Secure use reference](https://docs.github.com/en/actions/reference/security/secure-use) covers workflow trust, secrets, and minimum permissions.
