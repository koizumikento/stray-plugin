# Backend Security And Reliability Review Aspects

Use this reference for server-side, API, job, infra-adjacent, and service code.

## Security

- Are authentication and authorization checks present at the real enforcement point?
- Could untrusted input reach SQL, shell commands, templates, or internal service calls unsafely?
- Are secrets, tokens, or internal identifiers logged, returned, or persisted accidentally?
- Are tenancy, ownership, and access-scope checks preserved across refactors?

## Data Integrity

- Could partial failure leave the system in an inconsistent state?
- Are transactional boundaries correct?
- Are retries idempotent, or can they duplicate writes or side effects?
- Could concurrent requests race on shared state, counters, or status transitions?

## Reliability

- Are timeouts, cancellation, retries, and circuit-breaking behaviors explicit?
- Could this block a request thread, event loop, or worker pool unexpectedly?
- Are external dependency failures handled in a way that matches product expectations?
- Does the change make incident recovery harder by hiding state transitions or failure causes?

## Performance

- Does this introduce N+1 queries, unbounded scans, or repeated remote calls?
- Are batch sizes, pagination, and query predicates still safe at production scale?
- Could memory usage grow with request size, tenant size, or queue depth?
- Is caching used safely, including invalidation and staleness tradeoffs?

## Contracts

- Does the API response shape, status code, or validation behavior change?
- Are migrations, consumers, and versioned clients accounted for?
- Are background jobs and event consumers still compatible with old messages and schemas?
