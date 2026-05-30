---
name: "japan-gov-case-finder"
description: "Use when the user asks for official examples, case studies,自治体事例,企業事例,or precedent initiatives related to a Japan policy issue from whitepapers or government documents. Do not use for general evidence gathering or KPI search."
---

# Japan Gov Case Finder

Find reusable official case examples from Japanese government whitepapers and related documents.

Use this skill when the user asks:

- "中小企業白書から賃上げ事例だけ拾って"
- "自治体の防災DX事例を政府資料から探して"
- "この課題の先行事例を提案書に使える形でまとめて"

## Workflow

1. Define the case type: municipality, company, program, technology, partnership, or community activity.
2. Search relevant whitepapers, case collections, ministry reports, and linked materials.
   - Follow official URL roles in `../../references/official-url-model.md`.
   - Use `../../references/egov-whitepaper-route-map.md` for known whitepaper routes and slugs.
   - Use `../../references/download-cache-policy.md` only for task-needed downloads; final citations stay on official URLs.
3. Extract cases with source, actor, problem, intervention, result, and transferability.
4. Mark whether outcomes are evidenced or merely described.
5. Package cases for proposal, research, or article reuse.

## Output Expectations

| Case | Actor | Issue | Intervention | Reported result | Source | Reuse note |
|---|---|---|---|---|---|---|

Also include `使いやすい事例`, `注意が必要な事例`, and `不足している実証`.

## Guardrails

- Do not treat highlighted cases as representative.
- Do not infer causal effect when the source only describes an example.
- Do not copy long case text verbatim.
