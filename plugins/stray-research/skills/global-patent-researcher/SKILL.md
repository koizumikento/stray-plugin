---
name: "global-patent-researcher"
description: "Use when the user wants to plan or conduct a global patent research workflow using current public web patent databases, including prior-art, novelty, invalidity-candidate, freedom-to-operate precheck, or patent landscape research, while protecting confidential invention details before external searches. Do not use for legal opinions, patent drafting, filing strategy, API integration, or Japan-only patent searches."
compatibility: "Requires internet access and a browsing-capable Codex environment because this skill relies on current public patent databases and source-backed verification."
---

# Global Patent Researcher

Plan and run public-web patent research across current global patent databases. Help the user define the search question, build search strategies, inspect candidate patent documents, and report findings with links, search logs, search dates, and uncertainty. Treat Japan as a supplemental jurisdiction unless the user explicitly asks for deeper Japanese patent work.

Use this skill when the user needs:

- global prior-art or novelty research before writing, filing, or investing in an invention
- invalidity-candidate research against one or more claims
- freedom-to-operate precheck to identify patents or applications that need professional review
- patent landscape research for a technology area, competitor set, or trend
- search strings, CPC/IPC classification candidates, synonym sets, or a reproducible patent-search log

## Do Not Use For

- legal advice, patentability opinions, infringement opinions, clearance opinions, or validity opinions
- drafting patent claims or preparing filing strategy
- Japan-only searches that require detailed J-PlatPat, FI, or F-term work as the primary task
- API integration, scraping, bulk data pipelines, or paid database automation
- trademark, design, copyright, licensing, or contract research unless only incidental to a patent question
- conclusively determining whether an invention is new, non-obvious, valid, invalid, infringed, or free to operate

## Preferred Sources

- Espacenet for broad worldwide patent search, patent families, classifications, citations, and legal-status leads.
- PATENTSCOPE for PCT publications, international collections, cross-lingual search, and multilingual query expansion.
- Google Patents for fast keyword, CPC, assignee, inventor, claims, and non-patent-literature discovery.
- The Lens when patent-scholar links, collection management, or broader patent analytics are useful.
- USPTO Patent Public Search when the research specifically needs U.S. patent text or U.S. search syntax.
- J-PlatPat only as a supplemental source for Japanese documents, Japanese applicants, Japanese legal-status checks, or FI/F-term exploration.

## Workflow

1. Classify the research type before searching.
   - prior-art or novelty research: focus on disclosures before the relevant date
   - invalidity-candidate research: map candidate references to the target claim elements and priority date
   - freedom-to-operate precheck: focus on active or pending rights in the target jurisdictions and current claims
   - landscape research: focus on classification, assignee, filing-year, citation, family, and jurisdiction patterns
2. Protect confidential information before using external tools.
   - ask for confirmation before putting unpublished invention details, client names, non-public target claims, or sensitive product plans into external websites
   - if the user has not cleared external disclosure, work from abstracted technical features, generic terminology, or locally provided public patent numbers only
   - remind the user that public web databases and search engines may log queries or expose search terms to third parties
3. Decompose the invention or target patent.
   - identify core technical features, optional features, use cases, problem statements, effects, materials, components, and process steps
   - separate must-have claim elements from contextual details
   - capture the relevant dates, jurisdictions, assignees, inventors, and known document numbers
4. Build the search strategy.
   - create English-first keyword sets with synonyms, spelling variants, abbreviations, broader terms, narrower terms, and functional equivalents
   - identify CPC and IPC candidates from seed documents and classification search
   - add assignee, inventor, citation, patent-family, priority-date, and jurisdiction constraints only when they improve precision
   - include Japanese keywords or J-PlatPat classification checks only when Japanese coverage is materially relevant, for example when the applicant or inventors are Japanese, Japan is a target filing or FTO jurisdiction, or the technology area is known to have dense Japanese filings
5. Search iteratively across public databases.
   - browse current public databases during the task; do not rely on remembered patent data or stale cached results
   - start broad in Espacenet, PATENTSCOPE, or Google Patents to find seed documents and terminology
   - use the best seed documents to discover classifications, citations, families, and alternative wording
   - rerun refined searches with classification plus keyword combinations
   - check at least two major sources when the result affects a user decision
6. Review candidate documents.
   - inspect title, abstract, independent claims, drawings, description passages, priority data, assignee, family, citations, and legal-status indicators as relevant
   - for invalidity and FTO prechecks, compare candidate claims or disclosures element by element against the target features
   - distinguish applications from granted patents and note when claims may have changed
7. Maintain a reproducible search log.
   - record the search date, database, query, filters, classification codes, hit counts when useful, and reason for each refinement
   - preserve links to important documents and explain why each document was included or rejected
8. Synthesize cautiously.
   - lead with the strongest candidate documents or strongest landscape signals
   - separate verified bibliographic facts from interpretive assessment
   - state coverage gaps, translation risks, legal-status uncertainty, and sources not checked
   - recommend the next targeted search or professional review step when the stakes are high

## Output Expectations

For prior-art, novelty, invalidity-candidate, or FTO precheck work, include:

- research type, target technology, jurisdictions, and relevant date assumptions
- databases searched and exact search date
- keyword sets, classification candidates, and final search strings
- important patent documents with publication numbers, titles, assignees, dates, source links, and why they matter
- an element-by-element mapping when claims or invention features are being compared, using a table like:

  | Target claim element / feature | Candidate document | Where disclosed (paragraph/column/figure) | Match | Notes |
  |---|---|---|---|---|

  with `Match` rated as disclosed, partially disclosed, or not found
- search gaps, uncertainty, and recommended next checks

For landscape work, include:

- search scope and inclusion/exclusion criteria
- databases and search strings used
- leading assignees, classifications, jurisdictions, filing-year trends, or citation clusters when supported by sources
- representative documents and links
- limits of the dataset and what would require paid tools or deeper analysis

## Guardrails

- Do not present findings as legal advice.
- Do not say an invention is patentable, non-obvious, valid, invalid, infringed, or clear to operate.
- Do not imply the search is exhaustive. Patent searching is iterative and database coverage varies.
- Do not rely on one database when a material conclusion depends on global coverage.
- Do not treat machine translations as definitive for claim interpretation.
- Do not treat a published application's claims as the same thing as granted claims.
- Do not assume legal status is current without checking an official register or a database that exposes legal-status data.
- Do not use APIs, scraping, automated bulk download, or paid database workflows unless the user explicitly changes the scope.
- Do not use confidential invention details in external services without user confirmation.
- Do not imply legal-status data, database coverage, or publication availability is current unless checked during the task.
