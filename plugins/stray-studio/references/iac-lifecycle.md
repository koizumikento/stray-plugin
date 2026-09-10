# IaC Lifecycle, Identity, And Dependencies

Use for repository-managed infrastructure identity, state, change execution, and dependency decisions. Apply only to the affected contracts and preserve the calling skill's plan/review/implementation and live-access boundaries. This reference does not authorize deployment or require a new CI platform.

## Identity And State Boundaries

1. Trace humans, provisioning CI, runtime workloads, and emergency operators to effective permissions, role inheritance, impersonation, and cross-environment access. Keep ordinary runtime access separate from deployment and administration. Check platform-owned policies before redefining or weakening them.
2. Prefer managed workload identity or short-lived federation where the platform and clients support it. Restrict the issuer, audience, subject/repository/environment and applicable branch/workflow conditions; OIDC alone does not make broad trust safe. Keep untrusted PR code away from privileged jobs. If a long-lived key is necessary, document its owner, storage, rotation, revocation, and recovery rather than silently generating one.
3. Identify state ownership, backend location, access, encryption, recovery, and concurrent writers. For shared operation, prefer a supported remote backend with state locking and recovery/versioning appropriate to the backend. Local disposable fixtures may use isolated local state; never commit state or saved plans. Distinguish an intentional bootstrap stage from permanent shared local state.
4. Match state boundaries to access, lifecycle, and the impact of a failed change. Separate names, directories, or Terraform CLI workspaces are not access controls. CLI workspaces are unsuitable where separate credentials/access controls are required; distinguish them from HCP Terraform workspaces. Do not mandate one state per resource or invent organizational folders to achieve a boundary already enforced elsewhere.
5. Trace cross-state data access. Reading a remote state's outputs can require access to its complete snapshot; do not assume outputs alone restrict exposure. Prefer the existing explicit publication mechanism for shared non-secret values when broad state access would violate the boundary. Keep plan/state artifacts access-controlled and out of ordinary review uploads.

## Reproducible Changes

1. Record the source revision, target environment/backend, inputs, tool/provider/module versions, and proposed replacement/deletion effects. Tie apply to the reviewed plan or the managed platform's equivalent run identity; do not silently re-plan a different revision after review and call it the approved change. Inspect stale plans and state drift before proceeding.
2. Preserve backend locking and serialize conflicting writes through the existing workflow. A lock does not make DB, cloud, and client changes transactional, and different states can still manage overlapping targets. Do not disable locking or force-unlock an active writer to get past a failure.
3. Inspect plan/test execution before running it: providers, external data sources, provisioners, and tests can perform live operations. Use offline validation and mock providers with synthetic data for local checks. Inspect credentialed plans under the user's authorized scope and protect their output.
4. Give each resource one management authority. Before adoption, removal, rename, or module restructuring, account for imports, address moves, lifecycle settings, dependent resources, and the recovery procedure. Terraform deletion guards are not a substitute for service-side protection and restricted delete permissions where those are required. Avoid broad `ignore_changes`, routine targeting, and state surgery that conceal drift.
5. Define how authorized operators detect and reconcile manual changes: compare desired and actual state, decide which is authoritative, and preserve evidence before an overwrite. Do not silently auto-remediate drift. A Git revert does not guarantee restoration of destroyed data or reverse an irreversible migration.
6. On partial or ambiguous failure, identify completed effects and durable state before retrying; reconcile dependencies and recovery ownership. Reuse the shared credential lifecycle rules for secret/DB writes. Keep failed-run evidence and do not claim a no-op or successful rollback without the relevant proof.

## Dependency And Toolchain Integrity

- Use the repository's pinned toolchain and verify required features against its versions. Keep Terraform version constraints and Provider source/version constraints explicit, and commit the root configuration's `.terraform.lock.hcl` for reviewed Provider selections/checksums.
- Do not treat that lockfile as a remote-module lock. Use an exact registry module version or immutable VCS reference where reproducibility is required. Account for local modules through the repository revision; shared reusable modules may declare compatible constraints without dictating every consumer's version.
- Inspect the trust and update path for modules, Providers, CI actions, base images, and build artifacts. Prefer established maintained sources and reviewed immutable selections appropriate to the ecosystem; do not use an unreviewed moving branch or image tag as proof of repeatability. Assign an update/support-lifecycle owner so pinning does not mean never patching.
- Inspect provisioners and downloaded scripts before executing them; do not pipe an untrusted download into a shell. Reuse existing scanners or policy checks with their actual scope and version documented. Do not install overlapping scanners or treat a clean scan as proof of effective permissions or operational readiness.

## Evidence And Checks

Use the existing repository entry points for format/validate, changed input guards, mocks, and helper tests. Add policy checks only for meaningful repeatable contracts that existing tools do not cover. For lifecycle changes, check wrong-target rejection, concurrent writes, import/move versus replacement, reviewed-plan correspondence, and a failed/retried operation as applicable. A synthetic test proves the simulated contract, not live isolation, drift status, or recovery. Manual work needs an owner, prerequisites, order, completion check, and dependent work that waits.

## Official Basis

Entry points checked 2026-09-10; verify the deployed version and backend rather than hardcoding latest behavior.

- [Terraform style and workflow](https://developer.hashicorp.com/terraform/language/style), [dependency lockfile](https://developer.hashicorp.com/terraform/language/files/dependency-lock), and [CLI workspaces](https://developer.hashicorp.com/terraform/language/state/workspaces).
- [Terraform automation](https://developer.hashicorp.com/terraform/tutorials/automation/automate-terraform), [state locking](https://developer.hashicorp.com/terraform/language/state/locking), and [remote-state data access](https://developer.hashicorp.com/terraform/language/state/remote-state-data).
- [GitHub Actions OIDC](https://docs.github.com/en/actions/concepts/security/openid-connect) and [Google Cloud service-account key guidance](https://docs.cloud.google.com/iam/docs/best-practices-for-managing-service-account-keys); use the equivalent identity documentation for other targets.
