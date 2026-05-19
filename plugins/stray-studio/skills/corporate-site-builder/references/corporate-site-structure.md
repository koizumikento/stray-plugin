# Corporate Site Structure Reference

Use this reference for new Astro corporate sites, clean rebuilds, or major content-architecture decisions. Preserve an existing repository convention when it is already clear and sufficient.

## Astro Folder Structure

```text
src/
  pages/
    index.astro
    company/index.astro
    business/index.astro
    business/[slug].astro
    news/index.astro
    news/[slug].astro
    careers/index.astro
    contact/index.astro
    policies/privacy.astro
    policies/terms.astro
  content/
    news/
    business/
    careers/
    reports/
  data/
    site.ts
    navigation.ts
    footer.ts
    company.ts
    contact.ts
    metrics.ts
    social.ts
  content.config.ts
  layouts/
    BaseLayout.astro
    CorporateLayout.astro
    ArticleLayout.astro
  components/
    global/
    sections/
    cards/
    ui/
  styles/
    global.css
    tokens.css
  assets/
    images/
    logos/
    icons/
public/
  favicon.svg
  og/
  documents/
```

Use the folders with these boundaries:

- `src/pages/`: URL routes and page composition only. Do not hide repeated content data inside page files.
- `src/content/`: repeatable, article-like, slugged, filterable, or archiveable content.
- `src/data/`: compact structured data reused across pages, such as navigation, footer, company profile facts, contact destinations, metrics, and social links.
- `src/layouts/`: page frames, metadata shells, article layouts, and corporate-wide wrappers.
- `src/components/global/`: sitewide components such as header, footer, mobile navigation, and SEO helpers.
- `src/components/sections/`: corporate page sections such as hero, mission, business overview, news list, trust links, careers banner, and contact CTA.
- `src/components/cards/`: repeated display units such as business cards, news cards, metric cards, link cards, people cards, and report cards.
- `src/components/ui/`: small primitives such as buttons, containers, tabs, accordions, badges, and section headings.
- `public/documents/`: static PDFs and downloads that should be linked from content or data files.
- For detailed image, logo, OG image, PDF, video, and optimization rules, use `asset-management.md`.

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

## Corporate Sitemap

Start from this sitemap for a normal corporate site, then remove or add routes based on the company context:

- Home `/`: company identity, what the company does, primary routes, trust signals, latest news, careers/contact entry points, and footer sitemap.
- Company `/company/`: company overview, mission, values, representative message, profile table, history, leadership, offices, and access.
- Business `/business/`: business, service, product, brand, or project index.
- Business detail `/business/[slug]/`: individual business/service/brand detail pages generated from content.
- News `/news/`: news, press releases, announcements, media coverage, or corporate updates.
- News detail `/news/[slug]/`: individual news items generated from content.
- Careers `/careers/`: recruiting message, culture, roles or external ATS links, work style, benefits, and hiring FAQ.
- Contact `/contact/`: inquiry categories, form or external contact destination, sales/press/recruiting routing, and office/contact details.
- Policies `/policies/...`: privacy policy, terms, accessibility, security, data, AI, or compliance policy pages.
- Optional trust routes: `/sustainability/`, `/ir/`, `/governance/`, `/security/`, `/press/`, or `/reports/` only when the company context justifies them.

Treat the homepage as a hub, not as a full substitute for durable lower pages. A default homepage should include:

- Hero: company name, concise business definition, primary CTA, and domain-relevant visual.
- Mission or purpose: the issue the company addresses and why it exists.
- Business overview: summary cards that route to business/service/brand details.
- Proof or trust: numbers, facts, awards, reports, policies, customers, or other sourced trust elements.
- News: latest items from the news collection.
- Careers or culture: recruiting route when relevant.
- Contact CTA: clear next step for customers, partners, press, candidates, or investors.
- Footer sitemap: complete corporate navigation, policies, external destinations, and company basics.

## Content Growth Rules

Separate content that can grow from shared fixed data before implementation:

- Put content in `src/content/` when it may grow, needs a slug, has body text, appears in an index, needs filtering, or may be archived.
- Put content in `src/data/` when it is small, shared, mostly fixed, and used to render navigation, cards, tables, CTAs, metadata, or sitewide facts.
- Do not hardcode repeatable company facts, news items, business entries, policy links, report links, or footer links directly inside page components.
- For frontmatter fields, sort order, visibility rules, and TypeScript data conventions, use `content-management.md`.

Use `src/content/` collections for content that can accumulate over time:

- News, press releases, announcements, and media coverage
- Business, service, product, brand, project, or case-study detail pages
- Careers articles, interview posts, role pages, recruiting updates, and hiring FAQ entries
- Sustainability, ESG, governance, security, transparency, annual, or integrated reports
- Events, seminars, webinars, talks, and media appearances
- Blog, insights, columns, research notes, and owned media articles
- Downloadable resources, whitepapers, decks, PDFs, press kits, and report metadata
- Policy pages when version history or multiple policy documents matter

Use `src/data/` for compact shared information:

- Site metadata and default SEO values
- Header navigation and mobile navigation
- Footer sitemap and external destinations
- Company profile facts, office locations, and access summaries
- Contact destinations and inquiry category definitions
- Social links, owned media links, product links, app links, and store links
- Business category summaries used on the homepage and index pages
- Trust metrics, CTA labels, report links, and policy link groups
