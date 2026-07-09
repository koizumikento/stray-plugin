---
name: "japan-gov-background-builder"
description: "Use when the user wants a neutral 課題背景・社会背景 or government framing built from Japanese official sources. Do not use for proposal-ready advocacy, a specific claim's evidence, or a named-document summary."
---

# Japan Gov Background Builder

Build a neutral, source-backed account of how Japanese government documents frame a social or policy issue. Government statements, observed facts, and agent interpretation must remain separate.

## Do Not Use For

- Product-, service-, or stakeholder-specific proposal wording; use `japan-gov-proposal-context-adapter`.
- Evidence for a supplied claim; use `japan-gov-evidence-finder`.
- A named whitepaper or chapter as the primary object; use `japan-whitepaper-brief`.

## Workflow

1. Define the theme, audience, time range, and whether the user needs issue framing, trend context, or policy context.
2. Search the latest relevant official series page and no more than two additional source families unless exhaustive research is requested.
   - Follow `../../references/official-url-model.md` and `../../references/egov-whitepaper-route-map.md`.
   - Prefer HTML and official statistics; download only task-needed files under `../../references/download-cache-policy.md`.
   - Count source families and list checked families using `../../references/evaluation-rubric.md`.
3. Extract government-stated problems, affected groups, trends, and policy direction. Label the edition, data period, and responsible body.
4. Separate the result into `政府の明示的な見方`, `公式データで確認できる事実`, and `解釈`; keep normative framing separate from statistical evidence.
5. Check that no sentence implies endorsement of the user's organization or solution. If proposal synthesis is also requested, finish the neutral background first and then hand it to `japan-gov-proposal-context-adapter` in the same task.
6. Stop widening the search after the bounded source families yield no new official support; report checked routes and gaps.

## Output

- `中立な課題背景`
- `政府の問題設定と政策方向`
- `背景に使える統計・図表`
- `政府記述と解釈の区分`
- `確認した公式資料`
- `不足する根拠・追加確認`

## Guardrails

- Do not turn neutral background into sales copy or imply government endorsement.
- Do not treat a whitepaper as current law, procedure, or proof of a product need.
- Cite official landing URLs and downgrade unverifiable items rather than filling gaps by inference.
