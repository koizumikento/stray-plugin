# Skill Review

Use this reference when reviewing a single `SKILL.md`, a draft agent skill, trigger wording, workflow clarity, or whether a proposed skill should exist.

## Review Focus

1. Identify the exact skill artifact:
   - file path or proposed skill name
   - existing skill or draft
   - decision the review must support
2. Check trigger quality:
   - description says when to use the skill
   - description says when not to use it
   - wording avoids over-triggering on adjacent tasks
3. Check scope and ownership:
   - the skill owns one clear job
   - overlap with existing skills is visible and intentional
   - split, merge, or narrow decisions are grounded in the text
4. Check instruction-first quality:
   - workflow is imperative and concrete
   - outputs, assumptions, guardrails, and stop conditions are explicit
   - scripts, references, or metadata exist only when they materially help
5. Judge whether the skill should exist:
   - keep if the job is clear and distinct
   - narrow if the scope is too broad
   - merge if another skill already owns the job
   - remove if the trigger is vague or value is redundant

## Output

- State the review scope.
- List confirmed issues first.
- Give a direct recommendation: keep, narrow, merge, remove, clarify, or repaired.
- Call out overlap with local skills by name when visible.
- When the user asked for edits, list the repaired instruction areas and final review status.

## Review-Fix Loop

- When the user asks to repair the skill, run a review pass first, preferably through a focused subagent when available.
- Fix only confirmed trigger, scope, workflow, output, metadata, or guardrail issues.
- Re-review the updated skill text after each repair pass until no actionable skill findings remain or the main skill stop condition applies.

## Guardrails

- Do not turn skill review into code review.
- Do not produce a test plan unless the user asked for validation review.
- Do not rewrite the skill unless the user explicitly asked for edits or a review-fix loop.
- Do not invent overlap without evidence from the skill text or local skill set.
