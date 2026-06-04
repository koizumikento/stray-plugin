# Observability Reference

Use this reference when the changed flow needs new or revised logs, traces, metrics, crash signals, or audit events. Use `logging.md` for detailed application logging design.

## Design Defaults

- Prefer structured events with stable field names over ad hoc prose logs.
- Attach correlation identifiers such as request, job, user, tenant, or trace IDs when they materially help join events across boundaries.
- Log at the boundary where intent, outcome, and failure reason are clearest instead of emitting many low-signal lines.
- Separate operational logs, product analytics, and audit events. They serve different readers and retention needs.
- Keep logs, traces, metrics, crash reports, analytics, and audit events correlated where the platform supports it, but do not collapse them into one generic event stream.

## Safety And Privacy

- Do not log secrets, tokens, raw credentials, or unnecessary personal data.
- Redact or hash sensitive identifiers unless operators genuinely need the raw value to debug safely.
- Treat auth, permission checks, money movement, destructive writes, and admin actions as candidates for explicit audit events.
- Keep retention, access, and export assumptions in mind when deciding what fields become searchable.

## Common Risk Areas

- Logs that cannot be grouped because event names and field keys drift between code paths.
- Error handling that records a stack or message but not the failed operation, subject, or remediation clue.
- Background jobs, retries, and async handlers that emit success logs but hide partial failure or duplicate delivery.
- High-volume paths that log too much detail and create cost, noise, or accidental data exposure.
- Telemetry that cannot be joined across client, server, worker, and integration boundaries because request, trace, job, or tenant context was dropped.
