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

1. Fix the statistical action and scope: discovery, retrieval, comparison, or analysis; topic; geography; period; unit; population; desired output grain; and any requested row limit.
2. Inspect exposed tools and any available tool search before determining access state. Honor an explicitly required MCP; otherwise match the required e-Stat capability by description and input schema, not only the example server name `e-stats-mcp`.
   - `available`: a verified matching tool responds; continue with it.
   - `tool unavailable`: no matching tool is found after discovery; continue bounded work through official e-Stat pages, verified downloads, or supplied data. If the user requires a named MCP, report that requirement as unmet and link only verified setup documentation; do not present fallback work as MCP execution.
   - `credential/authorization failure`: report the actual missing or rejected credential (for example, `E_STAT_APP_ID`) without exposing its value; do not retry with guessed credentials.
   - `tool/data error`: preserve the error and try one narrower query or official table page, then stop if the same failure remains.
3. Discover narrowly. Use a supplied `statsDataId` directly; otherwise search by official statistic, survey, geography, and period. After two materially different narrowed searches return no suitable candidate, report the queries and stop.
4. Inspect metadata before values: table title, dimensions/codes, geography, time axis, unit, annotations, update date, and required filters.
5. Retrieve through the verified single-table tool (such as `get_stats_data`) and use bulk tools only for a justified multi-table request. When MCP is unavailable, official downloadable files may be used only if their table identity and metadata are verified; label this `official-web fallback`, not an MCP result. Identify supplied data separately and verify its provenance, table identity, and metadata before use.
6. Verify retrieval coverage before aggregating or ranking:
   - Confirm whether the tool retrieves all pages automatically; otherwise follow `NEXT_KEY` using `startPosition` within the requested bounds.
   - Record filters, row limit, retrieved count, and the filtered `TOTAL_NUMBER` when available. Reconcile counts and verify that no continuation remains before calling the result `complete` for the selected scope.
   - Mark intentional capped retrieval `limited`; mark failed pages, mismatched counts, or unverified coverage `incomplete`, retaining the error and remaining range. For files, use verified table/file coverage and row counts as completion evidence instead of API pagination fields.
7. Separate published values from agent-derived calculations. Check comparable definitions, units, seasonal adjustment, survey/calendar/fiscal year, and breaks in series.
8. Return exact table IDs, selected codes/filters, official URL, access path, and reproduction notes.

## Output

For discovery:

| Candidate | statsDataId | Survey/table | Coverage | Time/unit | Fit | Caveat |
|---|---|---|---|---|---|---|

For analysis:

| Result | Source table | Filters/dimensions | Period/area | Unit | Published or derived | Caveat |
|---|---|---|---|---|---|---|

Also include `アクセス状態`, `使用したツールまたはfallback`, `取得範囲・件数・完了状態`, `再現メモ`, `除外候補`, and `停止理由・追加確認`.

## Guardrails

- Do not fabricate table IDs, values, MCP availability, or successful retrieval.
- Do not compare tables before definitions, dimensions, units, and time bases are compatible.
- Do not present limited or incomplete retrieval as a complete national total or ranking; confine conclusions to the verified coverage.
- Do not hide filters or present agent-derived estimates as published official statistics.
