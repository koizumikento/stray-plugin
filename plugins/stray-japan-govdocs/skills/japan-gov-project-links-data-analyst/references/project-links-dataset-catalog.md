# Project LINKS Dataset Catalog

This reference is a starting map for MLIT Project LINKS datasets under the G-Spatial Information Center organization `sosei-joho`. Verify current metadata with CKAN before using it.

## Official Entry Points

- G-Spatial organization: `https://www.geospatial.jp/ckan/organization/sosei-joho`
- CKAN package search: `https://www.geospatial.jp/ckan/api/3/action/package_search?fq=organization%3Asosei-joho&rows=100&start=0`
- CKAN package detail: `https://www.geospatial.jp/ckan/api/3/action/package_show?id=<dataset-name>`
- MLIT Project LINKS: `https://www.mlit.go.jp/links/`

## CKAN Transport And Fallback

CKAN actions above are HTTPS JSON endpoints, not assumed local tool names.

1. Send a bounded GET request to `package_search`; paginate with `start` only when the returned `count` exceeds the rows already inspected.
2. Accept metadata only when the HTTP response is usable JSON and CKAN returns `"success": true`.
3. Resolve a selected dataset with `package_show` before using resource URLs, license fields, notes, or modification dates.
4. On transport failure, blocked scripted access, malformed JSON, or `success: false`, retain the exact failure and fall back in order:
   - organization HTML page;
   - individual CKAN dataset landing page;
   - MLIT Project LINKS page.
5. HTML/MLIT fallback proves only what is visible there. Do not claim complete live inventory, current resource URLs, or license metadata that the fallback did not expose.

## Source And Quality Model

Most datasets are created by MLIT Policy Bureau Information Policy Division for Project LINKS and published through G-Spatial Information Center.

Common rules:

1. Treat CKAN `package_show` metadata as the live source for resource URLs, license, area, period, quality notes, and restrictions.
2. Read the dataset's `99_*dataspecificationdocument*.xlsx` before interpreting columns or units.
3. Expect UTF-8 CSV for tabular data and GeoJSON for spatial resources.
4. Expect privacy, confidentiality, aggregation, hierarchy, suppression, masking, or generalization where notes mention those treatments.
5. Re-state the dataset's quality limitation when using results: completeness and accuracy are not guaranteed when data creation depends on source-document condition, submitted-report quality, or LINKS Veda extraction.

## Current Dataset Map

Snapshot checked from CKAN API on 2026-06-16. Re-check before analysis.

| Dataset name | Title | Domain | Main resources | Period/area from metadata | Analysis fit |
|---|---|---|---|---|---|
| `project-links` | Project LINKS ポータルサイト | Portal | Overview PDF | See linked datasets | Discover Project LINKS scope and official landing pages. |
| `links-mujinkoukuukihikoukeikaku-2025_` | 無人航空機飛行計画データ（2025年度） | Drone flight plans | Monthly flight-plan GeoJSON, accident CSV, specification XLSX | 2024-07 to 2025-06 for flight plans; accident data as of 2025-11; Japan | Spatial/monthly trend analysis, flight-area aggregation, accident context. |
| `links-mujinkoukuukihikoukeikaku-2024` | 無人航空機飛行計画データ（2024年度） | Drone flight plans | Monthly flight-plan GeoJSON, accident CSV, airspace GeoJSON, specification XLSX | 2022-12 to 2024-06 for flight plans; Japan | Longer drone-flight trend and airspace-overlay analysis. |
| `links_kankoutoukei_2025` | 観光統計データ（2025年度） | Tourism | Lodging statistics CSV, travel-consumption CSVs, specification XLSX | 2021-2024; Japan | Prefecture-level lodging and domestic travel spending analysis. |
| `links-ippanryokyaku-2025` | 一般旅客自動車運送事業関連データ（路線バス・貸切バス・タクシー）（2025年度） | Passenger road transport | Route bus, charter bus, taxi performance CSVs, business-overview CSV, specification XLSX | Verify metadata; national passenger transport business data | Bus/taxi performance and operator business condition analysis. |
| `links-akiyabank-2025` | 空き家・空き地バンク登録物件および成約物件データ（2025年度） | Vacant house/land bank | Registered property CSV, closed-deal property CSV, specification XLSX | As of 2025-03-31; Japan sample | Property attributes and transaction pattern exploration. |
| `links-naikoukaiungyou-2025` | 内航海運業データ（2025年度） | Coastal shipping | Business overview, seafarer situation, seafarer labor survey CSVs, specification XLSX | Vessel data before FY2023, FY2024-FY2025 for selected files; Japan | Operator, vessel, seafarer, labor and shipping business analysis. |
| `links-naikoukaiungyou-2024` | 内航海運業データ（2024年度） | Coastal shipping | Business overview, coastal shipping statistics, port survey CSVs, specification XLSX | FY2022 and 2013-FY2022 ranges by file; Japan | Historical coastal shipping and port-related analysis. |
| `links-tetsudoujigyou-2025` | 鉄道輸送実績・財務関連データ（2025年度） | Railway business | Six transport/finance CSVs and specification XLSX | FY2012-FY2022; Japan | Railway operator transport performance, route km, profit/loss, income statement, balance sheet analysis. |
| `links-rideshare-2025` | 自家用有償旅客運送データ（2025年度） | Public ride share | Transport performance CSV, registry CSV, specification XLSX | FY2020-FY2024 and FY2022-FY2025 ranges by file; Tokyo, Tokushima, Nagasaki transport offices | Public ride-share performance and registration analysis. |
| `links-rentacars-2025` | 貸渡実績報告書データ（2025年度） | Rental cars | Rental performance CSV, vehicle deployment CSV, specification XLSX | FY2023-FY2024 and FY2024 ranges by file; Japan | Rental-car utilization, vehicle count, rental fee and distance analysis. |
| `links-soukogyou-2025` | 倉庫業データ（2025年度） | Warehouse business | Warehouse usage/business condition CSVs, specification XLSX | FY2019-FY2024 and FY2015-FY2023 ranges by file; Japan | Warehouse use, capacity, and business-condition analysis. |
| `links-soukogyou-2024` | 倉庫業データ（2024年度） | Warehouse business | Warehouse registration/application CSV, usage report CSV, specification XLSX | Registration data before FY2023, FY2023 usage; Chubu transport bureau | Regional warehouse registration and usage analysis. |
| `links-kamotsujidousyaunsojigyo-2025` | 貨物自動車運送事業データ（2025年度） | Trucking/freight road transport | Business performance CSV, finance CSV, specification XLSX | FY2023; Nara transport office | Regional trucking performance and finance analysis. |
| `links-kamotsujidousyaunsojigyo-2024` | 貨物自動車運送事業データ（2024年度） | Trucking/freight road transport | Business performance CSV, finance CSV, specification XLSX | FY2015-FY2022 for performance; FY2015-FY2019 sample finance; Japan | National trucking performance and sample finance analysis. |
| `links-jidousyaunsoujigyoujiko-2025` | 自動車運送事業事故データ（2025年度） | Road transport accidents | Accident report and police-statistics integration CSV, specification XLSX | FY2023-FY2024; Japan | Recent commercial road-transport accident analysis. |
| `links-jidousyaunsoujigyoujiko-2024` | 自動車運送事業事故データ（2024年度） | Road transport accidents | Accident integration CSV, accident report CSV, specification XLSX | FY2023 for integrated file; FY2003-FY2023 for accident reports; Japan | Long-horizon accident report analysis and recent integrated accident context. |
| `links-ippanryokyakuteikikourojigyou-2024` | 一般旅客定期航路事業データ（2024年度） | Passenger ferry | Permit application CSV, ship accident report CSV, marine forecast area GeoJSON, specification XLSX | FY2007-FY2024, FY2008-FY2023, FY2023 by file; Japan/sample | Ferry route/ship attributes, accident, and marine-area aggregation analysis. |
| `links-modalshift-2024` | モーダルシフト関連データ（2024年度） | Modal shift | Coastal vessel transport statistics CSV, automobile transport statistics CSV, specification XLSX | FY2013-FY2023; Japan sample | Freight modal-shift baseline, transport distance, load factor, and origin-destination comparison. |

## Resource Selection Rules

1. For a domain question, first choose the dataset family, then inspect the latest and prior-year variants.
2. For analysis across years, prefer the dataset whose resources explicitly cover the requested historical range; do not assume the publication year equals coverage year.
3. For operator or business-performance analysis, start from business/performance CSVs and only add finance CSVs after checking compatible keys.
4. For spatial analysis, start with GeoJSON resources and inspect geometry and masking before spatial joins.
5. For dashboards, use the specification document to build human-readable metric labels and unit notes.

## Suggested Cache Layout

Use the shared Japan govdocs cache, with `mlit/project-links` as the source slug:

```text
tmp/japan-govdocs/downloads/mlit/project-links-<dataset-name>/<year>/<sha256-12>-<resource-name>
tmp/japan-govdocs/extracted/mlit/project-links-<dataset-name>/<year>/<sha256-12>-<resource-name>.txt
```

Manifest fields should include:

- `document_id`: `mlit-project-links-<dataset-name>`
- `title`: CKAN dataset title
- `ministry`: `国土交通省`
- `document_slug`: `project-links-<dataset-name>`
- `ministry_slug`: `mlit`
- `year`: publication or dataset year when clear
- `landing_page`: CKAN dataset URL
- `source_url`: CKAN resource URL
- `license_or_terms_url`: CKAN license URL and, when present, Project LINKS terms URL
- `notes`: source period, area, quality limitation, and whether the file was sampled or masked

## Common Output Cautions

Use these cautions when supported by dataset metadata:

- The data may have been processed for confidentiality and personal-information protection.
- Source reports may be sampled, limited to selected transport offices, or limited to selected operators.
- LINKS Veda extraction or source-document quality can affect completeness and accuracy.
- Data coverage period, metadata registration date, metadata modification date, and publication year are different concepts.
- Some datasets describe fiscal years while others use calendar months or as-of dates.
