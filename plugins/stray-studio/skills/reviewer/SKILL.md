---
name: "reviewer"
description: "Use when the user wants a findings-first review, audit, preflight, or critique of code, diffs, documentation, UI, artifacts, Codex skills, plugin manifests, prompts, evals, release readiness, or repository compliance. Do not use for implementing fixes, creating new artifacts from scratch, general research, or legal advice."
---

# Reviewer

Run a focused review of the user's target artifact. Treat this as a quality gate: identify concrete risks, explain why they matter, and keep recommendations actionable without taking over implementation unless the user explicitly asks for fixes.

Use this skill for review requests such as code review, PR review, doc review, UI review, skill review, plugin review, prompt review, validation review, release preflight, compliance preflight, or broad "look this over" requests where the user expects critique.

## Do Not Use For

- Implementing requested fixes before presenting the review
- Building, writing, or redesigning an artifact from scratch
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
5. Report in review order:
   - findings first, ordered by severity or decision impact
   - then open questions or assumptions
   - then a short summary of residual risk, coverage gaps, or recommended next actions
6. If no actionable findings remain:
   - say so directly
   - mention the main areas checked
   - call out any unverified risk caused by missing context, missing tests, or incomplete artifacts

## Output Expectations

- Primary output is a concise review, not a patch.
- Each finding should include:
  - severity or priority signal when useful
  - file, line, section, screen, or artifact reference when available
  - the specific problem
  - why it matters
  - the smallest reasonable correction direction when helpful
- For release and compliance preflights, include a practical recommendation such as ready, ready with fixes, or hold pending review.
- For skill, plugin, prompt, and eval reviews, include a direct recommendation such as keep, narrow, merge, remove, clarify, or block until testable.

## Guardrails

- Keep `reviewer` as a review skill; do not drift into implementation, rewriting, or artifact production unless the user explicitly asks.
- Do not bury high-risk findings under minor wording or style comments.
- Do not claim complete legal compliance, complete security coverage, or exhaustive test coverage.
- Do not replace specialized creation skills. Route implementation follow-up to the relevant builder, writer, skill authoring, or research skill.
- Do not absorb dedicated security preflight work when `security-preflight` owns the requested review.
- Do not load every reference by default. Use only the references that match the review target.

## Reference

Start with the routing table in the workflow, then load the smallest applicable reference files.
