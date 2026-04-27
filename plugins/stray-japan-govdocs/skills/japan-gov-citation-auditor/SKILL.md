---
name: "japan-gov-citation-auditor"
description: "Use when the user asks whether existing citations to Japanese government whitepapers or official documents are current, official, correctly described, or still suitable. Trigger on 引用が古くないか, 最新版か確認, URLが公式か, 出典監査, 白書引用チェック. Do not use for finding new evidence from scratch unless the audit finds a gap."
---

# Japan Gov Citation Auditor

Audit existing citations to Japanese government whitepapers and official documents.

Use this skill when the user asks:

- "この資料の白書引用が古くないか確認して"
- "このURLは公式出典として使っていい?"
- "引用している統計時点と白書年度が合っているか見て"

## Workflow

1. Extract cited title, URL, year, edition, section, and claim.
2. Verify official source status from the landing page, not only a direct PDF.
3. Check latest edition and whether the cited edition is intentionally historical.
4. Compare publication year, target period, statistic reference period, and user's claim.
5. Recommend keep, update, replace, or caveat.

## Output Expectations

| Citation | Status | Issue | Recommended action | Replacement source |
|---|---|---|---|---|

Also include `最新版との差`, `公式性の確認`, and `引用時の注意`.

## Guardrails

- Do not update historical citations when the user intentionally cites an older edition.
- Do not treat a direct PDF URL as sufficient without a landing page.
- Do not rewrite claims beyond what the source supports.
