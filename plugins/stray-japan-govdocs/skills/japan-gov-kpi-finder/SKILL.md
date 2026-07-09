---
name: "japan-gov-kpi-finder"
description: "Use when the user asks what official 指標 or KPI candidates could measure a Japanese social issue or intervention. Do not use to trace a specific chart or to retrieve/analyze a chosen e-Stat table."
---

# Japan Gov KPI Finder

Design a source-backed measurement shortlist before committing to a particular statistical table.

## Do Not Use For

- Source data behind an identified figure or number; use `japan-gov-chart-data-tracer`.
- Search, extraction, or analysis of a selected e-Stat table; use `japan-gov-estat-data-analyst`.
- General background with no measurement decision.

## Workflow

1. Define the decision, intervention logic, population, geography, time horizon, and what change should count as success.
2. Build a measurement chain: `input` → `output` → `outcome` → `impact`, plus context and guardrail indicators.
3. Search official plans, administrative review sheets, whitepaper figures, ministry statistics, and e-Stat metadata for candidate definitions.
   - Follow `../../references/official-url-model.md`; search no more than the latest relevant series plus two source families unless exhaustive work is requested.
4. For each candidate, record definition/formula, numerator/denominator, source family, granularity, update frequency, lag, comparability, and failure mode. Mark proxies explicitly.
5. Rank a small primary set and alternatives against validity, actionability, timeliness, stability, and burden.
6. If the user then asks to fetch values or validate a specific e-Stat table, hand the selected definition and dimensions to `japan-gov-estat-data-analyst` and continue in the same task.
7. Stop after the bounded search if no official indicator fits; report the measurement gap instead of inventing availability.

## Output

| Indicator | Role | Definition/formula | Official source family | Coverage/update | Decision use | Limitation |
|---|---|---|---|---|---|---|

Also include `推奨KPIセット`, `代替・proxy`, `guardrail指標`, `使うべきでない指標`, and `取得が必要な統計`.

## Guardrails

- Do not present a proxy or context indicator as a direct outcome.
- Do not mix survey, calendar, fiscal, and publication years without labels.
- Do not fabricate an e-Stat table ID or data availability during indicator design.
