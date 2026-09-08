# API And Communication Reference

Read this when changing API contracts, handlers, clients, integrations, or streams, or diagnosing latency, lost responses, cancellation, or connectivity. Skip it when communication behavior is unchanged and existing code settles the task.

## Workflow

1. Trace the contract and both sides of each boundary.
   - Inspect UI/platform callers, server handlers, external providers, jobs, validation, auth, and generated clients. Reuse the repository's contract format instead of adding a new specification or generator by default.
   - Make inputs, outputs, errors, pagination, and compatibility explicit. Validate at the receiving trust boundary and enforce resource-level authorization; do not rely on UI controls or client-supplied ownership.
   - Prefer additive changes. Identify breaking changes and update affected callers together when feasible, accounting for older deployed clients.
   - For webhooks, verify the provider's authentication/signature and replay requirements before trusting the payload or accepting work.
2. Define what a response means.
   - Distinguish nonblocking code such as `async/await` from request/response completion, deferred work, and a long-lived stream. HTTP can support deferred work without changing protocol.
   - If the response completes the operation, define the committed result. If it only accepts work, define the operation identifier, status/result retrieval, terminal states, retention, and durability promised to the caller. Use the async reference for processing after acceptance.
   - Do not report accepted work as completed. A 202 plus a status endpoint is one option, not a requirement for every API. See [asynchronous request-reply](https://learn.microsoft.com/en-us/azure/architecture/patterns/asynchronous-request-reply).
3. Bound waiting and retries.
   - Choose connection/request deadlines and an overall time budget appropriate to the operation. Propagate cancellation where supported, but distinguish stopping the wait from cancelling server work or undoing a committed change.
   - Treat a lost response or timeout after a write as an unknown outcome, not proof that nothing happened. Use an idempotent replay or result lookup when the contract supports it.
   - Retry only failures that the contract makes safe to retry. Do not automatically retry a non-idempotent operation without evidence it is safe or was not applied. See [RFC 9110 section 9.2.2](https://www.rfc-editor.org/rfc/rfc9110.html#section-9.2.2).
   - Bound attempts and elapsed time, honor applicable retry guidance, and use backoff with jitter for transient failures. Assign retry ownership deliberately so client, SDK, handler, and worker retries do not multiply unchecked.
   - For an idempotency key, define scope, payload matching, lifetime, concurrent requests, and replayed responses; use the data reference for atomic storage enforcement. An HTTP method's idempotency does not by itself promise identical response bodies.
4. Diagnose connections and streams when relevant.
   - Check the effective API URL, origin, DNS, TLS, proxy, load balancer, timeout configuration, CORS, and credential forwarding along the failing path. Separate connection failures from application responses; do not disable certificate verification or broaden access to hide a failure.
   - Change infrastructure settings only when required by the app flow and covered by the authorized target and effect.
   - For SSE/WebSocket flows, define authentication and expiry, subscription cleanup, reconnection, missed/duplicate event handling, resume position or authoritative state refresh, and bounded buffering for slow consumers.
   - A stream does not require a queue or durable worker by itself. Separate transport reconnection from business-operation retries.
5. Validate the consumer-visible behavior.
   - Exercise relevant invalid input, forbidden access, stale clients, delayed or missing responses, rate limiting, duplicate requests, and cancellation.
   - For writes, check a response lost after successful execution and ensure recovery preserves the intended side effect. Verify replayed and first results against the same application contract.
   - For streams, test disconnect/reconnect and recovery of current state. Report exactly which external-service, network, or client-compatibility behavior remains unverified.
