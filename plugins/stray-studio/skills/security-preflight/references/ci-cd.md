# CI/CD Security Checks

Use this reference for GitHub Actions, release workflows, deployment workflows, package publishing, workflow permissions, and CI artifacts.

## Review Focus

1. Workflow permissions.
   - Check top-level and job-level `permissions`.
   - Flag missing explicit permissions, `write-all`, broad `contents: write`, and write permissions in PR-triggered jobs.
   - Allow job-level elevation only for a specific release, deployment, attestation, or publishing job with clear need.

2. `pull_request_target` and untrusted code.
   - Treat `pull_request_target` plus checkout of PR head code plus build/test/script execution as Critical when secrets, write tokens, OIDC, cache, artifact, or release behavior can be reached.
   - Prefer splitting untrusted `pull_request` validation from privileged `workflow_run` or maintainer-approved workflows.
   - Treat artifacts from untrusted workflows as untrusted inputs.

3. Third-party actions and reusable workflows.
   - Enumerate `uses:`.
   - Recommend full-length commit SHA pinning for third-party actions and reusable workflows in privileged paths.
   - Pair SHA pinning with update automation and maintainer trust review; SHA pinning is not a safety guarantee.

4. Secrets, OIDC, and publishing credentials.
   - Search for `secrets.*`, token-like env names, cloud keys, PATs, and package-publish tokens.
   - Prefer OIDC/trusted publishing over long-lived credentials.
   - Check that `id-token: write` is limited to jobs that need OIDC, attestations, or trusted publishing, and is not used with untrusted code execution.

5. Artifacts and caches.
   - Check `upload-artifact` paths for `.` or `**`, hidden files, `.env`, keys, `.git`, logs, and workspace-wide uploads.
   - Check `retention-days`, artifact consumption by privileged jobs, and `download-artifact` followed by execution.
   - Review cache keys and restore keys for cache poisoning or cross-trust-boundary reuse.

6. Branch protection, rulesets, and workflow ownership.
   - YAML cannot prove branch protection. Use connected GitHub settings or mark as unverified.
   - Check CODEOWNERS coverage for `.github/workflows`, required reviews, required checks, no force-push/delete, bypass restrictions, and unique job names when settings are available.

7. Deployment environments and release provenance.
   - Check `environment:` usage for staging/production deploy jobs.
   - Verify required reviewers, prevent self-review, branch/tag restrictions, and environment secrets when connected settings are available.
   - For release artifacts, check SBOM, digest, signing, artifact attestations, `attestations: write`, and verification instructions.

8. Runners and execution isolation.
   - Flag `runs-on: self-hosted`, especially in public repositories, PR-triggered workflows, deploy jobs, or jobs with secrets.
   - Treat public repo plus self-hosted runner plus PR trigger as Critical unless proven isolated and safe.

## Severity Defaults

- Critical: `pull_request_target` executing PR head code with secrets/write/OIDC; `permissions: write-all` in untrusted paths; public repo self-hosted runner on PR triggers.
- High: unpinned third-party actions in privileged paths; long-lived deploy credentials; broad artifact upload; release/deploy without protected environment; missing top-level permissions.
- Medium: missing artifact retention; no CODEOWNERS for workflows; no CodeQL/dependency review/Scorecard; no SBOM/provenance for release artifacts.

## Guardrails

- Do not run untrusted workflows or scripts to reproduce a CI issue.
- Do not expose secrets from logs or artifacts.
- Do not mutate branch protection, environment protection, secrets, runners, or publishing settings during a review-only task.
- Separate YAML-visible facts from GitHub-hosted settings and operations that require organization access.

## Useful Source Baselines

- GitHub Actions secure-use reference.
- GitHub workflow syntax for `permissions`.
- GitHub Security Lab guidance on preventing unsafe `pull_request_target` use.
- GitHub artifact attestations and `actions/attest`.
- OpenSSF Scorecard.
- SLSA and `slsa-verifier`.
- NIST SSDF and NIST SP 800-204D for DevSecOps CI/CD supply-chain security.
