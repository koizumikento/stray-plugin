---
name: "security-preflight"
description: "Use when the user wants a security-focused preflight, audit, or review of a repository, diff, pull request, app, API, CI/CD workflow, release surface, dependency set, infrastructure-as-code, container setup, or secret-handling posture before shipping or publishing. Do not use for exploit execution, penetration testing, incident response, legal/compliance advice, implementing fixes without a review request, or broad non-security code review."
compatibility: "Repository access is required. Internet or connected GitHub/cloud tools are useful for current advisories and hosted settings, but local static evidence must be separated from external or unverified evidence."
---

# Security Preflight

Run a focused security preflight for software work before it ships, merges, or is published. Treat this as a bounded risk review: find concrete security issues, state what was checked, preserve secrets, and separate repository evidence from settings or runtime state that require external verification.

Use this skill when the user asks for a security review, security preflight, secret check, release security check, CI/CD security check, supply-chain check, dependency vulnerability preflight, IaC security pass, container hardening pass, or "is this safe to ship?" security-focused review.

## Do Not Use For

- General code review where security is only one incidental concern; use `reviewer`.
- Implementing fixes before presenting findings; use the relevant builder after the review if the user asks for fixes.
- API or SaaS terms, commercial-use, privacy-policy, or data-processing terms review; use a terms/compliance skill.
- Formal penetration testing, active scanning of systems, exploit execution, credential validation, incident response, or forensic investigation.
- Jurisdiction-specific legal, regulatory, certification, or audit-signoff advice.

## Reference Selection

Load only the smallest reference set that matches the scope:

- `references/application.md`: app, API, auth, authorization, sessions, input handling, SSRF, uploads, errors, and logs.
- `references/secrets-and-data.md`: secrets, credentials, `.env`, PII, telemetry, logs, backups, exports, and rotation guidance.
- `references/supply-chain.md`: dependency manifests, lockfiles, SCA, SBOM, package publishing, provenance, signing, and malicious package risk.
- `references/ci-cd.md`: GitHub Actions, workflow permissions, `pull_request_target`, third-party actions, OIDC, artifacts, protected environments, and release attestations.
- `references/infra-containers.md`: Terraform/IaC, cloud IAM, public exposure, network rules, Dockerfiles, images, and Kubernetes manifests.

Use the relevant existing `reviewer` references only for non-security review dimensions that the user explicitly includes.

## Workflow

1. Define the review scope before inspecting details.
   - Identify whether the target is a diff, branch, pull request, repository, release surface, app/API, CI/CD workflow, dependency set, IaC, container setup, or secret-handling posture.
   - Name the intended audience, environment, data sensitivity, and deployment or publication path when known.
   - If the scope is too broad for reliable coverage, narrow it explicitly and state exclusions.

2. Establish the evidence boundary.
   - Separate local repository evidence, command output, connected GitHub/project settings, connected cloud/runtime settings, and user-provided claims.
   - Do not infer hosted settings such as branch protection, secret scanning, cloud IAM usage, or deployment approvals from YAML alone.
   - Mark unavailable hosted settings or runtime state as unverified, not safe.

3. Load the matching reference files.
   - For an app or API, start with `application.md`.
   - For any repository or release review, include `secrets-and-data.md` and `supply-chain.md` unless clearly irrelevant.
   - For `.github/workflows`, deployment, release, or package publishing, include `ci-cd.md`.
   - For Terraform, cloud policy files, Dockerfiles, Compose, Helm, Kustomize, or Kubernetes manifests, include `infra-containers.md`.

4. Inspect from highest-risk boundaries first.
   - Check authentication, authorization, tenant/object ownership, secrets, privileged CI paths, release credentials, dependency risks, public exposure, and destructive or externally reachable workflows before style or hygiene.
   - Prefer structured parsers or project-native tools where available; use `rg` for targeted static searches.
   - If running scanners such as CodeQL, Semgrep, OSV-Scanner, npm audit, pip-audit, trivy, checkov, tfsec, or OpenSSF Scorecard, report the exact command and scope.

5. Protect secrets and sensitive data throughout the review.
   - Never print, quote, validate, call, or reuse discovered secret or PII values.
   - Report only the secret type, file path, line number when safe, variable/key name, and remediation direction.
   - If a committed secret is suspected, treat it as compromised and recommend revoke/rotate plus history/log/artifact review by the owner.

6. Classify findings by decision impact.
   - Use Critical for likely credential exposure, privileged untrusted-code execution, unauthenticated sensitive access, tenant breakout, or public exposure of sensitive data.
   - Use High for broad authorization gaps, dangerous CI permissions, unpinned third-party workflow actions in privileged paths, long-lived deploy credentials, exploitable injection patterns, or public admin/storage/network exposure.
   - Use Medium for missing hardening, weak evidence, stale dependency hygiene, missing automated checks, or safeguards that are present but incomplete.
   - Use Low for narrow hygiene issues that improve posture but do not materially affect the current ship decision.

7. Produce a findings-first preflight result.
   - Start with findings ordered by severity and grounded in concrete files, lines, settings, commands, or missing evidence.
   - Then list unverified areas, assumptions, and required human or external verification.
   - End with a practical recommendation: ready, ready with fixes, hold, or needs specialist sign-off.

## Output Expectations

- Scope reviewed, evidence sources used, and references loaded.
- Findings first, each with severity, evidence, impact, and smallest reasonable remediation direction.
- Secret/PII findings redacted by design.
- Commands or scanners run, skipped, unavailable, or intentionally avoided.
- Clear separation between confirmed findings, unverified settings, and specialist-review items.
- Ship recommendation: ready, ready with fixes, hold, or needs specialist sign-off.

## Guardrails

- Do not claim the artifact is secure, compliant, certified, penetration-tested, or audit-passed.
- Do not execute exploits, active probes, credential checks, login attempts, cloud mutations, destructive commands, or production scans.
- Do not call external services with discovered tokens, keys, cookies, credentials, or private URLs.
- Do not expose secret or PII values in final answers, comments, logs, screenshots, PR descriptions, or issue text.
- Do not automatically revoke, rotate, delete, rewrite history, change branch protection, change cloud IAM, or publish artifacts unless the user explicitly asks after the review.
- Do not treat scanner output as complete coverage; note false-positive, false-negative, reachability, and runtime-state limits.
- Route cryptographic design, business authorization policy, formal compliance, legal interpretation, active incident response, and production penetration testing to qualified human review.
