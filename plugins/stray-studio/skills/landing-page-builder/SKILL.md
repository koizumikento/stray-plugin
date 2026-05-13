---
name: "landing-page-builder"
description: "Use when the user wants to create, revise, or ship a landing page in the current repository, including conversion-focused section structure, messaging hierarchy, responsive implementation, CTA flow, and supporting UI polish. Do not use for brand strategy, research-only work, full product app development beyond the landing page, or one-off theming of an existing artifact."
---

# Landing Page Builder

Create or improve a landing page that is meant to persuade a specific audience to take a clear action. Focus on conversion structure, message clarity, proof strategy, visual hierarchy, minimum viable SEO hygiene, and shipped implementation in the current repository.

Use this skill when the user wants to:

- build a new LP or conversion-focused marketing landing page
- refresh an existing landing page to improve clarity or conversion
- turn product notes, feature bullets, or rough copy into a working page
- add CTA sections, proof blocks, pricing teasers, FAQ sections, or hero messaging
- make a landing page responsive, more polished, and easier to scan

## Do Not Use For

- brand strategy or broader identity system work
- research-only requests that should start from current web evidence
- full product app implementation outside the landing page flow
- one-off restyling of an existing artifact without changing its message or structure
- screenshot capture work for launch assets

## Core Principles

- Start from the conversion goal, not from decorative UI.
- Keep one primary audience and one primary CTA visible throughout the page.
- Make the page easy to scan: strong hierarchy, short sections, and proof near claims.
- Make the product, service, or outcome feel already in use. Prefer concrete UI, workflow states, outputs, examples, or customer outcomes over generic illustration.
- Put credible proof early enough to support the first major claim: logos, quantified outcomes, named customers, security posture, marketplace depth, or fresh product activity.
- Choose a proof mode intentionally: workflow simulation, live product/demo surface, customer outcome gallery, quantified enterprise proof, ecosystem depth, or trust/compliance proof.
- Treat dynamic style as communication, not decoration. Motion, layering, scroll effects, and interactive states should reveal product value, guide attention, or make proof easier to understand.
- Always decide the search posture: indexable page, campaign-only page, or explicitly noindex page.
- Treat basic SEO hygiene as mandatory even when paid traffic is the main acquisition path.
- Preserve the repository's existing stack and design language unless the user asks for a deliberate change.
- Prefer a smaller coherent page over a bloated page with redundant sections.

## Reference Material

- Use `references/lp-patterns.md` when a landing page needs stronger structure, visual proof, CTA strategy, or reference-backed design direction.
- Use `references/dynamic-visual-style.md` when the LP needs motion, dimensional product visuals, interactive hero treatments, animated proof, or conversion-supporting visual polish.
- For reference-led work, base decisions on structured checks of comparable LPs. Use subagents only when the user explicitly asks for subagents, delegation, or parallel analysis.

## Workflow

1. Frame the landing page brief.
   - Identify the offer, target audience, primary CTA, and traffic context.
   - Gather any available inputs such as existing copy, screenshots, logos, testimonials, pricing notes, or competitor references.
   - Stop if the request is really about strategy, research, or a full application flow instead of an LP.

2. Run a reference-led structure pass when design direction is weak, ambiguous, or explicitly requested.
   - Use `references/lp-patterns.md` as the baseline pattern library.
   - When comparable LPs are named or directly needed for implementation, check each LP separately for hero promise, CTA split, above-the-fold proof, section order, trust signals, product visualization, interaction, and SEO posture.
   - Keep reference checks implementation-facing: page structure, proof, CTA, visual pattern, and SEO posture. Route broad market research, product positioning, or category strategy elsewhere.
   - If the user explicitly asks for subagents, delegation, or parallel analysis, assign different LPs to separate subagents and ask for the same structure checklist from each one.
   - Synthesize references into a small set of usable decisions: section archetype, proof mode, CTA rhythm, first-screen visual proof, and SEO posture.
   - Do not copy a reference page's styling wholesale; adapt only patterns that support the current offer and repository constraints.

3. Inspect the current implementation surface.
   - Find the existing route, page, layout, styling system, component conventions, and asset locations.
   - If no landing page exists yet, choose the smallest credible web surface that fits the repository.
   - Preserve established framework and styling patterns unless they block the page goal.

4. Define the conversion structure before editing.
   - Decide the section order, usually some subset of: hero, first-screen proof, problem, value proposition, product or output proof, trust, feature or benefit blocks, objection handling, CTA, FAQ, and footer.
   - Make the message hierarchy explicit: headline, subhead, supporting proof, and CTA text.
   - Pick the structure that matches buyer intent: workflow lifecycle, build path, product surface map, customer outcome story, platform taxonomy, or compliance/trust path.
   - Remove or de-emphasize sections that distract from the main action.

5. Define the dynamic visual approach when motion, interaction, product simulation, or higher-end polish is relevant.
   - Use `references/dynamic-visual-style.md` to choose the motion role, layering model, product visual treatment, and interaction states.
   - Skip heavy dynamic treatment for straightforward copy, structure, or static layout edits unless it improves conversion clarity.
   - Prefer small, purposeful motion: reveal workflow progression, compare before/after, highlight live status, show product response, or clarify depth.
   - Plan responsive behavior for every dynamic element before implementation so animation, media, and layered objects do not overlap text or shift layout.
   - Respect `prefers-reduced-motion` and avoid motion that hides information, delays CTA access, or creates layout instability.

6. Define the page metadata and search posture.
   - Decide whether the page should be indexed, noindexed, or canonicalized elsewhere.
   - Set or update the essential metadata: title, meta description, social sharing metadata, and canonical URL when relevant.
   - Make sure the title, meta description, H1, and page copy name the category, audience, and current wedge when organic traffic matters.

7. Implement the page end to end.
   - Build or revise the layout, copy structure, components, assets, and CTA flow.
   - Keep responsive behavior intentional on both desktop and mobile.
   - Ensure the visual treatment supports the message rather than competing with it.
   - Show real product state, output examples, customer results, or plausible workflow details above or immediately below the hero.

8. Tighten credibility and conversion details.
   - Add social proof, trust cues, objection-handling, or FAQ content where the page needs it.
   - Make forms, buttons, links, and anchor navigation obvious and reliable.
   - Use CTA labels that match the user's actual next job, such as `Deploy`, `Open account`, `Download for macOS`, `Start with AI`, `Request a demo`, or `Talk to sales`.
   - If copy is missing, write concise placeholder or production-ready copy based on the available product context and state the assumption.

9. Validate the shipped LP.
   - Check the main path on desktop and mobile layouts.
   - Verify CTA targets, forms, anchors, and obvious broken states.
   - Check the SEO minimums: title, description, heading structure, index or noindex choice, and obvious performance problems.
   - Confirm the first viewport communicates the offer, primary CTA, and concrete proof without relying on in-page explanatory text.
   - Check dynamic visuals with motion enabled and reduced motion, and confirm they do not block CTA access, readability, or mobile layout stability.
   - Run the repository's relevant lint, typecheck, tests, or build steps when they apply.

10. Hand off clearly.
   - Summarize the audience, CTA, and section logic that shaped the page.
   - State the chosen proof mode and any reference-derived patterns used.
   - State the dynamic visual approach and any reduced-motion or responsive assumptions.
   - State the chosen SEO posture and any metadata or indexing assumptions.
   - Report what was implemented, what was assumed, and what remains unverified.
   - If the work expands into brand system design, route to `brand-designer`. If it becomes artifact-only restyling, route to `artifact-theme-applier`.

## Output Expectations

- A working LP change in the repository, or a concrete blocker report
- The primary audience and CTA the page was optimized around
- The section structure and key messaging choices
- The proof mode, first-screen proof, and any reference patterns applied
- The dynamic visual approach when relevant, including motion role, layered visual treatment, and reduced-motion handling
- The chosen SEO posture and essential metadata decisions
- Validation performed, especially responsive, CTA-path, and SEO-minimum checks
- Any assumptions made for missing copy, assets, proof, or analytics details

## Guardrails

- Do not treat a landing page like a generic app feature or dashboard screen.
- Do not overload the page with multiple competing CTAs unless the user explicitly wants that tradeoff.
- Do not drift into broad brand strategy, market research, or campaign planning.
- Do not add heavy dependencies or a new frontend stack for a single LP unless the user explicitly asks for it.
- Do not skip the index or noindex decision, metadata basics, or heading structure just because the page is conversion-focused.
- Do not stop at visual polish if the CTA flow, hierarchy, or copy structure is still weak.
- Do not use decorative visuals as a substitute for product proof, output examples, customer outcomes, or trust evidence.
- Do not add complex animation, canvas, video, or 3D when CSS transitions, static product proof, or a simple interaction would communicate the same value more reliably.
