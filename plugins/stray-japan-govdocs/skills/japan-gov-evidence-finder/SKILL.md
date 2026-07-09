---
name: "japan-gov-evidence-finder"
description: "Use when the user provides a claim and wants official Japanese government 根拠・出典 to support, qualify, or reject it. Do not use for neutral background, KPI discovery, citation freshness audits, or broad document summaries."
---

# Japan Gov Evidence Finder

Test discrete claim units against Japanese official sources and state the exact scope each source can support.

## Do Not Use For

- Neutral issue framing without a supplied claim; use `japan-gov-background-builder`.
- Existing citation audits; use `japan-gov-citation-auditor`.
- Indicator candidates; use `japan-gov-kpi-finder`.

## Workflow

1. Split compound prose into atomic claim units: actor, action/state, population/geography, magnitude, time, and causal or comparative wording. Never audit an entire paragraph as one claim.
2. Choose the source type for each unit:
   - whitepapers/policy plans for official framing;
   - e-Stat or ministry statistics for numeric facts;
   - primary laws, notices, or guidance for obligations;
   - evaluation documents for outcome or causal claims.
3. Search the latest applicable official route plus at most two relevant ministry/statistics/evaluation source families unless exhaustive coverage is requested.
   - Follow `../../references/official-url-model.md` and `../../references/egov-whitepaper-route-map.md`.
   - Use `japan-gov-estat-data-analyst` in the same task when table discovery or numeric retrieval is necessary.
   - Count source families and list checked families using `../../references/evaluation-rubric.md`.
4. Map evidence to one or more claim units without carrying support across unsupported population, period, geography, definition, or causality.
5. Grade the verdict as `direct`, `qualified`, `context only`, `contradicted`, or `not found`; separately rate evidence strength as `Strong`, `Medium`, or `Weak` using `../../references/evaluation-rubric.md`, then propose the narrowest source-faithful wording.
6. Validate official landing URL, edition/data period, source location, and source role. Stop after the bounded search and list checked routes when no official support is found.

## Output

| Claim unit | Verdict | Strength | Evidence summary | Official source | Period/scope | Location | Safe wording | Caveat |
|---|---|---|---|---|---|---|---|---|

Also include `分割した主張`, `根拠が弱い箇所`, `反証・不一致`, `追加確認`, and `取得した資料`.

## Guardrails

- Do not invent quotes or expand a source beyond its population, period, definition, or stated certainty.
- Do not treat general policy concern as proof of a specific product need or causal claim.
- For legal or procedural claims, provide source location and scope without substituting for professional advice.
