# Compliance Preflight

Use this reference when reviewing a repository, package, plugin, app, docs bundle, or internal tool before publishing, open-sourcing, distributing, or broadly sharing it.

## Review Focus

1. Define the distribution surface:
   - public open source, customer delivery, marketplace publication, internal distribution, or partner sharing
   - source code, docs, assets, fonts, screenshots, datasets, generated outputs, APIs, models, or SDKs included
2. Inspect obvious compliance artifacts:
   - `LICENSE`, `NOTICE`, `README`, contribution docs, privacy or terms docs, attribution files, and release notes
   - package metadata that references license or publisher information
   - docs that describe third-party integrations or bundled assets
3. Check common release blockers:
   - missing or unclear project license
   - copied third-party code or assets without visible attribution
   - external APIs, models, datasets, fonts, screenshots, or generated outputs with unclear reuse terms
   - marketplace or plugin metadata that overstates safe capabilities
4. Classify actionability:
   - ready as-is
   - add a file, notice, or attribution
   - confirm a third-party term before release
   - escalate for legal or policy review
5. Respect routing boundaries:
   - a single vendor API terms question belongs to a focused terms checker
   - deep transitive dependency license analysis is outside this preflight unless explicitly requested
   - vulnerability scanning is security review, not compliance preflight

## Output

- Release target and assumptions.
- Files or artifacts inspected.
- Main compliance gaps or confirmations.
- Prioritized punch list.
- Items that still need human, legal, procurement, or policy review.
- Recommendation: ready, ready with fixes, or hold pending review.

## Validation Cases

Positive cases:

- "Before we open-source this repo, check for obvious license, attribution, and third-party release gaps."
- "We're about to publish this Codex plugin. What compliance files or notices might be missing?"
- "Can you do a release preflight on this package before we ship it to customers?"
- "This repo bundles screenshots, fonts, and an external API integration. Tell me what we should verify before distribution."

Negative cases:

- "Check the latest OpenAI API terms for resale restrictions." Route to a terms checker.
- "Scan every transitive package in package-lock.json and classify each license." Treat as deeper license audit.
- "Find CVEs and dependency vulnerabilities before release." Route to security review.
- "Tell me whether this contract clause is enforceable in Germany." Decline legal advice.

## Guardrails

- Do not present this as legal advice.
- Do not claim the repository is fully compliant.
- Do not ignore copied assets, fonts, screenshots, or datasets just because source licensing looks fine.
- Do not skip third-party terms when the repo depends on external APIs or platforms to function.
