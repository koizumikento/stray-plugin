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

## Site Structure Defaults

Default corporate sites usually start with Home, Company, Business, News, Careers, Contact, and Policies. Add IR, sustainability, governance, safety/security, press, reports, search, language switching, support, case studies, stores, apps, or owned media only when the company context justifies them.

Use `references/corporate-site-structure.md` when you need the full pattern list, sitemap, homepage model, folder structure, or content-growth rules.

## Minimum Fact Gate

Before implementing public-facing corporate content, confirm that the available inputs are enough to avoid inventing company facts:

- Minimum facts: company or organization name, what it does, primary audience or stakeholder groups, main business/service/brand areas, contact or next-step destination, and whether careers, IR, sustainability, safety/security, policy, or press routes should exist.
- If minimum facts are missing and cannot be inferred from repository content, ask concise questions before writing production copy.
- If the user wants a structural prototype despite missing facts, build clearly labeled content scaffolding and avoid factual claims, certifications, numbers, leadership names, reports, policy promises, or external destinations that were not provided.
- If the request needs legally sensitive claims, investor disclosures, ESG statements, safety/security assurances, financial results, hiring commitments, or regulated industry content that is not sourced, stop that part with a blocker note instead of fabricating it.
- If enough facts exist for the core site but not for optional sections, implement the core routes and mark optional sections as omitted, draft-only, or externally owned in the handoff.

## Framework And Content Defaults

Use a static-site-first framework for new corporate sites unless the existing repository already has a strong stack. Default new builds to Astro with TypeScript, static output, file-based routing, reusable `.astro` components, Astro Content Collections, Markdown/MDX body content, and TypeScript data modules for shared site data.

Keep an existing Next.js, Nuxt, Eleventy, SvelteKit, Vite, or other stack when it is already present and sufficient. Do not migrate a working existing site to Astro unless the user asks for a framework change or the current stack blocks the requested SSG/content workflow.

Do not add a CMS for this skill. If non-engineer editing is requested, first improve repository-versioned Markdown/MDX/YAML/JSON files, schemas, examples, and README notes. If the user explicitly requires live editing, approvals, preview drafts, or dashboard publishing, stop and report that this conflicts with the no-CMS default before changing architecture.

Use `references/astro-implementation.md` for Astro routes, layouts, content collections, metadata, MDX rendering, image imports, or client-side interactive components. Use `references/content-management.md` for content collection schemas, frontmatter fields, visibility rules, sort order, and TypeScript data modules.

## Asset Management Defaults

Manage assets as part of the site architecture, not as incidental files. Add only assets that are referenced by routes, content entries, metadata, or documented future placeholders.

Use `src/assets/` for images, logos, and icons imported by components or content-rendering code. Use `public/` only for stable public URLs such as favicons, OG images, PDFs, downloads, and externally referenced files.

Use `references/asset-management.md` for detailed placement, optimization, metadata, licensing notes, source-original handling, public document placement, audit guidance, and optional WebP derivative generation.

## Reference Material

When building a new Astro corporate site or deciding where content should live, use `references/corporate-site-structure.md` for:

- the default Astro folder structure
- the reference corporate sitemap and homepage structure
- rules for separating growing content in `src/content/` from shared fixed data in `src/data/`

Load this reference only when the task involves new site structure, content architecture, or a major corporate-site rebuild.

Use `references/content-management.md` when defining content collections, frontmatter fields, sort order, visibility rules, or TypeScript data modules. Load it only when the task involves content modeling, index pages, collection schemas, or repeated content.

Use `references/asset-management.md` when adding, reorganizing, auditing, or optimizing images, logos, icons, OG images, PDFs, videos, or downloads. Use `scripts/asset_audit.py` for deterministic asset audits and optional WebP derivative generation.

Use `references/astro-implementation.md` when creating or modifying Astro routes, content collections, dynamic pages, layouts, image imports, metadata, MDX rendering, or client-side interactive components.


## Visual Style And Motion Guidance

Name the site's style posture before styling: trust-first, mission-led, product-led, brand-led, enterprise/global, or culture-led.

Use real photography, product imagery, office/process visuals, generated bitmap visuals, data visuals, or subtle interactive scenes that reveal the company domain quickly. Keep IR, ESG, policy, safety, and security pages visually restrained and information-dense.

Use motion only when it clarifies hierarchy, transitions, comparison, or progressive disclosure. Design mobile navigation, sticky headers, carousels, mega menus, media-heavy heroes, reduced-motion behavior, keyboard access, and text-over-media readability explicitly.

## Workflow

1. Frame the corporate site brief.
   - Identify the company type, business model, maturity, listing status, markets, languages, and primary visitor groups.
   - Gather available company profile material, brand assets, services, product links, news sources, hiring links, IR/ESG materials, policies, and competitor or reference sites.
   - Apply the minimum fact gate: decide whether to ask for missing facts, build only a structural prototype, omit optional sections, or report a blocker for unsourced sensitive claims.
   - Stop or route elsewhere if the request is actually a single landing page, brand strategy, research-only benchmarking, or app feature work.

2. Inspect the existing implementation surface.
   - Find the current routes, layout, navigation, content files, styling system, component conventions, metadata setup, and asset locations.
   - Identify whether the site is static, MDX/content-file driven, app-routed, or tied to a CMS that should be left alone rather than expanded.
   - Preserve the established framework and content workflow unless they block the corporate site goal.
   - For new builds without an established framework, choose Astro, load the Astro implementation reference, and define the file-based content model before designing pages.

3. Choose the corporate pattern and sitemap.
   - Pick the closest pattern from the pattern list and name the reason.
   - Start from the reference corporate site structure, then remove irrelevant routes and add justified trust routes.
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
   - Apply the content growth rules before deciding whether each item belongs in `src/content/`, `src/data/`, or a component prop.
   - Prefer reusable modules for news lists, brand cards, business cards, statistics, company profile tables, leadership cards, timeline/history, ESG index cards, report/download lists, policy link groups, contact categories, and footer sitemap columns.
   - Separate corporate news from brand/product news when the company has multiple brands or services.

6. Implement end to end.
   - Update routes, components, content files, styles, metadata, links, images, responsive behavior, and accessibility details.
   - For new Astro builds, follow the reference Astro structure unless the existing repository convention is clearer.
   - For Astro builds, define content collections, YAML frontmatter schemas, sort rules, visibility rules, and typed data modules before duplicating page data inside components.
   - When adding assets, place them according to the asset management defaults, optimize web-facing images, and keep source originals separate from shipped asset folders.
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
   - Run the asset audit script when images, PDFs, downloads, videos, or source-like assets were added or reorganized.
   - Run the repository's relevant lint, typecheck, tests, or build commands when available.

8. Hand off clearly.
   - Summarize the chosen corporate pattern, sitemap, key visitor routes, and trust elements.
   - List the pages or modules implemented or changed.
   - State what was validated and what remains content-dependent, compliance-dependent, or externally owned.
   - If IR, ESG, governance, safety, security, financial, legal, or policy claims were added from user-provided material, state that specialist review may still be needed before publication.

## Output Expectations

- A working corporate website change in the repository, or a concrete blocker report
- The framework choice, including whether Astro was used by default or an existing stack was preserved
- The file-based content model used for company facts, pages, news, navigation, and repeated modules
- The route and folder structure used, especially where growing content and shared data live
- The chosen corporate site pattern and why it fits
- The sitemap, top navigation, footer sitemap, and key lower pages
- The visual style posture and any dynamic visual or motion choices
- The trust elements included, such as IR, sustainability, safety, security, governance, policies, awards, media, numbers, or reports
- Asset handling performed, including optimization, public document placement, alt text assumptions, and any unusually large assets
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
- Do not introduce a CMS. Use repository-versioned content files and schemas instead.
- Do not introduce a router, design system, or content platform migration unless the existing repo cannot support the requested site.
