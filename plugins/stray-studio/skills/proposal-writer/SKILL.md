---
name: "proposal-writer"
description: "Use when the user needs a proposal, business case, plan, or memo asking a decision-maker for approval, funding, permission, or commitment, with evidence status and an approval path. Do not use for articles, operational runbooks, research-only work, or brainstorming without a decision target."
---

# Proposal Writer

Turn an input brief, rough notes, or a conversation into a decision-oriented document that helps the reader approve, fund, endorse, or otherwise say yes. Keep the work centered on the audience, the decision being requested, the best argument order, and the most likely objections.

Use this skill when the user wants to:

- draft a proposal, plan, memo, business case, or recommendation for approval
- turn scattered notes into a structured document that supports a decision
- sharpen a draft so it is easier to review, approve, or discuss
- compare options and recommend one with clear reasoning

## Do Not Use For

- publishable articles, blog posts, newsletters, or editorial writing
- marketing copy where the primary goal is attention or brand voice
- pure brainstorming with no decision, approval, or recommendation target
- factual research as the main deliverable
- operational runbooks or step-by-step process documentation
- proposal context whose main need is Japanese government-backed policy framing, official documents, whitepaper evidence, ministry ownership, or public-sector sales positioning; use `japan-gov-proposal-context-adapter`

## Workflow

1. Frame the decision before writing.
   - Identify the decision owner or approval body, the exact approval or commitment requested, the proposer or next-step owner, and the decision deadline or review window.
   - Identify the context, constraints, urgency, budget, authority boundary, and timing assumptions.
   - If the main gap is Japanese government-backed proposal context rather than drafting the decision document itself, defer to `japan-gov-proposal-context-adapter` before writing.
   - If the brief is underspecified, ask focused clarification questions that unblock the decision target first.

2. Choose the argument strategy.
   - Decide whether the document should lead with the recommendation, the problem, the opportunity, or the risk.
   - Identify the strongest proof points and the objections most likely to come up.
   - If there are multiple viable paths, compare them explicitly and explain why the recommended one is preferred.
   - Maintain a compact evidence ledger that labels material claims as verified, user-provided but unverified, assumption, estimate, or unresolved; do not flatten those states into equally certain prose.

3. Build the structure around the reader.
   - Use a sequence that fits the audience's decision process, not the author's notes.
   - Keep the request, rationale, tradeoffs, and next step easy to scan.
   - Make the recommendation unambiguous.

4. Draft for persuasion and clarity.
   - State the decision being requested early.
   - Keep paragraphs short and concrete.
   - Use plain language, specific outcomes, and explicit tradeoffs.
   - Surface risks and objections instead of hiding them.

5. Tighten the approval path.
   - Check that the recommendation matches the evidence and constraints.
   - Remove side tangents, repeated points, and unsupported claims.
   - Make the first action after approval obvious, including who acts, what happens, and by when. Name what happens if the decision is deferred or rejected when that matters.

6. Deliver in the requested format.
   - Match the requested output shape, such as full draft, outline, revision, or a few title options plus draft.
   - Include assumptions only when they materially affect the draft.
   - Keep the final document centered on the decision, not on the writing process.

## Output Expectations

- A clear proposal, plan, memo, or business case in the requested tone and length
- An explicit decision request or recommendation
- The decision owner, requested approval, decision deadline/window, and first action after approval
- Evidence status for material claims, estimates, and assumptions
- A structure that fits the audience and approval context
- Clear treatment of options, objections, risks, and tradeoffs when relevant
- A concrete next step or call to action
- Minimal unsupported claims and no invented facts

## Guardrails

- Do not turn the task into article writing or editorial rewriting.
- Do not bury the recommendation beneath background material.
- Do not omit objections or tradeoffs when they matter to the decision.
- Do not overcomplicate the structure if a short decision memo will do.
- Do not invent facts, approvals, metrics, or commitments.
- Do not present assumptions, estimates, or user-provided claims as independently verified evidence.
- Do not ask open-ended clarification questions without also proposing a reasonable default direction.
