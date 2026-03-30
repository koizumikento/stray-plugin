---
name: "landing-page-builder"
description: "Use when the user wants to create, revise, or ship a landing page in the current repository, including conversion-focused section structure, messaging hierarchy, responsive implementation, CTA flow, and supporting UI polish. Do not use for brand strategy, research-only work, full product app development beyond the landing page, or one-off theming of an existing artifact."
---

# Landing Page Builder

Create or improve a landing page that is meant to persuade a specific audience to take a clear action. Focus on conversion structure, message clarity, visual hierarchy, minimum viable SEO hygiene, and shipped implementation in the current repository.

Use this skill when the user wants to:

- build a new LP or marketing page
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
- Always decide the search posture: indexable page, campaign-only page, or explicitly noindex page.
- Treat basic SEO hygiene as mandatory even when paid traffic is the main acquisition path.
- Preserve the repository's existing stack and design language unless the user asks for a deliberate change.
- Prefer a smaller coherent page over a bloated page with redundant sections.

## Workflow

1. Frame the landing page brief.
   - Identify the offer, target audience, primary CTA, and traffic context.
   - Gather any available inputs such as existing copy, screenshots, logos, testimonials, pricing notes, or competitor references.
   - Stop if the request is really about strategy, research, or a full application flow instead of an LP.

2. Inspect the current implementation surface.
   - Find the existing route, page, layout, styling system, component conventions, and asset locations.
   - If no landing page exists yet, choose the smallest credible web surface that fits the repository.
   - Preserve established framework and styling patterns unless they block the page goal.

3. Define the conversion structure before editing.
   - Decide the section order, usually some subset of: hero, problem, value proposition, proof, feature or benefit blocks, CTA, FAQ, and footer.
   - Make the message hierarchy explicit: headline, subhead, supporting proof, and CTA text.
   - Remove or de-emphasize sections that distract from the main action.

4. Define the page metadata and search posture.
   - Decide whether the page should be indexed, noindexed, or canonicalized elsewhere.
   - Set or update the essential metadata: title, meta description, social sharing metadata, and canonical URL when relevant.
   - Make sure the heading structure and page copy support both scanability and the intended search intent when organic traffic matters.

5. Implement the page end to end.
   - Build or revise the layout, copy structure, components, assets, and CTA flow.
   - Keep responsive behavior intentional on both desktop and mobile.
   - Ensure the visual treatment supports the message rather than competing with it.

6. Tighten credibility and conversion details.
   - Add social proof, trust cues, objection-handling, or FAQ content where the page needs it.
   - Make forms, buttons, links, and anchor navigation obvious and reliable.
   - If copy is missing, write concise placeholder or production-ready copy based on the available product context and state the assumption.

7. Validate the shipped LP.
   - Check the main path on desktop and mobile layouts.
   - Verify CTA targets, forms, anchors, and obvious broken states.
   - Check the SEO minimums: title, description, heading structure, index or noindex choice, and obvious performance problems.
   - Run the repository's relevant lint, typecheck, tests, or build steps when they apply.

8. Hand off clearly.
   - Summarize the audience, CTA, and section logic that shaped the page.
   - State the chosen SEO posture and any metadata or indexing assumptions.
   - Report what was implemented, what was assumed, and what remains unverified.
   - If the work expands into brand system design, route to `brand-designer`. If it becomes artifact-only restyling, route to `artifact-theme-applier`.

## Output Expectations

- A working LP change in the repository, or a concrete blocker report
- The primary audience and CTA the page was optimized around
- The section structure and key messaging choices
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
