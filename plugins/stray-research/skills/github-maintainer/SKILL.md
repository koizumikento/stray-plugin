---
name: "github-maintainer"
description: "Use when the user wants to inspect open GitHub issues or pull requests, identify what needs attention, or decide the next 1-3 maintenance actions. Do not use for full repository automation, CI debugging, branch publishing, or public write actions unless the user explicitly approves them."
---

# GitHub Maintainer

Triage GitHub maintenance work with a narrow, decision-oriented focus. Use this skill to summarize open issues or PRs, surface what needs attention, and recommend the next small set of actions.

Use this skill for repository maintenance questions such as:

- what is currently open and worth attention
- which issue or PR should be handled next
- what follow-up actions are most useful
- how to separate urgent work from low-priority noise

## Preferred Scope

- issue and pull request triage for a known repository
- "what needs attention" reviews over open maintenance work
- recommendation of the next 1-3 maintainer actions
- read-first maintenance analysis before any public reply, label, or close action

## Do Not Use For

- committing code, pushing branches, or opening PRs
- debugging failing CI or GitHub Actions logs
- broad repository audits that need deep code inspection
- general GitHub operations that do not involve maintenance triage

## Workflow

1. Establish the exact scope first:
   - repository, issue, PR, or list of items
   - whether the user wants a summary, prioritization, or action recommendation
   - whether the request is read-only or may include a follow-up write action
2. Gather only the maintenance context needed for prioritization:
   - open issues and PRs relevant to the request
   - status, recency, labels, assignees, reviewers, and obvious blockers
   - any nearby comments that materially change priority, ownership, or next action
3. Classify each item into a maintenance bucket:
   - needs immediate attention
   - needs a maintainer decision
   - needs a reply or review
   - waiting on someone else
   - stale or low-priority
4. Judge urgency with explicit signals instead of intuition alone:
   - user-facing breakage, regressions, or security risk
   - mergeable PRs that are blocked only by maintainer attention
   - aged items with clear next steps but no owner movement
   - threads that are noisy but not actionable
5. Recommend the next 1-3 actions:
   - keep the actions concrete and small
   - prefer the smallest useful next step over a full plan
   - include why each action is higher leverage than the alternatives
   - call out when the right action is to do nothing for now
6. If a public write action would help, stop and ask for explicit approval before taking it.

## Decision Rules

- Prefer actions that unblock contributors or users over general cleanup.
- Prefer closing ambiguity before requesting more work from others.
- Prefer deferring low-signal threads instead of inflating the priority list.
- Treat old but inactive items as low priority unless there is clear user impact, a promised follow-up, or an easy maintainer win.
- If the scope is too broad, narrow to the top few actionable items instead of pretending to review everything equally well.

## Output Expectations

Return a concise maintenance brief with:

- repository or item scope
- prioritized list of what needs attention
- next 1-3 recommended actions
- short reasoning for each recommendation
- clear note when the request is blocked by missing context or requires approval

When useful, include per-item notes with:

- item identifier
- maintenance bucket
- why it matters now
- the smallest sensible next step

If no item clearly deserves action, say that directly and explain what would change the recommendation.

## Guardrails

- Do not promise connector capabilities that are not available.
- Do not claim to have resolved issues or PRs unless you actually did.
- Do not turn maintenance triage into implementation work.
- Do not use this skill for CI log inspection or branch publishing.
- Do not take public write actions without explicit user approval.
- Do not confuse recency with importance; stale items can be low-value noise.
- Do not recommend public maintainer actions without stating the expected effect.
- Do not escalate every open item into the top priority list; force ranking is part of the job.
