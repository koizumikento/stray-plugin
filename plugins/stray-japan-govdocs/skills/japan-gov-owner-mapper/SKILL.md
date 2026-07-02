---
name: "japan-gov-owner-mapper"
description: "Use when the user asks which Japanese ministry, agency, policy area, or official document context owns or frames a theme. Do not use for budget tracing, KPI search, detailed single-whitepaper summaries, local or municipal governance topics, private-sector-only topics, or legal/procedural questions."
---

# Japan Gov Owner Mapper

Map a user theme to the relevant Japanese ministries, agencies, whitepapers, and policy contexts.

Use this skill when the user asks:

- "孤独・孤立対策はどの省庁文脈で見るべき?"
- "AI人材は文科省と経産省のどちらの話?"
- "観光DXはどの白書から見るのが自然?"

## Workflow

1. Identify the user's theme and decision context.
2. Search official whitepaper routes and ministry pages for the theme.
   - Follow official URL roles in `../../references/official-url-model.md`.
   - Use `../../references/egov-whitepaper-route-map.md` for known whitepaper routes and slugs.
   - Use `../../references/download-cache-policy.md` only for task-needed downloads; final citations stay on official URLs.
3. Map each ministry's mandate and document context.
4. Distinguish primary owner, adjacent owners, and weak/noisy mentions.
   - Treat a ministry as adjacent when its mandate covers the theme in more than one official source (for example both a whitepaper section and a statistics or program page); treat a single isolated mention as weak/noisy.
5. Note when another source type is better than a whitepaper.

## Output Expectations

| Role | Ministry/agency | Why relevant | Key official documents | Use when |
|---|---|---|---|---|

Also include `主担当候補`, `周辺省庁`, `使うべき白書`, and `避けるべき誤分類`.

## Guardrails

- Do not present overlapping mandates as conflict without source evidence.
- Do not force a ministry mapping when the topic is local, private, or legal-procedure specific.
