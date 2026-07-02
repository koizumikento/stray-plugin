---
name: "japan-gov-kpi-finder"
description: "Use when the user asks for official indicators, KPI candidates, measurable outcomes, 指標, 統計, or ways to measure a social or policy issue in Japan. Trigger on KPIを探して, 公式指標, 公的統計, 測る指標, アウトカム指標. Do not use for tracing the source data behind a specific chart, table, figure, or statistic; use japan-gov-chart-data-tracer for that. Do not use for broad background, quote collection, budget tracing, or legal/procedural lookup."
---

# Japan Gov KPI Finder

Find official KPI or indicator candidates for a Japan policy or social issue.

KPI finder discovers candidate indicators for a theme or intervention. It does not start from a specific figure/table/statistic; use `japan-gov-chart-data-tracer` when the task is to trace source data for an identified chart or number.

Use this skill when the user asks:

- "買い物弱者問題を測る公式指標はある?"
- "孤独・孤立対策のKPI候補を出して"
- "この施策のアウトカム指標に使える統計を探して"

## Workflow

1. Define the issue and what should be measured.
2. Search whitepaper figures, e-Stat, ministry statistics pages, policy plans, and administrative review sheets.
   - Start from official landing pages and URL roles in `../../references/official-url-model.md`.
   - Use `../../references/egov-whitepaper-route-map.md` for known whitepaper routes and slugs.
   - Download only task-needed files under `tmp/japan-govdocs/` following `../../references/download-cache-policy.md`; final citations stay on official URLs.
   - When the task requires actual e-Stat table search, metadata inspection, or data extraction, hand off to `japan-gov-estat-data-analyst`. Pass the candidate indicator name, the survey or statistics name, any known `statsDataId`, and the required geography and period; expect back table candidates or retrieved data with metadata and caveats.
   - Bound the search: inspect the latest official series page plus at most two relevant ministry, statistics, program, or database source families unless the user asks for exhaustive coverage.
   - If no official indicator supports the measurement need after those checks, stop widening the search and report it under `追加確認` or `公式根拠なし` with the checked sources.
3. Separate outcome indicators, output indicators, proxy indicators, and context indicators.
4. Record data source, update frequency, geography, time lag, and limitations.
5. Explain how each indicator can and cannot be used.

## Output Expectations

| Indicator | Type | Official source | Coverage | Update cycle | Why useful | Limitation |
|---|---|---|---|---|---|---|

Also include `おすすめKPI`, `代替指標`, `使うべきでない指標`, and `追加取得先`.

## Guardrails

- Do not present proxy indicators as direct outcomes.
- Do not mix survey years and publication years without labeling them.
- Do not fabricate e-Stat availability.
