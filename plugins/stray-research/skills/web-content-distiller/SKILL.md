---
name: "web-content-distiller"
description: "Use when the user provides a web page or URL and wants clean, analysis-ready content with clutter removed while preserving the important structure. Do not use for generic browsing, domain research, or package-manager installation tasks."
---

# Web Content Distiller

Extract the useful substance from a web page and strip away navigation, ads, chrome, and other noise. The goal is a clean reading or analysis input, not a summary, not interpretation, and not a general web browsing workflow.

Use this skill when the user wants to convert a page into something that is easier to read, quote, compare, or feed into later analysis.

## Do Not Use For

- domain synthesis or factual research across multiple sources
- generic browsing or answering questions about the web page itself
- installation or setup workflows for CLI tools
- rewriting the page into a new article or summary
- full-site scraping or crawling

## Workflow

1. Identify the source and the target shape.
   - Confirm the URL, local file, or pasted HTML/text.
   - Confirm whether the output should preserve headings, lists, tables, code blocks, or links.
   - Stop if the user really wants a summary instead of extracted content.

2. Choose the lightest extraction path that preserves structure.
   - Prefer browser or CLI extraction when a page is live and readable.
   - Prefer direct text or HTML parsing when the user already has the source locally.
   - Fall back to manual cleanup only when automatic extraction loses essential content.

3. Remove clutter without losing meaning.
   - Strip navigation, cookie banners, footer boilerplate, repeated menus, and sidebar noise.
   - Keep the main article, document body, code samples, tables, captions, and meaningful link text.
   - Preserve headings and section order whenever they help downstream analysis.

4. Verify the extraction.
   - Check that the result still contains the page's core claim or topic.
   - Check that tables, lists, or code blocks were not flattened into unreadable prose.
   - If the output is missing critical structure, retry with a different extraction path.

5. Produce the distilled artifact.
   - Return clean markdown or text unless the user asked for another format.
   - Keep labels or short notes only when they help the reader understand the structure.
   - Avoid commentary about the page unless the user asked for analysis.

## Output Expectations

- A clean, readable extraction of the page content
- Preserved structure for headings, lists, tables, and code where possible
- Minimal extraneous markup or page chrome
- A short note about the extraction path when it materially affects fidelity
- A short note when structure had to be approximated or reconstructed

## Guardrails

- Do not summarize unless asked.
- Do not infer missing meaning from removed text.
- Do not broaden into research, fact-checking, or opinion.
- Do not add installation instructions for external tools unless the user asked for setup help.
- When extraction quality is poor, say what was lost and why instead of pretending the result is exact.
