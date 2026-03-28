# Data And Migrations Review Aspects

Use this reference for schema changes, data backfills, ETL, storage-layer changes, and migration-heavy diffs.

## Migration Safety

- Is the migration safe to run in production with current data volume?
- Does it require locking, table rewrites, or long-running operations that could impact availability?
- Can old and new application versions coexist during rollout?
- Is rollback actually possible, or only nominally possible?

## Data Correctness

- Could the transformation lose, duplicate, truncate, or mis-map data?
- Are nullability, default values, and enum or status changes handled safely?
- Are timezone, locale, encoding, and precision assumptions explicit?
- Are backfills idempotent and resumable?

## Operational Readiness

- Is there a rollout order between code deploy, migration, and backfill?
- Are monitoring, validation queries, or post-deploy checks identified?
- Does the change include cleanup steps for temporary compatibility code?
- If the migration fails halfway, is the recovery path realistic?

## Performance And Scale

- Will the migration or query change degrade read or write performance materially?
- Are indexes added before query patterns depend on them?
- Could this create hotspots, queue buildup, or replication lag?

## Review Guidance

- Be stricter here than on ordinary app code because data mistakes are costly to reverse.
- Call out missing rollout or rollback detail when the diff changes persistent data shape or semantics.
