# Supply Chain Security Checks

Use this reference for dependencies, package managers, vulnerability scanning, SBOMs, provenance, publishing, and malicious package risk.

## Review Focus

1. Dependency manifests and lockfiles.
   - Identify package ecosystems and lockfiles such as `package-lock.json`, `pnpm-lock.yaml`, `yarn.lock`, `poetry.lock`, `uv.lock`, `requirements*.txt`, `Pipfile.lock`, `go.sum`, `Cargo.lock`, and container base images.
   - Check that lockfiles are committed, current, and used in CI through frozen installs such as `npm ci` or equivalent.

2. Known vulnerabilities and SCA.
   - Prefer OSV, Dependabot, npm audit, pip-audit, cargo audit, govulncheck, trivy, or repo-native SCA.
   - Classify by package, version, affected range, fixed version, direct/transitive scope, production/dev scope, reachability when available, and exception rationale.
   - Do not claim completeness: SCA generally covers known vulnerabilities and may miss unknown malware, 0-days, or unreachable-code nuance.

3. SBOM and inventory.
   - Check whether CycloneDX or SPDX SBOMs are generated for release artifacts, containers, or shipped packages.
   - Check whether SBOMs are machine-readable, tied to a build/release, and usable for later vulnerability or VEX workflows.
   - Treat SBOM presence as inventory transparency, not a safety guarantee.

4. Malicious package and typosquatting risk.
   - Review newly added packages, similar names, low-history packages, suspicious install scripts, obfuscated code, unexpected network/file operations, sudden maintainer changes, and packages introduced shortly after publication.
   - Treat these signals as heuristic; escalate rather than declaring malicious without strong evidence.

5. Package publishing and provenance.
   - For npm, PyPI, container, or binary publishing, check trusted publishing/OIDC, short-lived credentials, 2FA, scoped tokens, provenance/attestations, signing, and verification guidance.
   - State clearly that provenance, signatures, and attestations prove origin or integrity properties, not that code is harmless.

6. Containers and base images.
   - Check base image pinning, digest use, image scanning, SBOM/provenance, unnecessary OS packages, and high/critical CVEs.
   - Pair this with `infra-containers.md` for Dockerfile hardening and runtime settings.

## Suggested Tools

- `osv-scanner` for multiple ecosystems and lockfiles.
- GitHub Dependabot alerts and dependency-review action when connected context exists.
- OpenSSF Scorecard for repository posture such as maintained, security policy, pinned dependencies, dangerous workflows, token permissions, and signed releases.
- `npm audit`, `pip-audit`, `cargo audit`, `govulncheck`, `trivy`, or project-native equivalents when already used by the repo.

## Guardrails

- Do not remove or upgrade dependencies automatically during a review-only task.
- Do not treat scanner output as final severity without checking exploitability, scope, environment, and fix availability.
- Do not recommend package deletion or publish blocking solely on typosquatting heuristics; recommend isolation and maintainer/security review.
- Do not create, reveal, or mutate publishing tokens.

## Useful Source Baselines

- NIST SSDF SP 800-218.
- CISA SBOM guidance and minimum elements.
- OpenSSF Scorecard.
- OpenSSF package repository security principles.
- SLSA.
- OSV-Scanner.
- GitHub Dependabot, code scanning, secret scanning, and Actions secure-use docs.
- npm and PyPI trusted publishing/provenance/attestation docs.
- NIST SP 800-190 for container security.
