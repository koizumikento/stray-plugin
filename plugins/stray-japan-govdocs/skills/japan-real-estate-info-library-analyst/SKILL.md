---
name: "japan-real-estate-info-library-analyst"
description: "Use when the user wants to retrieve, compare, map, or analyze Japan MLIT Real Estate Information Library data using reinfolib-mcp, including real estate transaction prices, land prices, urban planning, nearby facilities, station ridership, population mesh, or disaster-risk geospatial data. Trigger on 不動産情報ライブラリ, reinfolib, 地価, 取引価格, 用途地域, 都市計画, 周辺施設, or 災害リスク. Do not use for Project LINKS datasets, broad housing policy background, legal real-estate advice, property valuation guarantees, or live real-estate listings."
---

# Japan Real Estate Info Library Analyst

Use `reinfolib-mcp` to retrieve and analyze MLIT Real Estate Information Library data with explicit geography, source type, and interpretation limits.

## Do Not Use For

- MLIT Project LINKS datasets; use `japan-gov-project-links-data-analyst`.
- Broad housing policy background without a data retrieval task; use `japan-gov-background-builder`.
- Legal advice, appraisal opinions, investment recommendations, or guaranteed property valuations.
- Live listings, broker inventory, private parcel records, or personally identifiable property-owner information.
- General web research about a neighborhood when official real estate library data is not required.

## Workflow

1. Scope the place and data need.
   - Resolve address, municipality code, prefecture, coordinates, radius, tile zoom, property type, period, and required output format.
   - Ask for a location only if neither address/municipality nor coordinates can be inferred safely.
2. Confirm `reinfolib-mcp` availability.
   - Use the configured MCP tools when available.
   - If unavailable, stop with setup guidance: configure `reinfolib-mcp` and provide `REINFOLIB_API_KEY`.
3. Choose the narrowest data path.
   - Use municipality search before transaction search when codes are unknown.
   - Use coordinate/geospatial tools for land price, urban planning, facilities, station ridership, population mesh, or disaster risk.
   - Prefer GeoJSON when the user needs mapping or spatial joins; prefer JSON summaries for brief tabular answers.
4. Retrieve and profile data.
   - Confirm feature counts, date ranges, geometry types, coordinate assumptions, and any missing or generalized values.
   - For tiles, record zoom, x, y, and how coordinates were converted.
5. Analyze conservatively.
   - Separate official records from agent-derived summaries such as averages, medians, or spatial counts.
   - Label transaction periods, land-price reference years, facility types, and risk-layer names.
6. Report with clear limits.
   - Explain that results are official-source data retrieval and exploratory analysis, not appraisal, legal, or investment advice.

## Output Expectations

| Finding | Data type | Area/coordinates | Period/layer | Method | Caveat |
|---|---|---|---|---|---|

Also include `使用したMCPツール`, `再現メモ`, `地理条件`, `データ限界`, and `追加確認`.

## Guardrails

- Do not infer exact market value for a specific property unless the user provides a defensible valuation methodology and asks only for data support.
- Do not merge layers by proximity without stating buffers, CRS assumptions, and join behavior.
- Do not expose or infer personal information.
- Do not treat disaster-risk or urban-planning layers as a complete substitute for local legal confirmation.
- Stop if the requested data requires an API key that is not configured.
