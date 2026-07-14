# Stray Skill Ops Guidance

## Routing and Metadata

- Treat each routing case's `expect` list as an ordered workflow, not an unordered label set.
- Represent an intentional no-skill boundary with `expect: []` and `no_skill: true`.
- Keep structural validation distinct from runtime or model-evaluated behavior; never imply that one proves the other.
- Update the authoring guide, validator, fixtures, and tests together when metadata rules change.
- Keep pull-request validation deterministic. Do not add paid model calls, provider secrets, or nondeterministic evaluators without explicit approval.

## Validation

- Run `PYTHONDONTWRITEBYTECODE=1 uv run --with pyyaml==6.0.3 python plugins/stray-skillops/skills/skill-routing-validator/scripts/validate_routing_cases.py` after changing triggers, routing cases, metadata, manifests, or README skill tables.
- Run `PYTHONDONTWRITEBYTECODE=1 uv run --with pyyaml==6.0.3 --with pytest==9.1.1 python -m pytest -q -p no:cacheprovider plugins/stray-skillops/skills/skill-routing-validator/tests` after changing the validator itself.
