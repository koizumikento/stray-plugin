---
name: "japan-whitepaper-brief"
description: "Use only when the user names a specific Japanese government whitepaper, annual report, chapter, or official policy document and wants that source briefed directly. Prefer request-driven skills for background, evidence, priority, owner mapping, proposal context, citation audit, KPI, budget, cases, or chart data."
---

# Japan Whitepaper Brief

Brief a specific Japanese government whitepaper, annual report, chapter, or official policy document.

Use this skill when the user asks:

- "令和7年版高齢社会白書を5分で読めるようにして"
- "防災白書の避難所関連の章だけ要約して"
- "ものづくり白書のAI関連部分を読んで"
- "この政府PDFを提案書向けに整理して"

## Workflow

1. Identify the exact document.
   - Confirm title, ministry, year, chapter, and official landing page where possible.
   - If the user does not specify a year or edition, use the latest official edition.
   - If the user specifies a Western year, era year, or edition label, resolve that edition from the official series page.
   - Check the task-local source index under `tmp/japan-govdocs/sources/` if it exists, but verify the official landing page before trusting cached paths.
   - Use the URL role hierarchy in `../../references/official-url-model.md`.
2. Verify source status.
   - Prefer official `.go.jp` or recognized government-managed source pages.
   - Record publication date or edition when available.
3. Read the minimal needed body.
   - Use HTML first.
   - Use chapter PDFs before full PDFs.
   - Follow `../../references/download-cache-policy.md` for downloads.
   - Store downloaded files under the deterministic local path rules in the cache policy.
4. Brief for the user's use case.
   - Summarize key claims, background, statistics, measures, and implications.
   - Preserve uncertainty when the document is descriptive rather than prescriptive.
5. Provide citation-ready pointers.
   - Use official URLs and section names rather than local files.

## Output Expectations

Return Japanese output with:

- `対象資料`: title, ministry, year, official URL
- `何を言っているか`: 5-8 bullets
- `重要な政策背景`
- `重要な統計・図表`
- `提案・記事・調査で使える示唆`
- `引用候補`: short paraphrase guidance and source location
- `注意点`: what the whitepaper does not prove
- `取得した資料`: downloaded files only, with official URLs and reason

## Guardrails

- Do not summarize an unofficial copy when official sources are available.
- Do not overquote government text.
- Do not treat the document as current law or procedural guidance.
- Do not download the full PDF if a chapter-level source answers the request.
