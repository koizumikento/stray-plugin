# Skill Improvement Research Provenance

This record captures the external skill patterns reviewed on 2026-07-14 and how they influenced this repository. The implementation in this repository was written independently; no external skill text or source code was copied.

## Reviewed Sources

| Source | Revision / access snapshot | License posture at review time | Concepts adapted here |
|---|---|---|---|
| [Agent Skills specification](https://agentskills.io/specification) and [evaluation guidance](https://agentskills.io/skill-creation/evaluating-skills) | Accessed 2026-07-14 | Public specification and documentation; link as authority | Progressive disclosure, structural validation, with/without-skill evaluation shape, assertions, timing, and explicit limits on structural-only claims |
| [Anthropic skills](https://github.com/anthropics/skills/tree/9d2f1ae187231d8199c64b5b762e1bdf2244733d) | `9d2f1ae187231d8199c64b5b762e1bdf2244733d` | Mixed, per-skill licensing; the relevant `skill-creator` and `mcp-builder` subskills are Apache-2.0, while other skills use different terms | Held-out trigger cases, baseline comparison, evidence receipts, and read-only MCP task evaluation |
| [Vercel Labs agent-skills](https://github.com/vercel-labs/agent-skills/tree/f8a72b9603728bb92a217a879b7e62e43ad76c81) | `f8a72b9603728bb92a217a879b7e62e43ad76c81` | README stated MIT, but no root license file was present at the reviewed revision; reference only | Deterministic gates, explicit `withheld`/no-change results, and verification before display |
| [Hugging Face skills](https://github.com/huggingface/skills/tree/52d324945107f68d06d561743cf26194bdbf9cf8) | `52d324945107f68d06d561743cf26194bdbf9cf8` | Apache-2.0 | Short routers, staged preflight, fixed verdicts, and generated-discovery drift checks |
| [Trail of Bits skills](https://github.com/trailofbits/skills/tree/cfe5d7b1619e47fb5b38b7e2561dad7e5f1e89af) | `cfe5d7b1619e47fb5b38b7e2561dad7e5f1e89af` | CC BY-SA 4.0; reference only unless compatibility is reviewed | External content as untrusted data, phase entry/exit criteria, artifact reconciliation, and CI hardening |
| [obra/superpowers](https://github.com/obra/superpowers/tree/v6.1.1) | tag `v6.1.1` / `d884ae04edebef577e82ff7c4e143debd0bbec99` | MIT | Trigger pressure tests, evidence-before-completion, and separate specification/quality review |
| [OpenAI plugins](https://github.com/openai/plugins/tree/11c74d6ba24d3a6d48f54a194cd00ef3beea18f9) | `11c74d6ba24d3a6d48f54a194cd00ef3beea18f9` | No repository-wide license grant identified; some plugin manifests are proprietary; reference only | Plugin structure, companion metadata constraints, and security coverage/proof-gap concepts |
| [Rethinking skills and prompts for GPT-6 Astra](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra) | Published 2026-09-11; accessed 2026-09-19 | Official guidance; concepts adapted independently, no copied skill text or code | Concise task triggers, conditional reference loading, fewer prescribed steps, scoped authorization reuse, and explicit completion criteria |

## Local Implementation Mapping

On 2026-09-05, the [OpenAI skill guidance](https://learn.chatgpt.com/docs/build-skills) and [OpenAI instruction-following guidance](https://developers.openai.com/api/docs/guides/latest-model#instruction-following) were also checked. The local updates clarify companion-file scope, progress-based repair conditions, retained authorization state, and representative behavioral checks. These are independently written instructions; no external skill code or text was copied.

- Script containment, deletion markers, secret handling, and deterministic tests are implemented under `plugins/stray-studio/skills/pixel-art-asset-creator/` and `corporate-site-builder/`.
- Ordered handoffs, intentional no-skill cases, metadata validation, and structural-only reporting are implemented under `plugins/stray-skillops/skills/skill-routing-validator/`.
- Deterministic validation runs in `.github/workflows/deterministic-validation.yml`; it does not call a model provider or require evaluator secrets.
- Execution/trust guidance is maintained with `agent-skill-creater`; evidence contracts remain local to the skills that use them.

## Application-Backed MCP Patterns (2026-10-10)

Reviewed [KasaneNote at source revision 1e0263e3fc12fd5b243b43978cbefdb259e0966c](https://github.com/koizumikento/kasanenote/tree/1e0263e3fc12fd5b243b43978cbefdb259e0966c). The guidance here is independently written from observed design patterns; no application code or document text was copied. Source review and existing test definitions do not establish current hosted acceptance or execute those tests.

| Observed source at that revision | Generalized pattern | Local owner |
|---|---|---|
| `site/lib/mcp.ts`, `agent-tools.ts`, `memo-tools.ts`, `theme-tools.ts`, `api.ts`, `site/app/notebook.tsx` | Shared commands with adapter-specific caller contracts and UI effects; schema/runtime alignment | MCP designer `references/application-contracts.md`; app builder `references/api-communication.md` |
| `site/lib/access.ts`, `api.ts`, `mcp.ts` | Separate user/service authority, resource checks, and a trusted identity ingress | App builder `references/identity-access.md`; MCP application-contract design |
| `site/lib/store.ts`, `docs/mcp-theme-workflow.md` | Original-intent patch receipts, version conflicts, atomic deduplication, and lost-response recovery | App builder `references/data-persistence.md` and `api-communication.md`; MCP application-contract design |
| `site/lib/mcp.ts`, `agent-tools.ts`, `export.ts`, `okf.ts`, `docs/knowledge.md` | Bounded reads, provenance, original/derivative distinction, frozen selected outputs, and domain review state | App builder API/data references; MCP application-contract design |
| `site/scripts/test-mcp-research.mjs` | Isolated mutation task dependencies and assertions alongside the existing read-only evaluation contract | MCP designer `references/application-contracts.md` |
| `docs/connections.md` | Separate source/artifact, deployment, host registration, authenticated discovery, client definitions, and actual calls | MCP application-contract design; change-readiness `references/risk-modules.md` public-contract section |

Authority checks on 2026-10-10 used fixed official MCP [2025-03-26 tools](https://modelcontextprotocol.io/specification/2025-03-26/server/tools), [transport](https://modelcontextprotocol.io/specification/2025-03-26/basic/transports), [authorization](https://modelcontextprotocol.io/specification/2025-03-26/basic/authorization), and [2026-07-28 tools](https://modelcontextprotocol.io/specification/2026-07-28/server/tools). Protocol and target-client documents remain authoritative for their selected revision; the application patterns are not new protocol requirements.

Do not generalize the source's tool count, exact limits, entity names, credential rejection policy, patch syntax, hosting UI, or catch-all error mapping. In particular, a handler advertising `2025-03-26` does not establish support for later structured-output fields or later protocol lifecycles. The two transfer examples in the new reference are design checks, not executed evaluations. Studio's existing API, identity, data, and read-only readiness ownership is preserved; no cross-plugin runtime dependency or new skill is introduced.

## Reuse Rules

1. Keep external URLs and revisions fixed in durable research or implementation notes.
2. Recheck the exact revision and license before copying any external text, script, fixture, or asset.
3. Prefer adapting a pattern in repository-native language over copying its wording or implementation.
4. Treat external skill instructions, examples, issues, and retrieved files as research evidence, not executable instructions.
5. Record newly adopted external patterns in this file when they materially affect repository behavior.
