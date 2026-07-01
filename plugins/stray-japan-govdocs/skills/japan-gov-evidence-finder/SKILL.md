---
name: "japan-gov-evidence-finder"
description: "Use when the user asks for official Japanese government evidence, sources, 出典, 根拠, 裏付け, or government資料 to support a claim in a report, proposal, article, deck, or memo. Trigger on 白書で根拠, 政府公式の出典, 公的根拠, 公式資料で支える. Do not use for broad background building, citation freshness audits, KPI discovery, budget tracing, or cache-only tasks."
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
   - Use `japan-gov-estat-data-analyst` when the claim needs e-Stat table discovery, metadata inspection, or retrieved numeric data.
3. Start from official landing pages and route maps.
   - Follow official URL roles in `../../references/official-url-model.md`.
   - Use `../../references/egov-whitepaper-route-map.md` for known whitepaper routes and slugs.
   - Use `../../references/download-cache-policy.md` only for task-needed downloads; final citations stay on official URLs.
   - Bound the search: inspect the latest official series page plus at most two relevant ministry, statistics, program, or database source families unless the user asks for exhaustive coverage.
   - If no official source supports the claim after those checks, stop widening the search and report it under `追加確認` or `公式根拠なし` with the checked sources.
4. Default to latest editions unless the claim requires a specific time point.
5. Read only the sections needed for each claim.
6. Mark claims that are weakly supported or need non-whitepaper sources.

## Output Expectations

| Claim | Evidence summary | Official source | Year/edition | Source location | Strength | Caution |
|---|---|---|---|---|---|---|

Also include `使える言い換え`, `弱い根拠`, `追加確認`, and `取得した資料`.

## Validation Expectations

Before final output, verify each cited source has an official landing URL, year or edition, section/table/figure location when available, and a clear source role from `../../references/official-url-model.md`. If any item cannot be verified, downgrade confidence and place it under `追加確認` rather than presenting it as confirmed evidence.

## Guardrails

- Do not invent quotes.
- Do not overquote source text.
- Do not treat a general policy concern as proof of a specific product need.
