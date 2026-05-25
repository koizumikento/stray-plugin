# Plugin Review

Use this reference when reviewing a Codex plugin package, `.codex-plugin/plugin.json`, marketplace entry, plugin skill layout, discovery copy, or distribution readiness.

## Review Focus

1. Identify the plugin surface:
   - plugin root
   - `.codex-plugin/plugin.json`
   - marketplace entry
   - skills, MCP servers, apps, hooks, and assets declared by the plugin
2. Check manifest consistency:
   - `name`, `version`, `description`, and `skills` path are coherent
   - interface text reflects the actual skill set
   - default prompts point to supported workflows
   - category and display metadata are not misleading
3. Check packaging boundaries:
   - skills live under `plugins/<plugin-name>/skills/<skill-name>/`
   - skills are not placed inside `.codex-plugin/`
   - repo-local guidance and marketplace entries do not contradict the manifest
4. Check discovery and routing:
   - new or removed skills are represented in plugin descriptions when needed
   - descriptions avoid claiming unsupported capabilities
   - plugin scope remains coherent instead of becoming a catch-all bundle
5. Check JSON and release hygiene:
   - manifests parse as JSON
   - paths referenced by manifest or docs exist
   - deleted skills are removed from discovery copy

## Output

- Findings first, with file references.
- Manifest and marketplace consistency issues.
- Routing/discovery issues.
- Recommended edits or hold/ready decision.

## Guardrails

- Do not turn plugin review into broad product strategy.
- Do not add `-local` suffixes or rename plugins unless explicitly requested.
- Do not assume custom subagents are first-class plugin components; treat them as project or user config unless the platform supports otherwise.
