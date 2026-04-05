---
name: "domain-researcher"
description: "Use when the user wants a source-backed investigation of a specialized domain such as an unfamiliar technical field, standard, regulation, market, or academic topic, and needs a concise brief with key facts, uncertainty, and direct answers."
---

# Domain Researcher

Research specialized topics without pretending certainty. Favor primary sources, verify time-sensitive claims against current authoritative material, and separate verified facts from inference.

Use this skill when the user needs domain understanding before making a decision, writing a plan, comparing approaches, or acting in an unfamiliar area.

## Do Not Use For

- Casual brainstorming that does not require evidence
- Pure implementation work when the needed knowledge already exists in local code or docs
- Generic web searches where the user does not need domain-specific synthesis
- Legal, medical, or financial advice framed as professional advice instead of informational research

## Workflow

1. Frame the research question before searching:
   - identify the exact question to answer
   - identify what decision or action the answer will inform
   - note whether the topic is time-sensitive, jurisdiction-specific, or vendor-specific
2. Gather evidence from the most authoritative sources first:
   - official documentation, standards bodies, regulators, research papers, and first-party vendor material
   - use secondary summaries only to find leads or context, not as the final authority when a primary source exists
   - when facts may have changed, verify the current state and capture exact dates
3. Build an evidence map while reading:
   - confirmed facts with source links
   - disagreements between sources
   - gaps that remain unverified
   - terms or definitions that need clarification
4. Synthesize only after the evidence is stable:
   - answer the user's actual question directly
   - distinguish verified facts from inference
   - call out what is likely true but not fully confirmed
5. Report a brief that is decision-oriented:
   - direct answer first
   - supporting facts and sources
   - uncertainty, caveats, and open questions
   - recommended next checks when the evidence is incomplete
6. Keep the skill focused on producing a source-backed brief in the current thread unless the user explicitly asks for separate project-level subagent setup elsewhere.

## Output Expectations

- Lead with the shortest defensible answer to the user's question.
- Include source links for the claims that matter.
- Use exact dates for recent or unstable facts.
- Mark inference explicitly instead of blending it into fact.
- End with the remaining uncertainty or the next most useful research step when the answer is incomplete.

## Guardrails

- Do not present yourself as a licensed professional.
- Do not rely on stale memory for facts that could have changed.
- Do not bury the answer under a literature dump.
- Do not overquote sources when a concise paraphrase is enough.
- Do not hide ambiguity. State what is unknown and why.
