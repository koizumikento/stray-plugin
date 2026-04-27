---
name: "japan-govdoc-cache-manager"
description: "Use when the user asks to temporarily save, cache, inspect, or trace Japanese government whitepapers, government資料, official PDFs/HTML, source files, local paths, manifest records, or tmp/japan-govdocs/. Trigger on Japanese requests like 白書を一時保存, 政府資料をキャッシュ, PDF/HTMLを保存, 索引を残す, 取得元を追跡, ローカルに保存していない. Do not use for ordinary summaries unless local caching or traceability is central."
---

# Japan Govdoc Cache Manager

Manage temporary local storage and traceability for Japanese government whitepapers and official documents.

Use this skill when the user asks:

- "白書をローカルに一時保存して"
- "政府PDF/HTMLをキャッシュしてから読んで"
- "取得した公式資料の索引を残して"
- "白書を参照したのに保存していないので追跡できるようにして"
- "tmp/japan-govdocs/ のファイル名ルールを確認して"

## Workflow

1. Confirm the source type.
   - Japanese government whitepaper, annual report, official policy document, PDF, HTML, spreadsheet, or related source file.
2. Check the official route before caching.
   - Use `../../references/egov-whitepaper-route-map.md` for listed whitepapers.
   - Use `../../references/official-url-model.md` for URL roles and edition selection.
3. Prepare the temporary folder.
   - Use `tmp/japan-govdocs/sources/`, `tmp/japan-govdocs/downloads/`, and `tmp/japan-govdocs/extracted/`.
   - Confirm `tmp/` is ignored by git before downloading.
4. Apply deterministic names.
   - Use canonical `ministry_slug` and `document_slug` from the route map when available.
   - Store files under the path rules in `../../references/download-cache-policy.md`.
5. Record traceability.
   - Append `manifest.jsonl` records with official URL, local path, hash, size, title, ministry, year, and reason.
   - Add or update `tmp/japan-govdocs/sources/whitepaper-index.json` when a reusable route is learned.
6. Return a concise cache report.
   - Say what was cached, what was only indexed, what was skipped, and why.

## Output Expectations

- `確認した公式経路`
- `保存したファイル`
- `更新した索引`
- `manifest記録`
- `保存しなかった資料と理由`
- `次に読むべきローカルファイル`

## Guardrails

- Do not download whole archives unless the user explicitly asks for a bounded dataset build.
- Do not treat direct PDF URLs as sufficient without an official landing page.
- Do not cite local cache paths as final sources; cite official URLs.
- Do not move cached files into versioned docs folders unless the user explicitly asks for a persistent research artifact.
