# Prompt Review

Use this reference when reviewing system prompts, developer instructions, agent instructions, skill instructions, eval prompts, or reusable LLM task prompts.

## Review Focus

1. Identify the prompt surface:
   - audience: model, agent, evaluator, or human operator
   - authority level and interaction with other instructions
   - tools, permissions, and context assumptions
2. Check behavioral clarity:
   - task ownership is explicit
   - success and failure outputs are clear
   - stop conditions and escalation paths exist
   - important non-goals are stated
3. Check conflict and priority risk:
   - instructions do not conflict with higher-priority policy or repo guidance
   - tool use rules are actionable
   - output format does not fight the task
4. Check robustness:
   - ambiguity and missing context are handled
   - prompt avoids overbroad "always" rules unless justified
   - examples do not accidentally narrow or broaden the instruction
   - eval prompts can judge outputs consistently
5. Diagnose the failure before recommending a prompt change:
   - inspect the actual model input and available evidence, retrieval coverage, tool results, and output when supplied
   - distinguish instruction ambiguity or conflict from missing evidence, retrieval failure, tool/integration defects, and model capability limits
   - state the supporting observation and uncertainty; when traces or results are absent, label the cause as a hypothesis rather than a reproduced defect
   - target the responsible component; do not prescribe stronger instructions to repair unavailable data or a failed tool
   - name the failure the change should reduce and the outcome check that would demonstrate improvement; use separate improvement and untouched confirmation cases when comparing candidates
6. Check safety and operational risk:
   - no hidden instruction to exfiltrate secrets or bypass approvals
   - no destructive behavior without explicit user intent
   - tool and filesystem assumptions are stated accurately

## Output

- Findings first, with quoted short excerpts only when needed.
- Conflict, ambiguity, or missing-boundary risks.
- Concrete rewrite direction, not a full rewrite unless requested or needed for an explicit review-fix loop.
- For a proposed behavioral repair, include the observed failure, supported or hypothetical cause, repair target, and confirmation method. Distinguish wording quality from measured outcome improvement; do not claim improved accuracy without evaluation evidence.
- Recommendation: keep, clarify, narrow, split, or block.

## Guardrails

- Do not rewrite the whole prompt unless asked or needed for an explicit review-fix loop.
- Do not nitpick wording that does not change behavior.
- Do not ignore instruction hierarchy or tool availability.
