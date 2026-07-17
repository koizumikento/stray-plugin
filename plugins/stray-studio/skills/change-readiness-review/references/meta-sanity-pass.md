# Meta Sanity Pass

Use this pass once only when the change materially alters structure. It is not a second general code review.

## Trigger

Apply when the change:

- moves, splits, or combines responsibility across modules, components, or services;
- changes state ownership, persistence, orchestration, execution, or deployment shape;
- changes data or control flow across component boundaries; or
- introduces or replaces a major abstraction, framework, middleware, or shared helper used by multiple flows.

Do not trigger from diff size, file count, commit count, the word `refactor`, a simple move/rename, documentation-only work, tests-only work, or the presence of a deep-review trigger.

## Check

Using evidence already collected, ask:

1. Does the resulting structure still satisfy the requested outcome, exclusions, and operating constraints?
2. Did simplification, optimization, centralization, or relocation remove a required capability?
3. Are responsibility, state, error handling, and data/control-flow ownership still complete and consistent?
4. Are compatibility, safety, and operational tradeoffs proportionate to the requested change?
5. Is current complexity itself causing a concrete in-scope defect or operational burden?

Only the last question may support simplification, and only when the present design creates a concrete failure or material operating cost. Do not turn architectural preference into a blocking finding.

Do not acquire another full snapshot, rerun successful tests, reread the whole repository, or add another reviewer for this pass. Merge any confirmed issue into the normal finding policy.
