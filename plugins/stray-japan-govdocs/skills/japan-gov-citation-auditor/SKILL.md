---
name: "japan-gov-citation-auditor"
description: "Use when the user supplies existing Japanese government 引用・URL and wants officiality, freshness, 最新版, edition, or claim-fit audited. Do not use to find evidence from scratch unless the audit exposes a specific gap."
---

# Japan Gov Citation Auditor

Audit existing citations against their exact claims and record when the audit was performed.

## Do Not Use For

- New evidence discovery without supplied citations; use `japan-gov-evidence-finder`.
- A general request for the latest policy position without a citation set.
- Rewriting claims beyond the verified source scope.

## Workflow

1. For each citation, capture the claim unit it supports, title, URL, issuing body, edition/year, section/table/figure, and intended historical or current use.
2. Verify the official landing page and source role under `../../references/official-url-model.md`; do not accept a direct PDF alone when a landing route should exist.
3. Compare publication/edition year, source data period, update date, and the claim's time scope. Preserve intentionally historical citations.
4. Assign `keep`, `update`, `replace`, `caveat`, or `unverified`.
5. For an update or replacement, state whether the new source preserves, narrows, or broadens the original claim scope. Never silently substitute a newer edition whose definitions or coverage differ.
6. Attempt at most one official landing-page repair and one latest-edition replacement per citation. If neither is verified, mark `要差し替え`, record checked routes, and stop.
7. Add `checked_at` in ISO 8601 form and validate official URL, edition, source location, and claim fit before reporting.

## Output

| Citation | Supported claim unit | Status | Edition/data period | Scope effect | Recommended action | Replacement | checked_at |
|---|---|---|---|---|---|---|---|

Also include `最新版との差`, `公式性の確認`, `定義・範囲の差`, and `未検証事項`.

Report `最新版との差` with the `None`, `Minor`, `Content`, or `Direction` drift level defined in `../../references/evaluation-rubric.md`.

## Guardrails

- Do not update an intentionally historical citation merely because a newer edition exists.
- Do not treat URL officiality as proof that the cited claim is supported.
- Downgrade confidence when a landing page, edition, or exact source location cannot be verified.
