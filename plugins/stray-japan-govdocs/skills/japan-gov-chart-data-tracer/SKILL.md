---
name: "japan-gov-chart-data-tracer"
description: "Use when the user asks to find the source data behind a chart, table, figure, graph, 図表, 元データ, Excel, e-Stat, or statistic in a Japanese government whitepaper or official document. Trigger on 白書のグラフの元データ, 図表を再分析, 統計表を探して. Do not use for ordinary summary, broad evidence collection, or KPI brainstorming without a specific figure or statistic."
---

# Japan Gov Chart Data Tracer

Trace whitepaper charts and figures back to official source data where possible.

Use this skill when the user asks:

- "白書のこのグラフの元データを探して"
- "この図表を再分析できる形にしたい"
- "白書の統計表がe-Statにあるか確認して"

## Workflow

1. Identify the chart, table, figure number, title, edition, and source note.
2. Check the whitepaper's linked Excel, CSV, statistical appendix, or data page.
3. Search e-Stat or ministry statistics pages when the source note names an official survey.
4. Distinguish original data, reproduced table, processed estimate, and commissioned survey.
5. Return retrievable data links and limitations.

## Output Expectations

| Figure/statistic | Whitepaper source | Source data candidate | Format | Can reproduce? | Caveat |
|---|---|---|---|---|---|

Also include `取得できるデータ`, `取得できない理由`, `再利用時の注意`, and `取得した資料`.

## Guardrails

- Do not claim a chart is reproducible when only a rendered PDF exists.
- Do not scrape bulk data when a source API or official table exists.
- Do not ignore transformations, estimates, or survey scope.
