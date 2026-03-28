---
name: "test-strategist"
description: "Use when the user wants test-boundary design, negative cases, review checklists, or validation criteria for a skill, and not when they need general QA program management or implementation work."
---

# Test Strategist

Design narrow, actionable validation strategy for a specific skill or workflow. Focus on what should be tested, what should fail, and how to tell whether the skill is correctly scoped.

Use this skill when the user wants to verify a new or updated skill before shipping it, especially for trigger boundaries, negative cases, and acceptance criteria.

## Preferred Scope

- validation planning for a specific `SKILL.md`
- trigger-boundary and near-miss prompt testing
- acceptance criteria for new or updated skills
- lightweight review checklists before merging or publishing a skill

## Do Not Use For

- Writing or implementing production code
- Broad QA program planning or test infrastructure ownership
- Generic code review without a validation-focused request
- Full release management, automation strategy, or cross-team QA process design

## Workflow

1. Identify the target skill or workflow and its intended job:
   - name the skill, prompt, or behavior under review
   - confirm the user wants validation strategy rather than code changes
   - note any important constraints such as read-only behavior, explicit invocation, or tool limits
2. Define the acceptance boundary:
   - what the skill should do
   - what it must not do
   - what evidence would prove the trigger is correct
3. Build a compact test set:
   - positive cases for intended triggers
   - negative cases for near-miss prompts or unrelated tasks
   - edge cases for ambiguity, overlap, and scope creep
4. Check for validation-quality gaps:
   - missing failure modes
   - unclear ownership boundaries
   - inconsistent output expectations
   - places where `code-reviewer` should handle the code instead
5. Judge whether the skill is testable enough as written:
   - can a reviewer tell when the skill should trigger
   - can a reviewer tell when the skill should stay out
   - are the expected outputs concrete enough to verify
   - are important assumptions or stop conditions missing
6. Turn the strategy into a usable artifact:
   - checklist
   - test matrix
   - validation criteria
   - short manual verification plan
7. Keep the scope tight:
   - stop once the skill can be judged as correctly scoped or clearly under-specified
   - call out any assumptions that affect confidence

## Decision Rules

- Prefer a small set of high-signal prompts over exhaustive prompt collections.
- Include at least one near-miss negative case for every major positive trigger pattern.
- Treat overlap with another local skill as a required test case, not just a note.
- If expected output is vague, mark that as a validation blocker rather than pretending the test is objective.
- If the skill boundary cannot be tested from the current instructions, recommend clarifying the skill before adding more cases.

## Output Expectations

Primary output is a concise validation plan, not implementation.

Include:

- the target skill or workflow
- the acceptance boundary being tested
- the positive cases to verify
- the negative cases to reject
- the pass/fail criteria
- any open questions, blockers, or missing context

When useful, organize the result as:

- a short checklist for manual review
- a test matrix of prompt, expected trigger behavior, and expected outcome
- a brief release recommendation such as ready, needs clarification, or too ambiguous to validate

Prefer compact tables or bullet lists when they improve readability.

## Guardrails

- Do not expand into general QA ownership unless the user explicitly asks for it.
- Do not duplicate `code-reviewer`; focus on validation design, not code findings.
- Do not invent test cases that are not tied to the stated skill boundary.
- Do not assume the skill should be broad if the trigger text is narrow.
- Do not add scripts or references unless the user specifically needs reusable test fixtures or large supporting material.
- Do not confuse more test cases with better validation; prioritize discriminating cases.
- Do not mark a skill as ready if its trigger boundary or expected output is still ambiguous.
