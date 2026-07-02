---
name: "japan-gov-project-links-data-analyst"
description: "Use when the user wants to find, inspect, download, profile, join, analyze, or summarize MLIT Project LINKS datasets from G-Spatial Information Center, including transport, tourism, logistics, aviation, housing, accident, and business-performance CSV/GeoJSON data. Trigger on Project LINKS, G空間のLINKS, geospatial.jp/ckan/organization/sosei-joho, 国交省LINKSデータ, or these datasetsを分析. Do not use for broad government background, ordinary whitepaper evidence collection, chart-source tracing outside Project LINKS, real-time timetable/GTFS work, or legal/procedural advice."
---

# Japan Gov Project LINKS Data Analyst

Analyze MLIT Project LINKS open datasets from G-Spatial Information Center with source traceability, dataset-specific caution, and reproducible data handling.

Use this skill when the user asks to inventory, choose, inspect, download, profile, or analyze Project LINKS datasets, especially under the G-Spatial organization `sosei-joho`.

## Do Not Use For

- Broad Japan policy background or social issue framing; use `japan-gov-background-builder`.
- Official evidence for a claim when the data source is not already Project LINKS; use `japan-gov-evidence-finder`.
- KPI candidate discovery without a Project LINKS dataset focus; use `japan-gov-kpi-finder`.
- Tracing source data behind a specific whitepaper chart or figure outside Project LINKS; use `japan-gov-chart-data-tracer`.
- Current operation data such as live timetables, GTFS feeds, fares, flight status, or real-time transport service APIs.
- Legal, licensing, application, or procedural advice beyond summarizing official terms and dataset cautions.

## Workflow

1. Scope the user's data question.
   - Identify the domain: rail, road freight, passenger road transport, ride share, rental cars, warehouse, coastal shipping, passenger ferry, modal shift, drone flight plans, transport accidents, tourism, or vacant houses.
   - Identify the operation: catalog, dataset selection, schema inspection, data profiling, metric calculation, joining, visualization, or source-backed summary.
   - Resolve requested years, geography, operators, transport modes, or administrative offices before downloading data.
2. Verify the current source inventory live.
   - Start from the G-Spatial CKAN organization or `package_search` for `organization:sosei-joho`.
   - Use `package_show` for selected datasets before relying on resource names, URLs, license text, periods, or quality notes.
   - Use `references/project-links-dataset-catalog.md` as a starting map, not as the source of truth.
3. Select only the needed resources.
   - Read the dataset notes and the `99_*dataspecificationdocument*.xlsx` resource before interpreting CSV or GeoJSON columns.
   - If no specification document resource exists, keep the raw column names as-is, treat units and definitions as unverified, and record that limitation under `注意`.
   - Download only task-needed resources and follow `../../references/download-cache-policy.md`.
   - Prefer official CKAN resource URLs and cite dataset landing pages in final output.
4. Profile before analysis.
   - Confirm encoding, row count, column names, units, period coverage, geography, key fields, missing values, suppressed or bucketed values, and duplicate rows.
   - For GeoJSON, confirm coordinate reference assumptions, geometry type, feature count, and whether locations have been generalized or masked.
   - For joins, state the join keys, grain, one-to-one or one-to-many behavior, and rows dropped or duplicated.
5. Analyze conservatively.
   - Keep calculations reproducible from named files and columns.
   - Separate values directly present in the dataset from derived indicators.
   - Avoid comparing datasets across years or domains until file definitions, units, and sampling or masking rules are checked.
6. Report with provenance and limitations.
   - Include dataset name, resource names, period, area, license or terms URL, fetched or checked date, and quality cautions.
   - State whether the result is suitable for exploratory analysis, policy memo support, dashboarding, or only a rough check.

## Reference Use

- Use `references/project-links-dataset-catalog.md` for known datasets, domains, resource patterns, CKAN endpoints, and skill-design notes.
- Use `../../references/download-cache-policy.md` for local cache layout and manifest fields.
- Use `../../references/official-url-model.md` only for general official URL role discipline; Project LINKS dataset truth comes from CKAN metadata and MLIT Project LINKS pages.

## Output Expectations

For catalog or dataset-selection requests, return:

| Dataset | Domain | Resources | Period/area | Best for | Cautions |
|---|---|---:|---|---|---|

For analysis requests, return:

| Result | Dataset/resource | Calculation | Period/area | Caveat |
|---|---|---|---|---|

Also include:

- `使用データ`: dataset landing page, resource names, and specification document.
- `再現メモ`: files, columns, filters, joins, and units.
- `注意`: Project LINKS quality notes, masking/statistical processing, and limits on interpretation.
- `次に見るべきデータ`: adjacent Project LINKS datasets or official statistics when relevant.

## Guardrails

- Do not treat Project LINKS data as complete administrative truth; many datasets are processed, sampled, masked, or created from submitted reports.
- Do not infer exact individual, operator, route, property, aircraft, or accident details when metadata says data has been anonymized, generalized, aggregated, or suppressed.
- Do not mix fiscal years, calendar years, publication years, registration dates, and metadata modification dates without labels.
- Do not publish local cache paths as citations; cite official CKAN or MLIT URLs.
- Stop and report the issue if a dataset page, resource URL, license, or specification document cannot be verified live.
