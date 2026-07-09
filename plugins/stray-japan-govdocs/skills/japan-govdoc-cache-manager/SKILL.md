---
name: "japan-govdoc-cache-manager"
description: "Use when the user wants Japanese official documents 一時保存・索引・cache inspected, repaired, or traced under tmp/japan-govdocs/. Do not use for ordinary reading unless local storage or provenance is central."
---

# Japan Govdoc Cache Manager

Manage temporary official-document files and source indexes with a schema that distinguishes index-only work from downloaded-file caching.

## Do Not Use For

- Ordinary summaries or evidence gathering that do not require local caching or provenance repair.
- Persistent/versioned document archives unless the user explicitly requests a bounded artifact.

## Workflow

1. Verify the official landing route using `../../references/official-url-model.md` and, for listed whitepapers, `../../references/egov-whitepaper-route-map.md`.
2. Select one mode:
   - `index-only`: record verified official routes without downloading content.
   - `download-cache`: save task-needed source/extracted files and create manifest records.
3. Use `tmp/japan-govdocs/{sources,downloads,extracted}` and confirm `tmp/` is ignored by git before any download.
4. Follow deterministic paths and the exact schema in `../../references/download-cache-policy.md`.
   - Canonical source index shape: `{"records": [...]}`; an empty `records` array is valid for an initialized index.
   - Every non-empty source-index record requires `document_id`, `title`, `ministry`, `year`, and `landing_page`.
   - Every downloaded or extracted file requires one `manifest.jsonl` record with all policy-required fields.
   - In index-only mode, `manifest.jsonl` may be absent or empty only when no files exist under `downloads/` or `extracted/`.
5. Hash and size downloaded files after writing them; never copy guessed metadata into the manifest.
6. Validate with:
   `uv run python plugins/stray-japan-govdocs/skills/japan-govdoc-cache-manager/scripts/validate_cache.py tmp/japan-govdocs`
   Use the repository's Python runner if `uv` is unavailable.
7. Repair only the invalid record/file requested. Re-run validation once; if failure remains, preserve the error and stop rather than deleting unrelated cache entries.
8. Report what was cached, only indexed, skipped, or unresolved.

## Output

- `mode`: index-only / download-cache
- `確認した公式経路`
- `保存したファイル`
- `更新した索引`
- `manifest記録`
- `validator結果`
- `保存しなかった資料と理由`

## Guardrails

- Do not bulk-download archives without an explicit bounded dataset request.
- Do not cite local paths as final sources or accept a direct file URL without its official landing route.
- Do not write outside `tmp/japan-govdocs/` unless the user explicitly asks for a persistent artifact.
