---
name: "japan-gov-chart-data-tracer"
description: "Use when the user asks to find the source data behind a specific chart, table, figure, graph, 図表, 元データ, Excel, e-Stat, or statistic in a Japanese government whitepaper or official document. Trigger on 白書のグラフの元データ, この図表を再分析, この統計表を探して. Do not use for KPI brainstorming or candidate indicator discovery without a specific figure/table/statistic; use japan-gov-kpi-finder for that. Do not use for ordinary summary or broad evidence collection."
---

# Japan Gov Chart Data Tracer

Trace whitepaper charts and figures back to official source data where possible.

Chart-data tracing starts from an identified figure, table, source note, or statistic and works backward to source data. If the user needs candidate metrics for a policy issue, use `japan-gov-kpi-finder`.

Use this skill when the user asks:

- "白書のこのグラフの元データを探して"
- "この図表を再分析できる形にしたい"
- "白書の統計表がe-Statにあるか確認して"

## Workflow

1. Identify the chart, table, figure number, title, edition, and source note.
2. Check the whitepaper's linked Excel, CSV, statistical appendix, or data page.
   - Start from official landing pages and URL roles in `../../references/official-url-model.md`.
   - Use `../../references/egov-whitepaper-route-map.md` for known whitepaper routes and slugs.
   - Download only task-needed files under `tmp/japan-govdocs/` following `../../references/download-cache-policy.md`; final citations stay on official URLs.
3. Search e-Stat or ministry statistics pages when the source note names an official survey.
   - When the source data is an e-Stat table and the user needs retrieval or reanalysis, hand off to `japan-gov-estat-data-analyst`. Pass the `statsDataId` or survey/table name, the whitepaper edition and figure number, the needed dimensions and filters, and the official source URL; expect back the retrieved table with metadata, applied filters, and caveats.
4. Distinguish original data, reproduced table, processed estimate, and commissioned survey.
5. Return retrievable data links and limitations.

## Output Expectations

| Figure/statistic | Whitepaper source | Source data candidate | Format | Transformed? | Can reproduce? | Caveat |
|---|---|---|---|---|---|---|

Set `Transformed?` to yes with the transformation method (aggregation, estimate, index, commissioned processing) when the whitepaper figure is not the raw source data as published.

Also include `取得できるデータ`, `取得できない理由`, `再利用時の注意`, and `取得した資料`.

## Guardrails

- Do not claim a chart is reproducible when only a rendered PDF exists.
- Do not scrape bulk data when a source API or official table exists.
- Do not ignore transformations, estimates, or survey scope.
