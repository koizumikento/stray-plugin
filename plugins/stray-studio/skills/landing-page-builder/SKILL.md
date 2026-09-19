---
name: "landing-page-builder"
description: "Use when building or revising a conversion landing page, including message, proof, CTA, SEO, and responsive implementation. Excludes corporate sites, app flows, and theme-only restyling."
---

# Landing Page Builder

Create or improve a landing page that is meant to persuade a specific audience to take a clear action. Focus on conversion structure, message clarity, proof strategy, visual hierarchy, minimum viable SEO hygiene, and shipped implementation in the current repository.

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
- Use only supplied or verified facts for customer names, logos, testimonials, results, certifications, and security or compliance claims. Omit unsupported proof; label simulated screens, workflows, and data visibly as demos or examples on the page.
- Choose a proof mode intentionally: workflow simulation, live product/demo surface, customer outcome gallery, quantified enterprise proof, ecosystem depth, or trust/compliance proof.
- Treat dynamic style as communication, not decoration. Motion, layering, scroll effects, and interactive states should reveal product value, guide attention, or make proof easier to understand.
- Always decide the search posture: indexable page, campaign-only page, or explicitly noindex page.
- Treat basic SEO hygiene as mandatory even when paid traffic is the main acquisition path.
- Preserve the repository's existing stack and design language unless the user asks for a deliberate change.
- Prefer a smaller coherent page over a bloated page with redundant sections.

## Reference Material

- Use `references/lp-patterns.md` when a landing page needs stronger structure, visual proof, CTA strategy, or reference-backed design direction.
- Use `references/dynamic-visual-style.md` when the LP needs motion, dimensional product visuals, interactive hero treatments, animated proof, or conversion-supporting visual polish.
- For reference-led work, base decisions on structured checks of comparable LPs. Parallelize independent read-only reference checks when that materially speeds comparison, using the same evidence checklist and keeping implementation ownership in one place.

## Workflow

1. Identify the offer, audience, primary CTA, traffic context, and available product facts/assets. Inspect the affected route, layout, styles, components, and repository conventions. Preserve the current stack; choose the smallest credible surface only if no page exists. Route brand strategy, broad research, app flows, and theme-only changes elsewhere.
2. Investigate design references only when direction is weak, ambiguous, or requested. Use `references/lp-patterns.md` and compare hero promise, CTA split, first-screen proof, section order, trust, product visualization, interaction, and SEO posture. Keep the work implementation-facing and adapt useful patterns without copying a site's styling wholesale.
   - For at least two independent comparable pages, use at most three read-only checks in parallel when capacity is available and it materially helps. Give each the same checklist, prohibit repository writes, and synthesize before editing. Keep one page, coupled decisions, and all implementation with one owner.
3. Define the smallest conversion structure: message hierarchy, headline/subhead, proof mode, CTA rhythm, objection handling, and justified sections. Choose a workflow, product surface, outcome, platform, or trust-led pattern that fits the buyer. Put real or visibly labeled demo proof near the hero and remove distractions from the main action.
4. Decide search posture and relevant visuals. Choose index, noindex, or canonicalization and set title, description, social metadata, and canonical URL where needed; align category/audience wording for organic traffic. For motion or interactive product proof, use `references/dynamic-visual-style.md`; plan responsive and reduced-motion states before implementation. Static copy/layout edits need no heavy motion treatment.
5. Implement layout, copy, assets, and CTA flow across relevant desktop/mobile widths. Keep forms, buttons, links, and anchors reliable, with labels matching the visitor's next action. Add trust and FAQs only from supplied/verified facts. Label simulated UI/data visibly on the page and omit unsupported proof.
6. Validate the main path: offer/CTA/proof in the first viewport, working targets/forms/anchors, headings and search metadata, accessibility, responsive layouts, obvious performance issues, and applicable repository checks. Check motion and reduced-motion behavior when changed; neither may hide content, delay CTA access, or destabilize layout. Trace factual proof to sources and verify demo labels on the page.
7. Fix confirmed defects and rerun affected checks. Reassess a stalled hypothesis instead of repeating unchanged failures; continue while evidence improves. Stop only an action missing safe capability, input, or authorization, and continue independent work. Report implemented behavior, audience/CTA, section/proof choices, reference use, SEO/motion decisions, assumptions, and validation gaps. Required failing checks or unresolved in-scope defects mean the work is incomplete.

## Guardrails

- Do not treat a landing page like a generic app feature or dashboard screen.
- Do not overload the page with multiple competing CTAs unless the user explicitly wants that tradeoff.
- Do not drift into broad brand strategy, market research, or campaign planning.
- Do not add heavy dependencies or a new frontend stack for a single LP unless the user explicitly asks for it.
- Do not skip the index or noindex decision, metadata basics, or heading structure just because the page is conversion-focused.
- Do not stop at visual polish if the CTA flow, hierarchy, or copy structure is still weak.
- Do not use decorative visuals as a substitute for product proof, output examples, customer outcomes, or trust evidence.
- Do not add complex animation, canvas, video, or 3D when CSS transitions, static product proof, or a simple interaction would communicate the same value more reliably.
