---
name: "product-designer"
description: "Use when the user wants to design or refine a product concept, feature, workflow, or strategy and the work should start from current web research rather than memory alone, with concrete product decisions such as a feature brief, PRD outline, scope boundary, or validation plan as the output instead of a research-only brief. Do not use for visual design polish, generic brainstorming without evidence, or pure domain research with no product decision to make."
compatibility: "Requires internet access and a browsing-capable Codex environment because this skill starts from current web research."
---

# Product Designer

Turn current external evidence into concrete product design decisions. Always start with current web research, then move from facts and signals to product direction, feature scope, tradeoffs, acceptance criteria, and validation steps.

Use this skill when the user wants to:

- shape a new product or feature direction
- compare product approaches against the current market
- define user, problem, positioning, or scope before implementation
- turn research into a feature brief, concept, PRD outline, or validation plan
- pressure-test an existing feature idea against user need, scope, and success metrics

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
   - Keep the proposal specific enough to inform roadmap, specs, experiments, or acceptance criteria.

5. Convert the direction into an implementation-ready feature shape.
   - State the user need, target user, and the smallest valuable version of the feature.
   - Define what is in scope now, what is explicitly out of scope, and what can wait.
   - Add acceptance criteria, user-facing edge cases, and a lightweight rollout or experiment plan when they matter.

6. Produce a usable design artifact.
   - Match the artifact to the user's need: concept brief, feature brief, PRD outline, opportunity framing, or validation plan.
   - Include assumptions, open questions, success metrics, and what must be validated next.
   - Keep the output decision-oriented instead of turning it into a long research dump.

7. Stay within the design boundary.
   - If the user only needs a source-backed investigation, use `domain-researcher` instead.
   - If the user needs screenshots, theming, or visual assets, route to the more specific local skill.

## Output Expectations

- A direct product recommendation or design direction
- The target user, problem, and proposed value
- The minimum useful scope, explicit out-of-scope line, and acceptance criteria when relevant
- Research-backed rationale with source links
- Explicit separation between verified facts and inference
- Key tradeoffs, risks, success metrics, and next validation steps

When useful, structure the result as:

- product brief
- feature concept
- PRD outline
- feature design checklist
- opportunity assessment

## Guardrails

- Do not skip web research. This skill starts from current browsing even when the topic looks familiar.
- Do not pretend research certainty where the evidence is weak.
- Do not collapse into visual design critique unless the user asks for it.
- Do not return generic product advice without tying it to evidence and a concrete decision.
- Do not stop at feature naming or broad intent when the user needs scope, criteria, or validation details.
- Do not duplicate `domain-researcher`; the job here is design synthesis, not research alone.
