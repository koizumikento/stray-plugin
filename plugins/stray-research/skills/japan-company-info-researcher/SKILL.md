---
name: "japan-company-info-researcher"
description: "Use when the user wants to search, retrieve, compare, or summarize Japanese company and corporate activity information using gbizinfo-mcp, including basic corporate profiles, certifications, awards, finance, patents, procurement, subsidies, or workplace data. Trigger on gBizINFO, gbizinfo, 法人情報, 法人番号, 企業情報, 補助金, 調達, 特許, 認定, or 表彰. Do not use for investment advice, private credit scoring, non-Japan company research, registry filings outside gBizINFO, or broad market research without a company lookup."
---

# Japan Company Info Researcher

Use `gbizinfo-mcp` to retrieve and summarize Japanese corporate information from gBizINFO while preserving corporate identifiers, endpoint provenance, and missing-data boundaries.

## Do Not Use For

- Investment recommendations, credit decisions, or definitive due diligence opinions.
- Non-Japan company research or private databases outside gBizINFO.
- Legal registry interpretation beyond summarizing retrieved fields.
- Broad market sizing or product research that does not require company lookup; use `domain-researcher` or `product-designer`.
- Patent landscape research across many sources; use `global-patent-researcher`.

## Workflow

1. Scope the company lookup.
   - Resolve company name, corporate number, location, industry, keyword, or target activity type.
   - Identify which data groups matter: basic, certification, award, corporation, finance, patent, procurement, subsidy, or workplace.
2. Confirm `gbizinfo-mcp` availability.
   - Use the configured MCP tools when available.
   - If unavailable, stop with setup guidance: configure `gbizinfo-mcp` and provide `GBIZINFO_API_TOKEN`.
3. Search before detail retrieval.
   - Use company search to disambiguate names unless the user provides a corporate number.
   - Show likely matches before deep retrieval when names are ambiguous.
4. Retrieve relevant endpoints.
   - Use only the needed `hojin_get_*` or `hojin_update_info_*` tools for the user's question.
   - Use `references/endpoint-guide.md` to map the question to the right data group, and verify actual tool names from the configured MCP tool list.
   - Preserve raw-field uncertainty when an endpoint returns empty or partial data.
5. Synthesize carefully.
   - Separate retrieved facts from inference.
   - Label the endpoint, corporate number, update timing when available, and absent data.

## Output Expectations

| Company | Corporate number | Data group | Finding | Source endpoint | Caveat |
|---|---|---|---|---|---|

Also include `使用したMCPツール`, `同名候補`, `取得できなかった情報`, and `追加確認`.

## Guardrails

- Do not treat absence from one endpoint as proof that an activity never occurred.
- Do not score companies, infer solvency, or make investment/credit recommendations.
- Do not merge similarly named companies without corporate-number confirmation.
- Do not expose secrets or API tokens in output.
- Stop if the requested data requires an API token that is not configured.
