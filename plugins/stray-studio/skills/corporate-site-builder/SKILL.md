---
name: "corporate-site-builder"
description: "Use when building or revising a static, repository-managed corporate information site. Route live CMS/editorial app flows to fullstack-app-builder and single-offer pages to landing-page-builder."
---

# Corporate Site Builder

Create or improve a corporate website that explains who the company is, what it does, why it is trustworthy, and where each visitor should go next. Treat the site as a durable company information system, not a one-page campaign asset.

## Do Not Use For

- single-offer landing pages that should use `landing-page-builder`
- broad brand identity work without site implementation
- research-only benchmarking or inspiration gathering
- full product application flows, dashboards, auth, or data-backed user workflows
- live CMS editing, editorial approvals, preview dashboards, authenticated publishing, or other content-platform workflows; use `fullstack-app-builder`
- one-off visual restyling of an existing artifact without changing corporate structure
- investor relations, ESG, or legal content authoring that requires specialist compliance review

## Site Defaults

Start with the company's visitor groups and durable lower pages, not only a dramatic homepage. Home, Company, Business, News, Careers, Contact, and Policies are a starting point; add IR, sustainability, governance, safety/security, press, reports, search, languages, support, case studies, stores, or media only when justified. Put proof near claims and stakeholder routes where visitors expect them, including a full footer sitemap.

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

Do not add a CMS for this skill. If non-engineer editing is requested, first improve repository-versioned Markdown/MDX/YAML/JSON files, schemas, examples, and README notes. If live editing, approvals, preview drafts, or dashboard publishing are required, hand the app workflow to `fullstack-app-builder` in the same task. Do not silently add a CMS under this skill or migrate an existing site.

## Asset Management Defaults

Manage assets as part of the site architecture, not as incidental files. Add only assets that are referenced by routes, content entries, metadata, or documented future placeholders.

Use `src/assets/` for images, logos, and icons imported by components or content-rendering code. Use `public/` only for stable public URLs such as favicons, OG images, PDFs, downloads, and externally referenced files.

## Reference Selection

Read only the material needed for the requested change:

| Decision | Reference |
|---|---|
| New site structure, content architecture, or major rebuild; sitemap/homepage patterns and growing content versus fixed data | `references/corporate-site-structure.md` |
| Collections, frontmatter schemas, sorting, visibility, indexes, or shared data | `references/content-management.md` |
| Asset placement, licensing, optimization, source originals, public downloads, or deterministic audit | `references/asset-management.md`; use `scripts/asset_audit.py` for audits or optional WebP derivatives |
| Astro routes, layouts, dynamic pages, collections, metadata, MDX, image imports, or client interactivity | `references/astro-implementation.md` |

## Visual Style And Motion Guidance

Name the site's style posture before styling: trust-first, mission-led, product-led, brand-led, enterprise/global, or culture-led.

Use real photography, product imagery, office/process visuals, generated bitmap visuals, data visuals, or subtle interactive scenes that reveal the company domain quickly. Keep IR, ESG, policy, safety, and security pages visually restrained and information-dense.

Use motion only when it clarifies hierarchy, transitions, comparison, or progressive disclosure. Design mobile navigation, sticky headers, carousels, mega menus, media-heavy heroes, reduced-motion behavior, keyboard access, and text-over-media readability explicitly.

## Workflow

1. Frame the requested change using available company facts, business model, maturity, listing status, markets, languages, visitor groups, and source assets. Apply the Minimum Fact Gate; implement supported core routes while identifying omitted, draft, or externally owned sections. Route non-corporate work to its owner.
2. Inspect affected routes, layout/navigation, content, styles, metadata, assets, and repository guidance. Preserve the existing stack and content workflow; for a new site, apply the static Astro defaults and relevant references.
3. Choose the corporate pattern, sitemap, CTA priorities, navigation, footer, and justified stakeholder/utility routes. Define a style posture and homepage hub with the smallest credible set of identity, mission, business, proof, news, trust, careers, and contact elements. The first viewport must make the company and its direction clear.
4. Implement the affected pages and reusable modules end to end. Model growing content separately from shared data, define applicable schemas/sort/visibility rules, and separate corporate from brand/product news where needed. Use authoritative supplied external destinations. Optimize shipped assets, preserve source originals separately, and mark empty/draft/unavailable material honestly. Prefer repository-native CSS and components before new motion dependencies.
5. Validate the experience on the relevant surface.
   - When the site runs locally, inspect the homepage, primary navigation, footer, and a representative affected lower page in a real browser at desktop and mobile widths. Check wrapping, media framing, menus, sticky headers, cards, tables, timelines, and columns for clipping or overlap.
   - Verify navigation, external links, language/search utilities, CTAs, and contacts; identify any intentional placeholder rather than treating it as working.
   - Check page titles/descriptions, social metadata where supported, heading structure, semantic landmarks, keyboard/focus behavior, alt text, contrast, and typography.
   - For dynamic changes, verify motion and reduced-motion states, hover/focus behavior, media loading, and mobile stability. Run the asset audit for added/reorganized images, PDFs, downloads, video, or source-like assets.
   - Run the repository checks relevant to the change; distinguish rendered behavior from build success and unverified surfaces.
6. Fix confirmed in-scope defects and rerun the affected check. Reassess stalled hypotheses rather than repeating unchanged failures. Continue while evidence supports progress; stop only a blocked action and continue independent authorized work. Completion requires working requested routes and resolved required checks and findings.
7. Report the working routes, pattern, sitemap, framework/content choices, visual and asset decisions, validation evidence, and missing content or external dependencies. Identify sourced IR/ESG, financial, safety/security, legal, or policy material that still needs specialist review before publication.

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
