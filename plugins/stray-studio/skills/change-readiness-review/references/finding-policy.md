# Readiness Finding Policy

Use this policy to distinguish confirmed blockers from useful but non-gating observations.

## Blocking Contract

A finding controls readiness only when all of the following are true:

1. It is within the requested change or a directly affected contract, trust boundary, caller, data path, deployment path, or required artifact.
2. The change introduces, worsens, exposes, or fails to satisfy the problem.
3. A realistic failure path can be stated.
4. The impact is concrete enough to justify correction before sharing.
5. The evidence meets the calibration rules below.

Use `High` for security exposure, secret disclosure, destructive behavior, data loss, primary-flow outage, or comparable impact. Use `Medium` for correctness, contract, explicit requirement, important product-flow, build, test, migration, or required-artifact failures that should be fixed before sharing.

## Evidence Calibration

Classify the main support for each candidate:

- `observed`: directly visible in repository, Git, GitHub, or command state.
- `reproduced`: demonstrated by a safe targeted test or minimal reproduction.
- `source_confirmed`: established by source, specification, authoritative contract, or primary documentation.
- `inferred`: derived from confirmed facts but not directly observed.

Prefer reproduced or source-confirmed evidence for blocking findings. An inferred blocker is allowed only when its premises, failure path, and impact are explicit and no safer verification is reasonably available. Put unresolved possibilities in proof gaps instead of presenting them as defects.

## Do Not Block On

- Naming, formatting, style, or preference without concrete behavioral impact.
- Optional refactors, alternate architecture, speculative hardening, or unrelated cleanup.
- Existing defects that the change neither worsens nor exposes.
- Missing dedicated tests when deterministic evidence already proves a low-risk behavior.
- An unavailable check that cannot materially change the decision.
- Feedback whose only content is acknowledgement, status, a question, a nit, or an optional suggestion.

## Incomplete Contract

`INCOMPLETE` is not a synonym for uncertainty. Use it only when:

- the reviewed target cannot be identified or sealed;
- evidence acquisition is demonstrably incomplete or inconsistent;
- a required check or artifact is unavailable; or
- the missing evidence could realistically hide a High or Medium finding or change readiness.

State the missing evidence, why it matters, and the smallest action that would make another review decisive.
