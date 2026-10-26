# Shared Document Lint

Use this check before delivering saved Markdown or plain-text documents from the article, proposal, playbook, Japanese editing, and document-review workflows. This is a shared completion check, not another skill or an automatic Japanese style rewrite.

## Workflow

1. Select the exact final `.md` or `.txt` files and read the target project's rules. Run its required checks as well; this baseline does not replace them. Keep quotations, code, identifiers, uncertainty, conditions, obligations, and meaning intact. For unsaved chat prose, do not create inspection copies solely for lint; use the semantic checks below and report mechanical validation as not run when relevant.
2. Locate this plugin's `scripts/document-lint/` relative to this reference. Use an editable, versioned source checkout with Node.js 22 or later and npm. Install the lockfile dependencies once using the setup command below when dependency setup is authorized by the task. Installation downloads packages from the npm registry; it does not upload drafts. Do not modify a host-managed installed-plugin cache. If dependencies or a writable source checkout are unavailable, continue useful drafting/review work, report `document-lint=not-run` with the reason, and give the setup command for an appropriate source checkout. Never claim a pass.
3. Run the checker with explicit file paths. Use the common profile for English, skill definitions, and mixed-language examples. Add `--ja` for predominantly Japanese prose; it adds a length warning to the same common rules. Split a mixed file set into separate invocations. Paths resolve from the shell's current directory, not from the plugin directory. Directories, globs, and other formats are intentionally unsupported.
4. Resolve errors within the authorized edit scope. In review-only mode, report them without editing. Review terminology and length warnings in context: keep justified long sentences, necessary uncertainty, identifiers, and original quotations. Warnings do not block completion or require a rewrite. The checker reads files and prints findings; it does not auto-fix, write reports, access the network, or discover/execute the target project's lint configuration.
5. Review meaning and evidence: check actors, conditions, negation, numbers, units, certainty, source support, paragraph flow, and the reader's required action. For Word/PDF/slides, use the format's own rendering checks; this tool checks only `.md`/`.txt` sources and makes no layout claim.
6. Save any authorized fixes, rerun against the final files, and read back the delivered result. Further edits invalidate the prior check. Completion evidence is the command, selected profile, file count, error/warning counts, and material unresolved findings. Keep process notes outside body-only deliverables. Exit `0` means selected mechanical checks passed, including when warnings remain; `1` means lint errors; `2` means validation was unavailable or input/configuration failed.

## Commands

Set `lint_root` to the absolute path of `scripts/document-lint/` in the chosen Studio source checkout. Quote paths, including paths with spaces. No credentials or model service are needed.

```sh
lint_root="/absolute/path/to/stray-plugin/plugins/stray-studio/scripts/document-lint"
npm ci --prefix "$lint_root" --ignore-scripts --no-audit --no-fund
node "$lint_root/check.mjs" -- "/absolute/path/to/README.md"
node "$lint_root/check.mjs" --ja -- "/absolute/path/to/調査メモ.md"
npm test --prefix "$lint_root"
```

Use direct `node` invocation from the document's working directory to keep relative input paths unambiguous. The bundled configuration and dictionary are resolved relative to the checker even when invoked from another project. Caller ignore files cannot silently exclude explicitly selected targets. Empty documents have no prose findings; their substantive completeness still needs review.

## Initial Rules

The source of truth is [textlint.json](../scripts/document-lint/textlint.json), the additive [textlint-ja.json](../scripts/document-lint/textlint-ja.json), [terms.yml](../scripts/document-lint/terms.yml), and [markdownlint.json](../scripts/document-lint/markdownlint.json). Dependency versions and transitive dependencies are pinned by the adjacent package manifest and lockfile. Do not copy these rules into individual skills.

| Rule | Level | Violation | Allowed example or exception |
|---|---|---|---|
| `prh`: GitHub | warning | `Github`, `GITHUB` in prose | `GitHub`; retain identifiers and original quotations |
| `prh`: ChatGPT | warning | `ChatGpt`, `Chatgpt` in prose | `ChatGPT` |
| `prh`: Node.js | warning | `NodeJS` in prose | `Node.js`; do not rewrite package names or identifiers |
| `MD011` | error | Reversed Markdown link delimiters | Normal Markdown links; fenced bad examples |
| `MD018` | error | Missing space after a Markdown heading marker | Correct headings; fenced code |
| `sentence-length`, Japanese profile only | warning | More than 100 UTF-16 code units per sentence | English uses common; justified long Japanese sentences may remain |

These are intentionally narrow spellings, not case-insensitive bans. `prh` checks normal prose, headings, and emphasis; it skips Markdown code, block quotations, and links, including link labels. Plain text has no Markdown node protections. The length warning counts according to the pinned rule's parsing and code-unit behavior; it is not a readability score. There is no blanket ban on speculative language, passive voice, headings, list ratios, or particular Japanese sentence endings. No external link validation or factual validation is performed.

The 100-unit threshold follows the default in the [Japanese technical-writing preset](https://github.com/textlint-ja/textlint-rule-preset-ja-technical-writing#1文の長さは100文字以下とする) and [sentence-length](https://github.com/textlint-rule/textlint-rule-sentence-length#options); it is a review prompt, not a scientifically validated readability boundary. The former 160-unit threshold was a provisional local choice. [GitHub Docs](https://docs.github.com/en/contributing/collaborating-on-github-docs/using-the-content-linter) also treats `MD011` and `MD018` as errors. Preferred names follow [GitHub](https://brand.github.com/foundations/logo), [OpenAI](https://openai.com/brand/), and [Node.js](https://nodejs.org/en/about/branding) official branding; local dictionary spellings and their severity remain project policy. Terminology stays advisory because a spelling match alone cannot distinguish a product name from an original quotation or identifier.

## Exceptions and Rule Changes

1. Prefer Markdown code for literal identifiers and code examples, block quotations for original quoted prose, and fenced blocks for deliberately malformed Markdown examples. Do not hide ordinary prose in those nodes to evade checks.
2. When a legitimate Markdown example cannot use those forms, add a reason and disable only the relevant rule around the smallest range. Re-enable it immediately. For example, `<!-- textlint-disable prh -->` and `<!-- textlint-enable prh -->`, or `<!-- markdownlint-disable-next-line MD018 -->`. A Japanese sentence can similarly use a narrow `sentence-length` exception. Keep a reason in a separate comment from a lint directive. Review suppressions as part of the document diff. For plain text, retain justified warnings rather than relying on Markdown structure or comment directives.
3. Add new dictionary entries with both correction and allowed examples in `terms.yml`'s `specs`. Add runner regression cases in `test.mjs` when behavior changes. Rerun the existing-document pilot below and the repository scan before promoting a warning or adding an error rule. Do not bulk-rewrite unrelated documents to satisfy a stylistic preference.
4. Keep CI and local use on the same checked-in configs and lockfile. CI failure becomes a merge gate only when repository branch/ruleset settings require its `Document lint` check. Those remote settings are not changed by adding a workflow.

Known exceptions are covered in `test.mjs`: an inline Japanese quotation containing `Github` and a plain-text `NodeJS` identifier still produce warnings but pass unchanged. Markdown block quotations and inline code are skipped. A legitimate `#hashtag` produces `MD018`, and the regex `(^|/)[Cc]+odespace/` produces `MD011`; each can use a documented next-line exception. Tests confirm that the same rule still detects the following unsuppressed line, and that warnings never hide real Markdown errors.

## Existing-Document Pilot — 2026-10-26

Ran against eight existing files without rewriting them. With the initial 160-unit threshold, applying `--ja` to all eight produced two length warnings; one was an irrelevant English-paragraph warning. After changing terminology to warning and length to 100, the former five-file Japanese selection produced 12 length warnings. Seven came from English instructions in `egov-whitepaper-route-map.md`, so that file now uses common alongside the other English/mixed references. The final four-file Japanese selection produces five advisory length findings and zero errors. All warnings were inspected; no source document was rewritten just to satisfy the limit.

| Existing file (repository-relative) | Final profile | Errors | Warnings | Inspection |
|---|---|---|---|---|
| `docs/keiba-prediction-agent-skill-design.md` | ja | 0 | 1 | Line 228: 123 units; a plugin-discovery recommendation with a literal path and field names. Retain; splitting is optional |
| `plugins/stray-japan-govdocs/mcp/administrative-procedures-mcp/README.md` | ja | 0 | 2 | Lines 103/189: 133/102 units. The setup sentence could be split into steps; the metadata explanation is only slightly over the limit. Advisory, retained |
| `plugins/stray-japan-govdocs/mcp/administrative-procedures-mcp/docs/dataset-yaml-guide.md` | ja | 0 | 1 | Line 47: 203 units. A useful clarity candidate combining editor behavior and a path condition; retain here because a rewrite is outside this lint-settings change |
| `plugins/stray-japan-govdocs/mcp/administrative-procedures-mcp/docs/development.md` | ja | 0 | 1 | Line 343: 104 units; explains a constraint and two schema choices. Retain; no forced split |
| `plugins/stray-japan-govdocs/references/egov-whitepaper-route-map.md` | common | 0 | 0 | English instructions with Japanese document names. At 100, ja incorrectly prompted review of seven English sentences (lines 7/13/14/81/83/84/88); use common |
| `plugins/stray-research/skills/japan-news-brief/references/fixed-format.md` | common | 0 | 0 | English instructions with Japanese format examples |
| `plugins/stray-studio/skills/japanese-ai-style-editor/references/editing-patterns.md` | common | 0 | 0 | Initial ja warning on English paragraph, line 23 (222 units); select common for this reference |
| `plugins/stray-studio/skills/japanese-ai-style-editor/references/validation-cases.md` | common | 0 | 0 | English instructions with deliberate Japanese editing cases |

The initial common-profile scan covered all 177 then-tracked Markdown/text files: zero errors and zero warnings. The final common scan includes this new guide (178 files), also with zero errors and zero warnings. The runner's ten regression tests pass under the CI runtime, Node.js 24.22.1, including the exact 100/101-unit boundary and the known exceptions above. This checks the selected rules' compatibility, not absence of writing problems. The pilot is a small, manually inspected sample, not a measured false-positive rate or runtime proof that an agent always invokes the checker. The repository workflow repeats the tracked-file common scan and the four Japanese-profile files above; the other four are already included in the common scan.
