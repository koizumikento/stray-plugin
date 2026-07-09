---
name: "japan-gov-budget-tracer"
description: "Use when the user wants to trace a Japanese policy theme to 予算, government programs, or 行政事業レビュー and distinguish funding lifecycle states. Do not use for eligibility, application, or procurement advice."
---

# Japan Gov Budget Tracer

Trace a policy issue to identifiable Japanese government programs and budget records without collapsing requests, enactment, execution, and evaluation into a single claim that “budget exists.”

## Do Not Use For

- Subsidy eligibility, application procedures, procurement qualification, or legal advice.
- General policy background without a budget or program question; use `japan-gov-background-builder`.

## Workflow

1. Fix the issue, fiscal year or range, ministries, desired amount basis, and whether the user asks about planned, authorized, executed, or evaluated spending.
2. Use whitepapers and policy plans only to derive official program terms; verify budget status in budget documents, program pages, contracts or execution reports, and administrative review sheets.
   - Follow `../../references/official-url-model.md` and use task-needed downloads only under `../../references/download-cache-policy.md`.
3. Assign every finding exactly one lifecycle state:
   - `政策・構想のみ`
   - `概算要求`
   - `政府予算案`
   - `成立当初予算`
   - `成立補正予算`
   - `配賦・公募・契約`
   - `執行実績`
   - `行政事業レビュー・評価`
4. Record fiscal year, amount, unit, account or program identifier, ministry, source date, and whether the amount is program-wide or attributable to the issue.
5. Connect objectives, outputs, outcomes, and review findings only where the source makes the link. Rate confidence `High`, `Medium`, or `Low` using `../../references/evaluation-rubric.md`.
6. Search the latest official budget route plus at most two relevant program/review source families unless exhaustive tracing is requested. Count and report checked families using `../../references/evaluation-rubric.md`; stop if no official linkage is found.

## Output

| Program or budget item | Ministry | FY | Amount and unit | Lifecycle state | Issue link | Evidence | Confidence |
|---|---|---:|---:|---|---|---|---|

Also include `白書・政策との接続`, `成立と執行の差`, `行政事業レビュー`, and `確認できない範囲`.

## Guardrails

- Do not call a request, draft, or policy mention an enacted budget.
- Do not claim issue-specific funding from a larger program total without an official allocation.
- Do not infer eligibility, future funding, or procurement opportunity.
