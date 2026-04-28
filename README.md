# Stray Plugin Suite

Repo-local Codex plugin family for skill operations, research workflows, delivery/artifact production, and Japan government document work.

The marketplace bundle is defined in `.agents/plugins/marketplace.json` as `stray-suite`. It currently exposes four local plugins:

| Plugin | Root | Purpose |
|---|---|---|
| Stray Skill Ops | `plugins/stray-skillops/` | Create, review, audit, test, and operate Codex skills and subagents. |
| Stray Research | `plugins/stray-research/` | Run current, source-backed research, product direction, maintenance triage, and practical preflight checks. |
| Stray Studio | `plugins/stray-studio/` | Build, review, and produce apps, pages, content, visual artifacts, screenshots, and playbooks. |
| Stray Japan Gov Docs | `plugins/stray-japan-govdocs/` | Work with Japanese government whitepapers, official documents, evidence, KPI, budget, case, chart-data, citation, and cache workflows. |

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
| `skill-reviewer` | Reviewing a `SKILL.md` for trigger quality, scope boundaries, overlap risk, and output clarity. |
| `skill-overlap-auditor` | Auditing local skills as a routing system for ambiguous triggers, duplicate ownership, gaps, and split/merge recommendations. |
| `test-strategist` | Designing validation boundaries, negative cases, prompt tests, and review checklists for skills. |
| `subagent-creator` | Creating or updating custom Codex subagents under `.codex/agents/`. |
| `multi-agent-patterns` | Designing multi-agent workflows, handoffs, shared state, and quality gates. |
| `ai-eval-ci` | Adding AI or agent evaluations to CI to catch prompt and behavior regressions. |
| `context-compression` | Compressing long-running task context while preserving file paths, decisions, errors, and next steps. |

Notable support files:

- `plugins/stray-skillops/skills/agent-skill-creater/agents/openai.yaml`
- `plugins/stray-skillops/skills/subagent-creator/agents/openai.yaml`
- `plugins/stray-skillops/skills/subagent-creator/references/subagent-best-practices.md`

### Stray Research

`plugins/stray-research/` owns current research, decision support, and preflight checks. Skills that depend on current facts generally require internet or browser access.

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
| `api-terms-checker` | Checking current practical usage restrictions for third-party APIs or SaaS terms. Not legal advice. |
| `repo-compliance-preflight` | Practical release/open-source/distribution preflight for license, notices, attribution, assets, API terms, and release docs. Not legal advice. |

Notable support files:

- `agents/openai.yaml` exists for `web-researcher`, `domain-researcher`, `idea-explorer`, and `product-designer`.
- Validation cases exist at:
  - `plugins/stray-research/skills/api-terms-checker/references/validation-cases.md`
  - `plugins/stray-research/skills/repo-compliance-preflight/references/validation-cases.md`

### Stray Studio

`plugins/stray-studio/` owns delivery and artifact production. It is execution-oriented: build the thing, review the change, or produce the usable artifact.

| Skill | Use for |
|---|---|
| `fullstack-app-builder` | Building, modifying, or debugging shipped app flows across UI, API, auth, database, migrations, observability, and validation. |
| `landing-page-builder` | Creating or revising landing pages with conversion structure, messaging hierarchy, CTA flow, responsive implementation, and SEO basics. |
| `code-reviewer` | Findings-first review of diffs, PRs, branches, staged changes, or files. |
| `artifact-theme-applier` | Applying a coherent visual theme to an existing artifact without changing its core structure. |
| `brand-designer` | Defining or refining brand identity, visual principles, tone guidance, and mini style guides. |
| `article-writer` | Drafting or revising publishable articles, blog posts, newsletters, or editorial pieces. |
| `proposal-writer` | Drafting decision-oriented proposals, plans, internal requests, business cases, or approval memos. |
| `ops-playbook-writer` | Turning operational knowledge into SOPs, runbooks, playbooks, checklists, or handoff guides. |
| `json-canvas-editor` | Creating, editing, or repairing JSON Canvas `.canvas` files. |
| `marketing-screenshot-creator` | Planning or producing polished app screenshots for docs, landing pages, release notes, demos, or social posts. |
| `slack-gif-creator` | Creating Slack-friendly animated GIFs with sizing, loop timing, crop, and file-size constraints. |

Notable support files:

- `plugins/stray-studio/skills/article-writer/agents/openai.yaml`
- `plugins/stray-studio/skills/code-reviewer/agents/openai.yaml`
- `plugins/stray-studio/skills/code-reviewer/references/`
- `plugins/stray-studio/skills/fullstack-app-builder/references/`

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
