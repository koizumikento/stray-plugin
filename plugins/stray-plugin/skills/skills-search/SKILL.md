---
name: "skills-search"
description: "Use when the user wants to find existing agent skills before creating a new one, compare similar skills across GitHub or official catalogs, or decide whether to adopt, adapt, or write a new skill. Do not use for implementation work, generic web research, or anything tied to package managers or ccpm."
---

# Skills Search

Find existing agent skills first, then judge whether they are good enough to reuse or should be adapted. Keep the work narrowly focused on skill discovery and comparison, not on building the final skill itself.

Use this skill when the user wants to:

- search GitHub, official catalogs, or local plugin skills for related examples
- compare similar skills and identify overlap or gaps
- decide whether to adopt an existing skill, adapt it, or create a new one

## Preferred Scope

- local plugin skill discovery before authoring a new skill
- GitHub or official catalog comparison for a specific capability
- overlap analysis against existing skills in the current plugin
- recommendation work that ends in a concrete adopt, adapt, or create decision

## Do Not Use For

- writing or editing the target skill itself
- generic domain research that is not about skills
- package-manager-based discovery flows
- `ccpm`-specific workflows or other external orchestration tools

## Workflow

1. Define the search scope before looking anything up:
   - the target capability or workflow
   - whether the search should cover local skills, GitHub, official catalogs, or all three
   - the decision that the search must support
2. Search in order of authority and relevance:
   - local `skills/` folders in the current plugin first
   - official or first-party skill catalogs next when available
   - GitHub repositories or examples only when they add useful coverage or missing patterns
3. Keep the candidate set small and useful:
   - prefer the best 3-5 candidates instead of collecting many weak matches
   - drop candidates that only share vague terminology but not the same job
   - stop broadening the search when the recommendation is already clear
4. Compare candidates against the target need using the same criteria every time:
   - trigger boundary: what user request should activate the skill
   - owned job: the one task or workflow the skill actually covers
   - non-goals: what the skill explicitly avoids
   - dependencies: tools, scripts, MCP servers, or external services it assumes
   - fit with local plugin: whether it overlaps with an existing local skill
   - adaptation cost: whether it can be narrowed or reused without dragging in unrelated complexity
5. Classify each candidate into one of these outcomes:
   - adopt as-is
   - adapt with narrower scope
   - use as reference only
   - do not use
6. Make the recommendation from the plugin's point of view:
   - prefer reuse when a candidate already fits the job cleanly
   - prefer adaptation when the core workflow is useful but the candidate is too broad, tool-heavy, or tied to another ecosystem
   - recommend creating a new skill only when the gap is real and specific
7. Stop once the decision is clear:
   - if one or two strong matches exist, report them and why they fit
   - if no good match exists, explain the gap and what a new skill would need to cover

## Output Expectations

Return a concise search brief with:

- the target capability being searched
- the most relevant candidate skills, with a short reason for each
- a direct recommendation: adopt, adapt, or create new
- the reasoning behind that recommendation
- the main gap that still remains if none of the candidates is a fit
- source links or file paths for the candidates you inspected

When useful, present each candidate with:

- source
- owned job
- why it matches or fails
- recommended outcome

If the answer is "create new", end with a one-paragraph outline of what the new skill must cover and what it should avoid.

## Guardrails

- Keep the search outcome-oriented, not encyclopedic.
- Do not conflate skill discovery with skill authoring.
- Do not recommend a new skill unless the existing candidates really miss the need.
- Do not assume a package manager or external index exists unless the user explicitly provides one.
- Prefer local plugin context when it is sufficient; expand outward only when needed.
- Do not mistake popularity for fitness; a weaker but narrower candidate may be the better model.
- Do not ignore maintenance burden; avoid importing workflows that depend on tools this plugin does not want to own.
- Do not stop at "there are examples"; finish with an explicit decision.
