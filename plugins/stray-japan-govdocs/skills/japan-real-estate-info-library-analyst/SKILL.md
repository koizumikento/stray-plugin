---
name: "japan-real-estate-info-library-analyst"
description: "Use when the user wants MLIT Real Estate Information Library data retrieved, mapped, compared, or analyzed for a defined place/layer. Do not trigger on 地価・不動産 policy discussion without a data operation."
---

# Japan Real Estate Info Library Analyst

Retrieve and analyze official real-estate/geospatial layers with explicit geography, access state, derivations, and interpretation limits.

## Do Not Use For

- General housing/land-price policy background without data retrieval; use `japan-gov-background-builder`.
- Project LINKS datasets; use `japan-gov-project-links-data-analyst`.
- Appraisal, investment, legal, listing, or private parcel/owner requests.

## Workflow

1. Require a data action and scope: address/municipality/coordinates, radius or tile, property/layer type, period, and output. A topic word such as `地価` alone is not enough.
2. Determine access state:
   - `available`: configured `reinfolib-mcp` responds; continue.
   - `tool unavailable`: report missing MCP configuration and use public official landing/specification pages only for bounded metadata discovery.
   - `credential/authorization failure`: report the missing/rejected `REINFOLIB_API_KEY`; do not guess credentials.
   - `tool/data error`: retain the error and try one narrower geography/layer request; if it repeats, stop.
3. Resolve municipality codes before transaction queries when needed. Use coordinate/geospatial paths for land prices, planning, facilities, ridership, population mesh, or risk layers.
4. Prefer GeoJSON for mapping/spatial joins and JSON/table output for summaries. Record feature count, geometry/CRS assumptions, period, layer name, missing/generalized values, and tile `z/x/y` when used.
5. Separate official records from derived medians, averages, counts, buffers, and spatial joins. State formulas, buffers, CRS, join behavior, and excluded records.
6. When API access is unavailable, label public-page findings `official-web fallback`; do not claim unavailable values or coverage. Stop if the requested result requires API-only data.
7. Report that the result is exploratory official-data analysis, not an appraisal or legal conclusion.

## Output

| Finding | Data type/layer | Area/coordinates | Period | Method | Published or derived | Caveat |
|---|---|---|---|---|---|---|

Also include `アクセス状態`, `使用したMCPツールまたはfallback`, `再現メモ`, `地理条件`, `データ限界`, and `停止理由・追加確認`.

## Guardrails

- Do not infer a specific property's exact market value or expose/infer personal information.
- Do not merge spatial layers without explicit buffers, CRS assumptions, and join behavior.
- Do not treat hazard or planning layers as a substitute for current local legal confirmation.
