# Skill Authoring Guide

Use this reference after `SKILL.md` has routed the request to skill authoring.

## Authoring Checklist

1. Name the skill exactly as requested unless the user asks to normalize it.
2. Write frontmatter with `name` and a trigger-oriented `description`.
3. State the skill's one owned job in the opening paragraph.
4. Add a `Do Not Use For` section when neighboring skills or likely collisions exist.
5. Use numbered workflow steps for the main execution path.
6. State output expectations, assumptions, guardrails, and stop conditions when they affect correct use.
7. Keep repeated background, examples, and long decision rules in `references/`.
8. Validate that the skill is under `skills/`, not inside `.codex-plugin/`.
9. Review the matching plugin manifest only when a new or materially broadened skill changes user-facing discovery.
10. Add or update routing cases when the trigger or nearest handoff changes.

## When To Add Extra Files

- Add `references/` for large examples, detailed rules, domain background, or reusable checklists that would make `SKILL.md` harder to route from.
- Add `scripts/` only when deterministic execution, parsing, rendering, or validation is needed.
- Add `agents/openai.yaml` only for display metadata, dependency declarations, or invocation policy changes.

## `agents/openai.yaml`

Keep metadata small and purposeful:

```yaml
interface:
  display_name: "<Display Name>"
  short_description: "<One-line user-facing summary>"
  default_prompt: "<Useful starter prompt>"
policy:
  allow_implicit_invocation: false
dependencies:
  tools:
    - type: "mcp"
      value: "<server-name>"
      description: "<why the skill requires it>"
      transport: "streamable_http"
      url: "<server-url>"
```

Omit `policy` and `dependencies` unless they are needed. Omit `transport` and `url` when the dependency is not a remote MCP server or the install surface resolves it by name; do not invent connection metadata.

## Quality Bar

- The trigger description should make implicit invocation safer, not merely sound polished.
- The workflow should be imperative enough for another agent to follow without guessing.
- The non-goals should name realistic neighboring requests.
- The skill should not own an entire domain when it only needs to own one workflow.
- References should extend the entry point; they should not repeat it.
- Companion metadata should describe the same scope as the frontmatter and default workflow.
- Trigger changes are incomplete until intended and near-miss prompts can be distinguished.
