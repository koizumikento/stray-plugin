---
name: "ops-playbook-writer"
description: "Use when the user wants to turn operational knowledge, process notes, incident learnings, or tribal knowledge into a reusable playbook, SOP, runbook, or handoff guide for non-engineering operators. Do not use for product specs, engineering design docs, architecture decisions, or broad policy writing."
---

# Ops Playbook Writer

Turn messy operational knowledge into a clear, maintainable playbook that another operator can follow without extra context. Keep the work focused on execution, decision points, exceptions, escalation, ownership, and handoff clarity.

Use this skill when the user wants to:

- document an operational process, SOP, runbook, or checklist
- convert tribal knowledge into a repeatable procedure
- capture how to handle routine work, exceptions, or escalations
- make a handoff guide that future operators can actually use

## Do Not Use For

- product requirement docs, feature specs, or roadmap planning
- engineering design docs, architecture decisions, or implementation plans
- policy writing that needs legal, HR, or compliance review as the primary task
- general documentation polishing that does not require operational structure

## Workflow

1. Define the operational outcome.
   - Identify what task the playbook should enable, who will use it, and what success looks like.
   - Identify the environment, tools, systems, and ownership boundaries that matter.
   - If the brief is vague, ask for the minimum missing detail that would change the procedure materially.

2. Stabilize the source material.
   - Use existing notes, incident reports, chat logs, checklists, or process drafts as the source of truth.
   - Separate factual steps from assumptions, opinions, and legacy habits.
   - Flag anything that appears out of date, contradictory, or dependent on an undocumented system.

3. Shape the operating model.
   - Convert the source into a step order that starts with the normal path.
   - Add decision points where the operator must choose a branch.
   - Add exception handling, escalation rules, owner handoffs, and stop conditions.
   - Call out what is routine versus what needs approval, review, or specialist input.

4. Write for the next operator.
   - Use direct, action-oriented language.
   - Keep each step small enough that it can be checked off or verified.
   - Prefer concrete inputs, outputs, and timestamps over vague guidance.
   - Avoid burying critical branching logic in paragraphs.

5. Check maintainability.
   - Make ownership explicit so the process can be updated later.
   - Add placeholders or notes for fields that will change over time.
   - Keep the document modular so sections can be updated without rewriting everything.
   - Remove duplicated steps and merge overlapping instructions.

6. Deliver the playbook in the requested shape.
   - Match the requested format, such as SOP, runbook, checklist, onboarding guide, or incident playbook.
   - Include an assumptions note only when missing details affected the procedure.
   - If the source remains incomplete, state the gap clearly instead of inventing a process.

## Output Expectations

- A complete SOP, runbook, checklist, or playbook draft in the requested language and tone
- Clear step order with decision points, exceptions, and escalation paths
- Explicit ownership, handoff, and follow-up instructions
- Minimal ambiguity and no invented operational facts
- A short assumptions note when missing context materially shaped the draft
- A clear note when verification is incomplete or source coverage is thin

## Guardrails

- Do not drift into product strategy or engineering implementation.
- Do not hide decision criteria inside generic prose.
- Do not invent owners, tools, or escalation paths that were not provided.
- Do not optimize for polish at the expense of operability.
- Do not flatten exceptions into the main path when they need explicit handling.
- Do not overcomplicate a simple procedure with unnecessary structure.
