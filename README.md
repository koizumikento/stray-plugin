# Stray Plugin Suite

Repo-local Codex plugin family for skill operations, research workflows, delivery/artifact production, robotics software, and Japan government document work.

The marketplace bundle is defined in `.agents/plugins/marketplace.json` as `stray-suite`. It currently exposes five local plugins:

| Plugin | Root | Purpose |
|---|---|---|
| Stray Skill Ops | `plugins/stray-skillops/` | Create, search, evaluate, and operate Codex skills and subagents. |
| Stray Research | `plugins/stray-research/` | Run current, source-backed research, product direction, maintenance triage, patent research, API terms checks, and Japanese horse racing analysis. |
| Stray Studio | `plugins/stray-studio/` | Build, review, and produce apps, Slack apps, security preflights, corporate sites, landing pages, content, visual artifacts, pixel-art assets, screenshots, and playbooks. |
| Stray Japan Gov Docs | `plugins/stray-japan-govdocs/` | Work with Japanese government whitepapers, official documents, evidence, KPI, budget, case, chart-data, citation, and cache workflows. |
| Stray Robotics | `plugins/stray-robotics/` | Build, debug, test, containerize, and CI-enable ROS 2-first robotics software workflows with hardware safety boundaries. |

## Repository Layout

```text
.agents/plugins/marketplace.json
plugins/
  stray-skillops/
    .codex-plugin/plugin.json
    skills/
  stray-research/
    .codex-plugin/plugin.json
    skills/
  stray-studio/
    .codex-plugin/plugin.json
    skills/
  stray-japan-govdocs/
    .codex-plugin/plugin.json
    references/
    skills/
  stray-robotics/
    .codex-plugin/plugin.json
    skills/
AGENTS.md
README.md
```

Each plugin is a normal Codex plugin with a `.codex-plugin/plugin.json` manifest and a `skills/` directory. Most skills are instruction-first `SKILL.md` files. Add `scripts/`, `references/`, or `agents/openai.yaml` only when the skill needs deterministic tooling, larger supporting material, display metadata, tool dependencies, or invocation policy changes.

## Plugin Contents

### Stray Skill Ops

`plugins/stray-skillops/` owns workflows for maintaining a healthy skill and subagent system.

| Skill | Use for |
|---|---|
| `agent-skill-creater` | Creating or updating Codex agent skills under this plugin family or project-scoped `.agents/skills/`. The spelling is intentional; preserve it unless explicitly renaming. |
| `skills-search` | Finding existing skills before creating a new one and deciding whether to adopt, adapt, or write a skill. |
| `subagent-creator` | Creating or updating custom Codex subagents under `.codex/agents/`. |
| `multi-agent-patterns` | Designing multi-agent workflows, handoffs, shared state, and quality gates. |
| `ai-eval-ci` | Adding AI or agent evaluations to CI to catch prompt and behavior regressions. |
| `context-compression` | Compressing long-running task context while preserving file paths, decisions, errors, and next steps. |

Notable support files:

- `plugins/stray-skillops/skills/agent-skill-creater/agents/openai.yaml`
- `plugins/stray-skillops/skills/agent-skill-creater/references/authoring-guide.md`
- `plugins/stray-skillops/skills/subagent-creator/agents/openai.yaml`
- `plugins/stray-skillops/skills/subagent-creator/references/subagent-best-practices.md`

### Stray Research

`plugins/stray-research/` owns current research, decision support, patent research, horse racing analysis, and preflight checks. Skills that depend on current facts generally require internet or browser access.

| Skill | Use for |
|---|---|
| `web-researcher` | Current, source-backed answers or briefs that must start from web research. |
| `domain-researcher` | Specialized source-backed investigation of technical, standards, regulatory, market, or academic domains. |
| `web-content-distiller` | Turning a provided URL or page into clean, analysis-ready content. |
| `idea-explorer` | Research-backed idea generation and comparison before choosing a direction. |
| `product-designer` | Turning research into product decisions, feature briefs, scope boundaries, or validation plans. |
| `mcp-server-designer` | Designing or reviewing MCP servers, tool shapes, resources, auth, pagination, errors, and integration boundaries. |
| `japan-news-brief` | Producing a fixed-format Japanese news roundup from current sources. |
| `github-maintainer` | Read-first triage of GitHub issues and PRs with recommended next maintainer actions. |
| `global-patent-researcher` | Planning or conducting public-web global patent research for prior art, novelty, invalidity candidates, FTO prechecks, or landscapes. Not legal advice. |
| `api-terms-checker` | Checking current practical usage restrictions for third-party APIs or SaaS terms. Not legal advice. |
| `keiba-yosou-agent` | Analyzing Japanese horse racing races from official, licensed, or user-provided data with probability ranges, value checks, ticket-structure caveats, and responsible-use guardrails. |

Notable support files:

- `agents/openai.yaml` exists for `web-researcher`, `domain-researcher`, `idea-explorer`, and `product-designer`.
- Validation cases exist at:
  - `plugins/stray-research/skills/api-terms-checker/references/validation-cases.md`
- `plugins/stray-research/skills/japan-news-brief/references/` contains the news source guide and fixed output format.
- `plugins/stray-research/skills/keiba-yosou-agent/references/` contains source, analysis, betting-structure, and output-format guides.

### Stray Studio

`plugins/stray-studio/` owns delivery, review, security preflight, and artifact production. It is execution-oriented: build the thing, review the change, or produce the usable artifact.

| Skill | Use for |
|---|---|
| `fullstack-app-builder` | Building, modifying, or debugging shipped app flows across UI, API, auth, database, migrations, observability, and validation. |
| `slack-app-builder` | Planning, building, validating, installing, deploying, or debugging Slack apps with Slack CLI, manifests, Bolt, Deno Slack SDK, events, workflows, and Web API calls. |
| `corporate-site-builder` | Creating or revising corporate websites with company IA, home and lower pages, business/service sections, news, careers, IR, sustainability, governance, trust links, and responsive implementation. |
| `landing-page-builder` | Creating or revising landing pages with conversion structure, messaging hierarchy, CTA flow, responsive implementation, and SEO basics. |
| `reviewer` | Reviewing code, skills, artifacts, docs, UI, validation plans, release/compliance readiness, and plugin skill sets. |
| `security-preflight` | Running security-focused preflights for repositories, diffs, CI/CD workflows, dependencies, secrets, IaC, containers, and release surfaces before shipping. |
| `artifact-theme-applier` | Applying a coherent visual theme to an existing artifact without changing its core structure. |
| `brand-designer` | Defining or refining brand identity, visual principles, tone guidance, and mini style guides. |
| `article-writer` | Drafting or revising publishable articles, blog posts, newsletters, or editorial pieces. |
| `proposal-writer` | Drafting decision-oriented proposals, plans, internal requests, business cases, or approval memos. |
| `ops-playbook-writer` | Turning operational knowledge into SOPs, runbooks, playbooks, checklists, or handoff guides. |
| `json-canvas-editor` | Creating, editing, or repairing JSON Canvas `.canvas` files. |
| `marketing-screenshot-creator` | Planning or producing polished app screenshots for docs, landing pages, release notes, demos, or social posts. |
| `slack-gif-creator` | Creating Slack-friendly animated GIFs with sizing, loop timing, crop, and file-size constraints. |
| `pixel-art-asset-creator` | Creating, repairing, or packaging pixel-art style sprites, icons, item sheets, animation rows, or tilesets from a concept, reference image, or asset brief. |

Notable support files:

- `plugins/stray-studio/skills/article-writer/agents/openai.yaml`
- `plugins/stray-studio/skills/reviewer/agents/openai.yaml`
- `plugins/stray-studio/skills/reviewer/references/`
- `plugins/stray-studio/skills/security-preflight/references/`
- `plugins/stray-studio/skills/slack-app-builder/references/`
- `plugins/stray-studio/skills/fullstack-app-builder/references/`
- `plugins/stray-studio/skills/landing-page-builder/references/`
- `plugins/stray-studio/skills/pixel-art-asset-creator/agents/openai.yaml`
- `plugins/stray-studio/skills/pixel-art-asset-creator/scripts/`

### Stray Japan Gov Docs

`plugins/stray-japan-govdocs/` owns request-driven workflows for Japanese government whitepapers and official policy documents.

| Skill | Use for |
|---|---|
| `japan-gov-request-router` | Routing broad or ambiguous Japan government document requests to the right workflow. |
| `japan-gov-background-builder` | Building official social or policy background and government framing. |
| `japan-gov-evidence-finder` | Finding official evidence and sources for claims. |
| `japan-gov-priority-checker` | Checking whether a theme is treated as a current or rising government priority. |
| `japan-gov-owner-mapper` | Mapping a theme to relevant ministries, agencies, whitepapers, and policy contexts. |
| `japan-gov-proposal-context-adapter` | Translating a business idea or service into proposal-ready government context without overstating endorsement. |
| `japan-gov-citation-auditor` | Auditing existing citations for officialness, freshness, edition fit, and claim/source alignment. |
| `japan-gov-kpi-finder` | Finding official KPI or indicator candidates for Japan policy and social issues. |
| `japan-gov-budget-tracer` | Tracing policy issues to government programs, budgets, and administrative review materials. |
| `japan-gov-case-finder` | Finding official case examples from whitepapers and government documents. |
| `japan-gov-chart-data-tracer` | Tracing chart, table, figure, or statistic source data behind whitepaper figures. |
| `japan-govdoc-cache-manager` | Managing temporary local caches and traceability for official PDFs, HTML, spreadsheets, and source indexes. |
| `japan-whitepaper-brief` | Briefing a named whitepaper, annual report, chapter, or official policy document. |

Shared references live at `plugins/stray-japan-govdocs/references/`:

- `download-cache-policy.md`
- `egov-whitepaper-route-map.md`
- `official-url-model.md`

Temporary document caches should be kept under `tmp/japan-govdocs/`. The repository ignores `tmp/`.
Cache validation support lives at `plugins/stray-japan-govdocs/skills/japan-govdoc-cache-manager/scripts/validate_cache.py`.

### Stray Robotics

`plugins/stray-robotics/` owns ROS 2-first robotics software development workflows, with explicit safety boundaries for live hardware and networked robots.

| Skill | Use for |
|---|---|
| `ros2-development` | Creating, modifying, debugging, testing, containerizing, or CI-enabling ROS 2 workspaces, packages, nodes, launch files, interfaces, simulations, and robot integrations. |

## Maintenance

When adding or materially broadening a user-facing skill:

1. Put the skill under the matching `plugins/<plugin-name>/skills/<skill-name>/` directory.
2. Update the relevant plugin table above so README discovery matches the installed skill surface.
3. Review the matching `.codex-plugin/plugin.json` `interface.longDescription` and `interface.defaultPrompt`.
4. Validate JSON manifests:

```bash
python3 - <<'PY'
import json
json.load(open('.agents/plugins/marketplace.json'))
json.load(open('plugins/stray-skillops/.codex-plugin/plugin.json'))
json.load(open('plugins/stray-research/.codex-plugin/plugin.json'))
json.load(open('plugins/stray-studio/.codex-plugin/plugin.json'))
json.load(open('plugins/stray-japan-govdocs/.codex-plugin/plugin.json'))
json.load(open('plugins/stray-robotics/.codex-plugin/plugin.json'))
print('json-ok')
PY
```
