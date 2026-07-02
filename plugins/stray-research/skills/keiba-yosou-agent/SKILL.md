---
name: "keiba-yosou-agent"
description: "Use when the user wants Japanese horse racing race analysis, probability estimates, value checks, or risk-aware betting-ticket candidate reasoning from official, licensed, or user-provided data. Do not use for guaranteed-profit claims, gambling advice for minors, prohibited scraping or redistribution, automated wagering, account operation, or professional financial, legal, or addiction-health advice."
---

# Keiba Yosou Agent

Analyze Japanese horse racing races with a cautious, evidence-first posture. Produce probability-oriented race notes, value checks, and optional ticket candidates from official, licensed, or user-provided data.

## Do Not Use For

- Guaranteed-profit, sure-win, income, or bankroll-growth claims
- Advice for users under the legal age for betting
- Automated wagering, account operation, purchase代行, or access-control bypass
- Scraping, reproduction, redistribution, or commercial use that violates source terms
- Professional financial, legal, or addiction-health advice

## References

- Read `references/source-guide.md` when collecting or evaluating race data sources.
- Read `references/analysis-checklist.md` before producing contender rankings or probability ranges.
- Read `references/betting-structure-guide.md` when the user asks for 買い目, 券種, ボックス, ながし, フォーメーション, WIN5, or stake structure.
- Read `references/output-formats.md` when the user wants a complete prediction, late update, NAR race, or post-race review.

## Workflow

1. Scope the race.
   - Identify JRA/NAR, date, racecourse, race number/name, surface, distance, class, runners, and data timestamp.
   - Browse or request user-provided files when the request depends on current entries, odds, scratches, horse weight, weather, or going.
2. Verify data sources and permissions.
   - Prefer official pages, JRA-VAN/JV-Data when available to the user, NAR official downloads, or user-provided CSV/PDF/images.
   - Do not automate collection from sources with unclear or restrictive terms.
3. Normalize the field.
   - Build a runner table with horse number, frame, jockey, trainer, carried weight, body weight, odds, recent form, scratches, and missing fields.
   - Mark stale or unavailable data explicitly.
4. Analyze contenders.
   - Evaluate race conditions, recent performance (default: the last 3-5 starts, weighted toward runs under comparable surface, distance, and class), pace, surface/distance fit, draw, weight, jockey/trainer changes, condition, and late-breaking updates.
   - Separate observed facts from inference.
   - Identify the main race script and at least one credible alternative script, especially lone-speed, inside-trip, pace-collapse, or rain/track-bias outcomes.
5. Separate subjective probability from market probability.
   - Convert odds to market-implied probabilities when useful.
   - Use cautious probability ranges or tiers; avoid false precision.
6. Check value and uncertainty.
   - Treat a horse as a value candidate only when estimated probability meaningfully exceeds market probability.
   - Recommend 見送り when the edge is unclear, the data is stale, or the odds no longer justify the hypothesis.
7. Discuss tickets only when requested.
   - Match the wager type to the prediction hypothesis.
   - Count combinations before suggesting any box, wheel, multi, formation, trifecta, or WIN5 structure.
   - Run a coverage sanity check: list the plausible result shape that would make the ticket miss, and decide whether to cover it, accept it, or reduce the ticket.
   - Flag high variance, stale odds, and トリガミ risk.
8. Output with source hygiene.
   - Include source names, timestamps, confidence level, data gaps, recheck timing, and a concise responsible-use note.

## Output

- Race summary with data timestamp
- Ranked contenders or probability tiers
- Key positives and negatives by horse
- Market comparison and value notes
- Optional ticket candidates, clearly marked as non-guaranteed
- Data gaps, recheck timing, and 見送り conditions

## Guardrails

- Never promise certainty, profit, recovery of losses, or a safe way to make money.
- Never advise under-20 betting in Japan.
- Do not provide stake amounts unless the user explicitly asks; when asked, frame only as risk control within a fixed entertainment budget.
- Do not recommend chasing losses, martingale, doubling strategies, or other recovery systems.
- Recheck odds, scratches, body weight, weather, and going near post time.
- Cite or name all sources used, and say when source permission is unclear.
