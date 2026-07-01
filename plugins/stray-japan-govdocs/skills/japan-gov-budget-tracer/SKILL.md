---
name: "japan-gov-budget-tracer"
description: "Use when the user asks whether a Japan policy issue has related government budget, programs, 行政事業レビュー, 予算, 事業, or funding signals. Trigger on 予算がついているか, 行政事業レビューを探して, 政府事業, 施策と予算. Do not use for grant application advice, procurement eligibility, or simple policy background."
---

# Japan Gov Budget Tracer

Trace a policy issue from whitepaper context to government programs, budgets, and administrative review materials.

Use this skill when the user asks:

- "国はこの課題に実際に予算をつけてる?"
- "子育てDXの白書記述から行政事業レビューを探して"
- "観光DXに関係する政府事業を確認して"

## Workflow

1. Define the issue and relevant ministry owners.
2. Use whitepapers to find official framing and policy terms.
   - Follow official URL roles in `../../references/official-url-model.md`.
   - Use `../../references/egov-whitepaper-route-map.md` for known whitepaper routes and slugs.
   - Use `../../references/download-cache-policy.md` only for task-needed downloads; final citations stay on official URLs.
   - Bound the search: inspect the latest official series page plus at most two relevant ministry, statistics, program, or database source families unless the user asks for exhaustive coverage.
   - If no official program or budget source supports the connection after those checks, stop widening the search and report it under `追加確認` or `公式根拠なし` with the checked sources.
3. Search budget documents, ministry program pages, and administrative review databases for matching terms.
4. Link programs to stated objectives, outputs, outcomes, and review-sheet evidence when available.
5. Report confidence and gaps; policy themes rarely map one-to-one to budget programs.

## Output Expectations

| Program/budget item | Ministry | Related issue | Evidence source | Objective/outcome | Confidence |
|---|---|---|---|---|---|

Also include `白書との接続`, `行政事業レビュー確認`, `予算確認の限界`, and `次に見る資料`.

## Guardrails

- Do not claim funding eligibility.
- Do not infer a program exists solely from a whitepaper theme.
- Do not provide procurement or subsidy procedure advice.
