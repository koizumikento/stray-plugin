---
name: "japan-gov-owner-mapper"
description: "Use when the user asks which Japanese 省庁・所管 or policy context formally owns or materially shares a theme. Do not use for budget tracing, priority scoring, or a single-document summary."
---

# Japan Gov Owner Mapper

Map formal responsibility and adjacent policy involvement without mistaking a whitepaper mention for statutory ownership.

## Do Not Use For

- Whether a topic is currently emphasized; use `japan-gov-priority-checker`.
- Which program receives funding; use `japan-gov-budget-tracer`.
- General thematic mentions without an ownership question.

## Workflow

1. Define the theme, government level, decision context, and whether “owner” means statutory mandate, policy coordination, program delivery, or document framing.
2. Gather evidence in descending authority:
   1. laws, cabinet/ministerial orders, official organization and jurisdiction pages;
   2. Cabinet decisions, basic plans, headquarters/council documents, and named responsible-body assignments;
   3. current program, budget, implementation, or administrative-review records;
   4. whitepaper or report mentions.
3. Use `../../references/official-url-model.md` and `../../references/egov-whitepaper-route-map.md` for official document routes; cite the exact mandate or assignment location.
4. Label each body `primary/formal`, `co-owner/coordinator`, `implementation owner`, `adjacent`, or `mention only`.
5. Assign confidence:
   - `high`: current tier 1 evidence plus corroborating tier 2 or 3 evidence;
   - `medium`: explicit tier 2 assignment or consistent tier 3 responsibility without verified formal mandate;
   - `low`: whitepaper mention, indirect relevance, or stale/ambiguous responsibility only.
6. Check recency and central/local boundaries. Stop rather than force a single owner when responsibility is genuinely shared or not assigned.

## Output

| Role | Ministry/agency | Responsibility type | Evidence tier | Official basis | Current? | Confidence |
|---|---|---|---|---|---|---|

Also include `主担当候補`, `共同・周辺主体`, `白書上の言及との違い`, `所管が曖昧な点`, and `誤分類リスク`.

## Guardrails

- Do not call a ministry the formal owner based only on a whitepaper or keyword hit.
- Do not present overlapping mandates as a conflict without evidence.
- Distinguish national jurisdiction, local implementation, independent agencies, and private roles.
