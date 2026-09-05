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
| "Our Japanese enterprise entity has a negotiated DPA and paid plan. Can we process EU customer data with this vendor's API?" | Trigger `api-terms-checker` | Freezes entity, plan, region, public terms, DPA/negotiated-document precedence, and unknowns before interpreting the use. |

## Negative Cases

| Prompt | Expected Trigger Behavior | Expected Outcome |
| --- | --- | --- |
| "Check whether our npm dependencies include GPL or AGPL packages." | Do not trigger `api-terms-checker` | Route to a dependency or repository compliance skill instead. |
| "Review this repository and tell me if it is ready to open-source." | Do not trigger `api-terms-checker` | Route to `reviewer` for compliance preflight. |
| "Write legal fallback language for our MSA." | Do not trigger `api-terms-checker` | Reject as negotiated legal drafting outside scope. |
| "Which vector database vendor should we choose for performance and price?" | Do not trigger `api-terms-checker` unless the user explicitly narrows to terms | Treat as product or vendor comparison, not terms review. |
| "Explain what MIT and Apache-2.0 licenses mean for our mobile app." | Do not trigger `api-terms-checker` | Route to a license-focused skill rather than API terms review. |

## Overlap Cases

| Prompt | Expected Trigger Behavior | Expected Outcome |
| --- | --- | --- |
| "We use three APIs in this repo. Check whether any of their terms could block public release." | Borderline: trigger `reviewer` first | Repo-level release framing makes this a compliance preflight audit with API terms as one sub-check. |
| "I copied a code snippet from a vendor SDK example. Is that allowed?" | Borderline: do not trigger `api-terms-checker` by default | This is closer to source reuse or repository compliance than service terms review. |
| "Can we ship this plugin if it depends on a hosted LLM API with nonstandard usage restrictions?" | Borderline: trigger `reviewer` or use both sequentially | Compliance preflight owns the release decision, while terms checking can support it. |

## Worked Classification Cases

These clauses and contexts are synthetic fixtures, not real vendor terms or legal advice. Classify only the stated use; do not carry these permissions or restrictions into a real service review. Unless a row says otherwise, assume Customer A contracts with Provider B on the paid Pro plan in Japan, synthetic terms version 1 is current and applicable, and no other incorporated documents or negotiated overrides apply.

| Case and Intended Use | Evidence Clause | Expected Classification and Reason | Next Check |
| --- | --- | --- | --- |
| Explicit permission: incorporate API outputs into a paid customer-facing application and deliver those outputs to customers. | "Pro customers may incorporate API outputs into paid applications and redistribute those outputs to their customers." | `allowed` for the stated use: both paid embedding and output redistribution are expressly permitted under the assumed governing terms. | Confirm the actual use stays within output delivery; a real review must verify current official terms and applicable overrides before reusing this conclusion. |
| Missing evidence: redistribute outputs to customers; an enterprise order form governs this account but has not been supplied. | "Commercial use is permitted. Output redistribution is governed by the customer's order form." | `needs-review`: commercial-use permission does not establish redistribution rights, and the controlling document is missing. | Obtain the applicable order form and confirm its redistribution clause and precedence; leave the decision unresolved until that evidence is available. |
| Explicit prohibition: sell customers copies of the account's API credentials. | "Customers must not resell, sublicense, or distribute API credentials to third parties." | `restricted`: the planned credential resale directly matches the express prohibition. | Change the design to avoid credential resale or obtain an applicable written amendment before proceeding; do not assume one exists. |

Check each case independently for the expected classification, supporting clause, assumptions, and next check. Passing the routing cases alone does not validate these judgments.

## Release Recommendation Rules

- Ready if the skill clearly triggers on current API terms questions and rejects repo-level or OSS-license requests.
- Needs clarification if reviewers cannot tell when a SaaS question is really a broader release audit.
- Too broad if it starts answering dependency license or repository publication questions directly.
- Incomplete if it gives a conclusion without identifying the governing entity, plan, region, effective version, and possible negotiated override, or without making those gaps explicit assumptions.
