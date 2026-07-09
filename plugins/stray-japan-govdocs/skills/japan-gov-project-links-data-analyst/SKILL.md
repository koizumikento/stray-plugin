---
name: "japan-gov-project-links-data-analyst"
description: "Use when the user wants 国交省Project LINKS・G空間 datasets cataloged, retrieved, profiled, joined, or analyzed. Do not use for generic policy research, live transport feeds, or non-LINKS geospatial data."
---

# Japan Gov Project LINKS Data Analyst

Work with MLIT Project LINKS datasets using live CKAN metadata, explicit transport/fallback paths, and reproducible file-level analysis.

## Do Not Use For

- Policy background or claim evidence not centered on a Project LINKS dataset.
- Real-time timetables, GTFS, fares, flight status, or operational APIs.
- Real Estate Information Library retrieval; use `japan-real-estate-info-library-analyst`.

## Workflow

1. Define the domain, operation (catalog/select/inspect/download/profile/join/analyze), years, geography, grain, and output.
2. Verify live inventory through the CKAN JSON API over HTTPS:
   - GET `https://www.geospatial.jp/ckan/api/3/action/package_search?fq=organization:sosei-joho&rows=<bounded>`.
   - GET `https://www.geospatial.jp/ckan/api/3/action/package_show?id=<dataset-name>`.
   - Treat `success: true` and the returned result as CKAN metadata; do not mistake `package_search` for a local tool name.
3. If the API is unavailable, blocked, or malformed, record the transport/error and fall back in order: G-Spatial organization page → dataset landing page → MLIT Project LINKS page. A fallback can verify discoverability, but not unobserved resource URLs, license fields, or completeness.
4. Use `references/project-links-dataset-catalog.md` only as a dated starting map. Select task-needed resources and read the dataset notes plus `99_*dataspecificationdocument*.xlsx` before interpreting columns.
5. Follow `../../references/download-cache-policy.md`; cite CKAN dataset landing pages and official resource URLs rather than local cache paths.
6. Profile encoding, rows, fields, units, periods, geography, keys, missing/duplicate/suppressed values, and spatial generalization. For joins, record grain, keys, cardinality, dropped rows, and duplications.
7. Separate published fields from derived calculations and validate cross-year/domain compatibility.
8. Stop and report the last verified level if the dataset page, needed resource, license/terms, or specification cannot be verified.

## Output

For selection:

| Dataset | Domain | Verified resources | Period/area | Best for | Cautions |
|---|---|---|---|---|---|

For analysis:

| Result | Dataset/resource | Calculation | Period/area | Published or derived | Caveat |
|---|---|---|---|---|---|

Also include `アクセス経路とfallback`, `使用データ`, `再現メモ`, `品質・匿名化上の注意`, and `最終確認日`.

## Guardrails

- Do not treat processed, sampled, masked, or submitted-report data as complete administrative truth.
- Do not infer individual/operator/property/aircraft details from generalized data.
- Do not mix fiscal, calendar, publication, registration, and metadata dates without labels.
