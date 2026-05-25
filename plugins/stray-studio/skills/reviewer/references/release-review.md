# Release Review

Use this reference when reviewing readiness to ship, publish, merge, distribute, or announce a change, package, plugin, app, or artifact.

## Review Focus

1. Define the release surface:
   - what is shipping
   - who receives it
   - where it is distributed
   - rollback or recovery options
2. Check blockers:
   - unresolved correctness, security, privacy, data, or compatibility risk
   - missing tests or validation evidence
   - missing docs, migration notes, changelog, or operator guidance
   - stale manifest, version, marketplace, or packaging metadata
   - secrets, credentials, private URLs, or unreviewed assets
3. Check sequencing:
   - migrations before code or code before migration
   - feature flags, rollout controls, cache invalidation, and backfills
   - downstream users, integrations, or docs that must be coordinated
4. Check communication:
   - release notes match actual behavior
   - limitations and known issues are visible
   - owner for follow-up monitoring is clear when needed

## Output

- Findings first, ordered by release impact.
- Recommendation: ready, ready with fixes, hold, or needs human sign-off.
- Required pre-ship actions and optional cleanup separated clearly.

## Guardrails

- Do not claim exhaustive security, legal, or QA coverage.
- Do not block on unrelated cleanup.
- Do not ignore operational sequencing when data, migrations, auth, or packaging are involved.
