---
name: "japan-whitepaper-brief"
description: "Use only when a specific Japanese 白書・年次報告・章 is the primary object to read or 要約. Do not use when proposal wording or cross-source policy synthesis is the main deliverable."
---

# Japan Whitepaper Brief

Produce a document-first brief that stays within the named source. Cross-source or proposal interpretation is secondary and only included when explicitly requested.

## Do Not Use For

- A named document used merely as input to a proposal; use `japan-gov-proposal-context-adapter`.
- Broad background, evidence, priority, ownership, KPI, budget, or chart-data tasks spanning sources.
- Law/procedure updates that require current primary legal or administrative sources.

## Workflow

1. Resolve exact title, issuing body, edition/year, chapter/section, and official landing page. Default to the latest edition only when no edition is specified.
2. Verify source roles under `../../references/official-url-model.md` and routes under `../../references/egov-whitepaper-route-map.md`. Recheck any task-local index before use.
3. Read the minimum official body needed: HTML first, then chapter/summary PDF, then full PDF only if necessary. Follow `../../references/download-cache-policy.md`.
4. Summarize the document's purpose, structure, key claims, evidence, measures, uncertainty, and what it does not establish. Distinguish descriptive findings from policy commitments.
5. Keep the core brief document-internal. Add `利用目的に応じた示唆` only when the user states a use case, label it as interpretation, and do not introduce unsupported cross-source claims.
6. Provide citation-ready official URLs and exact section/table/figure locations. If the edition or location cannot be verified, downgrade it to `追加確認`.

## Output

- `対象資料`: title, issuing body, edition/year, official URL
- `文書の目的と対象範囲`
- `何を述べているか`: 5–8 source-faithful bullets
- `重要な統計・図表`
- `政策措置と記述の強さ`
- `文書が証明しないこと`
- `引用候補と正確な位置`
- `利用目的に応じた示唆`（依頼時のみ、解釈と明記）
- `取得した資料`

## Guardrails

- Do not summarize an unofficial copy when official sources are available.
- Do not overquote, turn descriptive text into current law, or imply endorsement.
- Do not add generic proposal/business implications when the user only requested a brief.
