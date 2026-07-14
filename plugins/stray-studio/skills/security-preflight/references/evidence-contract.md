# Security Preflight Evidence Contract

Use this reference for every security preflight. It defines how candidate risks become findings, how reviewed boundaries remain auditable, and how missing proof affects the final ship recommendation. It does not authorize active testing, exploitation, remediation, or any external mutation.

## Evidence Boundary

Accept evidence only from sources already within the review scope:

- local repository files, history, diffs, manifests, lockfiles, and configuration
- output from safe, read-only commands or scanners run for this review
- connected GitHub, cloud, or runtime settings that the user authorized the reviewer to read
- user-provided architecture, policy, deployment, or operational facts, labeled as user-provided

Keep these evidence classes distinct. Repository configuration does not prove hosted settings or runtime behavior, and a user assertion does not become independently verified evidence.

This contract never authorizes:

- exploit payloads, proof-of-concept execution, active network probing, credential validation, login attempts, or production scans
- executing untrusted repository code merely to reproduce a suspected issue
- cloud, repository, CI, secret-store, dependency, or infrastructure mutation
- extracting, displaying, reproducing, or deliberately opening whole secret, credential, private-key, sensitive-log, dump, or PII values; bounded redacting scanners and pattern checks may identify a type and safe locator without exposing the value

When stronger proof would require one of those actions, record a proof gap and defer it to the appropriate authorized specialist or owner.

## Candidate Evidence Receipts

Create a receipt when inspection raises a plausible security-relevant claim. Keep stable candidate IDs so the final finding, coverage ledger, and any later remediation handoff can refer to the same record.

Record:

- `candidate_id`: stable identifier such as `AUTHZ-01` or `CI-03`
- `boundary`: application, secrets/data, supply chain, CI/CD, infrastructure/container, or a narrower named boundary
- `claim`: one falsifiable statement about the suspected condition and affected surface
- `evidence_class`: repository, command, connected setting, or user-provided
- `evidence_locator`: safe path and line, command and scoped result, setting name, or supplied document section
- `status`: exactly one of `confirmed`, `suppressed`, `deferred`, or `not_applicable`
- `rationale`: why the evidence supports that status without exposing sensitive values
- `decision_impact`: possible ship-decision effect; assign finding severity only after confirmation
- `next_owner`: owner or specialist needed when deferred; otherwise `none`

Redact evidence at collection time. For a suspected secret, keep only the secret type, safe path and line, variable or key name, and exposure context. Do not store the value, a reusable prefix, a full fingerprint, a private URL, or copied sensitive content in a receipt.

### Receipt Statuses

`confirmed`

- Direct evidence supports the claim within the stated scope.
- Promote the candidate to a finding and assign severity based on impact and reachability evidence.
- A scanner alert alone may confirm that an alert exists, but not exploitability or runtime reachability unless those are separately evidenced.

`suppressed`

- Specific counter-evidence refutes the candidate, proves a safe control, or shows that it duplicates another receipt.
- Record the counter-evidence or canonical candidate ID.
- Do not use `suppressed` merely because the issue was not reproduced, a scanner was unavailable, or runtime state could not be inspected.

`deferred`

- The claim remains plausible but the required proof is unavailable, outside the review scope, unsafe to collect, or owned by a specialist.
- Create a linked proof gap with the missing evidence, decision impact, owner, and safe verification action.
- Deferred candidates are not findings, but material deferred risk must affect the final recommendation.

`not_applicable`

- Scope evidence shows that the boundary or condition does not exist for this target, such as no package-publishing path in the reviewed repository.
- Record the inventory or scope evidence supporting non-applicability.
- Do not use `not_applicable` for an uninspected, unknown, inaccessible, or excluded surface; use `deferred` or an explicit scope exclusion.

## Coverage Ledger

Maintain one ledger row for each selected security boundary and each material high-risk sub-boundary. Record:

- boundary and review objective
- files, settings, commands, or other evidence sources inspected
- candidate receipt IDs produced
- counts of confirmed, suppressed, deferred, and not-applicable candidates
- explicit exclusions and their reason
- remaining proof-gap IDs

A boundary is `covered` only when the planned repository surface was inspected and every candidate has a final receipt status. Use `partial` when evidence or scope is incomplete and `not_reviewed` when the boundary was excluded. Never infer complete coverage from the absence of findings.

At minimum, reconcile coverage for every high-risk boundary named in the scope, including authentication/authorization, secrets, privileged CI or release paths, public exposure, and dependency or artifact trust where relevant.

## Proof Gaps

Create a proof-gap entry for each deferred candidate and for any material setting or runtime state needed for the decision but not evidenced by a candidate.

Record:

- `gap_id` and linked candidate or boundary
- the exact fact that remains unproven
- why it could not be established safely in this review
- potential decision impact if the unsafe condition exists
- the owner or qualified specialist who can verify it
- the smallest safe verification action and expected evidence artifact
- whether release may proceed before closure

Examples include effective cloud IAM, actual network reachability, branch-protection rules, environment approvals, runtime authorization policy, dependency reachability, and whether a suspected credential remains valid. Do not close these gaps by active probing under this skill.

## Final Decision Reconciliation

Before issuing the recommendation, reconcile all artifacts:

1. Ensure every reported finding traces to one `confirmed` candidate receipt.
2. Ensure every candidate has exactly one final status and appears in the relevant coverage row.
3. Ensure every `deferred` candidate has a proof gap, owner, and safe next verification step.
4. Ensure every `suppressed` candidate names counter-evidence or a canonical duplicate.
5. Ensure every `not_applicable` candidate names scope or inventory evidence.
6. Reconcile severity, reachability, affected environment, and existing controls without overstating what static evidence proves.
7. Map the evidence to one final recommendation:
   - `ready`: no confirmed blocking finding, material boundaries are covered, and remaining proof gaps are explicitly non-blocking
   - `ready with fixes`: bounded confirmed findings require completion before the stated release point, with clear validation and ownership
   - `hold`: a confirmed blocking finding or material unresolved risk makes proceeding unsafe
   - `needs specialist sign-off`: a material proof gap or specialist-owned policy prevents a defensible ready/hold decision

The recommendation must cite the confirmed candidate IDs and material proof-gap IDs that control it. Do not convert `deferred` into `confirmed`, or absence of evidence into `ready`, simply to produce a decisive answer.

## Handoff Boundary

For mixed review-and-fix requests, hand off only confirmed findings and explicitly accepted deferred-risk work. Include candidate IDs, safe evidence locators, desired postcondition, implementation owner, and checks to rerun. Do not edit, exploit, probe, rotate, revoke, delete, or mutate anything under this evidence contract or the `security-preflight` skill.
