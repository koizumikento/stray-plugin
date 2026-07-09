# Download Cache Policy

Use this policy whenever a Japan government document skill needs to read a PDF, HTML page, spreadsheet, or attachment from an official source.

For official URL roles and hierarchy, also follow `official-url-model.md`.

## Default Order

1. Start from an official landing page, not a direct PDF URL alone.
2. Prefer HTML pages when they contain the same body text.
3. Prefer chapter-level, overview, or summary PDFs over full-volume PDFs when they answer the user's question.
4. Download only the documents needed for the current task.
5. Do not crawl whole ministry sites or bulk-download whitepaper archives unless the user explicitly asks for a dataset build.

## Temporary Storage

Use the repository-local temporary folder:

```text
tmp/japan-govdocs/
  manifest.jsonl
  sources/
  downloads/
  extracted/
```

The `tmp/` directory must stay out of git. If it is not ignored yet, add it to `.gitignore` before downloading files.

Choose and report one cache mode:

- `index-only`: store verified source routes under `sources/` without downloading source content. `manifest.jsonl` may be absent or empty only while `downloads/` and `extracted/` contain no files.
- `download-cache`: store source or extracted files. Every file under `downloads/` or `extracted/` must have exactly one valid `manifest.jsonl` record.

## Known Source Index

Keep stable knowledge about whitepapers separate from downloaded files. A skill may create or update a task-local source index under:

```text
tmp/japan-govdocs/sources/
  whitepaper-index.json
  whitepaper-index.md
```

The source index records official landing pages and discovered document links. It is a cache, not a source of truth. Before using a cached entry, re-check the official landing page because ministries may move files, publish newer editions, or replace PDFs.

Use this canonical JSON shape, including for an initialized empty index:

```json
{
  "records": []
}
```

Every non-empty source index record requires:

- `document_id`
- `title`
- `ministry`
- `year`
- `landing_page`

Optional source-index fields are:

- `ministry_slug`
- `document_slug`
- `series`
- `edition`
- `egov_index_url`
- `series_landing_page`
- `edition_landing_page`
- `html_url`
- `pdf_index_url`
- `pdf_url`
- `chapter_urls`
- `summary_url`
- `data_urls`
- `archive_url`
- `publication_date`
- `last_checked_at`
- `notes`

This is the canonical optional-field set for a source-index record. All optional fields except `chapter_urls` and `data_urls` are non-empty strings when present. The two array fields contain only non-empty URL strings and may be empty. Omit unknown values instead of writing `null`. A record represents one edition, so do not nest an `editions` array. The cache validator rejects unknown fields and type mismatches.

Do not hard-code direct PDF paths into a skill as permanent truth. Hard-code only durable official index pages when they are part of the workflow, and still verify them live.

## Local Path Rules

Downloaded and extracted files should use deterministic paths so repeated runs can find the same material without guessing.

Use this layout:

```text
tmp/japan-govdocs/downloads/<ministry-slug>/<document-slug>/<year>/<sha256-12>-<part-slug>.<ext>
tmp/japan-govdocs/extracted/<ministry-slug>/<document-slug>/<year>/<sha256-12>-<part-slug>.txt
```

Path rules:

- `ministry-slug`: romanized or stable ASCII identifier, such as `cao`, `meti`, `mhlw`, `mlit`, `maff`, `soumu`, `moj`, `mext`, `mod`, `env`, or `npa`.
- `document-slug`: stable ASCII identifier for the whitepaper series, such as `disaster-management-white-paper` or `manufacturing-white-paper`.
- `year`: publication or edition year in four digits when known. Use the Japanese edition year only in metadata, not as the directory name.
- `sha256-12`: first 12 lowercase hex characters of the downloaded file hash.
- `part-slug`: `full`, `summary`, `chapter-01`, `chapter-02`, `appendix`, or another short ASCII section name.
- `ext`: preserve the actual file extension, such as `pdf`, `html`, `xlsx`, or `csv`.

If the title or ministry cannot be normalized confidently, use `unknown-ministry` or `unknown-document` and record the uncertainty in `manifest.jsonl`.

Use `egov-whitepaper-route-map.md` for the canonical `ministry_slug` and `document_slug` values for listed e-Gov whitepapers. Do not invent a new slug for a listed document unless the route map is missing or clearly stale.

## Manifest

Append one JSON object per downloaded file to `tmp/japan-govdocs/manifest.jsonl`.

Do not create manifest records for source-index entries that have no local file. Conversely, a file under `downloads/` or `extracted/` without a manifest record is invalid. An empty manifest is valid only when those folders contain no files.

Required fields:

- `document_id`
- `title`
- `ministry`
- `year`
- `landing_page`
- `source_url`
- `local_path`
- `content_type`
- `bytes`
- `sha256`
- `fetched_at`
- `reason`

Optional fields:

- `section`
- `part_slug`
- `document_slug`
- `ministry_slug`
- `publication_date`
- `license_or_terms_url`
- `notes`

## Citation Rule

Final answers must cite official URLs, not local cache paths. Local paths are for reading and traceability only.

## Stop Conditions

Stop and report the issue before downloading when:

- the file is unusually large for the task and a smaller official source exists
- the document appears to be scanned or image-only and OCR would be required
- the source cannot be tied to an official government landing page
- the user asks for broad harvesting without a clear output boundary
