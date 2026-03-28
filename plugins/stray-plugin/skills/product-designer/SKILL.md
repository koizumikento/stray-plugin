---
name: "product-designer"
description: "Use when the user wants to design or refine a product concept, feature, workflow, or strategy and the work should start from current web research rather than memory alone, with concrete product decisions as the output instead of a research-only brief. Do not use for visual design polish, generic brainstorming without evidence, or pure domain research with no product decision to make."
compatibility: "Requires internet access and a browsing-capable Codex environment because this skill starts from current web research."
---

# Product Designer

Turn current external evidence into concrete product design decisions. Always start with current web research, then move from facts and signals to product direction, scope, tradeoffs, and validation steps.

Use this skill when the user wants to:

- shape a new product or feature direction
- compare product approaches against the current market
- define user, problem, positioning, or scope before implementation
- turn research into a brief, concept, PRD outline, or validation plan

## Do Not Use For

- visual UI polish, branding, or marketing asset creation
- pure domain research where no product decision is being made
- implementation planning that already has a settled product direction
- generic ideation sessions that do not require evidence from the web

## Workflow

1. Frame the product decision before searching.
   - Identify the product, feature, or workflow under design.
   - State the target user, problem, and the decision that must be made.
   - Stop if the request is only asking for research or only asking for visual critique.

2. Gather current external evidence first.
   - Browse before proposing any direction. Do not rely on memory alone.
   - Prioritize official product sites, vendor docs, pricing pages, launch posts, public case studies, standards, and credible primary reporting.
   - Capture exact dates for current claims, especially for product availability, pricing, policy, or competitor moves.

3. Distill the evidence into product-relevant signals.
   - Separate confirmed facts from inference.
   - Extract user needs, market gaps, competitive patterns, constraints, and differentiators.
   - Note where evidence is thin, contradictory, or stale enough to weaken confidence.

4. Turn signals into product decisions.
   - Recommend a product direction, scope boundary, and target user/value proposition.
   - Name the key tradeoffs, rejected alternatives, and why they were rejected.
   - Keep the proposal specific enough to inform roadmap, specs, or experiments.

5. Produce a usable design artifact.
   - Match the artifact to the user's need: concept brief, feature brief, PRD outline, opportunity framing, or validation plan.
   - Include assumptions, open questions, and what must be validated next.
   - Keep the output decision-oriented instead of turning it into a long research dump.

6. Stay within the design boundary.
   - If the user only needs a source-backed investigation, use `domain-researcher` instead.
   - If the user needs screenshots, theming, or visual assets, route to the more specific local skill.

## Output Expectations

- A direct product recommendation or design direction
- The target user, problem, and proposed value
- Research-backed rationale with source links
- Explicit separation between verified facts and inference
- Key tradeoffs, risks, and next validation steps

When useful, structure the result as:

- product brief
- feature concept
- PRD outline
- opportunity assessment

## Guardrails

- Do not skip web research. This skill starts from current browsing even when the topic looks familiar.
- Do not pretend research certainty where the evidence is weak.
- Do not collapse into visual design critique unless the user asks for it.
- Do not return generic product advice without tying it to evidence and a concrete decision.
- Do not duplicate `domain-researcher`; the job here is design synthesis, not research alone.
