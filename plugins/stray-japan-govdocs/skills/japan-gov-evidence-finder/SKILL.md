---
name: "japan-gov-evidence-finder"
description: "Use when the user asks for official Japanese government evidence, sources, or grounds to support a claim in a report, proposal, article, deck, or memo. Do not use for broad background building, citation freshness audits, KPI discovery, or budget tracing."
---

# Japan Gov Evidence Finder

Find official evidence for claims using Japanese government whitepapers, annual reports, statistics, and policy documents.

Use this skill when the user asks:

- "地方公共交通が危機的だと言える公的根拠を探して"
- "この記事に政府公式の出典を足して"
- "この主張を白書や公式統計で支えられるか見て"

## Workflow

1. Extract each claim that needs support.
2. Decide the right source type.
   - Whitepapers for official framing and longitudinal trends.
   - e-Stat or statistics pages for raw numerical values.
   - Laws or guidance for obligations and procedures.
3. Start from official landing pages and route maps.
4. Default to latest editions unless the claim requires a specific time point.
5. Read only the sections needed for each claim.
6. Mark claims that are weakly supported or need non-whitepaper sources.

## Output Expectations

| Claim | Evidence summary | Official source | Year/edition | Source location | Strength | Caution |
|---|---|---|---|---|---|---|

Also include `使える言い換え`, `弱い根拠`, `追加確認`, and `取得した資料`.

## Guardrails

- Do not invent quotes.
- Do not overquote source text.
- Do not treat a general policy concern as proof of a specific product need.
