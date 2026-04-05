# Validation Cases

Use these cases to verify that `api-terms-checker` triggers on current third-party API or SaaS terms questions and stays out of adjacent compliance or legal work.

## Acceptance Boundary

The skill should trigger when the user needs a current, source-backed check of practical usage restrictions for a third-party API or SaaS, especially before integration or launch.

The skill should stay out when the request is really about:

- open-source dependency licensing
- full repository release readiness
- negotiated legal advice
- general vendor comparison with no terms focus

## Positive Cases

| Prompt | Expected Trigger Behavior | Expected Outcome |
| --- | --- | --- |
| "Can we use the OpenAI API inside a paid SaaS product and resell the feature to customers?" | Trigger `api-terms-checker` | Checks current official terms, identifies resale or pass-through constraints, and separates verified facts from inference. |
| "Before we integrate Anthropic, I want to know whether their terms say anything about training our own models on outputs." | Trigger `api-terms-checker` | Reviews current official terms and highlights model-training or model-improvement clauses. |
| "We want to embed a third-party transcription API in our enterprise product. What terms should we check before launch?" | Trigger `api-terms-checker` | Produces a practical clause checklist and flags what still needs human review. |
| "Can our internal ops team use this SaaS with customer data, or are there obvious retention and privacy concerns in the vendor docs?" | Trigger `api-terms-checker` | Focuses on official privacy and terms docs and summarizes practical operational constraints. |
| "Please verify the current acceptable use restrictions for this image API before we let users generate marketing creatives with it." | Trigger `api-terms-checker` | Identifies prohibited use categories and any ambiguous restrictions from current official sources. |

## Negative Cases

| Prompt | Expected Trigger Behavior | Expected Outcome |
| --- | --- | --- |
| "Check whether our npm dependencies include GPL or AGPL packages." | Do not trigger `api-terms-checker` | Route to a dependency or repository compliance skill instead. |
| "Review this repository and tell me if it is ready to open-source." | Do not trigger `api-terms-checker` | Route to `repo-compliance-preflight`. |
| "Write legal fallback language for our MSA." | Do not trigger `api-terms-checker` | Reject as negotiated legal drafting outside scope. |
| "Which vector database vendor should we choose for performance and price?" | Do not trigger `api-terms-checker` unless the user explicitly narrows to terms | Treat as product or vendor comparison, not terms review. |
| "Explain what MIT and Apache-2.0 licenses mean for our mobile app." | Do not trigger `api-terms-checker` | Route to a license-focused skill rather than API terms review. |

## Overlap Cases

| Prompt | Expected Trigger Behavior | Expected Outcome |
| --- | --- | --- |
| "We use three APIs in this repo. Check whether any of their terms could block public release." | Borderline: trigger `repo-compliance-preflight` first | Repo-level release framing makes this a preflight audit with API terms as one sub-check. |
| "I copied a code snippet from a vendor SDK example. Is that allowed?" | Borderline: do not trigger `api-terms-checker` by default | This is closer to source reuse or repository compliance than service terms review. |
| "Can we ship this plugin if it depends on a hosted LLM API with nonstandard usage restrictions?" | Borderline: trigger `repo-compliance-preflight` or use both sequentially | Preflight owns the release decision, while terms checking can support it. |

## Release Recommendation Rules

- Ready if the skill clearly triggers on current API terms questions and rejects repo-level or OSS-license requests.
- Needs clarification if reviewers cannot tell when a SaaS question is really a broader release audit.
- Too broad if it starts answering dependency license or repository publication questions directly.
