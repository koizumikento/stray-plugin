---
name: "idea-explorer"
description: "Use when the user wants to generate, widen, or compare ideas grounded in current web research from live external sources rather than memory alone, but does not yet need a concrete product decision, a deep domain brief, or a polished final artifact. Do not use for generic brainstorming with no need for evidence, or when a more specific local skill already owns the final output."
compatibility: "Requires internet access and a browsing-capable Codex environment because this skill starts from current web research before proposing ideas."
---

# Idea Explorer

Generate idea directions that are grounded in current external signals instead of generic brainstorming. Start by browsing the current landscape, then deliberately vary the source signals, idea axes, and concept shapes so the output is not a list of near-duplicates. Organize the ideas and show which ones look most promising and why.

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
   - When the first signal set looks obvious, use `references/web-signal-lenses.md` to widen the source mix before generating ideas.
   - For broad or high-volume ideation requests, use the optional multi-agent expansion pattern below when subagents are available.

3. Distill the signals into idea inputs.
   - Extract recurring patterns, unmet needs, unusual tactics, constraints, white space, and differentiators.
   - Pull signals from more than one shape of source when possible: category leaders, emerging tools, adjacent industries, user complaints, pricing or packaging moves, community discussions, and failed or criticized examples.
   - Include noncustomers, substitutes, complements, distribution moves, infrastructure shifts, regulation or policy changes, and weak signals when they are relevant to the domain.
   - Separate verified facts from inference.
   - Avoid copying what already exists too literally; use the evidence to widen the option space, not to clone.
   - Name the raw ideation ingredients before generating ideas: tensions, underserved audiences, surprising mechanisms, channel shifts, behavior changes, and constraints.

4. Generate a deliberate spread of options.
   - Produce multiple distinct directions instead of near-duplicates.
   - Vary the ideas across at least three useful axes such as audience, mechanism, tone, channel, scope, pricing, distribution, risk, time horizon, or positioning.
   - Include at least one contrarian, niche, premium, low-friction, and infrastructure-oriented direction when the domain allows it.
   - Borrow patterns from adjacent domains instead of only extending the most obvious examples found in search.
   - Create ideas by recombining signals, not by mapping one source to one idea.
   - Use multiple opportunity lenses from `references/web-signal-lenses.md`, such as job progress, buyer utility, market boundary shifts, four actions, constraint inversion, adoption wedges, distribution wedges, data advantage, trust and risk, and emotional reframing.
   - Keep each idea concrete enough that the user can evaluate it quickly.

5. Organize and pressure-test the ideas.
   - Group similar ideas or rank them when that helps the user compare.
   - Check for concept clumping: if two ideas share the same audience, mechanism, and value proposition, merge them or replace one with a more different direction.
   - Apply the diversity check in `references/web-signal-lenses.md` before finalizing.
   - For each strong candidate, include why it could work, what signal supports it, and what risk or unknown remains.
   - Reject weak or redundant ideas instead of padding the list.
   - Call out any intentionally odd or high-variance idea as such, and explain what it might reveal even if it is not the safest option.

6. Deliver a usable ideation artifact.
   - Match the output shape to the request: shortlist, option matrix, concept bullets, naming directions, content angles, or hypothesis list.
   - Recommend the best next narrowing step when the user has not asked for a final choice.
   - Route to a more specific skill if the user then wants one option developed into a real deliverable.

## Optional Multi-Agent Expansion

Use parallel subagents only when the user asks for many ideas, the topic is broad, or a single web-signal pass is likely to converge on obvious patterns. Do not make this the default path for small or tightly scoped ideation requests.

1. Assign each subagent a distinct research lens, not the same broad prompt.
2. Split scouts by source family or opportunity lens, for example:
   - category leaders, pricing, and packaging
   - user complaints, noncustomers, and failed examples
   - adjacent domains, substitutes, and complements
   - infrastructure shifts, policy, weak signals, and new constraints
   - distribution wedges, business model shifts, and adoption wedges
3. Require each scout to return source links, observed signals, 3-5 raw opportunity seeds, and what would make those seeds non-obvious.
4. Synthesize centrally before producing final ideas:
   - merge duplicate concepts
   - recombine signals across scouts
   - fill missing axes from `references/web-signal-lenses.md`
   - reject weak, repetitive, or evidence-thin ideas
5. If subagents are not available, run the same scout lenses sequentially and label them as separate passes.

## Output Expectations

- A clearly scoped set of distinct ideas, not a loose brainstorm dump
- Brief rationale tied to current web signals
- Explicit separation between verified facts and inference
- Source links for the claims or examples that materially shaped the idea set
- Visible variation across idea axes, with redundant concepts merged or discarded
- When multi-agent expansion is used, a short synthesis note describing which scout lenses contributed the strongest signals
- A short recommendation for how to narrow, test, or select next

## Guardrails

- Do not skip web research when the current landscape matters.
- Do not present generic filler ideas as if they were evidence-backed.
- Do not let all ideas share the same audience, channel, mechanism, or risk level unless the user explicitly constrained the space that tightly.
- Do not use subagents to multiply near-identical prompts; use them to separate research lenses and then synthesize centrally.
- Do not collapse into a final product decision when the task is still exploratory.
- Do not duplicate another local skill's final-output job.
- Do not overquote sources; paraphrase and synthesize.
