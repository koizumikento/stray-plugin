---
name: "japan-gov-priority-checker"
description: "Use when the user asks whether a theme is a current/rising 政策優先度 or 国が重視する課題 and wants official signals compared over time. Do not use for generic evidence, formal ownership, or future-funding predictions."
---

# Japan Gov Priority Checker

Score current policy emphasis from multiple dated official signals and make inference visible.

## Do Not Use For

- Formal ministry ownership; use `japan-gov-owner-mapper`.
- Existence or status of budget funding; use `japan-gov-budget-tracer`.
- Evidence for an unrelated supplied claim; use `japan-gov-evidence-finder`.

## Workflow

1. Define the theme, comparison period, government level, and what priority means for the decision. Default to the latest completed and current policy cycles, naming concrete years.
2. Collect dated, independent signals:
   - explicit priority in a current Cabinet decision, basic plan, strategy, or ministerial policy;
   - an active current-year program, enacted budget, implementation body, or review cycle;
   - a new/revised KPI, target, council,制度, or dedicated section;
   - recurrence across distinct ministries or source families;
   - stronger wording or placement versus the previous comparable edition.
3. Treat mirrors, summaries, repeated citations of one parent plan, and multiple pages in one document as one signal family.
4. Verify that programs and targets are current rather than merely announced or historical. Use budget tracing when lifecycle status matters.
5. Weight signals as `Strong`, `Medium`, or `Weak`, then map them to `high`, `medium`, `low`, or `unclear` using `../../references/evaluation-rubric.md`.
6. Compare like-for-like editions when claiming a rise or fall. Stop after the latest relevant series and two independent adjacent source families unless exhaustive research is requested.

## Output

- `結論`: high / medium / low / unclear, with the rubric mapping shown
- `対象期間と判定基準`
- `独立した優先度シグナル`
- `過年度からの変化`
- `現行施策・予算の確認状態`
- `反証・不確実性`

## Guardrails

- Do not infer priority from keyword frequency or one document alone.
- Do not count announced, expired, requested, and enacted measures as equivalent.
- Do not predict future budgets, adoption, or procurement.
