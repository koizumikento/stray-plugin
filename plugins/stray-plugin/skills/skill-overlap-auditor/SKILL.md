---
name: "skill-overlap-auditor"
description: "Use when the user wants to audit the current plugin's local skills as a set for overlapping triggers, ambiguous routing, duplicate ownership, missing coverage, or merge/split/narrow recommendations across the plugin as a whole. Do not use for candidate skill discovery, implementation work, or validation planning."
---

# Skill Overlap Auditor

Audit the local skills in this plugin as a system. Focus on whether the skills are cleanly separated, easy to route, and free of avoidable overlap.

Use this skill when the user wants to review the current plugin's skills together as a routing system, not when they want to search for candidate examples or write a new skill from scratch.

## Do Not Use For

- Searching GitHub, catalogs, or other external skill sources
- Comparing a small set of candidate skills to decide whether to adopt, adapt, or create
- Writing or editing a target skill implementation
- Validation planning for a single skill
- General code review or repository maintenance unrelated to skill routing

## Workflow

1. Define the audit scope before judging anything:
   - list the local skills to include
   - decide whether the audit covers only `SKILL.md` files or also `agents/openai.yaml` metadata
   - note any skills that should be excluded from the comparison
2. Build a compact inventory of each skill:
   - trigger description
   - owned job
   - do-not-use boundaries
   - output expectations and guardrails
3. Compare the skills for routing problems:
   - overlapping triggers
   - duplicated ownership
   - vague or competing descriptions
   - gaps where no skill clearly owns the job
4. Classify each issue with a concrete action:
   - narrow a trigger
   - merge two skills
   - split a broad skill
   - rename for clarity
   - add a missing skill
5. Check the plugin as a whole:
   - confirm the set has a clear division of labor
   - note any redundant skills that should be collapsed
   - note any important workflow that is still uncovered
6. Report the audit in a decision-oriented format:
   - findings first, ordered by severity or routing impact
   - then recommendations for narrow/merge/split changes
   - then any remaining gaps, assumptions, or uncertainties

## Output Expectations

Return a concise audit with:

- the skills or files that were compared
- the main overlap or ambiguity findings
- the concrete change recommended for each finding
- any gaps in coverage that remain after the audit
- any assumptions that limit confidence

When useful, include:

- a short matrix of skill name, owned job, and collision risk
- a one-line recommendation per skill: keep, narrow, merge, or split

## Guardrails

- Do not expand into external discovery; use `skills-search` for that.
- Do not take over candidate comparison for a new skill idea; use `skills-search` for adopt/adapt/create decisions.
- Do not drift into validation design; use `test-strategist` for that.
- Do not report style-only concerns unless they affect routing or ownership.
- Do not invent overlap where the descriptions are already distinct.
- Do not assume one skill should own everything related to skills.
- If the audit scope is too broad to judge reliably, say so and narrow it.
