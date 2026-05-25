# Skill Set Review

Use this reference when reviewing multiple local skills as a routing system for overlap, ambiguity, duplicate ownership, or missing coverage.

## Review Focus

1. Define the audit scope:
   - list the local skills included
   - decide whether the review covers only `SKILL.md` files or also `agents/openai.yaml`
   - note excluded skills
2. Build a compact inventory for each skill:
   - trigger description
   - owned job
   - do-not-use boundaries
   - output expectations and guardrails
3. Compare routing behavior:
   - overlapping triggers
   - duplicated ownership
   - vague or competing descriptions
   - gaps where no skill owns an expected job
4. Classify each issue with a concrete action:
   - narrow a trigger
   - merge two skills
   - split a broad skill
   - rename for clarity
   - add missing coverage
5. Check the plugin as a whole:
   - clear division of labor
   - redundant skills to collapse
   - important workflows still uncovered

## Output

- Findings first, ordered by routing impact.
- Include a one-line recommendation per affected skill: keep, narrow, merge, split, rename, or remove.
- Include assumptions or uncertainty when the audit scope is incomplete.

## Guardrails

- Do not expand into external skill discovery.
- Do not take over implementation.
- Do not report style-only concerns unless they affect routing or ownership.
- Do not assume one skill should own everything related to a broad domain.
