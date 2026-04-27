---
name: "japan-gov-request-router"
description: "Use when the user asks for Japan government-backed help but the requested action is broad or ambiguous, such as background, evidence, priority, owner, proposal context, citation check, KPI, budget, case, chart data, or a specific whitepaper. Do not use for legal advice, latest news only, application procedures, or non-Japan government research."
---

# Japan Gov Request Router

Route user instructions to the right Japan government document workflow. This skill is an entry point only; it should not perform heavy research or download files.

Use this skill when the user's request sounds like:

- "背景を整理して"
- "根拠を探して"
- "重要度を確認して"
- "どの省庁の話か整理して"
- "提案書向けに直して"
- "引用が古くないか見て"
- "KPIを探して"
- "予算がついているか見て"
- "事例を拾って"
- "図表の元データを探して"
- "この白書を読んで"

## Routing

1. Classify the user's action.
   - background,社会背景,課題背景,政府の見方 -> `japan-gov-background-builder`
   - evidence,根拠,出典,裏付け -> `japan-gov-evidence-finder`
   - priority,重要度,国が重視,強まっているか -> `japan-gov-priority-checker`
   - owner,所管,省庁,制度文脈 -> `japan-gov-owner-mapper`
   - proposal,企画書,営業資料,官公庁向けに直す -> `japan-gov-proposal-context-adapter`
   - citation,引用,古い,最新版,URL監査 -> `japan-gov-citation-auditor`
   - KPI,指標,測る,統計 -> `japan-gov-kpi-finder`
   - budget,予算,事業,行政事業レビュー -> `japan-gov-budget-tracer`
   - case,事例,自治体事例,企業事例 -> `japan-gov-case-finder`
   - chart,図表,元データ,Excel,e-Stat -> `japan-gov-chart-data-tracer`
   - named whitepaper or chapter -> `japan-whitepaper-brief`
2. Preserve edition constraints.
   - If no year or period is specified, use the latest official edition by default.
   - If a year, era year, or comparison period is specified, pass that constraint through.
3. Check source fit.
   - Use whitepapers for official framing, longitudinal issues, policy priorities, and ministry viewpoints.
   - Redirect away from whitepapers when the user needs law text, current news, forms, deadlines, or procedural instructions.
4. Apply shared references when routing.
   - Use `../../references/egov-whitepaper-route-map.md` as the listed-whitepaper route snapshot.
   - Use `../../references/official-url-model.md` for edition and URL roles.
   - Use `../../references/download-cache-policy.md` if downstream reading requires local files.

## Output Expectations

- Name the downstream skill.
- State the classification reason.
- Restate the expected output shape.
- Mention when the request should use a source type other than whitepapers.

## Guardrails

- Do not download documents directly.
- Do not force a whitepaper workflow onto legal, procedural, or breaking-news questions.
- Do not hide mixed intent. Split the task when the user asks for both official context and current rules.
