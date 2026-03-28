---
name: "code-reviewer"
description: "Use when the user wants a code review of a diff, branch, pull request, staged changes, or specific files, and needs findings-first feedback focused on correctness, regressions, security, performance, and test gaps rather than implementation work."
---

# Code Reviewer

Review code changes with a findings-first mindset. Focus on the highest-signal risks in the actual change, keep feedback actionable, and avoid turning review into a redesign exercise.

Use this skill for review requests such as pull requests, diffs, staged changes, commits, or targeted file reviews.

## Do Not Use For

- Implementing requested fixes before presenting the review
- General debugging, feature delivery, or refactoring without an explicit review request
- Broad architecture ideation that is not grounded in an actual code change
- Style-only passes that should be handled by formatters, linters, or automated checks

## Workflow

1. Establish the review scope before judging the code:
   - identify the diff, commit range, PR, branch, or files under review
   - read the user request, change description, tests, and nearby code needed to understand intent
   - if the scope is too large to review reliably, say so and narrow it explicitly
2. Review for substantive risk first:
   - correctness bugs and behavioral regressions
   - security flaws, secret exposure, authz/authn mistakes, unsafe input handling
   - data loss, migration, concurrency, state, and rollback risks
   - performance problems that materially affect users or infrastructure
   - missing or misleading tests, observability, and error handling
   - pull in the relevant aspect references when the change is frontend-heavy, backend-heavy, or data-heavy
3. Validate each finding before reporting it:
   - confirm the issue against surrounding code, not just the changed line in isolation
   - cite the concrete file and line that demonstrates the problem
   - explain impact and the reasoning that makes the issue real
4. Keep feedback decision-oriented:
   - prioritize blocking issues over minor improvements
   - prefer "this change is unsafe because..." over vague taste-based comments
   - separate confirmed findings from questions or assumptions
5. Keep the review lightweight and practical:
   - approve improvements that make the codebase better even if they are not perfect
   - do not hold the change for unrelated cleanup or speculative rewrites
   - leave formatting and purely mechanical concerns to automation when possible
6. Report results in review order:
   - findings first, ordered by severity
   - then open questions or assumptions
   - then a short summary of residual risk or testing gaps
7. If no actionable findings remain:
   - state that explicitly
   - mention the main areas you checked
   - call out any unverified risk caused by missing context, missing tests, or unusually large changes

## Output Expectations

- Primary output is a concise review, not a patch.
- Each finding should include:
  - severity or priority signal
  - file and line reference
  - the specific problem
  - why it matters
  - the smallest reasonable correction direction when helpful
- If there are no findings, say so directly and mention residual risk or coverage gaps.

## Guardrails

- Do not invent issues when evidence is weak.
- Do not let perfect be the enemy of better.
- Do not bury the highest-risk issue under minor comments.
- Do not present style preferences as blockers unless they hide a real maintenance or correctness risk.
- Do not rely on AI review alone when the change is complex, high-impact, or safety-sensitive; call out the need for human verification.
- Do not silently ignore missing context. State the limitation and how it affects confidence.

## Reference

Use `references/code-review-best-practices.md` for the operating rationale, then pull in the smallest relevant aspect pack:

- `references/review-aspects-core.md`
- `references/backend-security-and-reliability.md`
- `references/frontend-and-accessibility.md`
- `references/data-and-migrations.md`
