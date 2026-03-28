---
name: "web-researcher"
description: "Use when the user wants a current, source-backed answer or brief that must start from current web research rather than memory alone, but the task is not specialized enough for `domain-researcher`, not a product decision for `product-designer`, and not limited to extracting one provided page like `web-content-distiller`."
compatibility: "Requires internet access and a browsing-capable Codex environment because this skill must browse current web sources before answering."
---

# Web Researcher

Research current topics without drifting into deeper domain analysis, product design, or single-page extraction. Start with current web research, keep the source set small and relevant, and return a concise answer with links, dates, and uncertainty.

Use this skill when the user needs:

- a current answer grounded in live web evidence
- to compare a small set of current options, policies, products, or announcements
- to get a concise source-backed brief on a topic that does not need a specialized domain deep dive
- to verify claims that are likely to have changed since model training

## Do Not Use For

- specialized technical, regulatory, academic, or standards-heavy research that belongs in `domain-researcher`
- product direction, feature design, or market-position decisions that belong in `product-designer`
- extracting or cleaning one specific page or URL that belongs in `web-content-distiller`
- local codebase work or documentation review that can be answered without browsing

## Workflow

1. Frame the research question before searching:
   - Identify the exact question, comparison, or decision support needed.
   - Decide what the output should be: direct answer, short comparison, or compact brief.
   - Stop if the request is actually asking for deep domain synthesis, product design, or page distillation.

2. Gather current evidence first:
   - Do not answer from memory when the request depends on current facts.
   - Prefer official sites, vendor docs, standards bodies, primary reporting, and other first-party material.
   - Use secondary sources only when they add context or help locate primary sources.

3. Keep the evidence set small and useful:
   - Gather only the sources needed to answer the question confidently.
   - Prefer 3-6 strong sources over a long list of weak links.
   - Capture exact dates for claims about releases, pricing, policy, personnel, schedules, or other unstable facts.

4. Synthesize into the narrowest defensible answer:
   - Lead with the answer, not the research trail.
   - Separate verified facts from inference.
   - If comparing options, use the same criteria for each option and call out what remains unclear.

5. Report a brief with source hygiene:
   - Include links for the claims that matter.
   - Name uncertainty plainly when evidence is weak, conflicting, or stale.
   - If the evidence is insufficient, say what was found and why it does not fully answer the question.

6. Keep the skill within the generic web research boundary:
   - Use `domain-researcher` when the topic becomes specialized and evidence-heavy.
   - Use `product-designer` when the output must become a product recommendation or feature direction.
   - Use `web-content-distiller` when the user mainly needs a provided page converted into clean reading input.

## Output Expectations

- Lead with the shortest defensible answer to the user's question.
- Include source links for the claims that matter.
- Use exact dates for recent or unstable facts.
- Mark inference explicitly instead of blending it into fact.
- End with the remaining uncertainty or the next most useful check when the answer is incomplete.

## Guardrails

- Do not skip current web research when the request is current or unstable.
- Do not turn a short research task into a broad literature review.
- Do not present weakly supported inference as confirmed fact.
- Do not overquote sources when concise paraphrase is enough.
- Do not duplicate the jobs of `domain-researcher`, `product-designer`, or `web-content-distiller`.
