# Secrets And Data Exposure Checks

Use this reference for credentials, private configuration, logs, telemetry, backups, exports, dumps, and sensitive data handling.

## Review Focus

1. Secret inventory and repository exposure.
   - Look for API keys, PATs, SSH keys, private keys, signing secrets, webhook secrets, database URLs, cloud credentials, service-account files, `.env`, config files, and credential archives.
   - Check `.gitignore`, `.env.example`, config examples, Docker/Compose/Kubernetes manifests, Terraform variables, CI env blocks, and generated artifacts.

2. Secret scanning posture.
   - If connected GitHub context is available, check whether secret scanning, push protection, custom patterns, and alert handling are configured.
   - Distinguish provider-pattern findings, generic-pattern findings, and custom-pattern findings.
   - Treat all committed secrets as potentially compromised regardless of whether a scanner can validate them.

3. CI/CD and runtime secret handling.
   - Confirm long-lived credentials are avoided where OIDC or trusted publishing can be used.
   - Check token scopes, environment-specific secrets, protected environments, and whether secrets can reach fork PRs or untrusted code.
   - Review shell steps for accidental `echo`, artifact, cache, or debug-log exposure.

4. Logging and telemetry.
   - Search for request/response dumps, exception dumps, `console.log`, `logger`, `print`, `debug`, `trace`, OpenTelemetry attributes, analytics payloads, and audit-log emitters.
   - Ensure tokens, passwords, cookies, session IDs, connection strings, encryption keys, private URLs, and unnecessary PII are redacted, hashed, truncated, or omitted.
   - Prefer allowlist telemetry collection over broad capture and later redaction.

5. Backups, exports, and retained artifacts.
   - Look for `.sql`, `.dump`, `.bak`, `.zip`, `.tar`, `.csv`, `.jsonl`, logs, screenshots, traces, and exported reports.
   - Report sensitive-looking artifacts without quoting contents.
   - Check retention, encryption, access control, and deletion guidance when configuration is present.

## Safe Reporting

- Report secret findings as type, path, line number when safe, variable/key name, and remediation.
- Do not include secret values, token prefixes longer than necessary, full fingerprints, private URLs, personal data, or copied log content.
- Recommended remediation language: remove from source, revoke/rotate, invalidate sessions if relevant, purge logs/artifacts if needed, move to a secret manager, reduce scope, enable scanning/push protection, and add safe examples.

## Do Not Do

- Do not validate a secret by calling an API or logging in.
- Do not read or summarize whole private keys, `.env` files, credential JSON, database dumps, or personal data records.
- Do not rewrite git history, delete artifacts, revoke tokens, rotate secrets, or mutate secret stores without explicit user instruction after the review.
- Do not assume a secret is harmless because it is expired, test-looking, or in a private repository.

## Useful Source Baselines

- OWASP Secrets Management Cheat Sheet.
- OWASP Logging Cheat Sheet.
- GitHub Secret Scanning and alert-resolution docs.
- GitHub Actions secure-use and OIDC docs.
- AWS Secrets Manager, Google Secret Manager, Azure Key Vault docs.
- OpenTelemetry sensitive data guidance.
