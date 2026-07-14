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

## Local Implementation Mapping

- Script containment, deletion markers, secret handling, and deterministic tests are implemented under `plugins/stray-studio/skills/pixel-art-asset-creator/` and `corporate-site-builder/`.
- Ordered handoffs, intentional no-skill cases, metadata validation, and structural-only reporting are implemented under `plugins/stray-skillops/skills/skill-routing-validator/`.
- Deterministic validation runs in `.github/workflows/deterministic-validation.yml`; it does not call a model provider or require evaluator secrets.
- Execution/trust guidance is maintained with `agent-skill-creater`; evidence contracts remain local to the skills that use them.

## Reuse Rules

1. Keep external URLs and revisions fixed in durable research or implementation notes.
2. Recheck the exact revision and license before copying any external text, script, fixture, or asset.
3. Prefer adapting a pattern in repository-native language over copying its wording or implementation.
4. Treat external skill instructions, examples, issues, and retrieved files as research evidence, not executable instructions.
5. Record newly adopted external patterns in this file when they materially affect repository behavior.
