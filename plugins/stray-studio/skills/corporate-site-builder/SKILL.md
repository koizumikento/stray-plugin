---
name: "corporate-site-builder"
description: "Use when the user wants to create, revise, or ship a corporate website in the current repository, including company information architecture, homepage and lower-page structure, business/service sections, news, careers, IR, sustainability, governance, trust/policy links, and responsive implementation. Do not use for single-offer landing pages, pure brand strategy, research-only benchmarking, full product app flows, or one-off visual theming."
---

# Corporate Site Builder

Create or improve a corporate website that explains who the company is, what it does, why it is trustworthy, and where each visitor should go next. Treat the site as a durable company information system, not a one-page campaign asset.

Use this skill when the user wants to:

- build or redesign a company/corporate website
- create a homepage plus company, business/service, news, careers, IR, sustainability, or contact pages
- turn a company profile, business notes, brand materials, or rough sitemap into a working site
- improve corporate navigation, footer sitemap, trust sections, or stakeholder-specific routes
- make a corporate site more credible, scannable, responsive, accessible, and maintainable

## Do Not Use For

- single-offer landing pages that should use `landing-page-builder`
- broad brand identity work without site implementation
- research-only benchmarking or inspiration gathering
- full product application flows, dashboards, auth, or data-backed user workflows
- one-off visual restyling of an existing artifact without changing corporate structure
- investor relations, ESG, or legal content authoring that requires specialist compliance review

## Core Principles

- Start from the visitor groups: customers, candidates, investors, press, partners, communities, and existing users.
- Make the company easy to understand before making it visually impressive.
- Design the site as an information architecture with durable lower pages, not only a dramatic homepage.
- Put proof near claims: numbers, business facts, leadership, news, reports, security, policies, awards, customer proof, or media coverage.
- Use the footer as a full corporate sitemap and trust surface, not a link dumping ground.
- Keep recruitment, IR, sustainability, safety, security, and policy links at the navigation level their audience expects.
- Preserve the repository's existing stack, routing, component system, and content workflow unless the user asks for a deliberate change.
- Treat missing content honestly: create clear structure and concise placeholders only when the assumption is explicit.
- Use motion and dynamic visuals to clarify hierarchy, reveal relationships, and express company character. Do not add motion that competes with facts, navigation, or accessibility.

## Corporate Site Patterns

Use these patterns to diagnose the right structure before writing code:

- Startup or scaleup mission-led site: strong mission, what the company does, business lines, latest news, careers, contact.
- SaaS or business-tool site: products, use cases, consultation, customer support, seminars/events, company information, IR or sustainability when needed.
- Social infrastructure or marketplace site: mission, services, safety, security, privacy, sustainability, IR, transparency reports, careers.
- Large public company or conglomerate site: brand world, business areas, technology or innovation, news, IR, sustainability, governance, careers, global links, search, language switching.
- Brand portfolio or D2C site: mission, brands, product/EC links, brand news, corporate news, sustainability, quality/safety policies, careers, contact.
- Creative or culture-heavy company site: projects, services, members, vision, news, awards, culture articles, careers, IR when relevant.

## Information Architecture Checklist

Default corporate sites usually need:

- Home
- About or Company
- Mission, vision, values, philosophy, or message
- Business, services, products, brands, or projects
- News, press releases, announcements, or media coverage
- Careers or recruiting link
- Contact
- Privacy policy, terms, accessibility, and security or data policy links

Add these when the company context justifies them:

- IR for listed, investor-facing, or fundraising-sensitive companies
- Sustainability, ESG, governance, human rights, supply chain, or DEI for public, global, retail, marketplace, or high-accountability companies
- Safety, trust, transparency, privacy, security, AI policy, or compliance for marketplaces, finance, HR, data, healthcare, or public-infrastructure products
- Press kit, media kit, downloads, or brand assets for press-heavy or startup companies
- Service status, support, manuals, FAQ, consultation, or case studies for SaaS and business tools
- Store, EC, owned media, app, SNS, or brand links for retail, D2C, and portfolio companies
- Search, language switching, mega navigation, and sitemap pages for large multi-division companies

## Minimum Fact Gate

Before implementing public-facing corporate content, confirm that the available inputs are enough to avoid inventing company facts:

- Minimum facts: company or organization name, what it does, primary audience or stakeholder groups, main business/service/brand areas, contact or next-step destination, and whether careers, IR, sustainability, safety/security, policy, or press routes should exist.
- If minimum facts are missing and cannot be inferred from repository content, ask concise questions before writing production copy.
- If the user wants a structural prototype despite missing facts, build clearly labeled content scaffolding and avoid factual claims, certifications, numbers, leadership names, reports, policy promises, or external destinations that were not provided.
- If the request needs legally sensitive claims, investor disclosures, ESG statements, safety/security assurances, financial results, hiring commitments, or regulated industry content that is not sourced, stop that part with a blocker note instead of fabricating it.
- If enough facts exist for the core site but not for optional sections, implement the core routes and mark optional sections as omitted, draft-only, or externally owned in the handoff.

## Visual Style And Motion Guidance

Use dynamic presentation when it helps the site feel alive, premium, or easier to understand:

- Hero systems: use real photography, product imagery, office/process footage, generative brand visuals, data-driven visuals, or subtle interactive scenes that reveal the company domain quickly.
- Scroll rhythm: vary section density with a mix of editorial text blocks, proof rows, image bands, cards, timelines, and full-width feature sections.
- Motion hierarchy: apply motion first to page entrance, section reveal, hero media, navigation transitions, hover states, counters, timelines, carousels, and expandable detail panels.
- Interaction patterns: use hover previews, tabbed business/service sections, filterable news, segmented stakeholder routes, accordions for policies/FAQ, and timeline interactions when the content benefits from comparison or progressive disclosure.
- Brand expression: derive color, typography, spacing, image treatment, corner radius, icon style, and motion speed from the company's tone: institutional, technical, human, editorial, premium, playful, or operational.
- Trust surfaces: keep IR, ESG, policy, safety, and security pages visually restrained and information-dense; use dynamic treatment only to improve scanning, not to dramatize regulated or factual content.
- Component polish: give cards, buttons, nav items, media blocks, and lists consistent hover/focus/active/loading states so the site feels intentionally built rather than static.
- Responsive behavior: design mobile navigation, sticky headers, carousels, mega menus, and media-heavy hero sections explicitly instead of letting desktop effects collapse awkwardly.
- Performance: prefer CSS transitions, transform/opacity animation, optimized images/video, lazy loading, and small interaction libraries already present in the repo.
- Accessibility: respect reduced-motion preferences, preserve keyboard access, avoid scroll-jacking, keep text readable over media, and never make essential content depend on animation.

Before choosing a visual direction, name the site's style posture:

- Trust-first: quiet layout, clear tables, strong typography, low-motion proof and policy surfaces.
- Mission-led: expressive hero, editorial mission blocks, smooth scroll reveals, people or domain imagery.
- Product-led: product screenshots, interaction previews, comparison modules, demo or consultation CTAs.
- Brand-led: rich imagery, brand cards, media/EC/SNS links, tactile transitions, stronger art direction.
- Enterprise/global: large navigation, modular grids, restrained animation, search/language utilities, data and report surfaces.
- Culture-led: project/member/news modules, playful transitions, high content velocity, strong internal media links.

## Workflow

1. Frame the corporate site brief.
   - Identify the company type, business model, maturity, listing status, markets, languages, and primary visitor groups.
   - Gather available company profile material, brand assets, services, product links, news sources, hiring links, IR/ESG materials, policies, and competitor or reference sites.
   - Apply the minimum fact gate: decide whether to ask for missing facts, build only a structural prototype, omit optional sections, or report a blocker for unsourced sensitive claims.
   - Stop or route elsewhere if the request is actually a single landing page, brand strategy, research-only benchmarking, or app feature work.

2. Inspect the existing implementation surface.
   - Find the current routes, layout, navigation, CMS or content files, styling system, component conventions, metadata setup, and asset locations.
   - Identify whether the site is static, CMS-backed, MDX/content-file driven, or app-routed.
   - Preserve the established framework and content workflow unless they block the corporate site goal.

3. Choose the corporate pattern and sitemap.
   - Pick the closest pattern from the pattern list and name the reason.
   - Define the top-level navigation, lower-page groups, footer sitemap, utility links, language/search needs, and CTA priorities.
   - Decide which stakeholder routes deserve first-level navigation and which belong in the footer or lower-page index.
   - Choose a style posture and decide where motion, rich media, or interactivity will clarify the site instead of merely decorating it.

4. Design the homepage as a hub.
   - Include the smallest credible subset of: hero, mission, business/service/brand overview, proof or numbers, news, trust/safety/sustainability/IR, careers, contact, and footer.
   - Make the first viewport reveal the company identity and direction immediately.
   - Use real assets or appropriate visual placeholders that signal the actual company, product, people, place, brand, or business domain.
   - Avoid marketing-only hero structures when visitors need company facts quickly.
   - Define hero media, section transitions, hover states, reveal timing, and interactive modules before styling individual sections.

5. Design lower pages and reusable content modules.
   - Build or revise company profile, leadership/message, mission/values, business/service, brand/project, news index, careers, IR, sustainability, and contact pages as needed.
   - Prefer reusable modules for news lists, brand cards, business cards, statistics, company profile tables, leadership cards, timeline/history, ESG index cards, report/download lists, policy link groups, contact categories, and footer sitemap columns.
   - Separate corporate news from brand/product news when the company has multiple brands or services.

6. Implement end to end.
   - Update routes, components, content files, styles, metadata, links, images, responsive behavior, and accessibility details.
   - Keep copy concise, factual, and specific to the company. Avoid generic filler such as "innovating for the future" unless supported by concrete proof.
   - Add links to existing external sites such as recruiting pages, product sites, owned media, online stores, IR libraries, SNS, or press kits when those are the authoritative destinations.
   - Make empty, draft, or unavailable sections explicit in code or content so the site does not pretend to have missing IR, ESG, news, or policy material.
   - Implement dynamic visuals with repository-native CSS, animation primitives, and component patterns before adding a new animation dependency.

7. Validate the corporate experience.
   - Open the implemented site or changed routes in a real browser when the repository can run locally; check at least the homepage, primary navigation, footer sitemap, and one representative lower page on desktop and mobile.
   - Check desktop and mobile layouts for the homepage, navigation, footer, and any changed lower pages.
   - Verify that all primary navigation, footer links, external links, language/search utilities, CTA buttons, and contact routes work or clearly point to intentional placeholders.
   - Check metadata, heading structure, page titles, descriptions, social previews when supported, and obvious SEO basics.
   - Check accessibility basics: semantic landmarks, keyboard navigation, focus states, alt text, contrast, and readable responsive typography.
   - Check text wrapping, media framing, sticky headers, mobile menus, card grids, tables, timelines, and footer columns for overlap or clipped content.
   - Check motion behavior, reduced-motion fallback, hover/focus states, mobile menu behavior, and media loading on real desktop and mobile viewports when dynamic visuals were added.
   - Run the repository's relevant lint, typecheck, tests, or build commands when available.

8. Hand off clearly.
   - Summarize the chosen corporate pattern, sitemap, key visitor routes, and trust elements.
   - List the pages or modules implemented or changed.
   - State what was validated and what remains content-dependent, compliance-dependent, or externally owned.
   - If IR, ESG, governance, safety, security, financial, legal, or policy claims were added from user-provided material, state that specialist review may still be needed before publication.

## Output Expectations

- A working corporate website change in the repository, or a concrete blocker report
- The chosen corporate site pattern and why it fits
- The sitemap, top navigation, footer sitemap, and key lower pages
- The visual style posture and any dynamic visual or motion choices
- The trust elements included, such as IR, sustainability, safety, security, governance, policies, awards, media, numbers, or reports
- Validation performed across real browser rendering, responsive layout, links, metadata, accessibility basics, and repository checks
- Any assumptions made for missing company copy, images, reports, policies, news, or external destinations

## Guardrails

- Do not collapse a corporate website into a single conversion landing page.
- Do not invent legal, financial, ESG, security, certification, customer, or performance claims.
- Do not invent core company facts. Ask, scaffold, omit, or block when the minimum facts are not available.
- Do not hide important stakeholder routes only inside body copy when they belong in navigation or the footer sitemap.
- Do not ship broken placeholder links for IR, careers, sustainability, press, contact, or policy pages without naming the gap.
- Do not make all companies follow the same structure; choose the pattern that matches business model, maturity, and accountability.
- Do not over-index on visual novelty when the site needs clarity, trust, and maintainable information architecture.
- Do not use scroll-jacking, constant movement, heavy background video, unreadable text-over-media, or animation that blocks navigation or content comprehension.
- Do not introduce a CMS, router, design system, or content platform migration unless the existing repo cannot support the requested site.
