---
name: "context-compression"
description: "Use when a long-running task, debugging thread, or multi-step workflow needs to be compacted without losing file paths, decisions, errors, or next steps. Do not use for one-off summaries, general research, test planning, or implementation work that should be handled by a different skill."
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
3. Compress only the newest or least useful detail:
   - keep durable facts
   - drop repetition, chatter, and dead ends
   - do not regenerate the entire summary if only one span changed
4. Write the compressed state in a structured form:
   - `Session Intent`
   - `Files Modified`
   - `Files Read`
   - `Decisions Made`
   - `Current State`
   - `Next Steps`
   - `Open Questions`
5. Check the result for continuity:
   - could the task continue without re-reading the original thread
   - are the key files and decisions still named explicitly
   - are unresolved issues still visible instead of flattened away
6. If compression would remove a critical fact, keep the fact and compress elsewhere instead:
   - prefer a slightly larger summary over a misleadingly small one
   - never invent continuity that is not actually present

## Output Expectations

Return a compact task summary that lets the next agent or future turn continue safely. The summary should include:

- the current task goal
- the important file paths or identifiers
- the last known decisions
- the active blocker or uncertainty
- the next concrete step

## Guardrails

- Do not discard file paths just to save tokens.
- Do not replace unresolved issues with vague language.
- Do not merge distinct decisions into one blurred summary.
- Do not invent a clean state if the task is still messy.
- Do not use this skill as a substitute for a domain-specific brief or a code review.
