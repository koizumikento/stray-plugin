# Asynchronous Workflows Reference

Read this when work continues after acceptance, must survive process exit, or involves queues, events, webhooks, scheduled jobs, redelivery, or offline reconciliation. Ordinary `async/await` calls or displaying an SSE stream do not alone require this reference.

## Workflow

1. Define the lifecycle and user-visible result.
   - Identify the trigger, payload, authorized actor/resource, work identifier, durable state, and completion condition. Distinguish accepted, running, succeeded, failed, cancelled, and partial outcomes when applicable.
   - Decide which work must survive process death, how status is recovered, how long results remain available, and what cancellation can actually prevent. Use the existing queue, scheduler, or platform worker when it meets the need; do not add a broker by default.
2. Make acceptance and delivery consistent with persistence.
   - Do not acknowledge durable acceptance before work can be recovered under the promised failure model. Do not assume a successful HTTP response means the background side effect succeeded.
   - When a database update must produce a message, check the failure between commit and publication. Use an existing atomic mechanism, transactional outbox, or change-data capture when needed; do not add one for unrelated asynchronous work. See [AWS transactional outbox guidance](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/transactional-outbox.html).
   - Publish only committed changes. Define recovery when publication is repeated or delayed; an outbox does not make all downstream effects atomic or exactly once.
3. Handle duplicate delivery and uncertain effects.
   - Make local effects and deduplication/progress records atomic where supported. Acknowledge consumed work only after its required durable outcome is secured, according to the transport contract.
   - Keep processing safe when it stops after commit but before acknowledgement. Use stable operation identifiers and the data reference when atomic claims or storage constraints need design.
   - For remote side effects, use provider idempotency or result reconciliation where available. If a timeout leaves the outcome unknown, preserve that state for recovery instead of blindly repeating a potentially completed operation.
4. Bound retries, ordering, and recovery.
   - Separate permanent validation/permission errors from transient failures. Define attempts, time budget, backoff, rate limits, worker concurrency, and failure visibility; avoid multiplying retries already owned by an API client.
   - Define ordering only where the business invariant needs it, such as per object or version. Prevent an older attempt or stale worker from overwriting a newer result or cancellation using the platform's appropriate conditional update or ownership mechanism.
   - Make exhausted or invalid work visible through existing job state or failure queues. Define authorized replay, compensation, or repair where needed; do not hide failure with indefinite retries.
5. For offline reconciliation, distinguish data synchronization from asynchronous execution.
   - Persist pending local edits before promising they will survive restart. Define authoritative data, versions, conflicts, deletion propagation, and how pending/conflicting/synchronized state appears in the UI.
   - Choose conflict handling according to business rules. Do not assume resending resolves conflicts or device timestamps provide a reliable last-write order. See [Android offline synchronization and conflict resolution](https://developer.android.com/topic/architecture/data-layer/offline-first#synchronization).
6. Verify interruption and the eventual user-visible effect.
   - Exercise relevant duplicate or out-of-order delivery, process interruption before/after a durable write, lost acknowledgement, retry exhaustion, cancellation, and partial failure.
   - Check that durable business state, job status, status API, and UI converge to the agreed result; verify emails, imports, notifications, or other required effects rather than merely a successful enqueue.
   - Report trigger, completion/recovery path, observed results, and unverified worker/provider behavior. Preserve evidence of stuck or uncertain work.
