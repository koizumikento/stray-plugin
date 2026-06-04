# Logging Design Reference

Use this reference when an app change needs new or revised application logs, audit logs, background-job logs, integration logs, or incident diagnostics. Keep repository conventions and the deployed logging backend as the source of truth.

## When To Add Logs

- Add logs at boundaries where intent, outcome, and failure reason are clear: API handlers, server actions, background jobs, external integrations, auth checks, permission checks, migrations, imports, exports, and destructive or money-moving writes.
- Prefer a few durable event logs over many low-signal progress lines.
- Treat user-visible failures, support-relevant failures, retries, partial failures, duplicate deliveries, and degraded fallbacks as logging candidates.
- Do not add logs only to compensate for missing tests, unclear errors, or hidden control flow. Fix those issues directly when they are in scope.

## Event Shape

- Use a stable `event_name` that describes the domain event or operation, such as `invoice.create_failed` or `webhook.delivery_retried`.
- Include `timestamp`, `level`, `service`, `environment`, and `version` when the platform does not already attach them.
- Include correlation fields when available: `request_id`, `trace_id`, `span_id`, `job_id`, `tenant_id`, `actor_type`, and a safe `actor_id`.
- Include operation fields that explain the event: `action`, `object_type`, safe `object_id`, `result`, `reason`, `error_code`, `duration_ms`, `attempt`, and `retryable`.
- Keep field names and value types stable across related success, failure, and retry paths.

## Log Levels

- Use `DEBUG` for local or temporary diagnostic detail that is normally disabled in production.
- Use `INFO` for important lifecycle, integration, job, or business events that completed as expected.
- Use `WARN` for unexpected but handled conditions, degraded paths, retryable failures, suspicious inputs, or recoverable policy mismatches.
- Use `ERROR` for failed operations that need investigation, create data risk, or produce a user-visible failure.
- Use `FATAL` only for unrecoverable startup, runtime, process, or system failures.
- Avoid `WARN` and `ERROR` inflation. Too many high-severity events make filtering, alerting, and incident triage worse.

## Structured Fields

- Prefer structured logs with stable fields over prose-only messages.
- Keep the prose `message` short and human-readable; put queryable facts in fields.
- Follow existing project schema, logger helpers, cloud-provider conventions, OpenTelemetry semantic conventions, or Elastic Common Schema before inventing new names.
- Use timestamps, severity, trace context, resource or service context, and attributes in shapes that can map cleanly to the active logging backend.
- Do not make every possible field indexed or labeled. Design for the queries operators actually need.

## Privacy And Safety

- Never log secrets, tokens, raw credentials, private keys, session cookies, auth headers, payment credentials, or full security challenge material.
- Avoid unnecessary personal data. Redact, hash, truncate, or classify sensitive identifiers unless raw values are genuinely required and allowed.
- Do not log raw request bodies, response bodies, headers, uploaded files, prompts, messages, documents, or webhook payloads unless they are explicitly safe and necessary.
- Treat retention, access, export, and searchability as part of the field design.
- Sanitize or encode untrusted values so logs cannot be used for injection, terminal control, HTML/script execution, or forged log lines.

## Correlation

- Propagate request, trace, span, tenant, user, and job context through client/server, worker, queue, webhook, and external API boundaries when the app architecture supports it.
- Make async work joinable back to the originating request, scheduled task, imported file, webhook delivery, or user action.
- Preserve external provider request IDs, delivery IDs, idempotency keys, and rate-limit identifiers when they help support or incident investigation and are safe to store.
- For mobile, desktop, offline, or customer-controlled devices, record timestamp confidence or clock-offset context when exact timing may be unreliable.

## Cardinality And Cost

- Keep high-cardinality values such as user IDs, order IDs, trace IDs, session IDs, and raw paths out of labels, tags, index keys, or metric dimensions unless the backend explicitly supports them safely.
- Store dynamic identifiers as structured fields or metadata when operators need them for lookup.
- Bound enum-like fields such as `result`, `action`, `object_type`, `provider`, and `retryable`.
- Sample, suppress, aggregate, or downgrade high-volume success logs when they do not materially improve operations.
- Filter close to the source when safe so downstream systems do not ingest unnecessary sensitive or low-value data.

## Operational, Audit, And Analytics Events

- Separate operational logs, audit events, and product analytics. They have different readers, retention needs, privacy rules, and correctness expectations.
- Treat auth changes, permission decisions, admin actions, destructive writes, money movement, exports, impersonation, and security-sensitive configuration changes as audit-event candidates.
- Do not rely on product analytics as the only operational or debugging signal.
- Do not rely on operational logs as the durable audit trail when the product has explicit compliance, billing, or accountability requirements.

## Failure Modes To Verify

- Logging failures must not break the primary user flow unless the business requirement explicitly demands fail-closed audit behavior.
- Verify event names, field names, field types, levels, and sensitive-data exclusion in tests or review for security-sensitive or business-critical paths.
- Check behavior when the logging backend is unavailable, storage is full, permissions are missing, queues back up, or network connectivity is lost.
- Ensure log volume cannot exhaust disk, memory, queue capacity, database transaction logs, or vendor ingest limits.
- Confirm logs are not exposed through public routes, client bundles, static assets, screenshots, crash dialogs, or final answers.
