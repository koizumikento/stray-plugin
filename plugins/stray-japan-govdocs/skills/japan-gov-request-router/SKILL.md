---
name: "japan-gov-request-router"
description: "Use only when the user asks for Japan government-backed help or Japanese government documents and the requested action is broad, mixed, or ambiguous. Trigger on unspecific requests like 政府資料で見て, 白書ベースで整理, 公式資料を探して, or どのスキルを使うべき. Do not use when the user clearly asks for KPI, budget, citation audit, named whitepaper reading, chart source data, Project LINKS dataset analysis, cache management, cases, owner mapping, priority check, evidence finding, background building, or proposal adaptation; route directly to the specialized skill instead. Do not use for legal advice, latest news only, application procedures, or non-Japan government research."
---

# Japan Gov Request Router

Route broad or ambiguous user instructions to the right Japan government document workflow. This skill is an entry point only; it should not perform heavy research or download files.

Use this skill when the user's request sounds like:

- "このテーマを政府資料ベースでどう調べるべき?"
- "白書や公式資料で何が言えるか整理して"
- "企画書に使うなら、どの公的資料から見るのが自然?"
- "政府資料を探したいが、根拠・KPI・予算のどれを見るべきか未整理"
- "この依頼は白書要約なのか出典探しなのか切り分けて"

Do not use this router when the user's action is already clear. In those cases invoke the matching skill directly:

- KPI/指標/測る/公的統計 -> `japan-gov-kpi-finder`
- 予算/事業/行政事業レビュー -> `japan-gov-budget-tracer`
- 引用/最新版/URL監査/出典監査 -> `japan-gov-citation-auditor`
- named whitepaper, annual report, chapter, or government PDF to read -> `japan-whitepaper-brief`
- 図表/表/グラフ/統計値の元データ -> `japan-gov-chart-data-tracer`
- 一時保存/キャッシュ/manifest/local path -> `japan-govdoc-cache-manager`
- 事例/自治体事例/企業事例 -> `japan-gov-case-finder`
- 所管/省庁/制度文脈 -> `japan-gov-owner-mapper`
- 優先度/国が重視/政策上強まったか -> `japan-gov-priority-checker`
- 根拠/出典/裏付け for a claim -> `japan-gov-evidence-finder`
- 背景/社会背景/課題背景 -> `japan-gov-background-builder`
- proposal/企画書/営業資料/官公庁向け wording -> `japan-gov-proposal-context-adapter`
- Project LINKS/G空間LINKS/geospatial.jp `sosei-joho` dataset inventory, inspection, download, profiling, or analysis -> `japan-gov-project-links-data-analyst`

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
   - cache,一時保存,ローカル保存,PDF/HTML保存,manifest,索引 -> `japan-govdoc-cache-manager`
   - named whitepaper or chapter to read directly -> `japan-whitepaper-brief`
   - named whitepaper used only as one source for proposal wording -> `japan-gov-proposal-context-adapter`
   - Project LINKS, G空間LINKS, `geospatial.jp/ckan/organization/sosei-joho`, 国交省LINKSデータの一覧化/分析 -> `japan-gov-project-links-data-analyst`
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
