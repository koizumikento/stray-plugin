# Metric and provenance rules

## Result classes

- **Published field:** a value present in a survey record, including published
  classifications and reported annual counts.
- **Server-computed measure:** a result calculated by the bundled server from a
  reviewed definition in `dataset.yaml`. Report its formula and filters.
- **Agent-derived inference:** an interpretation or calculation not supplied by
  the dataset or server. Keep it separate and show enough inputs to reproduce it.

## Online status and rate

The bundled `オンライン率` is a count-based share: procedure types whose
`オンライン化の実施状況` is `1 実施済`, divided by all procedure types in the
active filter. It is not the share of transaction volume completed online.

If a volume-weighted rate is requested, inspect the relevant count fields and
their notes first. Do not silently substitute a procedure-count rate. State the
denominator, null treatment, applicable records, and whether server or agent
calculation produced the result.

## Published count cautions

- `総手続件数` describes fiscal 2023 annual volume and includes approximate and
  estimated values; local-government procedures may include sample-municipality
  estimates.
- `オンライン手続件数` can be null when the count is unknown. Zero generally
  means no online procedures, but some local-government records use zero where
  counting was difficult.
- Do not turn null into zero, sum formatted text, or infer missing online volume
  from total and non-online counts without labeling the derivation and checking
  applicability.

## Dates and provenance

- `published_at` is the publication date declared by the dataset definition.
- `as_of_date` is the data's stated reference point when supplied; an empty value
  means the server does not assert one.
- `fetched_at` is the local retrieval date and is not the survey reference date.
- Cite the source URL returned in provenance. Do not cite the vendored directory or
  generated Parquet file as the public source.

## Response metadata

Carry response `notes` into the answer when material. Use `quality_summary` to
qualify missingness and coverage. If `resolved_fields` appears, disclose the
server's correction from the requested label to the official field name.
