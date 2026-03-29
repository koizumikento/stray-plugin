---
name: "api-terms-checker"
description: "Use when the user wants to check the current usage terms, commercial restrictions, redistribution limits, model-training restrictions, data-handling clauses, or other practical compliance constraints for a third-party API or SaaS before integrating, shipping, or scaling its use. Do not use for negotiated legal advice, dependency license review, or full repository release audits."
compatibility: "Requires internet access and a browsing-capable Codex environment because this skill should verify current official terms before answering."
---

# API Terms Checker

Check whether a planned API or SaaS integration has obvious usage-term risks before the team relies on it. Focus on practical constraints that affect engineering, product, operations, and go-to-market decisions.

Use this skill when the user wants to:

- confirm whether an API appears usable for a planned product or workflow
- check commercial-use, resale, redistribution, or white-label restrictions
- identify data retention, logging, privacy, or training-related clauses
- spot prohibited use categories or approval requirements
- summarize the minimum terms the team should understand before shipping

## Do Not Use For

- negotiated legal advice or jurisdiction-specific counsel
- open-source dependency license classification
- a full repository or release compliance audit
- generic vendor comparison where terms are not the main question
- pretending certainty when the official terms are missing, unclear, or contradictory

## Workflow

1. Define the exact service and use case.
   - name the API, platform, or SaaS product
   - state how the user plans to use it
   - note whether the concern is internal use, customer-facing resale, embedding, or data processing
2. Verify current official sources first.
   - prefer the vendor's current terms of service, API terms, acceptable use policy, pricing terms, privacy or data-processing docs, and official help pages
   - capture exact dates for unstable sources or versioned legal pages
   - avoid relying on secondary summaries when the official text is available
3. Extract the minimum decision-shaping clauses.
   - commercial use or resale restrictions
   - redistribution, sublicensing, or pass-through limits
   - training, fine-tuning, or model-improvement clauses
   - data retention, logging, privacy, or subprocessors when materially relevant
   - prohibited use categories, approval requirements, or regional restrictions
4. Translate the clauses into operational impact.
   - what the team can likely do
   - what likely needs review before shipping
   - what looks blocked, unclear, or risky
   - what assumptions drive that judgment
5. Keep the answer practical.
   - separate verified facts from inference
   - quote only short excerpts when necessary
   - flag ambiguity instead of smoothing it over
6. End with the next decision step.
   - safe to proceed with routine caution
   - proceed only after legal or procurement review
   - blocked until a specific clause is clarified

## Output Expectations

- the service and intended use case
- the official sources checked, with links and dates
- the most relevant terms or restrictions
- a short risk assessment for the proposed use
- the next review step, if any

When useful, organize the result as:

- allowed or likely allowed
- unclear or needs review
- likely restricted or prohibited

## Guardrails

- Do not present this as legal advice.
- Do not rely on blog posts or forum posts when official terms exist.
- Do not answer from memory when the terms are time-sensitive.
- Do not collapse pricing questions into terms review unless pricing changes the legal restriction.
- Do not broaden into dependency license analysis; that belongs in a separate skill.
- Do not say a use is approved if the source only implies it indirectly.
