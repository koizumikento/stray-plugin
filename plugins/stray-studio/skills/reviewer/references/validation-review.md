# Validation Review

Use this reference when reviewing validation criteria, prompt/eval cases, acceptance boundaries, or manual test plans for a skill, workflow, or LLM behavior.

## Review Focus

1. Identify the target behavior:
   - skill, prompt, workflow, or eval under review
   - intended job and non-goals
   - constraints such as read-only behavior, explicit invocation, or tool limits
2. Check the acceptance boundary:
   - what should pass
   - what should fail
   - what evidence proves the behavior is correctly scoped
   - whether completion claims match the requested outcome and actual evidence, with blocked work and unverified requirements kept distinct
   - whether criteria were established before evaluating results, and later changes follow changed requirements or evidence rather than weakening the target to accept a result
3. Review the case set:
   - positive cases for intended triggers or desired behavior
   - negative cases for near-miss prompts or unrelated tasks
   - edge cases for ambiguity, overlap, and scope creep
4. Look for validation-quality gaps:
   - missing failure modes
   - vague expected outputs
   - overlap with another local skill or workflow
   - acceptance criteria that cannot be objectively judged
   - criteria that only count actions, require an unnecessary tool sequence, or treat artifact existence as sufficient without checking the requested property; allow valid alternative approaches and concrete human judgment for qualitative work
   - optional improvements promoted into mandatory conditions after the requested outcome is supported; scale criteria to the task without requiring a dedicated heading, file, or extra approval
5. Judge readiness:
   - ready if the boundary is testable and cases are discriminating
   - needs clarification if expected output or trigger behavior is ambiguous
   - too broad if the cases cannot distinguish success from failure

## Output

- Target behavior and acceptance boundary.
- Confirmed validation gaps first.
- Positive and negative case gaps when relevant.
- Pass/fail criteria issues.
- Release recommendation: ready, needs clarification, or too ambiguous to validate.

## Guardrails

- Do not expand into general QA ownership.
- Do not duplicate code review; focus on validation design.
- Do not invent cases unrelated to the stated boundary.
- Prefer a small set of high-signal cases over exhaustive prompt collections.
