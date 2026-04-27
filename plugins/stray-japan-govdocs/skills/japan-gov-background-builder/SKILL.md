---
name: "japan-gov-background-builder"
description: "Use when the user asks to整理, write, or understand the social or policy background of a theme using Japanese government whitepapers or official documents. Do not use for quote collection, KPI search, budget tracing, citation auditing, or specific whitepaper-only summaries."
---

# Japan Gov Background Builder

Build official background for a theme from Japanese government whitepapers and policy documents.

Use this skill when the user asks:

- "介護DXの企画書に使える社会背景を整理して"
- "地方交通がなぜ問題なのか政府資料ベースでまとめて"
- "防災SaaSの営業前に国の問題意識を知りたい"

## Workflow

1. Identify the theme, audience, and intended use.
2. Start from e-Gov and relevant ministry series pages.
3. Default to latest editions unless the user specifies a year or period.
4. Pull official issue framing, trend data, policy direction, and relevant terms.
5. Prefer HTML and chapter pages; use `../../references/download-cache-policy.md` for downloads.
6. Separate government-stated background from your interpretation.

## Output Expectations

- `政府がどう問題視しているか`
- `背景に使える統計・図表`
- `関連する白書・公式資料`
- `提案や説明に使える言い方`
- `白書だけでは不足する確認`
- `取得した資料`

## Guardrails

- Do not imply government endorsement of the user's project.
- Do not use whitepapers as current law or procedure.
- Do not bulk-download documents for exploratory background.
