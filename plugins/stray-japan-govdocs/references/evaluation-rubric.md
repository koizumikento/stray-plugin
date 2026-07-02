# Evaluation Rubric for Japan Gov Docs Skills

Shared scales for judging signal strength, evidence strength, citation drift, and confidence, plus how to count and bound source families. Referenced by `japan-gov-priority-checker`, `japan-gov-evidence-finder`, `japan-gov-citation-auditor`, `japan-gov-budget-tracer`, and `japan-gov-background-builder`.

## Priority Signal Strength

Weight signals before concluding (used by `japan-gov-priority-checker`):

- Strong: a dedicated section or chapter in a current whitepaper; a named plan, strategy, council, or new measure; an explicit budget or program mention tied to the theme.
- Medium: recurring coverage across two or more editions; cross-ministry recurrence; KPI or indicator language attached to the theme.
- Weak: isolated word mentions, one-off examples, or appearance only in generic boilerplate sections.

Map signals to the `結論` verdict:

- `high`: two or more strong signals, or one strong signal plus two or more medium signals.
- `medium`: one strong signal, or two or more medium signals.
- `low`: only weak signals after checking the bounded source set.
- `unclear`: signals conflict across ministries or editions, or the bounded search could not verify enough sources; say which.

## Evidence Strength

Rate each claim-to-source connection (used by `japan-gov-evidence-finder`):

- `Strong`: the claim is directly stated, or directly supported by a table or figure, in an official source with edition and location identified.
- `Medium`: the source discusses the same issue and supports the claim by close paraphrase or adjacent data, but does not state it directly.
- `Weak`: the connection requires the agent's inference across sources, or the source is dated, partial, or scoped differently than the claim.

Present `Weak` evidence under `弱い根拠` or `追加確認` instead of listing it beside strong evidence without distinction.

## Citation Drift Granularity

Report `最新版との差` using these levels (used by `japan-gov-citation-auditor`):

- `None`: latest edition confirmed, no relevant change.
- `Minor`: wording, layout, or section numbering changed; the cited claim is unaffected.
- `Content`: statistics, tables, or examples changed in ways that affect the cited claim.
- `Direction`: the policy framing or emphasis changed; the citation may now misrepresent the source.

## Confidence Labels

Rate traced connections (used by `japan-gov-budget-tracer` and similar tracing outputs):

- `High`: an official program, budget, or review document names the theme or its official policy term directly.
- `Medium`: the connection relies on shared terminology or the ministry's stated objectives, not a direct mention.
- `Low`: the connection is thematic inference only; state the gap and what would confirm it.

## Bounding Searches: Counting Source Families

When a skill says to inspect "the latest official series page plus at most two relevant ministry, statistics, program, or database source families," count as follows:

- One source family = one official series or database surface: a ministry whitepaper series page, a ministry policy/program page cluster, one statistics surface (e-Stat or a ministry statistics page), or one official database (行政事業レビュー, CKAN, and similar).
- Individual pages, chapters, or PDFs inside the same series page or database do not count as extra families.
- When reporting `公式根拠なし`, list the checked families explicitly, for example: (1) 中小企業白書 最新版 series page, (2) 経産省 施策ページ, (3) 行政事業レビュー検索 — checked, no direct support found.
