# Code Review

Use this reference when the target is a diff, branch, pull request, staged changes, commit, or specific source files.

## Review Focus

1. Establish the code review scope:
   - identify the diff, commit range, PR, branch, staged changes, or files under review
   - read the change description, tests, and nearby code needed to understand intent
   - narrow explicitly if the scope is too large for reliable review
   - record the exact base/head or file identity when the target is mutable, but route an explicit push or PR review-request readiness decision to `change-readiness-review`
2. Review substantive risk before style:
   - correctness bugs and behavioral regressions
   - security flaws, secret exposure, authn/authz mistakes, and unsafe input handling
   - data loss, migration, concurrency, state, and rollback risks
   - performance issues that materially affect users or infrastructure
   - missing or misleading tests, observability, and error handling
3. Pull in aspect packs only when relevant:
   - `review-aspects-core.md` for almost every code review
   - `backend-security-and-reliability.md` for APIs, services, jobs, and infra-adjacent changes
   - `frontend-and-accessibility.md` for UI and client-side changes
   - `data-and-migrations.md` for schema, migration, and persistent-data changes
4. Validate each finding:
   - confirm the issue against surrounding code, not only the changed line
   - cite the concrete file and line that demonstrates the problem
   - explain impact and the reasoning that makes the issue real
   - classify the main support as observed, reproduced, source-confirmed, or inferred; require explicit premises and failure path for an inferred blocker

## Tool Safety

- Use `--no-ext-diff --no-textconv` when displaying patches with `git diff`, `git show`, or `git log -p`.
- Do not checkout, reset, stage, commit, fetch, or otherwise mutate Git state for a review-only request.
- Project tests, builds, generators, hooks, filters, and package scripts can execute repository code. Run only the narrow checks appropriate to the repository trust boundary and report skipped checks as proof gaps when material.

## Output

- Findings first, ordered by severity.
- Then open questions or assumptions.
- Then fixes applied when the user asked for repair, followed by validation results, residual risk, or testing gaps.
- If no actionable findings remain, say so directly and name the areas checked.

## Review-Fix Loop

- Do not delegate by default. When the user asks for fixes, use at most one focused independent reviewer only when the user requested it or a concrete high-impact candidate would materially benefit.
- Ask each reviewer for confirmed findings with file and line evidence, not speculative cleanup.
- Prohibit nested delegation and retry with another reviewer; continue locally if the optional independent pass is unavailable.
- Merge duplicate findings, apply the smallest correction set, and run targeted tests or checks.
- Repeat review after each repair pass until no confirmed actionable findings remain or the main skill stop condition applies.

## Guardrails

- Do not present style preferences as blockers unless they hide correctness, safety, or maintenance risk.
- Do not ask for unrelated cleanup or speculative rewrites.
- Do not rely on AI review alone for complex or high-impact changes; call out needed human verification.
- Do not return a push or PR review-request readiness verdict from this general review profile.
- Use `code-review-best-practices.md` for operating rationale when needed.
