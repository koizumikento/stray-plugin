---
name: "reviewer"
description: "Use when the user wants a findings-first review of code, docs, UI, skills, plugins, prompts, evals, or releases, including an explicitly requested bounded review-fix loop. Do not use for unrequested implementation, blank-slate creation, security-only preflights, research, or legal advice."
---

# Reviewer

Run a focused review of the user's target artifact. Default to review-only. Enter review-fix mode only when the user explicitly asks to fix, address, or remediate findings as part of the same task; in that mode, preserve findings-first traceability and use a bounded repair loop.

Use this skill for review requests such as code review, PR review, doc review, UI review, skill review, plugin review, prompt review, validation review, release preflight, compliance preflight, or broad "look this over" requests where the user expects critique.

## Do Not Use For

- Standalone implementation without a findings-first review contract
- Building, writing, or redesigning an artifact from scratch
- Creating a new software test strategy, test matrix, QA plan, regression scope, or release checklist from scratch; use `test-design-strategist`
- General debugging without an explicit review request
- Broad brainstorming or strategy work that is not grounded in a concrete artifact
- Dedicated security preflights for repositories, diffs, CI/CD, dependencies, IaC, containers, secrets, or release surfaces; use `security-preflight`
- Negotiated legal advice, jurisdiction-specific legal interpretation, or a full dependency license audit

## Workflow

1. Establish the mode and review scope before judging anything:
   - select review-only unless the user explicitly requested fixes in the same task
   - do not treat a request for recommendations, a correction direction, or "what should change" as permission to edit
   - identify the artifact, diff, branch, file set, document, UI, prompt, skill, plugin, release surface, or repo under review
   - read the user's stated goal, target audience, constraints, and any nearby context needed to understand intent
   - if the scope is too large to review reliably, narrow it explicitly and state what is excluded
2. Select the smallest relevant reference set:
   - code changes: `references/code-review.md`, then relevant aspect packs
   - Codex skills: `references/skill-review.md`
   - multiple skills as a routing system: `references/skill-set-review.md`
   - plugin manifests or marketplace packaging: `references/plugin-review.md`
   - prompts, system instructions, or agent instructions: `references/prompt-review.md`
   - validation plans, eval cases, or acceptance criteria: `references/validation-review.md`
   - docs, README, AGENTS.md, runbooks, or handoff text: `references/docs-review.md`
   - UI screens, frontend experience, or visual interaction: `references/ui-review.md`
   - produced artifacts such as decks, reports, screenshots, canvases, or demos: `references/artifact-review.md`
   - release readiness: `references/release-review.md`
   - repository publication, licensing, attribution, or distribution preflight: `references/compliance-preflight.md`
   - security-first preflight: route to `security-preflight` instead of continuing here
3. Review for substantive risk first:
   - correctness, regression, security, safety, compliance, routing, usability, maintainability, or release risk depending on the artifact
   - missing tests, missing evidence, unclear acceptance criteria, misleading docs, weak boundaries, or stale discovery metadata
   - style-only issues only when they create real misunderstanding, maintenance risk, or user harm
4. Validate each finding before reporting it:
   - cite concrete evidence from the artifact under review
   - separate confirmed findings from assumptions, questions, or optional improvements
   - avoid inventing issues when evidence is weak or context is missing
5. In explicitly requested review-fix mode:
   - record the initial findings before editing and keep each change traceable to a confirmed finding
   - apply only the smallest in-scope fixes; preserve unrelated user changes and do not broaden into blank-slate redesign
   - rerun the checks that exposed each finding, then re-review the affected surface for regressions and stale findings
   - perform at most two focused repair passes; stop earlier when no actionable finding remains
   - stop and ask for direction when a fix needs a material product decision, external mutation, destructive action, or scope expansion
6. Report in review order:
   - findings first, ordered by severity or decision impact
   - then open questions or assumptions
   - in review-fix mode, then mapped fixes, validation, repair-pass count, and residual findings
   - otherwise, then a short summary of residual risk, coverage gaps, or recommended next actions
7. If no actionable findings remain:
   - say so directly
   - mention the main areas checked
   - call out any unverified risk caused by missing context, missing tests, or incomplete artifacts

## Output Expectations

- Primary output is a concise review; in explicit review-fix mode, also report the initial findings, mapped fixes, validation, repair-pass count, and residual findings.
- Each finding should include:
  - severity or priority signal when useful
  - file, line, section, screen, or artifact reference when available
  - the specific problem
  - why it matters
  - the smallest reasonable correction direction when helpful
- For release and compliance preflights, include a practical recommendation such as ready, ready with fixes, or hold pending review.
- For skill, plugin, prompt, and eval reviews, include a direct recommendation such as keep, narrow, merge, remove, clarify, or block until testable.

## Guardrails

- Keep `reviewer` review-only by default; never edit unless the user explicitly requested a review-fix loop.
- In review-fix mode, do not exceed two repair passes or fix items that were not grounded in the review without surfacing the scope change.
- Do not bury high-risk findings under minor wording or style comments.
- Do not claim complete legal compliance, complete security coverage, or exhaustive test coverage.
- Do not replace specialized creation skills. Route broad implementation follow-up to the relevant builder, writer, skill authoring, or research skill.
- Do not absorb dedicated security preflight work when `security-preflight` owns the requested review.
- Do not load every reference by default. Use only the references that match the review target.

## Reference

Start with the routing table in the workflow, then load the smallest applicable reference files.
