---
name: "skill-routing-validator"
description: "Use when designing, running, or repairing Codex skill trigger and near-miss cases. Owns routing evaluation, not skill authoring or general AI eval CI."
---

# Skill Routing Validator

Validate a local skill set as a routing system. Make intended prompts, neighboring prompts, and expected handoffs explicit, then keep the case inventory structurally reproducible.

## Do Not Use For

- Creating or rewriting the target skill; use `agent-skill-creater`.
- Reviewing a plugin without a routing-eval deliverable; use `reviewer`.
- Wiring general LLM quality evaluations into CI; use `ai-eval-ci`.
- Ordinary unit, integration, or end-to-end test design.

## Workflow

1. Define the routing surface.
   - Record the selected repository and skill paths explicitly. The bundled CLI validates this Stray marketplace checkout, not arbitrary repositories or an installed plugin cache.
   - Inventory the selected `SKILL.md` files and any companion `agents/openai.yaml` metadata that is present in the selected scope.
   - Record each skill's owned job, nearest neighbors, direct handoffs, and explicit non-goals.
2. Design discriminating cases.
   - Add intended prompts that should select one named skill.
   - Add near-miss prompts that should select a neighbor while explicitly rejecting the target skill.
   - Add ambiguous or mixed-intent cases only when the expected ordered handoff can be stated objectively.
   - Prefer a small high-signal set over paraphrase-heavy volume.
3. Maintain the versioned case inventory.
   - In this checkout, store schema-versioned cases in `references/routing-cases.json` with unique IDs, prompt, expected skills, rejected skills, and a short reason. For another repository, use its existing case inventory or a task-local result; do not write into the installed plugin cache.
   - Treat `expect` as an ordered handoff sequence. Keep its skill names unique.
   - Represent an intentional no-skill result with an empty `expect` array and `no_skill: true`; still list the nearest specialist skills in `reject`.
   - Give every skill in the selected scope both positive coverage and reject coverage.
4. Run deterministic validation.
   - For this marketplace checkout, run `uv run --with pyyaml python plugins/stray-skillops/skills/skill-routing-validator/scripts/validate_routing_cases.py` from its root; otherwise use a Python 3 runner with PyYAML installed.
   - For another repository or an installed plugin, use that repository's existing validator or inspect the selected files directly. Report which mechanical checks were unavailable; running the bundled CLI against its own checkout does not validate the user's repository.
   - Treat missing skills, name/path mismatch, malformed or duplicate-key JSON/YAML, overlong descriptions, broken local references, marketplace/manifest drift, invalid companion metadata, stale README inventory, missing case coverage, and contradictory expectations as failures.
5. Evaluate routing behavior.
   - When a classifier or Codex eval harness is available, run the case prompts and record actual selections separately from the expected inventory.
   - Start with changed boundaries and their nearest neighbors. Record the case ID, evaluated revision, actual ordered selections, unexpected questions or stops, completion evidence, and pass/fail. If testing a shortened description list, record the actual visible text rather than assuming a fixed host truncation length.
   - Otherwise review each case against frontmatter descriptions and report `runtime=not-run`; structural validation alone is not behavioral proof.
6. Repair narrowly.
   - Change the smallest trigger, handoff, case, or metadata boundary that explains the failure.
   - Rerun the failing cases after each change. After two attempts on the same collision without new evidence, reassess the owned-job boundary rather than repeating the same edit; continue while the evidence supports progress.

## Output

- Routing scope and case inventory path.
- Structural validation command and result.
- Manifest, metadata, reference, and README discovery checks included in that result.
- Behavioral results when an actual routing harness was available.
- Confirmed collisions, repaired files, and remaining unverified behavior.

## Guardrails

- Do not claim runtime routing passed when only the JSON and file structure were validated.
- Do not weaken a case merely to make an ambiguous description pass; repair the owned-job boundary first.
- Do not let one generic skill absorb a narrower specialist merely to eliminate a collision.
- Do not invent a required skill for every possible task; report intentional no-skill coverage as such.

## Stop Conditions

- Stop when expected behavior cannot be stated without a product or ownership decision.
- Stop when the remaining collision cannot be resolved without unavailable evidence or an ownership decision; return the prompts, actual evidence, and decision needed.
