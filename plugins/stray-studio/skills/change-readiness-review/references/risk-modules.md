# Triggered Risk Modules

Start with the fast path. Load only sections whose trigger is present in the captured change. Examples do not create requirements or findings by themselves.

## Input And Serialization

Trigger: parser, validator, serializer, schema, escaping, normalization, accepted syntax, upload, or protocol decoding.

- Check accepted and rejected inputs in the changed partitions only: empty, nullish, malformed, Unicode, delimiter, size, and boundary cases.
- Confirm validation occurs at the actual trust boundary and that normalization cannot change authorization or identity meaning.

## Product Flow And UI

Trigger: user workflow, command behavior, navigation, response, permissions, loading, empty, or error state.

- Check the changed happy path plus reachable empty, error, permission, stale, cancellation, and retry states.
- Confirm UI restrictions are backed by the real enforcement point and that state cannot become contradictory or unrecoverable.

## Security And Sensitive Data

Trigger: authentication, authorization, tenant or object ownership, secrets, PII, uploads, public endpoints, billing, CI privileges, or destructive operations.

- Check identity, authorization, scope, information exposure, secret handling, and fail-closed behavior at reachable entry points.
- If security is the primary requested lens rather than an incidental code-review dimension, route to `security-preflight`.

## Persistence And Migration

Trigger: database or durable write, schema, migration, state machine, queue, retry, backfill, or irreversible operation.

- Check atomicity, idempotency, partial failure, compatibility during rollout, recovery, rollback, and data preservation.
- Confirm new and old code/data shapes can coexist where rolling deployment requires it.

## Public Contract

Trigger: API, command, event, schema, configuration key, export, plugin surface, or shared-library compatibility change.

- Inspect actual consumers and parallel entry points.
- Check defaults, error shape, versioning, migration path, and compatibility promises.

## Concurrency And Distributed State

Trigger: parallelism, async work, cache, lock, job, webhook, polling, timeout, retry, or eventual consistency.

- Check races, cancellation, duplicate delivery, stale reads, idempotency, resource cleanup, ordering, and retry amplification.

## Deployment And Supply Chain

Trigger: CI, build, dependency, lockfile, generated artifact, environment variable, feature flag, infrastructure, IAM, container, or release configuration.

- Check required artifacts and configuration, privilege changes, reproducibility, rollout/rollback order, and the exact environment affected.
- Treat external hosted settings as unverified unless they were actually read from an authorized source.
