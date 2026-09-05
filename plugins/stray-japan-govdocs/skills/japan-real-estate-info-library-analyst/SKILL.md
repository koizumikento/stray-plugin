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
2. Inspect exposed tools and any available tool search before determining access state. Honor an explicitly required MCP; otherwise match the required official data capability by description and input schema, not only the example server name `reinfolib-mcp`.
   - `available`: a verified matching tool responds; continue.
   - `tool unavailable`: no matching tool is found after discovery; continue bounded metadata discovery through public official landing/specification pages or analyze supplied data with verified provenance and coverage. If the user requires a named MCP, report that requirement as unmet and link only verified setup documentation; do not present fallback work as MCP execution.
   - `credential/authorization failure`: report the actual missing/rejected credential (for example, `REINFOLIB_API_KEY`) without exposing its value; do not guess credentials.
   - `tool/data error`: retain the error and try one narrower geography/layer request; if it repeats, stop.
3. Resolve municipality codes before transaction queries when needed. Use coordinate/geospatial paths for land prices, planning, facilities, ridership, population mesh, or risk layers.
4. Prefer GeoJSON for mapping/spatial joins and JSON/table output for summaries. Record feature count, geometry/CRS assumptions, period, layer name, missing/generalized values, and tile `z/x/y` when used.
5. Separate official records from derived medians, averages, counts, buffers, and spatial joins. State formulas, buffers, CRS, join behavior, and excluded records.
6. When API access is unavailable, label public-page findings `official-web fallback` and identify supplied data separately; do not claim unavailable values or coverage. Report the unresolved portion if it requires API-only data, while completing supported work.
7. Report that the result is exploratory official-data analysis, not an appraisal or legal conclusion.

## Output

| Finding | Data type/layer | Area/coordinates | Period | Method | Published or derived | Caveat |
|---|---|---|---|---|---|---|

Also include `アクセス状態`, `使用したMCPツールまたはfallback`, `再現メモ`, `地理条件`, `データ限界`, and `停止理由・追加確認`.

## Guardrails

- Do not infer a specific property's exact market value or expose/infer personal information.
- Do not merge spatial layers without explicit buffers, CRS assumptions, and join behavior.
- Do not treat hazard or planning layers as a substitute for current local legal confirmation.
