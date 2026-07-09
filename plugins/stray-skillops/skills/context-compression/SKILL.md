---
name: "context-compression"
description: "Use when an ongoing task must be compacted so another turn or agent can continue with its files, decisions, evidence, failures, and next action intact. Do not use for one-off summaries, research briefs, or domain implementation."
---

# Context Compression

Compress active task context into a smaller, structured summary that preserves the artifact trail. The goal is not minimum tokens at any cost. The goal is to keep enough state that work can continue without re-reading the same material.

Use this skill when a conversation or task has grown large enough that the next step would otherwise risk losing:

- which files were read or modified
- which decisions were made and why
- exact error messages or identifiers
- what remains unresolved
- the next action that should happen first

## Do Not Use For

- Short sessions that still fit comfortably in context
- Generic conversation summarization without task continuity needs
- Research briefs that need external sourcing rather than compression
- Test design, code review, or implementation work owned by another skill
- Rewriting a single message when no ongoing task state must be preserved

## Workflow

1. Identify the minimum state that must survive compression:
   - task intent
   - changed files
   - read-only files worth remembering
   - decisions already made
   - exact failures, warnings, or constraints
   - open questions and next steps
2. Preserve the artifact trail explicitly:
   - use full file paths for files that matter
   - keep symbol names, config keys, error strings, and branch names
   - note dates or versions when facts may change
   - label important statements as observed, user-provided, inferred, or still unverified
   - retain the last verification time for volatile external state and active processes
3. Compress only the newest or least useful detail:
   - keep durable facts
   - drop repetition, chatter, and dead ends
   - do not regenerate the entire summary if only one span changed
4. Write the compressed state in a structured form:
   - `Session Intent`
   - `Files Modified`
   - `Files Read`
   - `Decisions Made`
   - `Harness State`
   - `Current State`
   - `Next Steps`
   - `Open Questions`
   - `Stop Or Escalation Conditions`
   - `Freshness And Provenance`
   - `Superseded State`
5. Check the result for continuity:
   - could the task continue without re-reading the original thread
   - are the key files and decisions still named explicitly
   - are unresolved issues still visible instead of flattened away
   - can a reader distinguish current state from an earlier result that has been replaced
6. If compression would remove a critical fact, keep the fact and compress elsewhere instead:
   - prefer a slightly larger summary over a misleadingly small one
   - never invent continuity that is not actually present
7. Update incrementally when a prior compressed state exists:
   - preserve still-valid decisions instead of regenerating them from memory
   - move replaced commands, hypotheses, and status into `Superseded State`
   - update verification timestamps only for facts that were actually rechecked

## Output Expectations

Return a compact task summary that lets the next agent or future turn continue safely. The summary should include:

- the current task goal
- the important file paths or identifiers
- the last known decisions
- commands run, validation results, active sessions or servers, failed attempts, and remaining checks
- the active blocker or uncertainty
- the next concrete step
- when to continue, retry, ask the user, or stop
- provenance and freshness for state whose validity can change
- explicit superseded items when an earlier summary is being updated

## Guardrails

- Do not discard file paths just to save tokens.
- Do not replace unresolved issues with vague language.
- Do not merge distinct decisions into one blurred summary.
- Do not invent a clean state if the task is still messy.
- Do not use this skill as a substitute for a domain-specific brief or a code review.
- Do not present inferred or stale state as freshly observed.
- Do not silently drop an earlier blocker merely because a newer summary is shorter.

## Stop Conditions

- Stop and keep a layered or longer summary when the requested compression would make current and superseded state indistinguishable.
- Stop and mark state unverified when the original evidence is unavailable; do not reconstruct it from plausibility.
