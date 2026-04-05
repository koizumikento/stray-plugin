---
name: "idea-explorer"
description: "Use when the user wants to generate, widen, or compare ideas grounded in current web research rather than memory alone, but does not yet need a concrete product decision, a deep domain brief, or a polished final artifact. Do not use for generic brainstorming with no need for evidence, or when a more specific local skill already owns the final output."
compatibility: "Requires internet access and a browsing-capable Codex environment because this skill starts from current web research before proposing ideas."
---

# Idea Explorer

Generate idea directions that are grounded in current external signals instead of generic brainstorming. Start by browsing the current landscape, then expand the option space, organize the ideas, and show which ideas look most promising and why.

Use this skill when the user wants to:

- brainstorm directions that should reflect the current market, tools, products, or public conversation
- widen the option space before choosing a product, feature, campaign, content angle, workflow, or concept
- compare several candidate directions with lightweight evidence instead of pure intuition
- turn a vague prompt into a structured set of plausible ideas and next cuts

## Do Not Use For

- generic brainstorming where current web evidence is unnecessary
- deep domain analysis that belongs in `domain-researcher`
- concrete product direction, prioritization, or scope decisions that belong in `product-designer`
- polished final deliverables such as full articles, brand systems, or visual assets that belong in more specific local skills
- extracting or cleaning one provided page or URL that belongs in `web-content-distiller`

## Workflow

1. Frame the ideation target before searching.
   - Identify what kind of ideas are needed: feature concepts, content angles, positioning directions, workflow options, campaign hooks, or another clear category.
   - Identify the audience, constraint, or decision this ideation will support.
   - Stop if the user is actually asking for a final decision, a deep research brief, or a finished artifact.

2. Gather current external signals first.
   - Browse before proposing ideas. Do not rely on memory alone when the current landscape matters.
   - Prefer official sites, launch posts, product pages, pricing pages, documentation, credible reporting, and strong examples in the wild.
   - Capture exact dates for unstable claims such as releases, pricing, policy shifts, or recent launches.

3. Distill the signals into idea inputs.
   - Extract recurring patterns, unmet needs, unusual tactics, constraints, white space, and differentiators.
   - Separate verified facts from inference.
   - Avoid copying what already exists too literally; use the evidence to widen the option space, not to clone.

4. Generate a deliberate spread of options.
   - Produce multiple distinct directions instead of near-duplicates.
   - Vary the ideas across at least one useful axis such as audience, mechanism, tone, channel, scope, or positioning.
   - Keep each idea concrete enough that the user can evaluate it quickly.

5. Organize and pressure-test the ideas.
   - Group similar ideas or rank them when that helps the user compare.
   - For each strong candidate, include why it could work, what signal supports it, and what risk or unknown remains.
   - Reject weak or redundant ideas instead of padding the list.

6. Deliver a usable ideation artifact.
   - Match the output shape to the request: shortlist, option matrix, concept bullets, naming directions, content angles, or hypothesis list.
   - Recommend the best next narrowing step when the user has not asked for a final choice.
   - Route to a more specific skill if the user then wants one option developed into a real deliverable.

## Output Expectations

- A clearly scoped set of distinct ideas, not a loose brainstorm dump
- Brief rationale tied to current web signals
- Explicit separation between verified facts and inference
- Source links for the claims or examples that materially shaped the idea set
- A short recommendation for how to narrow, test, or select next

## Guardrails

- Do not skip web research when the current landscape matters.
- Do not present generic filler ideas as if they were evidence-backed.
- Do not collapse into a final product decision when the task is still exploratory.
- Do not duplicate another local skill's final-output job.
- Do not overquote sources; paraphrase and synthesize.
