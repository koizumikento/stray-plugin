---
name: "change-readiness-review"
description: "Use when the author asks if local Git state is ready to push or an open pull request is ready for initial or repeat human review. Owns a read-only, state-sealed readiness decision. Do not use for general code review, fixes, security preflights, GitHub mutations, or maintenance triage."
---

# Change Readiness Review

Decide whether an author's exact local or pull-request state is ready to share. Keep the gate read-only, seal the reviewed evidence at the beginning and end, and return `READY`, `CHANGES_REQUIRED`, or `INCOMPLETE` without repairing the change. Local mode requires Git repository access; pull-request mode requires an authenticated GitHub CLI with read access.

## Do Not Use For

- General findings-first code or pull-request review, third-party review, or review-fix work; use `reviewer`.
- Security-first ship review; use `security-preflight`.
- GitHub issue or pull-request triage; use `github-maintainer`.
- Stage, commit, push, PR creation, review submission, reviewer requests, comments, labels, merges, or other mutations.
- Generic "review my changes" requests that do not ask for push or review-request readiness.

## Workflow

1. Fix the decision and checkpoint before inspecting details.
   - Use `LOCAL_PUSH` only when the author asks whether current local changes are ready to push.
   - Use `PR_REVIEW_REQUEST` only when the author asks whether their open pull request is ready for an initial or repeat human review request.
   - Route ordinary critique or any requested repair to `reviewer`; do not manufacture a readiness decision.
2. Read the request, repository guidance, change description, acceptance criteria, explicit exclusions, and nearby source needed to understand intent.
3. Create a mode-700 temporary directory outside the target repository and capture the initial state once.
   - For `LOCAL_PUSH`, resolve the comparison base from an explicit user choice, the branch upstream, or the remote default branch, then follow `references/local-gate.md`.
   - For `PR_REVIEW_REQUEST`, identify `initial` or `rerequest`, then follow `references/pull-request-gate.md`.
   - Treat helper output as evidence acquisition, never as a finding or readiness decision.
4. Run the fast path against the exact captured state.
   - Map the change to stated requirements.
   - Inspect changed symbols, direct callers and callees, public entry points, related tests, required artifacts, and unintended inclusions.
   - Run only the narrowest safe checks that materially support the decision. Do not execute code from an untrusted repository outside an appropriate sandbox.
5. Expand only when triggered.
   - Load only the matching sections of `references/risk-modules.md` for actual input, product-flow, security, persistence, contract, concurrency, or deployment changes.
   - Apply `references/meta-sanity-pass.md` once only for structural changes to responsibility, state ownership, component flow, major abstractions, or execution/deployment shape.
6. Resolve candidates with `references/finding-policy.md`.
   - Require an in-scope causal relationship, realistic failure path, concrete impact, and calibrated evidence.
   - Keep style, optional redesign, unrelated existing issues, and unsupported hardening out of the gate.
7. Capture the same checkpoint a second and final time.
   - Compare all state identity and evidence fingerprints, not only branch names or timestamps.
   - If relevant state changed, refresh only when the new state can be reviewed completely; otherwise return `INCOMPLETE`.
   - For pull requests, never reuse checks from another head OID and never declare readiness from a possibly truncated diff.
8. Return the result using `references/output-contract.md`, then remove all temporary snapshots and raw diff artifacts.

## Output

- One decision: `READY`, `CHANGES_REQUIRED`, or `INCOMPLETE`.
- Confirmed blocking findings first when present, each with severity, location, impact, evidence, and required correction.
- The comparison base or pull-request head identity, material checks performed, proof gaps, and residual risk needed to understand the decision.
- Natural Markdown for the user; internal hashes, complete snapshots, raw diffs, empty sections, and machine-oriented ledgers remain private.

## Guardrails

- Keep the target repository, Git state, pull request, issues, reviews, comments, and hosted settings read-only.
- Write diagnostic artifacts only inside the declared external temporary directory, with exclusive creation and restrictive permissions; always clean them up.
- Use `--no-ext-diff --no-textconv` when displaying Git patches and avoid project code execution when repository trust is unknown.
- Do not treat missing evidence as safety. Use `INCOMPLETE` only when the gap can materially change readiness or conceal a High or Medium defect.
- Do not use an independent reviewer by default. Use at most one only when the user requests it or a concrete High-impact candidate would materially benefit; prohibit nested delegation and retry with another reviewer.
- Never convert this gate into a repair loop. Preserve findings and hand remediation to `reviewer` or the relevant implementation skill, then rerun the gate on the resulting state.
