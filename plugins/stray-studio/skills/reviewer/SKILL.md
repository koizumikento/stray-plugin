---
name: "reviewer"
description: "Use when the user wants a findings-first review, audit, preflight, critique, or review-fix loop for code, diffs, documentation, UI, artifacts, Codex skills, plugin manifests, prompts, evals, release readiness, or repository compliance. Do not use for creating new artifacts from scratch, general research, unconstrained implementation work, or legal advice."
---

# Reviewer

Run a focused review of the user's target artifact. Treat this as a quality gate: identify concrete risks, explain why they matter, and keep recommendations actionable. When the user asks for fixes, run a review-fix loop: delegate review to subagents when available, apply the smallest correction set, then repeat review until no actionable findings remain or a clear stop condition is reached.

Use this skill for review requests such as code review, PR review, doc review, UI review, skill review, plugin review, prompt review, validation review, release preflight, compliance preflight, or broad "look this over" requests where the user expects critique.

## Do Not Use For

- Implementing fixes without first establishing a reviewed finding or explicit repair scope
- Building, writing, or redesigning an artifact from scratch
- Creating a new software test strategy, test matrix, QA plan, regression scope, or release checklist from scratch; use `test-design-strategist`
- General debugging without an explicit review request
- Broad brainstorming or strategy work that is not grounded in a concrete artifact
- Dedicated security preflights for repositories, diffs, CI/CD, dependencies, IaC, containers, secrets, or release surfaces; use `security-preflight`
- Negotiated legal advice, jurisdiction-specific legal interpretation, or a full dependency license audit

## Workflow

1. Establish the review scope before judging anything:
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
5. If the user asked for fixes or a review-fix loop:
   - send the review target and relevant context to one or more focused review subagents when subagents are available
   - ask subagents for confirmed, evidence-backed findings only; assign distinct lenses for broad targets such as code correctness, tests, UX, docs, skill routing, or release readiness
   - merge duplicate findings, discard unsupported claims, and decide the smallest correction set before editing
   - apply fixes directly when they are within the requested scope and repository guardrails
   - run the relevant validation or targeted checks after each repair pass
   - run another review pass after fixes and continue until no confirmed actionable findings remain
   - if subagents are unavailable, run the same review lenses as separate sequential passes and state that fallback
6. Stop the review-fix loop when:
   - no confirmed actionable findings remain
   - the remaining items require user, legal, security, product, design, credential, infrastructure, or external-system decisions
   - the same finding persists after two focused repair attempts
   - the loop has already completed three repair passes and further changes would be speculative or broad
7. Report in review order:
   - findings first, ordered by severity or decision impact
   - then open questions or assumptions
   - then fixes applied, validation performed, and residual risk or recommended next actions
8. If no actionable findings remain:
   - say so directly
   - mention the main areas checked
   - call out any unverified risk caused by missing context, missing tests, or incomplete artifacts

## Output Expectations

- Primary output is a concise review unless the user asked for fixes. In fix mode, output the review basis, applied changes, validation results, final review status, and any remaining blocker.
- Each finding should include:
  - severity or priority signal when useful
  - file, line, section, screen, or artifact reference when available
  - the specific problem
  - why it matters
  - the smallest reasonable correction direction when helpful
- For release and compliance preflights, include a practical recommendation such as ready, ready with fixes, or hold pending review.
- For skill, plugin, prompt, and eval reviews, include a direct recommendation such as keep, narrow, merge, remove, clarify, or block until testable.

## Guardrails

- Keep `reviewer` anchored in review evidence. Only implement fixes that directly address confirmed findings or an explicit review-fix request.
- Do not bury high-risk findings under minor wording or style comments.
- Do not claim complete legal compliance, complete security coverage, or exhaustive test coverage.
- Do not replace specialized creation skills. Route broad implementation follow-up to the relevant builder, writer, skill authoring, or research skill.
- Do not absorb dedicated security preflight work when `security-preflight` owns the requested review.
- Do not load every reference by default. Use only the references that match the review target.

## Reference

Start with the routing table in the workflow, then load the smallest applicable reference files.
