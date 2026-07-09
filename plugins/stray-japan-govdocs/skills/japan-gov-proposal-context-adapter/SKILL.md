---
name: "japan-gov-proposal-context-adapter"
description: "Use when the user wants a product, service, or initiative synthesized into 官公庁向け提案・企画書 context. Do not use for neutral background, a direct document summary, or procurement/legal advice."
---

# Japan Gov Proposal Context Adapter

Synthesize verified government context into a proposal argument while keeping official claims distinct from proposal-specific adaptation.

## Do Not Use For

- Neutral 課題背景 only; use `japan-gov-background-builder`.
- Reading a named whitepaper as the primary object; use `japan-whitepaper-brief`.
- Eligibility, application, procurement, or legal conclusions.

## Workflow

1. Define the offer, target public body/stakeholder, desired decision, delivery context, and claims the proposal needs to make.
2. Assemble upstream evidence rather than recreating every search inside this skill:
   - neutral context from `japan-gov-background-builder`;
   - claim-level support from `japan-gov-evidence-finder`;
   - owner roles from `japan-gov-owner-mapper`;
   - current emphasis from `japan-gov-priority-checker`;
   - budget status only when needed from `japan-gov-budget-tracer`.
   Invoke missing components in the same task, then synthesize their outputs.
3. Create a traceability map from each proposal statement to an official source or label it clearly as the user's hypothesis/offer.
4. Separate:
   - `政府資料が明示すること`;
   - `提案への適用・解釈`;
   - `未検証の前提`;
   - `政府資料が支持しないこと`.
5. Draft source-faithful wording for problem, policy relevance, proposed contribution, outcomes, and limitations. Include a safer alternative for any overclaim.
6. Stop before procedural, eligibility, or procurement claims. If the offer or target is too underspecified to adapt responsibly, state assumptions and provide only a provisional frame.

## Output

- `提案で使う政策文脈`
- `政府資料ベースの課題設定`
- `提案への接続とtraceability`
- `公式記述／適用解釈／未検証前提`
- `根拠資料`
- `言い過ぎになる表現と安全な言い換え`
- `次に必要な制度・予算・調達確認`

## Guardrails

- Do not imply government endorsement, product necessity, funding eligibility, or procurement fit.
- Do not use general policy language as proof that the proposed solution will work.
- Keep neutral source findings intact when adapting them for persuasion.
