# Documentation Review

Use this reference when reviewing README files, AGENTS.md, runbooks, handoff notes, API docs, setup docs, release notes, or internal process documentation.

## Review Focus

1. Identify the reader and job:
   - new contributor, operator, reviewer, customer, maintainer, or agent
   - task the document should enable
   - freshness assumptions and source of truth
2. Check correctness and completeness:
   - commands, paths, names, and prerequisites match the repo
   - setup and validation steps are executable
   - limitations and unsupported paths are clear
   - links and referenced files exist when local
3. Check usability:
   - order follows the reader's workflow
   - required decisions are surfaced before irreversible steps
   - examples are concrete and minimal
   - troubleshooting covers likely failure points
4. Check maintainability:
   - duplicated guidance is avoided or linked
   - volatile details are not copied into too many places
   - ownership and update triggers are clear

## Output

- Findings first, with file or section references.
- Missing or misleading steps before style edits.
- Open questions about intended audience or source of truth.
- Recommendation: ready, ready with edits, or needs rewrite.

## Guardrails

- Do not rewrite docs unless requested.
- Do not optimize for prose polish ahead of correctness.
- Do not assume external context that the document itself should provide.
