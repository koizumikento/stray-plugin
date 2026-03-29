# Observability Reference

Use this reference when the changed flow needs new or revised logs, traces, metrics, crash signals, or audit events.

## Design Defaults

- Prefer structured events with stable field names over ad hoc prose logs.
- Attach correlation identifiers such as request, job, user, tenant, or trace IDs when they materially help join events across boundaries.
- Log at the boundary where intent, outcome, and failure reason are clearest instead of emitting many low-signal lines.
- Separate operational logs, product analytics, and audit events. They serve different readers and retention needs.

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
