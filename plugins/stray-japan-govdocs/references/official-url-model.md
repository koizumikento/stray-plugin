# Official URL Model

Japanese government whitepaper URLs are not uniform across ministries. Treat the URL structure as a discoverable hierarchy, not as a single predictable pattern.

For the current e-Gov route-checking snapshot, see `egov-whitepaper-route-map.md`.

## URL Hierarchy

Use this model when collecting or reusing source URLs:

```text
e-Gov whitepaper index
  -> ministry/agency whitepaper series landing page
    -> edition landing page for a specific year
      -> HTML body, PDF index page, chapter PDFs, full PDF, summary PDF, data files
```

## Stable URL Types

Record URLs by role instead of assuming a path pattern:

- `egov_index_url`: e-Gov whitepaper listing page.
- `series_landing_page`: ministry page listing editions of one whitepaper series.
- `edition_landing_page`: page for a specific year or edition.
- `html_url`: HTML body or table-of-contents page.
- `pdf_index_url`: page listing PDFs for an edition.
- `pdf_url`: direct PDF file URL.
- `chapter_urls`: chapter or section PDF/HTML URLs.
- `summary_url`: overview or summary document URL.
- `data_urls`: Excel, CSV, statistical appendix, or figure data URLs.
- `archive_url`: WARP or other official archive URL for older editions.

## Edition Selection

Default to the latest official edition unless the user names a year, era year, edition, or comparison period.

Recognize edition requests such as:

- Western year: `2025`, `2025年版`, `FY2025`, `2025年度`
- Japanese era: `令和7年版`, `令和7年度版`, `平成30年版`
- Relative comparison: `去年と今年`, `前年度`, `過去5年`, `2019年から2024年`
- Ministry edition label, such as `外交青書2026`

When both Western year and Japanese era appear, preserve both in metadata. Do not assume every whitepaper uses the same edition convention: some use calendar year, some use fiscal year, some use report year, and some describe the prior year's activity.

For relative requests, resolve concrete years before reading and state the resolved years in the output. For example, if the current date is 2026-04-27, `去年と今年` should be resolved explicitly rather than left as relative wording.

If the requested edition cannot be found from the series landing page:

1. Check the same official domain's archive or older-edition links.
2. Check WARP only when the ministry points there or current official pages indicate archived editions.
3. Report that the specific edition was not found before falling back to the latest edition.

## Observed Patterns

These examples are patterns to recognize, not permanent hard-coded truth:

- e-Gov provides the cross-government whitepaper index and links out to each ministry or agency.
- Some whitepapers have a series page plus separate HTML and PDF pages for each edition.
- Some ministry pages list all chapter PDFs directly on the edition page.
- Some agencies provide full HTML for recent editions and PDF-only pages for newer or older editions.
- Some older editions are delegated to WARP, the National Diet Library web archive.
- A direct PDF URL alone is insufficient unless it can be tied back to an official landing page.

## Source Index Rule

When a skill learns official paths, store them in the task-local source index:

```text
tmp/japan-govdocs/sources/whitepaper-index.json
```

Do not treat cached URLs as current. Before reading, citing, or downloading a cached URL, re-check the relevant official landing page.

## Canonical Record Example

The required and optional fields are defined once in `download-cache-policy.md`; use that schema for every source-index record. The URL roles above map directly to fields in that canonical schema.

```json
{
  "records": [
    {
      "document_id": "cao-disaster-management-white-paper-2025",
      "title": "防災白書",
      "ministry": "内閣府",
      "year": "2025",
      "edition": "令和7年版",
      "landing_page": "https://www.bousai.go.jp/kaigirep/hakusho/r07/",
      "ministry_slug": "cao",
      "document_slug": "disaster-management-white-paper",
      "series_landing_page": "https://www.bousai.go.jp/kaigirep/hakusho/index.html",
      "edition_landing_page": "https://www.bousai.go.jp/kaigirep/hakusho/r07/",
      "pdf_index_url": "https://www.bousai.go.jp/kaigirep/hakusho/r7.html",
      "html_url": "https://www.bousai.go.jp/kaigirep/hakusho/r07/",
      "chapter_urls": [],
      "last_checked_at": "YYYY-MM-DDTHH:MM:SSZ"
    }
  ]
}
```

## Guardrails

- Prefer landing pages over direct file URLs for persistent records.
- Store direct PDF URLs only as edition-level evidence discovered from a landing page.
- Do not infer another ministry's URL pattern from one ministry's path.
- Do not infer a new year's URL by incrementing an old path unless the resulting page is verified live.
- When an e-Gov route is moved or blocked for scripted clients, verify through the same official domain using browser access or official site search before treating it as unavailable.
- Keep final citations on official URLs, not local cache paths.
