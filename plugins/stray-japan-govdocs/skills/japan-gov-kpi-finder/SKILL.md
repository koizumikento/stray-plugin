---
name: "japan-gov-kpi-finder"
description: "Use when the user asks for official indicators, KPI candidates, measurable outcomes, or statistics to measure a social or policy issue in Japan. Do not use for broad background, quote collection, budget tracing, or legal/procedural lookup."
---

# Japan Gov KPI Finder

Find official KPI or indicator candidates for a Japan policy or social issue.

Use this skill when the user asks:

- "買い物弱者問題を測る公式指標はある?"
- "孤独・孤立対策のKPI候補を出して"
- "この施策のアウトカム指標に使える統計を探して"

## Workflow

1. Define the issue and what should be measured.
2. Search whitepaper figures, e-Stat, ministry statistics pages, policy plans, and administrative review sheets.
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
