# Application Security Checks

Use this reference for web apps, APIs, full-stack features, backend services, and user-facing flows.

## Baseline Sources

- OWASP ASVS 5.0.0
- OWASP Top 10:2025
- OWASP API Security Top 10:2023
- OWASP Cheat Sheet Series
- OWASP Web Security Testing Guide
- NIST SSDF SP 800-218
- NIST SP 800-63B for authentication guidance when identity behavior is in scope

## Review Focus

1. Map the surface.
   - Identify routes, API handlers, server actions, background jobs, admin paths, webhooks, file upload/download paths, external URL fetchers, and data stores.
   - Note authentication mode, session/token type, tenant model, sensitive data classes, and externally reachable entry points.

2. Authentication and session management.
   - Check password or IdP flow, MFA assumptions, rate limiting, account enumeration, reset flow, session fixation, logout behavior, token lifetime, JWT verification, and cookie flags.
   - For cookies, look for `HttpOnly`, `Secure`, `SameSite`, domain/path scope, and secure invalidation behavior.
   - Do not test real accounts or enumerate users unless the user explicitly authorizes a safe test environment.

3. Authorization and object ownership.
   - Verify enforcement at the server-side boundary, not only UI visibility.
   - Look for BOLA/IDOR, missing tenant checks, missing owner checks, admin-only feature exposure, mass assignment, field-level authorization gaps, and stale authorization after refactors.
   - Treat business-rule authorization as a human-review boundary when the policy is not explicitly documented.

4. Input handling and injection.
   - Check schema validation, type coercion, boundary values, dangerous string concatenation, raw SQL, shell execution, template injection, unsafe deserialization, and dynamic path construction.
   - Prefer parameterized queries, ORM-safe APIs, contextual output encoding, safe templating, allowlists, and framework-native validators.
   - Do not treat input validation alone as XSS or SQL injection protection.

5. Browser and API protections.
   - Check CSRF protections for cookie-authenticated state changes, CORS allowlists, origin checks, CSP, HSTS, frame protections, and cache headers for sensitive content.
   - Look for unsafe DOM sinks such as `innerHTML`, inline scripts with untrusted data, and reflected user-controlled values.

6. SSRF and outbound fetches.
   - Search for URL import, webhook fetch, image/PDF fetch, proxy, metadata, and callback flows.
   - Check scheme allowlists, hostname/IP validation, private network blocking, DNS rebinding handling, redirect handling, timeouts, size limits, and response type restrictions.
   - Do not probe private networks, cloud metadata endpoints, or production URLs.

7. File upload and download.
   - Check extension allowlists, MIME distrust, magic/signature checks, size limits, storage isolation, random filenames, malware/CDR handoff, public URL exposure, and download authorization.
   - Avoid generating harmful payloads; use configuration and code evidence unless the user provides a safe test fixture.

8. Error handling, logging, and monitoring.
   - Check debug mode, stack traces, exception bodies, request/response dumps, and authz/authn audit events.
   - Ensure logs do not include passwords, tokens, cookies, API keys, private keys, session IDs, connection strings, or unnecessary PII.

## Common Evidence Searches

- Auth and session: `auth`, `session`, `jwt`, `cookie`, `csrf`, `sameSite`, `HttpOnly`, `Secure`
- Authorization: `authorize`, `permission`, `role`, `owner`, `tenant`, `admin`, `policy`
- Injection: `raw`, `query`, `execute`, `exec`, `spawn`, `innerHTML`, `dangerouslySetInnerHTML`, `eval`
- SSRF: `fetch`, `axios`, `request`, `http.get`, `url`, `webhook`, `callback`, `metadata`
- Uploads and logs: `upload`, `multipart`, `logger`, `console.log`, `print`, `debug`, `trace`

## Human Review Boundaries

- Threat modeling and abuse-case completeness.
- Cryptographic protocol design.
- Business authorization policy and role semantics.
- Production penetration testing or active security testing.
- Regulatory, legal, or contractual security obligations.
