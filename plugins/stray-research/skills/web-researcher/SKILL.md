---
name: "web-researcher"
description: "Use when the user wants a current, source-backed answer or brief that must start from live web research rather than memory alone, and no narrower research, product, terms, patent, news, MCP, GitHub-maintenance, or page-distillation skill owns the request."
compatibility: "Requires internet access and a browsing-capable Codex environment because this skill must browse current web sources before answering."
---

# Web Researcher

Research current topics without drifting into deeper domain analysis, product design, or single-page extraction. Start with current web research, keep the source set small and relevant, and return a concise answer with links, dates, and uncertainty.

Use this skill when the user needs:

- a current answer grounded in live web evidence
- to compare a small set of current options, policies, products, or announcements
- to get a concise source-backed brief on a topic that does not need a specialized domain deep dive
- to verify claims that are likely to have changed since model training
- to check a current fact quickly when no more specific local skill owns the task

## Do Not Use For

- specialized technical, regulatory, academic, or standards-heavy research that belongs in `domain-researcher`
- API or SaaS usage terms, commercial restrictions, redistribution, data-handling, or model-training clauses that belong in `api-terms-checker`
- patent prior-art, novelty, invalidity-candidate, freedom-to-operate precheck, or patent landscape work that belongs in `global-patent-researcher`
- latest Japan news roundups that belong in `japan-news-brief`
- MCP server design, tool shape, transport, auth, pagination, or protocol-boundary work that belongs in `mcp-server-designer`
- research-backed ideation or option generation that belongs in `idea-explorer`
- GitHub issue or pull request maintenance triage that belongs in `github-maintainer`
- product direction, feature design, or market-position decisions that belong in `product-designer`
- extracting or cleaning one specific page or URL that belongs in `web-content-distiller`
- local codebase work or documentation review that can be answered without browsing
- legal, medical, or financial advice framed as professional advice instead of informational research

## Workflow

1. Frame the research question before searching:
   - Identify the exact question, comparison, or decision support needed.
   - Decide what the output should be: direct answer, short comparison, or compact brief.
   - Note whether the answer depends on time range, geography, jurisdiction, vendor, product version, or audience.
   - Ask a clarification only when missing context would materially change the answer; otherwise state reasonable assumptions and continue.
   - Convert relative timing such as today, latest, recent, yesterday, or last week into exact dates and time zones when relevant.
   - Stop if the request is actually asking for a more specific local skill's job.

2. Gather current evidence first:
   - Do not answer from memory when the request depends on current facts.
   - Prefer official sites, vendor docs, standards bodies, primary reporting, research papers, and other first-party material.
   - For technical, API, standards, product documentation, or OpenAI product/API questions, prefer official documentation, specifications, standards bodies, research papers, and vendor material.
   - Do not rely on search result snippets as evidence; open and inspect the source pages that support the answer.
   - Use secondary sources only when they add context, help locate primary sources, or corroborate facts that no primary source covers.

3. Keep the evidence set small and useful:
   - Gather only the sources needed to answer the question confidently.
   - Prefer 3-6 strong sources over a long list of weak links.
   - Capture exact dates for claims about releases, pricing, policy, personnel, schedules, or other unstable facts.
   - Record publication or update dates when recency matters.
   - Note access limits such as paywalls, archived pages, partial access, or missing update dates when they affect confidence.
   - For unstable claims, prefer the latest authoritative source over older summaries.

4. Synthesize into the narrowest defensible answer:
   - Lead with the answer, not the research trail.
   - Separate verified facts from inference.
   - If comparing options, use the same criteria for each option and call out what remains unclear.
   - When sources conflict, separate what each source says instead of smoothing conflict into false consensus.
   - If evidence only supports a likely inference, label it as inference.

5. Report a brief with source hygiene:
   - Include links for the claims that matter.
   - Name uncertainty plainly when evidence is weak, conflicting, or stale.
   - If the evidence is insufficient, say what was found and why it does not fully answer the question.
   - Keep the answer compact and avoid including a search log unless the user asks for one.
   - Include only the source links that materially support the answer.

6. Keep the skill within the generic web research boundary:
   - Use `domain-researcher` when the topic becomes specialized and evidence-heavy.
   - Use `api-terms-checker` when terms, restrictions, data use, or commercial permission are the main question.
   - Use `global-patent-researcher` when the work becomes patent search, novelty, invalidity, FTO, or landscape research.
   - Use `japan-news-brief` when the user wants a latest Japan news roundup.
   - Use `mcp-server-designer` when the output must shape an MCP server or protocol boundary.
   - Use `idea-explorer` when the output should generate or compare idea directions from current signals.
   - Use `github-maintainer` when the task is GitHub issue or pull request maintenance triage.
   - Use `product-designer` when the output must become a product recommendation or feature direction.
   - Use `web-content-distiller` when the user mainly needs a provided page converted into clean reading input.

## Output Expectations

- Lead with the shortest defensible answer to the user's question.
- Include source links for the claims that matter.
- Use exact dates for recent or unstable facts.
- Mark inference explicitly instead of blending it into fact.
- End with the remaining uncertainty or the next most useful check when the answer is incomplete.
- Choose the lightest useful shape:
  - Direct answer: answer, key evidence, uncertainty.
  - Short comparison: criteria, options, recommendation if warranted, unknowns.
  - Compact brief: what is true or changed, why it matters, sources, caveats.

## Guardrails

- Do not skip current web research when the request is current or unstable.
- Do not turn a short research task into a broad literature review.
- Do not present weakly supported inference as confirmed fact.
- Do not overquote sources when concise paraphrase is enough.
- Do not treat search result snippets as evidence.
- Do not hide source conflicts, stale-source risk, missing update dates, paywalls, or partial access when they affect confidence.
- Do not provide professional legal, medical, or financial advice; keep those outputs informational, source-backed, and caveated.
- Do not over-escalate to deep domain research unless the topic genuinely needs specialized synthesis.
- Do not ask clarifying questions when a reasonable stated assumption would let the research proceed safely.
- Do not duplicate the jobs of narrower local skills.
