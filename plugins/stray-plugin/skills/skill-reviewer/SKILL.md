---
name: "skill-reviewer"
description: "Use when the user wants a focused review of a `SKILL.md` or agent skill design for trigger quality, scope boundaries, overlap risk, instruction-first quality, output clarity, and whether the skill should exist at all. Do not use for code diffs, general debugging, or validation planning."
---

# Skill Reviewer

Review Codex skills and agent skill designs as an artifact, not as code. Judge whether the skill is narrowly scoped, routes correctly, and is worth keeping as a separate skill.

Use this skill when the user asks for a review of:

- a new or existing `SKILL.md`
- trigger wording and implicit invocation behavior
- overlap with other local skills
- instruction-first quality and workflow clarity
- whether a proposed skill should be merged, narrowed, or deleted

## Do Not Use For

- Reviewing application code, diffs, or pull requests
- Designing tests or acceptance criteria for a skill
- General repository maintenance or GitHub triage
- Broad brainstorming that does not involve an actual skill artifact

## Workflow

1. Identify the exact skill artifact under review:
   - the file path or proposed skill name
   - whether the review is of an existing skill or a draft
   - the decision the review must support
2. Check trigger quality first:
   - whether the description is specific enough to invoke correctly
   - whether the wording avoids over-triggering on adjacent tasks
   - whether the `do not use` boundary is explicit enough
3. Check scope and ownership:
   - whether the skill owns one job
   - whether it overlaps with existing skills in this plugin
   - whether the boundary should be split, merged, or narrowed
4. Check instruction-first quality:
   - whether the workflow is imperative and concrete
   - whether it states outputs, assumptions, and stop conditions
   - whether it avoids unnecessary scripts, references, or metadata
5. Judge whether the skill should exist:
   - keep it if the job is clear and distinct
   - narrow it if the scope is too broad
   - merge it if another skill already owns the job
   - reject it if the trigger is too vague or the value is redundant
6. Report the outcome in review order:
   - confirmed issues first
   - then assumptions or open questions
   - then the final recommendation

## Output Expectations

- State the review scope explicitly.
- List the highest-signal problems or confirm that none remain.
- Give a direct recommendation: keep, narrow, merge, or remove.
- Call out any overlap with other local skills by name when visible.

## Guardrails

- Do not turn this into a code review.
- Do not produce a test plan; that belongs to `test-strategist`.
- Do not rewrite the skill unless the user explicitly asks for edits.
- Do not invent overlap concerns without evidence from the skill text or local skill set.
