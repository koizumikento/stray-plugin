---
name: "japan-gov-chart-data-tracer"
description: "Use when the user identifies a specific Japanese government chart, table, figure, source note, or statistic and wants its 元データ or reproducibility traced. Do not use to brainstorm KPIs or generally search e-Stat."
---

# Japan Gov Chart Data Tracer

Work backward from an identified official figure or number to its source data and transformations.

## Do Not Use For

- “What should we measure?” or candidate indicators; use `japan-gov-kpi-finder`.
- Searching, retrieving, or analyzing an e-Stat table without an identified upstream figure; use `japan-gov-estat-data-analyst`.
- Broad evidence collection without a figure, table, source note, or quoted statistic.

## Workflow

1. Identify the document, edition, figure/table number, title, page or section, source note, and displayed values. Ask only for the missing identifier needed to disambiguate.
2. Inspect the official landing page, linked Excel/CSV, statistical appendix, and source note.
   - Follow `../../references/official-url-model.md` and `../../references/egov-whitepaper-route-map.md`.
   - Cache only needed files under `../../references/download-cache-policy.md`.
3. Trace the chain from rendered figure to reproduced table, original survey/table, and downloadable data. Record every aggregation, rebasing, deflation, seasonal adjustment, estimate, or author calculation disclosed.
4. Classify the result as `original data`, `official reproduced data`, `processed estimate`, `commissioned survey`, or `rendered-only`.
5. If the chain resolves to an e-Stat `statsDataId` and retrieval or reanalysis is requested, pass the identified ID, filters, and transformation notes to `japan-gov-estat-data-analyst` and continue in the same task.
6. Attempt one official data-page route and one named-survey route after the document links. If neither verifies the source, stop and report the unresolved link.

## Output

| Figure/statistic | Document location | Source-data candidate | Transformation | Format/ID | Reproducible? | Caveat |
|---|---|---|---|---|---|---|

Also include `追跡経路`, `取得可能なデータ`, `再現手順`, `未解決点`, and `取得した資料`.

## Guardrails

- Do not call a chart reproducible when only a rendered PDF or incomplete source note exists.
- Do not erase transformations, survey scope, breaks in series, or estimation.
- Prefer official APIs/tables over bulk scraping and cite official landing pages.
