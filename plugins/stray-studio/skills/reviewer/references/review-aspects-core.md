# Core Review Aspects

Use this checklist for nearly every review, regardless of stack.

## Correctness

- Does the code actually implement the stated behavior?
- Are edge cases, nil or null handling, empty states, and error paths covered?
- Could the change break callers, contracts, or backward compatibility?
- Are assumptions about ordering, timing, or external responses justified?

## Regression Risk

- Does the change alter existing behavior without tests or migration notes?
- Are defaults, flags, config values, or environment-dependent branches changed?
- Could this break production-only, locale-specific, or permission-specific paths?

## Error Handling And Observability

- Are failures surfaced clearly, or silently swallowed?
- Are retries, timeouts, and fallback paths safe?
- Will logs, metrics, traces, or alerts make a real incident diagnosable?
- Does the change preserve useful context in exceptions and logs?

## API And Maintainability

- Are function and type boundaries clearer after the change, not blurrier?
- Does naming reflect behavior and domain intent?
- Is complexity increasing without a matching benefit?
- Is the reviewer being asked to infer too much from implicit behavior?

## Testing

- Do tests cover the changed behavior, not just the happy path?
- Are assertions meaningful, or are they too shallow to catch regressions?
- Are old tests now misleading because the behavior changed?
- If tests are absent, is the missing coverage material enough to call out?

## Review Guidance

- Report only the issues you can support with concrete evidence.
- Prefer a few high-signal findings over a long list of weak nits.
- Treat style as non-blocking unless it obscures correctness, safety, or maintenance.
