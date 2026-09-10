# Infrastructure Operations And Runtime

Use for affected storage, runtime, capacity, monitoring, recovery, or cost contracts. Select the applicable sections before design, including for initial test environments. Reuse platform-owned mechanisms and the app's existing contracts; do not invent an application instrumentation, queue, or deployment system for an infrastructure-only task. The calling skill's authorization and review scope remain in force.

## Data And Storage

- Identify data classification, intended readers/writers, location/residency requirements, retention, deletion, and recovery needs. Distinguish deliberately public static assets from private uploads, backups, and logs; check ACL/policy inheritance and supported public-access controls at the actual boundary.
- Define lifecycle behavior for current, noncurrent/versioned, temporary, and incomplete objects where supported. Verify that cleanup does not erase required backups, audit evidence, or recoverable versions. Avoid irreversible retention locks or customer-managed encryption keys without a requirement and an owner for key availability/recovery.
- Verify encryption and key access with the target service's actual defaults. A custom key is a design choice with operational dependencies, not universal proof of better security. Check that test environments use suitable synthetic/sanitized data and do not silently inherit production data or permissions.

## Runtime, Deployment, And Capacity

- Reuse the platform's execution model. For containers where applicable, check non-root execution, unnecessary privileges/capabilities, filesystem needs, and workload identity. Use runtime-specific guidance only for targets actually present; managed serverless work does not require a Kubernetes rollout.
- Trace startup/readiness/liveness and graceful shutdown/draining to existing app endpoints and time budgets. Do not invent a health endpoint that always succeeds or probes a downstream dependency in a way that causes restart storms. Align deployment cutover, minimum availability, compatible schema/config changes, and recovery; report required app changes explicitly.
- Relate maximum instances and concurrency to DB pool limits, connection headroom, downstream rate limits, subnet capacity, and service quotas. Include old/new instances overlapping during a rollout when relevant. Treat the estimate as a sizing hypothesis until measured; a service scaling limit is not necessarily a strict global connection cap.
- For jobs/queues, align producer and consumer timeouts, retry/backoff budgets, rate/concurrency limits, retention, failed-message handling, and safe replay. Check existing idempotency and duplicate-delivery contracts; do not infer exactly-once processing from queue configuration. Preserve caller ownership of app retry and idempotency logic.
- Record supported runtime/image versions, update ownership, deployment artifact identity, and maintenance constraints. Use existing rollback or forward-repair mechanisms appropriate to the data and service; do not promise rollback from a retained image alone.

## Observability And Response

- Start with service symptoms: latency, traffic, errors, and saturation; add queue age, failed work, storage capacity, or certificate expiry when the workload needs them. Reuse available telemetry and the established service objectives rather than inventing thresholds or adding every possible metric.
- Connect detection to a notification destination, responsible role, and response/runbook. Distinguish telemetry collection from alert evaluation and actual delivery. Record unknown recipients as a manual dependency; a log sink or alert resource alone does not prove someone will be notified.
- Separate operational and audit needs. Check collection, access, retention, routing/export, failure visibility, and cost of high-volume/cardinality data. Keep secrets and unnecessary personal data out of events. Reuse the app's existing correlation and logging conventions; platform logs may not prove business-level success.
- Verify alert conditions with synthetic/static tests where supported, and record whether delivery/response was exercised. Do not send a test page or notification to real people without matching authorization.

## Reliability And Recovery

- Record the workload's acceptable downtime (RTO) and data-loss window (RPO), failure domains, and dependency recovery order. Unknown values stay undecided; a disposable test environment may explicitly accept recreation and loss of synthetic data.
- Match backup, PITR, retention, redundancy, and deletion protection to those objectives. HA does not replace a backup, and a backup does not establish a working restore. Consider permission/key/network dependencies and isolation of recovery copies where required.
- Define the restore/verification target, owner, prerequisites, completion checks, and measured recovery evidence. Use an isolated target for authorized restore exercises; never overwrite a live database merely to validate a backup. Repository-only work leaves runtime recovery proof open.

## Cost And Resource Lifetime

- Identify material baseline and growth costs: compute minima/maxima, database/storage growth, logs, backups, network egress/NAT, and paid service dependencies. Use actual region/service pricing when making estimates, with workload assumptions and date; do not claim a fixed cost from an instance count alone.
- Distinguish budget alerts from spending enforcement. Confirm whether the selected product/plan supports caps, what they cover, timing/overshoot limitations, and the impact of stopping service. Alerts-only budgets do not enforce a cap; do not assume every budget product is alerts-only either. Avoid automatic billing shutdown or destructive cleanup without explicit scope and recovery decisions.
- Record resource owner, environment/purpose, cost attribution, intended lifetime, and the authorized stop/delete procedure. Labels help attribution but do not enforce isolation or expiry. Consider idle-resource removal, right-sizing, and stopping disposable workloads to reduce cost and waste; do not impose region changes or downtime against availability/data-location requirements.

## Reuse And Evidence

For application instrumentation and behavior, use existing [observability](../skills/fullstack-app-builder/references/observability.md), [logging](../skills/fullstack-app-builder/references/logging.md), and [asynchronous-work](../skills/fullstack-app-builder/references/async-workflows.md) guidance only when those contracts are affected. Security reviews also have the existing [infrastructure/container checks](../skills/security-preflight/references/infra-containers.md); reuse their technical checks without importing a different skill's mutation mode. Do not require an app suite for infrastructure definitions that leave app contracts unchanged.

Use the baseline's applicability, implementation, and evidence statuses. A configured backup, alert, scaling rule, encryption flag, or retention policy is declaration evidence; record actual restore, notification, effective access, load, and deletion proof separately. Name owned manual dependencies rather than expanding the task into live operations.

## Official Basis

Entry points checked 2026-09-10; choose the target service's version-specific details and justified exceptions.

- [Google SRE monitoring](https://sre.google/sre-book/monitoring-distributed-systems/) and [AWS recovery objectives](https://docs.aws.amazon.com/wellarchitected/latest/framework/rel_planning_for_recovery_objective_defined_recovery.html).
- [Kubernetes application security checklist](https://kubernetes.io/docs/concepts/security/application-security-checklist/); applies only to relevant Kubernetes controls, not every runtime.
- [Google Cloud budgets and alerts](https://docs.cloud.google.com/billing/docs/how-to/budgets); check actual product availability and enforcement scope.
- [Google Cloud Well-Architected Framework](https://docs.cloud.google.com/architecture/framework) for operations, reliability, performance, cost, security, and sustainability tradeoffs.
