---
name: "skill-routing-validator"
description: "Use when the user wants to design, run, or repair trigger and near-miss routing cases for Codex skills. Do not use for authoring the skill itself, general software tests, or AI eval CI implementation."
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
   - Inventory the selected `SKILL.md` files and companion `agents/openai.yaml` metadata.
   - Record each skill's owned job, nearest neighbors, direct handoffs, and explicit non-goals.
2. Design discriminating cases.
   - Add intended prompts that should select one named skill.
   - Add near-miss prompts that should select a neighbor while explicitly rejecting the target skill.
   - Add ambiguous or mixed-intent cases only when the expected ordered handoff can be stated objectively.
   - Prefer a small high-signal set over paraphrase-heavy volume.
3. Maintain the versioned case inventory.
   - Store schema-versioned cases in `references/routing-cases.json` with unique IDs, prompt, expected skills, rejected skills, and a short reason.
   - Treat `expect` as an ordered handoff sequence. Keep its skill names unique.
   - Represent an intentional no-skill result with an empty `expect` array and `no_skill: true`; still list the nearest specialist skills in `reject`.
   - Give every installed local skill both positive coverage and reject coverage.
4. Run deterministic validation.
   - Prefer `uv run --with pyyaml python plugins/stray-skillops/skills/skill-routing-validator/scripts/validate_routing_cases.py`; otherwise use a Python 3 runner with PyYAML installed.
   - Treat missing skills, name/path mismatch, malformed or duplicate-key JSON/YAML, overlong descriptions, broken local references, marketplace/manifest drift, invalid companion metadata, stale README inventory, missing case coverage, and contradictory expectations as failures.
5. Evaluate routing behavior.
   - When a classifier or Codex eval harness is available, run the case prompts and record actual selections separately from the expected inventory.
   - Otherwise review each case against frontmatter descriptions and report `runtime=not-run`; structural validation alone is not behavioral proof.
6. Repair narrowly.
   - Change the smallest trigger, handoff, case, or metadata boundary that explains the failure.
   - Rerun the failing cases after each change and stop after two focused attempts on the same unresolved collision.

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
- Stop after two focused repairs leave the same collision unresolved and return the prompts, actual evidence, and decision needed.
