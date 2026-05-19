# Asset Management Reference

Use this reference when adding, reorganizing, auditing, or optimizing assets for a CMS-free corporate site.

## Storage Rules

- Use `src/assets/images/` for imported page images that benefit from Astro image handling, responsive variants, or build-time optimization.
- Use `src/assets/logos/` for brand marks that are imported by components.
- Use `src/assets/icons/` for custom icons that are imported by components. Prefer existing icon libraries when available.
- Use `public/og/` for stable public Open Graph images.
- Use `public/documents/` for public PDFs, reports, press kits, and downloads that need stable URLs.
- Use `public/` for files that must be referenced by an external service, metadata tag, or stable absolute URL.

## Optimization Guidance

Optimize assets for web delivery before committing them. Keep small, web-ready derivatives in shipped asset folders, and keep source originals outside shipped folders unless they are explicitly required.

Size targets are guidance, not hard limits:

- Hero and large section images: prefer AVIF or WebP, usually under 300-500 KB when quality allows.
- Card images and thumbnails: usually under 100-200 KB.
- Logos and icons: prefer SVG when appropriate, or optimized PNG/WebP.
- PDFs: include only public final documents; compress when reasonable.
- Videos: prefer external hosting or compressed short clips; confirm before committing large video files.
- Source originals: keep RAW photos, PSD, AI, Figma exports, and uncompressed archives outside shipped asset folders unless explicitly needed.

## Metadata Rules

- Every meaningful image needs alt text at the usage site or in content frontmatter.
- Decorative images should use empty alt text and not repeat nearby text.
- Store captions, credits, and source notes in content frontmatter when they are content-specific.
- Do not invent photo credits, licensing, awards, certifications, or customer logos.

## Content References

For Markdown/MDX entries, reference images in frontmatter when they are part of cards, previews, or page heroes:

```yaml
---
title: "Example news"
date: "2026-05-19"
image: "../assets/news/example.webp"
imageAlt: "Team presenting the new service"
---
```

Use stable `public/` URLs for PDFs and downloads:

```yaml
---
title: "Sustainability Report 2026"
date: "2026-05-19"
file: "/documents/sustainability-report-2026.pdf"
---
```

## Asset Audit Script

Use `scripts/asset_audit.py` to find oversized or risky assets. The default mode is read-only:

```bash
python plugins/stray-studio/skills/corporate-site-builder/scripts/asset_audit.py --project-root .
```

To write optimized WebP derivatives without overwriting sources, run with Pillow:

```bash
uv run --with pillow python plugins/stray-studio/skills/corporate-site-builder/scripts/asset_audit.py --project-root . --optimize-dir tmp/optimized-assets
```

Review generated derivatives before replacing any committed assets.

## Guardrails

- Do not overwrite source assets automatically.
- Do not commit large source originals just because they were provided.
- Do not add unused asset dumps to the repository.
- Do not use blurred, dark, cropped, or purely atmospheric images when visitors need to understand the real company, product, people, place, or business.
- Do not let images or videos break responsive layout, text readability, or Core Web Vitals without naming the tradeoff.
