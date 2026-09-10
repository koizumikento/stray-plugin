# Infrastructure Design And Review Baseline

Use this shared reference when creating, changing, or reviewing repository-managed infrastructure. Select applicable sections before the first design or edit, including for a vague request such as "set up a test environment." This is a decision guide, not an instruction to deploy or a claim of benchmark compliance. The calling skill's implementation/review-only and authorization boundaries remain in force. Security-only reviews select security-relevant controls; they do not become full cost or performance audits.

## Select Applicable Controls

For initial environment design, consider every row below. For a bounded change, inspect the changed contract and its direct dependencies; do not reopen settled unrelated design or create a checklist report for a typo. Classify each relevant area as **address**, **covered by an existing mechanism**, **out of scope with reason**, or **undecided**. An unknown requirement is not evidence that the area is unnecessary. Reuse repository evidence, infer low-impact choices from context, and ask only for a decision that blocks the work.

| Area | Decision to make or evidence to locate |
|---|---|
| Requirements and ownership | Environment purpose, resource/schema owners, existing resources, policy constraints, data sensitivity, manual/external dependencies |
| IAM and authentication | Human/CI/runtime identities, effective and inherited permissions, federation trust, emergency access, environment boundaries |
| DB and credentials | App/migration/admin roles, current/future grants, secret generation/storage/state/retry/rotation |
| Network | Intended clients and exposure, ingress/egress, DNS/routes, identity, TLS, environment boundaries |
| Data and storage | Public/private intent, location, retention/deletion/recovery, key ownership, test-data handling |
| Runtime and deployment | Execution privilege, health and shutdown, updates/cutover/recovery, runtime support lifecycle |
| Capacity and asynchronous work | Concurrency/scaling versus downstream capacity, quotas, timeout/retry budgets, backlog and failed work |
| Observability and operations | Service symptoms, logs/metrics/audit, retention/access, notification route and response owner |
| Reliability and recovery | Acceptable outage/data loss, failure domains, backups, restore proof and recovery sequence |
| IaC lifecycle and dependencies | State/access boundaries, locking, reviewed change identity, drift/import/replacement/deletion, trusted versioned dependencies |
| Cost and resource lifetime | Cost drivers, budget notifications versus enforcement, owner, expiry/cleanup, unnecessary idle resources |

Use the DB/credential/network sections below, [IaC lifecycle](iac-lifecycle.md), and [operations and runtime](iac-operations.md) only where applicable. Prefer the repository's existing modules, monitoring, logging, and asynchronous-work guidance over duplicated implementations. These controls may belong to a platform team or manual procedure; record that boundary and its completion evidence instead of claiming IaC owns everything.

## Establish The Basis

1. Trace modules and all callers through environment inputs, grants, secret references, app clients, migration jobs, and bootstrap/runbook steps. Identify resource and schema owners, existing resources/import needs, DB engine and provider versions, environment purpose, data sensitivity, and recovery requirements.
2. For each material default, distinguish a service default, a recommendation, a formal requirement, and a project decision. Check the exact supported engine/provider version in official documentation. Record the source URL and applicable version or access date. Do not infer current defaults from memory or copy a benchmark value into every environment.
3. Prefer existing modules and native features. Consider cost, availability, client compatibility, and operation ownership before proposing new dependencies or resources. If evidence is unavailable, mark the decision unverified and continue independent work; ask only for a missing decision that materially blocks it.
4. Use common practice as a starting point, not proof of universal adoption or a binding requirement. Well-Architected frameworks cover operations, security, reliability, performance, cost, and sustainability; CIS supplies product-specific security recommendations. Record the benchmark edition/profile and actual applicable controls before making a compliance claim. Do not invent control IDs or reproduce an unchecked benchmark as a mandatory baseline.
5. Explicitly define values when safety, compatibility, cost, or a project requirement depends on them. Otherwise an intentional documented service default can be appropriate. Record the value's source, applicable version, and exception; do not parameterize every setting or freeze obsolete defaults merely to make the configuration look complete.

## DB Identity And Privileges

- Separate routine app access, migration/schema ownership, and bootstrap/emergency administration. Do not use a default administrator for routine application connections. Do not delete or disable the only recovery identity before a verified replacement exists, or alter provider-owned system identities.
- Check effective privileges: inherited memberships, provider-assigned roles, role/DB creation, grant options, ownership, schema `CREATE`/`USAGE`, table DML, sequences, functions, and default/public grants. A newly named user or an empty-looking role list does not establish least privilege; verify the provider's behavior and actual SQL grants.
- Give the app only the operations its callers need. Keep schema ownership and DDL out of routine app credentials. Give migration only the target scope it needs; do not silently grant instance-wide administration to make migrations pass.
- Account for existing and future objects: grants and default privileges must apply to the actual object creator/owner. Preserve the repository's migration authority and avoid a competing DDL tool. Check whether a platform API can create users but cannot establish the required SQL roles, and make that bootstrap dependency explicit.
- Trace each workload identity to every readable secret and then to its DB role. Reject an app reference to migration/admin credentials even under a different environment variable name. Compare secret identities across all grants, not just `DATABASE_URL` strings; secret IAM can permit reading other versions of the same secret. Different secret names can still contain the same credentials, which repository metadata alone cannot disprove.
- Check the chosen password or IAM authentication path against all app/migration clients. For passwords, define generation, policy enforcement, independent user/environment values, expiry/lockout tradeoffs, and emergency change behavior. Do not prescribe human-password rules blindly for machine credentials. For IAM, account for token lifetime/refresh, mappings, client support, and SQL privileges.

## Credential Lifecycle And State

- Inventory where plaintext can exist: generator, provider, command arguments, shell history, logs, plan/state and backups, secret store, connection URLs, build artifacts, and runtime configuration. Display masking (`sensitive`) and base64 encoding do not mean a value is absent from state or encrypted.
- Check native secret-generation and ephemeral/write-only support in the locked tool/provider versions. Trace the value through every consumer; a supported write-only destination does not make an ordinary persisted generator or data source ephemeral. Do not use `nonsensitive`, outputs, provisioner arguments, or debug logs to work around those boundaries.
- If secret-free state is a requirement and the stack cannot provide it, report the gap and propose an authorized external bootstrap or compatible supported approach. Do not silently relax the requirement, migrate toolchains, or introduce custom secret machinery. Even secret-free state needs restricted access, encryption, locking, backup/retention, and separation from runtime identities.
- Name the durable source of truth for a credential and its non-secret version/generation identifier. Trace generation, durable registration, DB update, derived client-specific connection strings, deployment, verification, and retirement of old credentials. URL-encode credential components and preserve each driver's TLS parameters.
- Prove ordinary reapply does not rotate or break credentials. Account for ephemeral values being regenerated, ambiguous API success, partial state persistence, and failure between any two writes. Do not feed independent fresh values to the DB and secret store on retry. A durable version read can support recovery only if its identity, access, and reconciliation after partial failure are defined.
- Treat rotation separately from initial provisioning. DB, secret store, and running clients are not one transaction. Define ordering, version pinning, rollout/connection-pool behavior, downtime or dual-credential strategy when required, recovery before old-version retirement, and explicit generation changes. Adding `depends_on` alone does not make the operation atomic.
- Restrict provisioning identities to the needed user-management, secret-write, and recovery-read scopes; restrict runtime identities to their own required secrets. Do not grant broad secret access to CI just because it deploys consumers. Review old-version retention/deletion and independently generated values across environments.

## Network And TLS Paths

- Build a small connection matrix for affected paths: source identity/environment, destination, protocol/port, ingress/egress, route/DNS/private endpoint or NAT, TLS/authentication, and intended allow/deny outcome. Include public entry points, internal services, DB, management/bootstrap access, and external integrations.
- Trace the complete path, not a firewall rule in isolation: public addresses, load balancers, routes, security-group/firewall precedence, inherited policies, IPv4/IPv6, DNS resolution, endpoints, egress, and identity checks. Restrict DB/admin ports to intended clients and management paths. Public web traffic may be intentional and must not be flagged solely for being public.
- Review broad ingress and egress with their business need. Do not mandate fixed NAT, full private routing, or private endpoints without evidence such as allowlists or isolation requirements. A minimal development setup may have deliberate exceptions; preserve them with rationale and required controls.
- Verify encryption and server identity separately: CA trust, hostname verification, TLS termination, and actual settings for each client/driver. Private IP alone is neither authentication nor proof of TLS verification.
- Check cross-environment connectivity, inherited IAM, shared credentials, CIDR overlap, and deployment-time subnet/connection/egress capacity where affected. Do not infer real denial or effective access from separate names, accounts/projects, or declarations alone.

## Durability And Recovery

- Match backups, PITR, retention, deletion protection, and restore procedures to the environment's data and availability requirements. Record intentional development exceptions instead of forcing production capacity or HA everywhere.
- Inspect updates for replacement/deletion, resource ownership, state moves/import, secret-version retirement, and irreversible effects. Identify recovery dependencies before applying. A backup flag or a runbook does not establish a successful restore; retain that runtime proof gap.

## Evidence And Validation

Reuse the project's record or a compact response table; do not require a new report file for every edit. For each material control record:

| Field | Meaning |
|---|---|
| Control and target | The intended property and affected resource/consumer |
| Applicability | Address, covered by an existing mechanism, out of scope with reason, or undecided; existing coverage still needs evidence |
| Implementation | Code-enforced, manual bootstrap, service-default-dependent, absent, or out of scope with reason; combine when necessary |
| Evidence | Repository definition, static/mock result, or authorized runtime result; mark unverified parts explicitly |
| Basis/exception | Applicable requirement, official source/version, adopted value, or justified exception |
| Manual dependency/proof gap | Responsible role (TBD if unknown), prerequisites, execution order, completion check, and downstream work that waits |

Reviewers retain their evidence receipt/coverage contract; these implementation statuses supplement it, not replace it. Missing runtime evidence is not proof of either safety or exploitation. Distinguish a documented manual boundary from a confirmed bad configuration.

- Select checks from changed contracts. Docs-only: content/references/diff. Review-only: scoped inspection and safe checks, no implementation gate solely for advice. IaC-only: format/validate, input guards, mock/policy tests and affected helper tests. Add app/migration/container checks only if their contracts actually change.
- Use synthetic values and isolated backends for local tests; inspect tools/data sources before execution. Credentialed plans, effective-privilege queries, deny probes, restores, and rotation exercises need the calling workflow's authorization. Security preflight must report prohibited active checks as proof gaps, not run them.
- Test desired allows and denies: app DML allowed but DDL/role escalation refused; migration works only in its intended scope; app references to privileged secrets are rejected, including alias keys and another version of the same secret; unintended DB/admin/cross-environment paths are denied. Validate future-object grants, no-op reapply, retry after partial failure, and rollback/rotation where changed.
- Scanner, validate, and mock passes prove only the properties they inspect. Do not claim actual password rejection, DB grants, reachability, restoration, or successful cutover without matching runtime evidence. Keep failures and unexecuted checks visible; never weaken tests or exceed scope to obtain a green gate.

## Official Starting Points

Use the target provider's and DB engine's versioned documentation. These entry points are examples, not a required cloud choice or a frozen baseline:

- [Terraform sensitive, ephemeral, and write-only values](https://developer.hashicorp.com/terraform/language/manage-sensitive-data).
- [PostgreSQL privileges](https://www.postgresql.org/docs/current/ddl-priv.html); switch to the deployed major version before applying defaults.
- [Cloud SQL PostgreSQL roles and provider defaults](https://docs.cloud.google.com/sql/docs/postgres/users).
- [Google Cloud VPC firewall behavior](https://docs.cloud.google.com/firewall/docs/firewalls); include routes, identity, and runtime evidence for the actual path.
- [Google Cloud Well-Architected Framework](https://docs.cloud.google.com/architecture/framework) and [AWS Well-Architected pillars](https://docs.aws.amazon.com/wellarchitected/latest/framework/the-pillars-of-the-framework.html): whole-design coverage.
- [CIS Benchmarks](https://www.cisecurity.org/cis-benchmarks): select the target product, edition, profile, and applicable recommendations; this reference does not certify compliance.

Source entry points checked 2026-09-10. They establish official guidance, not measured industry adoption. Recheck version-dependent behavior for the actual target; a retrieval date is not a permanent compatibility guarantee.
