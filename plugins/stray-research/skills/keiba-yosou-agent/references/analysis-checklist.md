# Analysis Checklist

Use this checklist before producing contender rankings, probability ranges, or value notes.

## Race Context

- JRA or NAR
- Race date, racecourse, race number, race name
- Surface: turf, dirt, jump, or other
- Distance, direction, inner/outer course when relevant
- Class, conditions, sex/age restrictions, handicap or set weights
- Field size, scratches, post positions, and frame numbers
- Weather, going, and timestamp

## Runner Table

Create or infer a compact table with:

- Horse number and frame
- Horse name
- Jockey
- Trainer or stable when available
- Carried weight
- Body weight and body-weight change
- Current odds and popularity when available
- Recent form and layoff
- Missing or stale fields

## Horse Evaluation

Check each contender across:

- Recent performance: finish, margin, time, final sectional, passing order, class level
- Race fit: surface, distance, course, direction, pace shape, field size
- Condition: layoff, rotation, body weight, training comments if available
- Draw and trip: inside/outside bias, expected position, traffic risk
- Weight: carried weight change and handicap context
- Jockey/trainer: switch, course tendency, stable form, but avoid overclaiming
- Pedigree: surface, distance, and going tendencies; keep this secondary unless strongly relevant
- Market: odds, popularity, movement, and mismatch with the evidence

## Fact vs Inference

Write facts as sourced observations:

- "The horse is drawn in gate 2."
- "The latest body weight is unavailable in the provided data."
- "The current single-win odds shown by the source are 8.4 at 14:10."

Write inference as judgment:

- "This draw likely helps if the horse can hold an inside stalking position."
- "The odds appear short relative to the uncertainty."
- "The race shape makes a wide closer less attractive unless the pace collapses."

## Probability Handling

- Convert decimal odds to rough market probability with `1 / odds` when useful.
- Remember that parimutuel odds include takeout and pool effects, so implied probabilities will not sum cleanly without normalization.
- Prefer probability ranges or tiers over exact percentages unless the user provides model outputs.
- Separate win probability, place/show probability, and "in the mix" confidence.
- Use "value candidate" only when the subjective probability range is meaningfully above the market-implied probability.

## Value Checks

Before suggesting a candidate:

- Is the data current enough?
- Does the estimated probability exceed the market enough to cover uncertainty?
- Did odds collapse after the initial analysis?
- Are scratches, jockey changes, body weight, weather, and going rechecked?
- Is the conclusion still valid if the main pace assumption is wrong?

Recommend 見送り when these checks fail.

## Confidence Labels

Use simple labels:

- High confidence: source data is current, thesis is clear, and uncertainty is limited.
- Medium confidence: core data exists but one or two important uncertainties remain.
- Low confidence: early data, missing odds/body weight, unclear pace, or heavy reliance on inference.

Never use confidence labels to imply guaranteed results.
