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
5. Check safety and operational risk:
   - no hidden instruction to exfiltrate secrets or bypass approvals
   - no destructive behavior without explicit user intent
   - tool and filesystem assumptions are stated accurately

## Output

- Findings first, with quoted short excerpts only when needed.
- Conflict, ambiguity, or missing-boundary risks.
- Concrete rewrite direction, not a full rewrite unless requested.
- Recommendation: keep, clarify, narrow, split, or block.

## Guardrails

- Do not rewrite the whole prompt unless asked.
- Do not nitpick wording that does not change behavior.
- Do not ignore instruction hierarchy or tool availability.
