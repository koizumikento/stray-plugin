# Astro Implementation Reference

Use this reference when creating or modifying Astro routes, content collections, dynamic pages, layouts, image imports, metadata, MDX rendering, or client-side interactive components for a corporate site.

Sources used when drafting this reference:

- Astro project structure: https://docs.astro.build/en/basics/project-structure/
- Astro routing: https://docs.astro.build/en/guides/routing/
- Astro routing reference: https://docs.astro.build/en/reference/routing-reference/
- Astro content collections: https://docs.astro.build/en/guides/content-collections/
- Astro components: https://docs.astro.build/en/basics/astro-components/
- Astro layouts: https://docs.astro.build/en/basics/layouts/
- Astro assets: https://docs.astro.build/en/reference/modules/astro-assets/
- Astro MDX integration: https://docs.astro.build/en/guides/integrations-guide/mdx/
- Astro template directives: https://docs.astro.build/en/reference/directives-reference/
- Astro CLI commands: https://docs.astro.build/en/reference/cli-reference/
- Astro configuration: https://docs.astro.build/en/reference/configuration-reference/
- Vite+ getting started and `vp` commands: https://viteplus.dev/guide/
- Vite+ check: https://viteplus.dev/guide/check
- Vite+ test: https://viteplus.dev/guide/test
- Vite+ build: https://viteplus.dev/guide/build
- Vite+ run and package scripts: https://viteplus.dev/guide/run

## Defaults

- Use Astro with TypeScript for new corporate sites unless the repository already has a strong framework.
- Keep `output: 'static'`, which is Astro's default. Do not add an adapter, SSR, server actions, sessions, or on-demand routes unless the user explicitly needs server-rendered behavior.
- Use `.astro` components first. Add React, Vue, Svelte, or another UI framework only when the repository already uses it or a specific interactive element justifies it.
- Use ordinary `<a>` elements for internal navigation. Astro does not require a framework-specific Link component.
- Use `astro.config.mjs` for configuration unless the existing project uses another supported Astro config format.

## Project Structure

Astro treats `src/pages/` as the required routing directory. Other directories are conventions, but use the corporate-site reference structure for new sites.

- `src/pages/`: route files. `.astro`, `.md`, and `.mdx` files here become routes.
- `src/content.config.ts`: content collection definitions and schemas.
- `src/content/`: Markdown/MDX content collection entries.
- `src/data/`: typed shared data modules, not route files.
- `src/components/`: reusable `.astro` or framework components.
- `src/layouts/`: page shells with `<slot />`.
- `src/assets/`: images and other source assets processed by Astro.
- `public/`: static assets copied untouched to the output.

Keep CSS and JavaScript authored for the site in `src/`, not `public/`, unless a stable unprocessed public URL is required.

## Routes

Use static route files for durable corporate pages:

- `src/pages/index.astro` -> `/`
- `src/pages/company/index.astro` -> `/company/`
- `src/pages/contact/index.astro` -> `/contact/`
- `src/pages/policies/privacy.astro` -> `/policies/privacy/`

Use dynamic routes for collection-backed pages:

- `src/pages/news/[slug].astro`
- `src/pages/business/[slug].astro`
- `src/pages/reports/[slug].astro`

In static output, every dynamic route must export `getStaticPaths()`. Return only string params, and pass the entry through `props` so the template does not re-query unnecessarily.

```astro
---
import { getCollection, render } from 'astro:content';

export async function getStaticPaths() {
  const entries = await getCollection('news', ({ data }) => !data.draft);

  return entries.map((entry) => ({
    params: { slug: entry.id },
    props: { entry },
  }));
}

const { entry } = Astro.props;
const { Content } = await render(entry);
---

<h1>{entry.data.title}</h1>
<Content />
```

Use `Astro.params` for route parameters only when needed inside the template. Prefer `Astro.props` for data passed from `getStaticPaths()`.

## Content Collections

Define collections in `src/content.config.ts` using `defineCollection()`, `glob()`, and `z` from `astro/zod`.

```ts
import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';

const news = defineCollection({
  loader: glob({ pattern: '**/*.{md,mdx}', base: './src/content/news' }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    date: z.coerce.date(),
    updatedAt: z.coerce.date().optional(),
    category: z.string().optional(),
    tags: z.array(z.string()).default([]),
    featured: z.boolean().default(false),
    priority: z.number().default(0),
    draft: z.boolean().default(false),
    archived: z.boolean().default(false),
  }),
});

export const collections = { news };
```

Use schemas for every corporate collection. They are optional in Astro, but required for this skill's CMS-free content workflow because they prevent silent frontmatter drift.

Query collection entries with `getCollection()` for lists and `getEntry()` for a specific entry. Always sort collection results explicitly before rendering an index.

```ts
const news = (await getCollection('news', ({ data }) => !data.draft && !data.archived))
  .sort((a, b) => b.data.date.valueOf() - a.data.date.valueOf()
    || b.data.priority - a.data.priority
    || a.data.title.localeCompare(b.data.title));
```

Render Markdown/MDX body content with `render(entry)`:

```astro
---
import { render } from 'astro:content';
const { entry } = Astro.props;
const { Content } = await render(entry);
---

<Content />
```

## Components And Layouts

Astro components render to HTML by default and do not ship client JavaScript unless needed.

Use TypeScript props for reusable components:

```astro
---
interface Props {
  title: string;
  description?: string;
}

const { title, description } = Astro.props;
---

<section>
  <h2>{title}</h2>
  {description && <p>{description}</p>}
</section>
```

Use layouts for page shells, metadata, navigation, footer, and shared slots:

```astro
---
interface Props {
  title: string;
  description?: string;
}

const { title, description } = Astro.props;
---

<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <title>{title}</title>
    {description && <meta name="description" content={description} />}
  </head>
  <body>
    <slot />
  </body>
</html>
```

## MDX

Use Markdown (`.md`) by default. Use MDX (`.mdx`) only when the content body needs components, JSX expressions, or richer inline structures.

If MDX is needed, add the official MDX integration:

```ts
import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';

export default defineConfig({
  integrations: [mdx()],
});
```

MDX supports frontmatter. When using UI framework components in MDX, add the appropriate `client:*` directive only when the component must be interactive.

## Images And Assets

Use `astro:assets` for local images imported from `src/assets/`.

```astro
---
import { Image } from 'astro:assets';
import heroImage from '../assets/images/hero.webp';
---

<Image src={heroImage} alt="Team working in the company office" />
```

Use stable public URLs for files in `public/`, such as PDFs and OG images:

```astro
<meta property="og:image" content="/og/default.png" />
<a href="/documents/company-profile.pdf">Company profile</a>
```

For `<Image />`, provide meaningful `alt` text. If an image is decorative, use `alt=""`.

## Client Interactivity

Keep corporate pages static by default. Use client directives only for UI framework components that need browser-side interactivity:

- `client:load`: immediately visible, high-priority interactive UI.
- `client:idle`: lower-priority interactive UI that can wait.
- `client:visible`: components below the fold, carousels, counters, or heavy interactive modules.
- `client:media`: interactive UI needed only for matching media queries.
- `client:only`: only when the component cannot render on the server.

Do not hydrate static cards, headings, links, tables, or simple content sections.

## Metadata

Define page metadata at the route level and pass it into layouts. For content-backed pages, derive title and description from collection schema fields.

Minimum metadata for corporate pages:

- `<title>`
- meta description
- canonical URL when the site URL is known
- Open Graph title, description, image, and type when supported
- page language via `<html lang="...">`

Do not invent social preview images or claims. Use `public/og/` for stable OG images.

## Validation

Prefer repository scripts and the repository's existing package manager or command wrapper. Do not assume `npm`.

- If the user specifies `vp`, or the repository documents or uses Vite+, use `vp` before falling back to package-manager scripts.
- Vite+ ships `vp` as the global CLI and `vite-plus` as the local project package.
- `vp dev`, `vp check`, `vp test`, `vp build`, and `vp preview` are built-in Vite+ commands.
- `vp check` is the preferred static check when available; it runs formatting, linting, and type checks together when configured.
- `vp test` runs the Vite+ test runner built on Vitest. It does not stay in watch mode by default; use `vp test watch` when watch mode is desired.
- `vp build` runs the built-in Vite production build. If a project has a custom `build` script that must be used instead, run it through `vp run build`.
- `vp run <script>` runs package scripts or configured Vite Task tasks. Use this when the intended command is a `package.json` script rather than a Vite+ built-in.
- `vp install`, `vp add`, and `vp remove` delegate through the project's package manager, so do not switch to raw package-manager commands unless the repository expects that.
- `pnpm-lock.yaml` -> use `pnpm`
- `bun.lock` or `bun.lockb` -> use `bun`
- `yarn.lock` -> use `yarn`
- `package-lock.json` -> use `npm`

Common command choices are:

```bash
vp dev
vp check
vp test
vp build
vp preview

# When intentionally running package.json scripts instead of Vite+ built-ins:
vp run <script>

# Package-manager fallback only when Vite+ is not in use:
<pm> run <script>
<pm> exec astro check
```

Use the exact script names in `package.json` when they differ. If there is no script and Vite+ is not in use, use the package manager's local binary runner rather than a global Astro install. `astro build` generates static files in `dist/` by default. `astro preview` serves the built output locally. `astro check` validates Astro and TypeScript diagnostics when configured.

Before handoff, validate:

- dynamic routes generated from content collections
- explicit collection sorting
- draft/archived filtering
- metadata and page titles
- image rendering and alt text
- static build output
- preview rendering for homepage, navigation, footer, and one representative detail route
