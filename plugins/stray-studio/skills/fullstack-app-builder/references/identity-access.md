# Identity And Access Reference

Read this when changing authentication, credentials, sessions, access enforcement, or tenant isolation, or diagnosing stale permissions and account changes. Skip it for changes whose identity and access behavior is already settled. Keep business permission semantics in [application-architecture.md](application-architecture.md).

Sources were checked on 2026-09-08. Apply protocol requirements to the selected flow; check the installed provider/framework's current documentation for configuration and revocation guarantees. The workflow and failure cases below synthesize those sources for application work.

## Workflow

1. Map the actor and policy across entry points.
   - Identify user or service identity, tenant context where applicable, operation, resource, readable/writable fields, and relevant business state. Separate authentication, session continuity, authorization, and tenant selection.
   - Define default-deny and least-privilege behavior in existing policy code. Use roles, ownership, relationships, or attributes according to the actual rule; do not introduce a policy engine just to name these concepts. See [OWASP authorization](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html).
2. Establish identity and credential handling.
   - Reuse maintained authentication libraries and established protocols. For OIDC, map external identity using the issuer and subject (`iss`, `sub`); do not merge accounts solely by email. Keep ID Token and API Access Token purposes distinct. See [OIDC identity stability](https://openid.net/specs/openid-connect-core-1_0.html#ClaimStability).
   - For JWT credentials, verify signatures, allowed algorithms, issuer, audience, expiry, and intended token kind with trusted configuration. Do not trust decoded claims or token-supplied key URLs before validation. For opaque credentials, use the provider's validation contract instead of inventing JWT handling. See [JWT best practices](https://www.rfc-editor.org/rfc/rfc8725.html#section-3).
   - For OAuth/OIDC callbacks, verify the selected flow's redirect and request/response binding. Use PKCE for public-client Authorization Code flows; do not introduce the Resource Owner Password Credentials grant. See [OAuth security BCP](https://www.rfc-editor.org/rfc/rfc9700.html#section-2).
   - For browser apps, decide where tokens are held and used. An existing same-domain server session may suffice; consider a BFF when its token isolation addresses the app's threat model, without requiring a new service. Configure cookies with appropriate Secure, HttpOnly, SameSite, domain/path, and CSRF protections. HttpOnly/BFF does not prevent malicious same-origin JavaScript from acting through the user's browser. See [RFC 10017](https://www.rfc-editor.org/rfc/rfc10017.html), published August 2026.
   - For native OAuth, use an external user agent and PKCE; do not treat an embedded shared client secret as confidential. Follow platform storage and device-lock requirements: Apple Keychain can hold credentials; Android Keystore protects cryptographic keys rather than arbitrary token strings. See [native-app OAuth](https://www.rfc-editor.org/rfc/rfc8252.html), [Apple Keychain](https://support.apple.com/guide/security/keychain-data-protection-secb0694df1a/web), and [Android Keystore](https://developer.android.com/privacy-and-security/keystore).
3. Enforce access wherever protected data or effects can be reached.
   - Distinguish permission to invoke a function, access an object, and read or change its properties. Allowlist writable and returned fields; identifier complexity and hidden controls do not confer authorization. See [OWASP object-property authorization](https://owasp.org/API-Security/editions/2023/en/0xa3-broken-object-property-level-authorization/).
   - Put enforcement on a server or privileged boundary traversed by every relevant API, server action, platform bridge, and worker path. Reuse the existing shared policy, including cache-hit and bulk paths, and check permission against the actual target. A page-level check does not protect a separately callable action. See [Next.js action authorization](https://nextjs.org/docs/app/guides/data-security#authentication-and-authorization).
4. Define validity and revocation over time.
   - Separate app sessions, identity-provider sessions, access tokens, and refresh tokens. Specify timeout, reauthentication, logout, account disablement, membership changes, and the permitted delay before previously allowed operations are denied.
   - Invalidate the intended server-side authority as well as local credentials. Self-contained access tokens need a revocation mechanism or an explicitly bounded remaining lifetime; refresh-token revocation does not by itself promise immediate rejection of every issued access token. See [session lifecycle](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html) and [token revocation](https://www.rfc-editor.org/rfc/rfc7009.html#section-3).
5. Carry verified scope through storage and delayed work.
   - Treat client tenant IDs as selectors; verify current membership or service authority. Scope protected database, cache, search, file, signed-URL, job-result, and deduplication access to the authorized context. Keep intentionally global and cross-tenant paths explicit.
   - Include result-changing identity/tenant attributes in cache scope; authorize before protected cache reads. Choose permission invalidation separately from data freshness. A namespaced key or storage prefix is not an access check.
   - Authenticate the producer/broker path and re-establish context at a worker. Recheck time-sensitive authority when delay can stale the original decision. Decide whether a committed business operation continues under service authority after user revocation; do not assume every job must continue or cancel. See [tenant isolation and asynchronous work](https://cheatsheetseries.owasp.org/cheatsheets/Multi_Tenant_Security_Cheat_Sheet.html).
   - Use [data-persistence.md](data-persistence.md) for database enforcement and [async-workflows.md](async-workflows.md) for durable acceptance, replay, and recovery.
6. Coordinate identity changes with client state.
   - Use [client-state.md](client-state.md) when logout, account/tenant switching, or permission changes affect displayed data, drafts, persisted caches, subscriptions, or in-flight requests. Prevent an old context's completion from repopulating the new context.
   - Define the handling of unsent edits and already accepted work; do not silently submit one account's draft under another account. UI cleanup does not replace server-side denial.
7. Validate the affected boundaries, including allowed paths.
   - Choose relevant cases below and exercise the real enforcement paths and configured roles where feasible. Report the observed scope, revocation delay, and any unverified provider, device, or worker behavior; do not claim immediate revocation from a UI-only check.

| Case | Required observation |
|---|---|
| Valid login with another user's object, forbidden field, or privileged operation | Each applicable permission is enforced; allowed operations still succeed |
| Correctly signed credential with wrong issuer, audience, or token purpose | The credential is rejected for this flow |
| Old session/token after logout or permission change | Acceptance matches the declared revocation scope and delay |
| Account/tenant change while an old response is pending | Previous-context data and edits do not enter the new context |
| Membership revoked while a job waits | Execution follows the stated reauthorization, continuation, or cancellation rule |
| Cache hit, signed URL, job result, or reused database connection for another tenant | The same declared isolation boundary holds outside the ordinary API path |
