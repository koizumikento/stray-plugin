# Betting Structure Guide

Use this only when the user asks for 買い目, 券種, ボックス, ながし, フォーメーション, WIN5, or stake structure. Keep ticket discussion secondary to probability, value, and risk.

## Ticket Types

- 単勝: Pick the winner. Best aligned with a strong win thesis and easy to compare with market probability.
- 複勝: Pick a horse to finish in the placing range. Useful for stability, but popular horses can have little value.
- 応援馬券: Single-win and place/show together. Treat as separate 単勝 and 複勝 components for analysis.
- 枠連: Pick the frame-number combination for first and second. Check same-frame implications.
- 馬連: Pick first and second in any order. Useful when two horses are strongly preferred but order is uncertain.
- 馬単: Pick first and second in exact order. Requires a stronger win thesis than 馬連.
- ワイド: Pick two horses that both finish in the placing range. Useful for stable axes and value partners; watch トリガミ.
- 3連複: Pick the first three in any order. Useful when order is uncertain but the top group is narrow.
- 3連単: Pick the first three in exact order. High variance; never make it the default.
- WIN5: Pick winners of five designated JRA races. Treat as a portfolio/combination problem, not a normal single-race ticket.

## Payout Rate Context

JRA has publicly announced different payout rates by wager type since June 7, 2014:

- 単勝 and 複勝: 80.0%
- 枠連, 馬連, and ワイド: 77.5%
- 馬単 and 3連複: 75.0%
- 3連単: 72.5%
- WIN5: 70.0%

Use these as risk context. Lower payout-rate, higher-complexity tickets require stronger evidence and better combination discipline.

## Buying Structures

- 1点買い: One exact ticket. Clear thesis, easy to review, high miss risk.
- Equal-unit multiple tickets: Simple and reviewable. Adding weak tickets does not improve expected value.
- ボックス: Buy all combinations among selected horses. Reduces missed order/combination risk but combinations grow quickly.
- ながし: Fix one or more axes and spread to partners. Good when the axis is credible; fails when the axis misses.
- マルチ: Cover alternate finishing orders for exact-order wagers. Useful only when order uncertainty is central; it increases combinations.
- フォーメーション: Put horses into first/second/third or axis/partner layers. Best for expressing a structured hypothesis and controlling combinations.
- Dutching / equal-payout allocation: Allocate stake so outcomes return similar payouts. Treat as a calculation aid; odds movement and minimum units can break the target.
- 見送り: Use this as a normal recommendation when value, data freshness, or confidence is insufficient.

## Structure Selection Rules

- Strong win thesis: consider 単勝, 馬単, or 3連単 first-position fixed, but only if odds justify it.
- Strong placing thesis but uncertain win: consider 複勝, ワイド, or 3連複 axis structures.
- Several top horses with uncertain order: prefer 馬連, ワイド, or 3連複 over exact-order tickets.
- Interesting longshot as partner: consider ワイド, 馬連, or 3連複 rather than forcing a win ticket.
- Wide third-place uncertainty: prefer 3連複 or a formation that widens only the third layer.
- No value: do not change ticket type to force action; recommend 見送り.

## Combination Discipline

Always count combinations before presenting ticket candidates.

For common cases:

- 馬連/ワイド box with `n` horses: `n * (n - 1) / 2`
- 馬単 box with `n` horses: `n * (n - 1)`
- 3連複 box with `n` horses: `n * (n - 1) * (n - 2) / 6`
- 3連単 box with `n` horses: `n * (n - 1) * (n - 2)`

For formations, count unique valid combinations. Remove duplicates, impossible repeats of the same horse, and scratched runners.

## Stake and Bankroll Guardrails

- Do not provide stake amounts unless the user explicitly asks.
- If asked, first ask or state assumptions for entertainment budget, loss limit, one-race limit, and one-day limit.
- Prefer flat, reviewable units for learning and post-race evaluation.
- Treat Kelly-style sizing only as a fragile reference calculation; probability error can make it dangerous.
- Do not recommend martingale, chasing losses, doubling after losses, or "recover today" systems.

## Risk Language

Use:

- "candidate"
- "fits this hypothesis"
- "value depends on odds staying above..."
- "見送り if odds shorten below..."
- "high variance"
- "トリガミ risk"

Avoid:

- "must buy"
- "safe"
- "sure thing"
- "profit strategy"
- "recover losses"
