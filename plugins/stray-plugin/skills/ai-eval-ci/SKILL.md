---
name: "ai-eval-ci"
description: "Use when the user wants to add AI or agent evaluations to CI, catch prompt regressions, compare model behavior, or enforce quality gates for LLM output. Do not use for ordinary unit tests, one-off manual prompt checks, or non-LLM code paths."
---

# AI Eval CI

Add AI and agent evaluations to CI so model quality regressions fail fast instead of shipping silently. Keep the workflow small, repeatable, and cheap enough to run on every relevant change.

## Workflow

1. Identify the behavior to protect.
   - Name the user-facing task, output shape, and failure modes.
   - Decide whether the gate protects prompt quality, tool use, retrieval accuracy, or end-to-end agent behavior.

2. Define the minimum eval set.
   - Prefer a small set of representative cases over broad but shallow coverage.
   - Include at least one happy path, one edge case, and one regression case when available.
   - Keep fixtures and expected outputs versioned with the repo.

3. Choose the scoring method.
   - Use deterministic assertions when the output can be checked structurally.
   - Use model-judged or rubric-based scoring only when semantic quality cannot be captured otherwise.
   - Add clear thresholds so the CI result is unambiguous.

4. Wire the eval into CI.
   - Run the eval in the same pipeline that validates the code or prompt change.
   - Fail the build when the score drops below the threshold or a required assertion fails.
   - Keep runtime and external dependencies low enough for routine CI usage.

5. Document the gate.
   - State what change should trigger the eval.
   - Explain how to run it locally before pushing.
   - Record where the fixtures, config, and results live.

## Outputs

- An eval definition or test fixture set.
- A CI step that runs the eval and fails on regression.
- A short note explaining what the gate protects and how to interpret failures.

## Assumptions

- The repo already has a place to store test fixtures or CI config.
- The eval can be expressed as a small, stable set of cases.
- Someone can run the same check locally before relying on CI.

## Guardrails

- Do not turn this into a full benchmark suite unless the user explicitly needs one.
- Do not add a model-judge dependency if a deterministic check is sufficient.
- Do not hide failures behind flaky thresholds or vague pass criteria.
- Do not add scripts, references, or metadata files unless they materially improve reliability.
