---
name: "repo-compliance-preflight"
description: "Use when the user wants a practical preflight check before publishing, open-sourcing, distributing, or broadly sharing a repository, package, app, or integration, with focus on obvious compliance gaps such as missing license files, attribution or notice obligations, third-party terms dependencies, and release-facing documentation gaps. Do not use for negotiated legal advice, deep security audits, or narrow API terms questions that belong to `api-terms-checker`."
---

# Repo Compliance Preflight

Run a practical compliance preflight on a repository before release or broader distribution. Focus on the minimum set of issues that are easy to miss but expensive to discover after publication.

Use this skill when the user wants to:

- check whether a repo looks ready to publish or open-source
- find missing license, notice, attribution, or third-party dependency disclosures
- identify external services or assets whose terms may affect release
- review release-facing docs for obvious compliance blind spots
- create a punch list before a legal, security, or partner review

## Do Not Use For

- negotiated legal advice or jurisdiction-specific interpretation
- a deep dependency license audit across every transitive package
- vulnerability scanning or security review
- a single external API terms question without repo-level release context
- brand strategy or general documentation polish unrelated to compliance

## Workflow

1. Define the release surface.
   - identify what is being shared: repo, package, plugin, app, docs bundle, or internal tool
   - note whether the target is public open source, customer delivery, marketplace publication, or internal distribution
   - identify any hosted APIs, models, datasets, images, fonts, or copied third-party code involved
2. Inspect the repository for obvious compliance artifacts.
   - `LICENSE`, `NOTICE`, `README`, contribution docs, privacy or terms docs, attribution files, and release notes
   - package metadata that references license or publisher information
   - docs that describe third-party integrations or bundled assets
3. Check for common release blockers.
   - missing or unclear project license
   - copied third-party code or assets without visible attribution
   - external APIs or models whose usage terms could constrain distribution
   - generated outputs or bundled data whose reuse terms are unclear
   - marketplace or plugin metadata that overstates what the artifact can do safely
4. Classify findings by actionability.
   - ready as-is
   - add a file, notice, or attribution
   - confirm a third-party term before release
   - escalate for legal or policy review
5. Produce a short preflight punch list.
   - highest-risk issues first
   - then moderate gaps
   - then optional cleanup that improves clarity
6. Stop at the preflight boundary.
   - identify missing information
   - point to follow-up skills or reviewers when deeper analysis is needed

## Output Expectations

- the release target and assumptions
- the files or artifacts inspected
- the main compliance gaps or confirmations
- a prioritized punch list
- the items that still need human review

When useful, include:

- a simple table of issue, why it matters, and next action
- a release recommendation such as ready, ready with fixes, or hold pending review

## Guardrails

- Do not present this as legal advice.
- Do not claim a repository is fully compliant; keep the scope to practical preflight checks.
- Do not turn this into a security or dependency vulnerability audit.
- Do not assume a dependency license audit is complete unless the user explicitly asks for one.
- Do not ignore copied assets, fonts, screenshots, or datasets just because source code licensing looks fine.
- Do not skip third-party terms when the repo depends on external APIs or platforms to function.
