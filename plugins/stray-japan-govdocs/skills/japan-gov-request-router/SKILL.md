---
name: "japan-gov-request-router"
description: "Use only when a 政府資料・白書 request is broad, mixed, or ambiguous and its primary action is unclear. Classify by requested action, then apply the specialized skill in the same task; do not stop at routing."
---

# Japan Gov Request Router

Resolve mixed or ambiguous requests by the requested deliverable, not isolated keywords. This router must dispatch and continue; it is not a research or download endpoint.

## Do Not Use For

- A request whose action already clearly matches one specialist skill; apply that skill directly.
- Legal advice, application procedures, breaking news only, or non-Japan government research.

## Workflow

1. Identify the primary object and action: a document to read, a claim to support, a citation to audit, a measurement to design, data to retrieve, or a proposal to synthesize.
2. Apply the first matching action test in this ordered table. Examples and nouns do not override the action test.

| Order | Requested action / distinguishing test | Downstream skill |
|---:|---|---|
| 1 | Save, inspect, repair, index, or trace local cached files | `japan-govdoc-cache-manager` |
| 2 | Turn an offer into proposal/営業/企画 wording; a named document is only an input | `japan-gov-proposal-context-adapter` |
| 3 | Read or brief a named whitepaper, chapter, report, or government PDF as the primary object | `japan-whitepaper-brief` |
| 4 | Audit supplied citations, URLs, editions, or freshness | `japan-gov-citation-auditor` |
| 5 | Trace 元データ for an identified figure, table, source note, or quoted statistic | `japan-gov-chart-data-tracer` |
| 6 | Search, retrieve, filter, compare, or analyze an e-Stat table/`statsDataId` | `japan-gov-estat-data-analyst` |
| 7 | Catalog, retrieve, profile, join, or analyze Project LINKS data | `japan-gov-project-links-data-analyst` |
| 8 | Retrieve, map, compare, or analyze Real Estate Information Library data | `japan-real-estate-info-library-analyst` |
| 9 | Trace a theme to budget/program/review lifecycle states | `japan-gov-budget-tracer` |
| 10 | Find official municipality/company/initiative cases | `japan-gov-case-finder` |
| 11 | Determine formal/adjacent ministry ownership | `japan-gov-owner-mapper` |
| 12 | Score whether official priority is current or rising | `japan-gov-priority-checker` |
| 13 | Decide what should be measured or shortlist KPI candidates | `japan-gov-kpi-finder` |
| 14 | Support, qualify, or reject a supplied claim with official evidence | `japan-gov-evidence-finder` |
| 15 | Build neutral issue/social/policy background | `japan-gov-background-builder` |

3. Use these collision rules:
   - A specific chart remains chart tracing even when its source note says e-Stat; after the table ID is found, continue with e-Stat only if retrieval/analysis is requested.
   - “What indicator?” is KPI design; “get values from this table” is e-Stat analysis.
   - Words such as `統計`, `地価`, or `白書` alone never determine routing.
   - A named document plus a proposal deliverable is proposal-first; a named document plus a summary deliverable is document-first.
4. For mixed intent, decompose into dependency order and apply each needed specialist in the same task (for example, neutral background → evidence → proposal, or chart trace → e-Stat retrieval).
5. Preserve requested edition, year, geography, and output constraints across dispatch.
6. Load/apply the selected downstream instructions and continue to the substantive output. Do not answer only with a skill name or routing explanation.

## Output

Return the downstream skill's substantive deliverable. Mention the route and decomposition briefly only when it clarifies a mixed request.

## Guardrails

- Do not download, research, or invent results inside the routing step.
- Do not force whitepapers onto law text, current procedures, forms, deadlines, or breaking news.
- If no row fits, state the missing action and route to a more appropriate non-whitepaper workflow.
