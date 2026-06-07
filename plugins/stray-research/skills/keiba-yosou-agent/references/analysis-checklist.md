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

## Pace and Scenario Audit

Before final rankings or tickets, write a short scenario audit:

- Expected leader and pressure: identify likely lone-speed horses, pace pressers, and whether the leader may get an uncontested trip.
- Position map: group runners by front, stalk, midfield, and closer. Do not treat every strong horse as if it can get the same trip.
- Track path: note whether inside, outside, front, or closing paths appear advantaged from the day's races or reported going.
- Alternate script: name at least one credible scenario that contradicts the main thesis, such as slow pace/front hold, fast pace/closer collapse, rain-softened stamina test, or boxed-in favorite.
- Surprise candidate: identify any horse outside the top market group that benefits strongly from the alternate script.

If the final ticket cannot win under any plausible alternate script, state that explicitly instead of hiding the concentration risk.

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
- Is a lightly regarded horse being dismissed only because of recent finishing position, despite having a favorable draw, pace role, jockey change, or course fit?
- Are heavily bet G2/G3 winners being upgraded too much without proof they can reproduce the performance at G1 pace?

Recommend 見送り when these checks fail.

## Miss-Prevention Questions

Ask these before finalizing a 1000-3000 yen style small-budget ticket:

- If the anchor runs into the money but the ticket still loses, which missing partner caused the failure?
- Is the ticket overconcentrated on one favorite pair or one race script?
- Is there one cheap coverage line that protects the most credible alternate script?
- Would adding that line create too much dilution, or is it worth replacing a low-value favorite combination?
- Are all selected partners there for distinct reasons, or are multiple tickets expressing the same fragile opinion?

## Confidence Labels

Use simple labels:

- High confidence: source data is current, thesis is clear, and uncertainty is limited.
- Medium confidence: core data exists but one or two important uncertainties remain.
- Low confidence: early data, missing odds/body weight, unclear pace, or heavy reliance on inference.

Never use confidence labels to imply guaranteed results.
