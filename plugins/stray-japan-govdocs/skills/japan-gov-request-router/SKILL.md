---
name: "japan-gov-request-router"
description: "Use only when a 政府資料・白書 request needs workflow selection. Resolve missing topic/action before selecting downstream skills; once scoped, apply them in the same task. Excludes clear specialist requests."
---

# Japan Gov Request Router

Resolve mixed or ambiguous requests by the requested deliverable, not isolated keywords. This router must dispatch and continue; it is not a research or download endpoint.

## Do Not Use For

- A request whose action already clearly matches one specialist skill; apply that skill directly.
- Legal advice, application procedures, breaking news only, or non-Japan government research.

## Workflow

1. Identify the primary object and action: a document to read, a claim to support, a citation to audit, a measurement to design, data to retrieve, or a proposal to synthesize.
   - If no topic, source, or substantive question is supplied, ask for that missing scope before choosing downstream skills. Do not turn a list of possible outputs into a commitment to run every specialist.
2. Apply the first matching action test in this ordered table. Examples and nouns do not override the action test.

| Order | Requested action / distinguishing test | Downstream skill |
|---:|---|---|
| 1 | Save, inspect, repair, index, or trace local cached files | `japan-govdoc-cache-manager` |
| 2 | Turn an offer into proposal/営業/企画 wording; a named document is only an input | `japan-gov-proposal-context-adapter` |
| 3 | Read or brief a named whitepaper, chapter, report, or government PDF as the primary object | `japan-whitepaper-brief` |
| 4 | Audit supplied citations, URLs, editions, or freshness | `japan-gov-citation-auditor` |
| 5 | Trace 元データ for an identified figure, table, source note, or quoted statistic | `japan-gov-chart-data-tracer` |
| 6 | Search, retrieve, filter, compare, or analyze an e-Stat table/`statsDataId` | `japan-gov-estat-data-analyst` |
| 7 | Search, filter, summarize, compare, or analyze the Digital Agency 行政手続等の棚卸調査 | `japan-gov-administrative-procedures-data-analyst` |
| 8 | Catalog, retrieve, profile, join, or analyze Project LINKS data | `japan-gov-project-links-data-analyst` |
| 9 | Retrieve, map, compare, or analyze Real Estate Information Library data | `japan-real-estate-info-library-analyst` |
| 10 | Trace a theme to budget/program/review lifecycle states | `japan-gov-budget-tracer` |
| 11 | Find official municipality/company/initiative cases | `japan-gov-case-finder` |
| 12 | Determine formal/adjacent ministry ownership | `japan-gov-owner-mapper` |
| 13 | Score whether official priority is current or rising | `japan-gov-priority-checker` |
| 14 | Decide what should be measured or shortlist KPI candidates | `japan-gov-kpi-finder` |
| 15 | Support, qualify, or reject a supplied claim with official evidence | `japan-gov-evidence-finder` |
| 16 | Build neutral issue/social/policy background | `japan-gov-background-builder` |

3. Use these collision rules:
   - A specific chart remains chart tracing even when its source note says e-Stat; after the table ID is found, continue with e-Stat only if retrieval/analysis is requested.
   - A specific chart remains chart tracing when its source is the administrative-procedures survey; continue with the survey analyst only after the source is established and analysis is requested.
   - “What indicator?” is KPI design; “get values from this table” is e-Stat analysis.
   - A named Digital Agency 行政手続等の棚卸調査, its fields, or its dataset ID routes to the administrative-procedures analyst. Generic official statistics without that survey identity remain e-Stat work.
   - Current forms, deadlines, fees, required documents, legal interpretation, and municipality-specific service availability do not route to the survey analyst.
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
