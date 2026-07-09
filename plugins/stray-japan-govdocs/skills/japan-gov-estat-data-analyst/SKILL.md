---
name: "japan-gov-estat-data-analyst"
description: "Use when the user wants an e-Stat 統計表 searched, retrieved, filtered, compared, or analyzed, including a statsDataId. Do not use for KPI ideation or tracing an identified whitepaper chart before its source table is known."
---

# Japan Gov e-Stat Data Analyst

Retrieve or analyze Japanese official statistics while keeping table IDs, metadata, dimensions, filters, units, and access path reproducible.

## Do Not Use For

- Candidate measures or KPI design before a table is selected; use `japan-gov-kpi-finder`.
- Tracing an identified chart or source note to its underlying table; start with `japan-gov-chart-data-tracer`.
- Project LINKS or Real Estate Information Library data.

## Workflow

1. Fix the statistical action and scope: discovery, retrieval, comparison, or analysis; topic; geography; period; unit; population; and desired output grain.
2. Determine the access state before promising data:
   - `available`: configured `e-stats-mcp` responds; continue with it.
   - `tool unavailable`: no MCP tool is configured; use official e-Stat web/table pages for bounded discovery and setup guidance.
   - `credential/authorization failure`: report the missing or rejected `E_STAT_APP_ID`; do not retry with guessed credentials.
   - `tool/data error`: preserve the error and try one narrower query or official table page, then stop if the same failure remains.
3. Discover narrowly. Use a supplied `statsDataId` directly; otherwise search by official statistic, survey, geography, and period. After two materially different narrowed searches return no suitable candidate, report the queries and stop.
4. Inspect metadata before values: table title, dimensions/codes, geography, time axis, unit, annotations, update date, and required filters.
5. Retrieve through `get_stats_data` for one table and bulk tools only for a justified multi-table request. When MCP is unavailable, official downloadable files may be used only if their table identity and metadata are verified; label this `official-web fallback`, not an MCP result.
6. Separate published values from agent-derived calculations. Check comparable definitions, units, seasonal adjustment, survey/calendar/fiscal year, and breaks in series.
7. Return exact table IDs, selected codes/filters, official URL, access path, and reproduction notes.

## Output

For discovery:

| Candidate | statsDataId | Survey/table | Coverage | Time/unit | Fit | Caveat |
|---|---|---|---|---|---|---|

For analysis:

| Result | Source table | Filters/dimensions | Period/area | Unit | Published or derived | Caveat |
|---|---|---|---|---|---|---|

Also include `アクセス状態`, `使用したツールまたはfallback`, `再現メモ`, `除外候補`, and `停止理由・追加確認`.

## Guardrails

- Do not fabricate table IDs, values, MCP availability, or successful retrieval.
- Do not compare tables before definitions, dimensions, units, and time bases are compatible.
- Do not hide filters or present agent-derived estimates as published official statistics.
