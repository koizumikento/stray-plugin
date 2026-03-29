# Validation Cases

Use these cases to verify that `repo-compliance-preflight` triggers on practical release-readiness checks for repositories and does not overtake narrow API terms or deep legal review work.

## Acceptance Boundary

The skill should trigger when the user wants a repository-level preflight before publishing, open-sourcing, distributing, or broadly sharing code, assets, docs, plugins, or packages.

The skill should stay out when the request is really about:

- a single vendor's current API or SaaS terms
- deep transitive dependency license analysis
- security or vulnerability review
- negotiated legal interpretation

## Positive Cases

| Prompt | Expected Trigger Behavior | Expected Outcome |
| --- | --- | --- |
| "Before we open-source this repo, check for obvious license, attribution, and third-party release gaps." | Trigger `repo-compliance-preflight` | Reviews visible repo artifacts and returns a prioritized preflight punch list. |
| "We're about to publish this Codex plugin. What compliance files or notices might be missing?" | Trigger `repo-compliance-preflight` | Checks release-facing files, plugin metadata, and obvious third-party dependency disclosures. |
| "Can you do a release preflight on this package before we ship it to customers?" | Trigger `repo-compliance-preflight` | Identifies blockers such as missing `LICENSE`, missing notice language, or unclear third-party dependencies. |
| "This repo bundles screenshots, fonts, and an external API integration. Tell me what we should verify before distribution." | Trigger `repo-compliance-preflight` | Includes non-code assets and external terms in the release checklist. |
| "We want to share this internal tool with another team. Please do a quick compliance preflight first." | Trigger `repo-compliance-preflight` | Produces a practical readiness check even for internal distribution. |

## Negative Cases

| Prompt | Expected Trigger Behavior | Expected Outcome |
| --- | --- | --- |
| "Check the latest OpenAI API terms for resale restrictions." | Do not trigger `repo-compliance-preflight` | Route to `api-terms-checker`. |
| "Scan every transitive package in package-lock.json and classify each license." | Do not trigger `repo-compliance-preflight` by default | Reject as a deeper dependency license audit than this skill owns. |
| "Find CVEs and dependency vulnerabilities before release." | Do not trigger `repo-compliance-preflight` | Route to a security or vulnerability workflow. |
| "Tell me whether this contract clause is enforceable in Germany." | Do not trigger `repo-compliance-preflight` | Reject as jurisdiction-specific legal advice. |
| "Rewrite our README to sound more polished." | Do not trigger `repo-compliance-preflight` | This is documentation editing, not compliance preflight. |

## Overlap Cases

| Prompt | Expected Trigger Behavior | Expected Outcome |
| --- | --- | --- |
| "This repo depends on two commercial APIs. Can we still release it publicly?" | Trigger `repo-compliance-preflight` first | Repo-level release framing makes this the owner; it may call for `api-terms-checker` as a sub-step. |
| "Check whether copied icons and fonts in this repo need attribution." | Trigger `repo-compliance-preflight` | Asset attribution belongs in release preflight even though it is not source-code licensing. |
| "Is our MIT license enough if we also bundle a proprietary SDK?" | Trigger `repo-compliance-preflight` | Evaluates the repo-level release picture rather than only the SDK terms. |

## Release Recommendation Rules

- Ready if the skill clearly owns repository-level release checks and defers narrow API terms questions.
- Needs clarification if reviewers cannot tell whether internal distribution counts as release surface.
- Too broad if it starts claiming complete legal compliance or full dependency license coverage.
