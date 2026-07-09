---
name: "japan-gov-case-finder"
description: "Use when the user wants official 自治体事例・企業事例 or precedent initiatives for a Japanese policy issue, with evidence quality and transfer limits. Do not use for general evidence, KPI discovery, or causal-effect claims."
---

# Japan Gov Case Finder

Find reusable cases in Japanese official sources and grade what each source actually proves.

## Do Not Use For

- Evidence supporting a supplied general claim; use `japan-gov-evidence-finder`.
- Indicator design; use `japan-gov-kpi-finder`.
- Claims that an intervention caused an outcome unless the official evaluation supports that conclusion.

## Workflow

1. Define actor type, issue, intervention, geography, period, minimum evidence, and number of useful cases.
2. Search relevant official case collections and whitepapers, then at most two adjacent ministry or evaluation source families unless exhaustive coverage is requested.
   - Follow `../../references/official-url-model.md`; use `../../references/download-cache-policy.md` only for task-needed files.
3. Extract actor, baseline problem, intervention, implementation context, reported result, measurement method, and source location.
4. Grade each case:
   - `A: 評価あり` — method, comparison or attribution limits, and measured outcome are reported.
   - `B: 成果測定あり` — quantified outcome or before/after result is reported without strong attribution.
   - `C: 実施記述のみ` — activity or anecdotal result is described without outcome measurement.
5. Assess transferability by prerequisites, scale, locality, delivery body, cost or capability, and known failure/selection bias.
6. Stop when the requested number of qualified cases is met or two consecutive source families add no qualifying case. Report search scope and missing evidence.

## Output

| Case | Actor | Intervention | Reported result | Evidence grade | Source | Transfer conditions |
|---|---|---|---|---|---|---|

Also include `使いやすい事例`, `実施記述に留まる事例`, `代表性の限界`, and `探索範囲・停止理由`.

## Guardrails

- Do not present highlighted cases as representative or successful by default.
- Do not upgrade self-reported outcomes into causal evidence.
- Paraphrase; do not reproduce long case text.
