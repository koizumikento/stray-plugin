# Content Management Reference

Use this reference for CMS-free corporate sites built from repository-versioned content files. The default model is Markdown/MDX with YAML frontmatter for body content, plus TypeScript modules for shared structured site data.

## Storage Model

Use Markdown or MDX with YAML frontmatter for entries that have body text, slugs, dates, categories, archive behavior, or index pages:

- `src/content/news/*.md`
- `src/content/business/*.md`
- `src/content/careers/*.md`
- `src/content/reports/*.md`
- `src/content/policies/*.md`
- `src/content/events/*.md`
- `src/content/insights/*.md`

Use TypeScript data modules for shared structured data that is reused across pages:

- `src/data/navigation.ts`
- `src/data/footer.ts`
- `src/data/company.ts`
- `src/data/contact.ts`
- `src/data/metrics.ts`
- `src/data/social.ts`
- `src/data/cta.ts`

Use JSON only for generated, imported, or machine-readable data that should not be hand-edited often.

## Frontmatter Rules

Keep frontmatter explicit and schema-validated with Astro Content Collections.

- Use quoted ISO date strings such as `"2026-05-19"`.
- Use `draft` to hide unfinished content from production indexes.
- Use `archived` to keep content addressable but remove it from normal lists when appropriate.
- Use `order` for intentional editorial or navigation order.
- Use `date`, `publishDate`, `updatedAt`, or type-specific dates such as `eventDate` when chronology matters.
- Use `priority` or `featured` only for limited promotion slots, not as a substitute for a clear primary sort.
- Do not infer display order from filenames except as a final stable fallback.

Common fields:

```yaml
---
title: "Example title"
description: "Short summary for index cards and metadata."
date: "2026-05-19"
updatedAt: "2026-05-19"
order: 10
priority: 0
featured: false
draft: false
archived: false
---
```

## Sorting Rules

Define a sorting rule for every repeatable collection before rendering index pages:

- News, press releases, announcements: `date` descending, then `priority` descending, then `title` or slug ascending.
- Reports, whitepapers, resources: `date` descending, then `title` ascending.
- Business, services, products, brands: `order` ascending, then `title` ascending.
- Case studies and projects: `featured` first when needed, then `date` descending or `order` ascending based on the page goal.
- Careers roles: `order` ascending or `updatedAt` descending, then `title` ascending; hide `closed` roles from current-opening lists.
- Careers articles and interviews: `date` descending, then `title` ascending.
- Events and seminars: upcoming items by `eventDate` ascending; past items by `eventDate` descending.
- Policies: `order` ascending, then `title` ascending; show `updatedAt` visibly when relevant.
- FAQ: `categoryOrder` ascending, then `order` ascending, then `title` ascending.
- People or leadership: `order` ascending, then `name` ascending.
- Navigation and footer groups: TypeScript array order is the display order.

Always filter out `draft: true` from production indexes unless the user explicitly asks for draft previews.

## Collection Examples

News:

```md
---
title: "New service launched"
description: "A concise summary for the news index."
date: "2026-05-19"
category: "press"
tags:
  - product
featured: false
priority: 0
draft: false
archived: false
---

News body...
```

Business detail:

```md
---
title: "Consulting"
summary: "Support for business transformation."
order: 10
featured: true
draft: false
---

Business detail body...
```

Report metadata with a static PDF:

```md
---
title: "Sustainability Report 2026"
description: "Annual sustainability report."
date: "2026-05-19"
type: "sustainability"
file: "/documents/sustainability-report-2026.pdf"
draft: false
---

Optional summary body...
```

## TypeScript Data Rules

Use TypeScript modules when data is compact, reused, and mostly fixed:

```ts
export const navigation = [
  { label: "Company", href: "/company/" },
  { label: "Business", href: "/business/" },
  { label: "News", href: "/news/" },
  { label: "Careers", href: "/careers/" },
  { label: "Contact", href: "/contact/" },
];
```

Prefer `as const` or exported TypeScript types when the data shape is shared across components. Keep display order in array order for navigation, footer groups, CTA groups, and manually curated homepage modules.

## Guardrails

- Do not add a CMS, admin UI, content API, preview workflow, or authentication flow.
- Do not put repeated content entries directly inside page components.
- Do not mix body-heavy content into TypeScript modules.
- Do not put navigation, footer, or company-wide configuration in Markdown just because it is content.
- Do not rely on filesystem order, glob order, or filenames for business-critical display order.
