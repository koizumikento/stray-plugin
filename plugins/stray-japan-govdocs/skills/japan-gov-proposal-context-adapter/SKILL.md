---
name: "japan-gov-proposal-context-adapter"
description: "Use when the user wants to turn a business idea, product, service, or initiative into proposal-ready Japanese government context for public-sector sales,企画書,or stakeholder materials. This is proposal-first even when a specific whitepaper is mentioned as a source. Do not use for direct document summaries, neutral background only, citation auditing, or legal/procurement procedure advice."
---

# Japan Gov Proposal Context Adapter

Translate a user idea into government-aligned proposal context using whitepapers and official documents.

This is proposal-first: the user's offer and argument shape the output. If the main task is to read or summarize a named whitepaper/chapter as the object itself, use `japan-whitepaper-brief` instead.

Use this skill when the user asks:

- "この事業アイデアを官公庁向け提案の文脈に直して"
- "自治体向け防災SaaSの提案背景を白書ベースで作って"
- "介護DXサービスを国の政策課題に接続して"

## Workflow

1. Extract the user's offer, target customer, and desired proposal angle.
2. Find official background, evidence, and policy language.
   - Start from official landing pages and URL roles in `../../references/official-url-model.md`.
   - Use `../../references/egov-whitepaper-route-map.md` for known whitepaper routes and slugs.
   - Download only task-needed files under `tmp/japan-govdocs/` following `../../references/download-cache-policy.md`; final citations stay on official URLs.
3. Identify where the idea aligns with government-stated issues and where it does not.
4. Produce wording that can fit a proposal without overstating government endorsement.
5. Include source-backed cautions and missing evidence.

## Output Expectations

- `提案で使う政策文脈`
- `政府資料ベースの課題設定`
- `刺さりやすい用語`
- `根拠として使う資料`
- `言い過ぎになる表現`
- `次に確認すべき制度・予算・調達情報`

## Guardrails

- Do not claim eligibility for funding or procurement.
- Do not write as if the government has endorsed the user's product.
- Do not replace procurement, grant, or legal review.
