---
name: "japan-gov-estat-data-analyst"
description: "Use when the user wants to search, retrieve, profile, compare, or analyze Japanese official statistics from e-Stat using e-stats-mcp. Trigger on e-Stat, 政府統計, 統計表, statsDataId, 統計データを取得, or official statistics analysis. Do not use for broad policy background, whitepaper-only evidence, Project LINKS datasets, non-Japan statistics, or legal/procedural advice."
---

# Japan Gov e-Stat Data Analyst

Find and analyze Japanese official statistics from e-Stat through `e-stats-mcp`, keeping the table ID, metadata, dimensions, filters, and limitations visible.

## Do Not Use For

- Broad background or policy framing without a concrete statistical data need; use `japan-gov-background-builder`.
- Candidate KPI discovery before an e-Stat table is needed; use `japan-gov-kpi-finder`.
- Source tracing for a specific whitepaper figure before the source note points to e-Stat; use `japan-gov-chart-data-tracer`.
- MLIT Project LINKS CSV/GeoJSON datasets; use `japan-gov-project-links-data-analyst`.
- Real-time weather or short-horizon forecasts; use `japan-weather-data-researcher`.

## Workflow

1. Scope the statistical question.
   - Resolve topic, geography, period, unit, population, and whether the user needs discovery, extraction, comparison, or a chart-ready table.
   - If the user provides a `statsDataId`, use it directly after fetching metadata.
2. Confirm `e-stats-mcp` availability.
   - Use the configured MCP tools when available.
   - If unavailable, stop with setup guidance: configure `e-stats-mcp` and provide `E_STAT_APP_ID`.
3. Discover tables narrowly.
   - Prefer `search_stats_by_keyword` for quick discovery and `get_stats_list` or `get_stats_list_csv` for structured filtering.
   - Avoid broad data-catalog calls until candidate stats codes or table IDs are narrowed.
4. Inspect metadata before data.
   - Use `get_meta_info` or `get_meta_info_csv` to identify dimensions, category codes, regions, time axes, units, and required filters.
   - Record the selected filters and explain excluded dimensions.
5. Retrieve data.
   - Use `get_stats_data` for one table and `get_stats_data_bulk` only when multiple IDs are truly needed.
   - Keep row limits explicit for previews; request broader data only after confirming the table shape.
6. Analyze and report.
   - Separate source values from derived indicators.
   - Label survey year, calendar year, fiscal year, publication/update timing, units, and geography.
   - Preserve official table names, `statsDataId`, and source URLs in the output.

## Output Expectations

For discovery:

| Candidate | statsDataId | Survey/table | Coverage | Time | Why it fits | Caveat |
|---|---|---|---|---|---|---|

For analysis:

| Result | Source table | Filter/dimension | Period/area | Unit | Derived? | Caveat |
|---|---|---|---|---|---|---|

Set `Derived?` to yes when the value is calculated by the agent (ratios, growth rates, aggregations) rather than published in the e-Stat table.

Also include `使用したMCPツール`, `再現メモ`, `除外した候補`, and `次に確認すべき統計`.

## Guardrails

- Do not fabricate e-Stat availability or table IDs.
- Do not compare values across tables until metadata, units, and definitions are checked.
- Do not hide filters or category codes that materially change the result.
- Do not call very broad catalog searches when a narrower table search can answer the question.
- Do not present an estimate as official if it is derived by the agent rather than published in e-Stat.
