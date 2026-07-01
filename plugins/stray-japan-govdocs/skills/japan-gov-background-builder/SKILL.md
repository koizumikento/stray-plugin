---
name: "japan-gov-background-builder"
description: "Use when the user asks to整理, write, or understand the social/policy background, 課題背景, 社会背景, or government framing of a theme using Japanese government whitepapers or official documents. Trigger on 企画書の背景, 提案書の背景, 政府はどう問題視, 国の問題意識. Do not use for quote collection, KPI search, budget tracing, citation auditing, or specific whitepaper-only summaries."
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
   - Follow official URL roles in `../../references/official-url-model.md`.
   - Use `../../references/egov-whitepaper-route-map.md` for known whitepaper routes and slugs.
   - Bound the search: inspect the latest official series page plus at most two relevant ministry, statistics, program, or database source families unless the user asks for exhaustive coverage.
   - If no official source supports the claim after those checks, stop widening the search and report it under `追加確認` or `公式根拠なし` with the checked sources.
3. Default to latest editions unless the user specifies a year or period.
4. Pull official issue framing, trend data, policy direction, and relevant terms.
5. Prefer HTML and chapter pages; use `../../references/download-cache-policy.md` for task-needed downloads and keep final citations on official URLs.
6. Separate government-stated background from your interpretation.

## Output Expectations

- `政府がどう問題視しているか`
- `背景に使える統計・図表`
- `関連する白書・公式資料`
- `提案や説明に使える言い方`
- `白書だけでは不足する確認`
- `取得した資料`

## Validation Expectations

Before final output, verify each cited source has an official landing URL, year or edition, section/table/figure location when available, and a clear source role from `../../references/official-url-model.md`. If any item cannot be verified, downgrade confidence and place it under `追加確認` rather than presenting it as confirmed evidence.

## Guardrails

- Do not imply government endorsement of the user's project.
- Do not use whitepapers as current law or procedure.
- Do not bulk-download documents for exploratory background.
