# Slack CLI Workflow

Use this reference for Slack CLI-centered work: project creation, initialization, inspection, validation, local run, workspace install, deploy, `slack api`, auth checks, and CI/CD command wiring.

## Official Docs

Use current official Slack docs before relying on remembered command behavior:

- Slack CLI overview: https://docs.slack.dev/tools/slack-cli/
- Install for Mac and Linux: https://docs.slack.dev/tools/slack-cli/guides/installing-the-slack-cli-for-mac-and-linux/
- Authorizing the Slack CLI: https://docs.slack.dev/tools/slack-cli/guides/authorizing-the-slack-cli/
- Running Slack CLI commands: https://docs.slack.dev/tools/slack-cli/guides/running-slack-cli-commands/
- `slack create`: https://docs.slack.dev/tools/slack-cli/reference/commands/slack_create/
- `slack install`: https://docs.slack.dev/tools/slack-cli/reference/commands/slack_install/
- `slack deploy`: https://docs.slack.dev/tools/slack-cli/reference/commands/slack_deploy/
- `slack manifest`: https://docs.slack.dev/tools/slack-cli/reference/commands/slack_manifest/
- `slack api`: https://docs.slack.dev/tools/slack-cli/reference/commands/slack_api/
- Slack CLI commands in GitHub Actions: https://docs.slack.dev/tools/slack-github-action/running-slack-cli-commands/
- Deno Slack SDK docs, when a Deno template is selected: https://docs.slack.dev/tools/deno-slack-sdk/

## Scope

- `slack create`, `slack init`, `slack run`, `slack install`, `slack deploy`
- `slack manifest validate`, manifest inspection, and source-of-truth checks
- `slack auth`, `slack login`, `slack auth list`, and service-token guidance that does not expose token values
- `slack api` for development checks, one-off Web API calls, or scripted automation
- GitHub Actions or other CI/CD jobs that invoke Slack CLI commands

## `slack create` And Templates

Start by listing current templates rather than assuming a fixed set:

```bash
slack create --list --skip-update
```

As of a local check on 2026-06-04 with `slack v4.0.1`, the list included:

- Getting started: `slack-samples/bolt-js-starter-template`, `slack-samples/bolt-python-starter-template`
- Starter agent: `slack-samples/bolt-js-starter-agent` and `slack-samples/bolt-python-starter-agent` with subdirectories such as `claude-agent-sdk`, `openai-agents-sdk`, and `pydantic-ai` for Python
- Support agent: `slack-samples/bolt-js-support-agent` and `slack-samples/bolt-python-support-agent` with similar SDK subdirectories
- Automation apps: `slack-samples/bolt-js-custom-function-template`, `slack-samples/bolt-python-custom-function-template`, `slack-samples/deno-starter-template`

Use explicit templates when reproducibility matters:

```bash
slack create my-project -t slack-samples/bolt-js-starter-template
slack create my-project -t slack-samples/bolt-python-starter-template
slack create my-project -t slack-samples/deno-starter-template
slack create my-project -t org/monorepo --subdir apps/my-app
```

`slack create` clones the selected template, creates or updates `.slack/` project metadata, sets the manifest source to local/project in `.slack/config.json`, and may install project dependencies. Treat dependency install failures separately from project structure creation; a generated project can exist even when npm, pip, or Deno dependency setup fails.

## Generated Project Structure

Generated structure is template-dependent. Use a pruned file listing after `slack create` to verify the actual project before editing:

```bash
find . \( -path './node_modules' -o -path './.venv' -o -path './.git' \) -prune -o -maxdepth 3 -type f -print | sort
```

Representative selected files observed from current templates are:

Bolt for JavaScript starter:

```text
.env.sample
.slack/config.json
.slack/hooks.json
README.md
app-oauth.js
app.js
assets/icon.png
listeners/index.js
manifest.json
package.json
package-lock.json
```

Bolt for Python starter:

```text
.slack/config.json
.slack/hooks.json
README.md
app.py
app_oauth.py
assets/icon.png
listeners/__init__.py
manifest.json
pyproject.toml
requirements.txt
tests/__init__.py
```

Deno starter:

```text
.slack/config.json
.slack/hooks.json
README.md
assets/default_new_app_icon.png
datastores/sample_datastore.ts
deno.jsonc
functions/sample_function.ts
functions/sample_function_test.ts
manifest.ts
triggers/sample_trigger.ts
workflows/sample_workflow.ts
```

Key files:

- `.slack/config.json`: local Slack CLI project metadata. Recent generated projects set the manifest source under `manifest.source`.
- `.slack/hooks.json`: project hook commands used by Slack CLI, including manifest generation. For example, Bolt JavaScript templates use `@slack/cli-hooks`; Deno templates use `deno_slack_hooks`.
- `manifest.json` or `manifest.ts`: app manifest source for the project. JSON is common in Bolt templates; TypeScript is common in Deno Slack SDK templates.
- Runtime entry points: examples include `app.js`, `app.py`, `functions/*`, `workflows/*`, and `triggers/*`.

## Workflow Notes

1. Check the installed CLI and version with `command -v slack` and `slack version`.
2. Check workspace authorization with `slack auth list` without exposing credentials.
3. Use `slack doctor` when CLI, project, runtime, or auth state looks inconsistent.
4. Confirm whether local manifest files or remote app settings are the source of truth.
5. Validate manifest changes with `slack manifest validate` or the closest project-specific command.
6. Use `slack api auth.test` when token resolution or API access must be proven.
7. Prefer `slack auth list` and `slack api auth.test` over token-printing commands. Only use token-revealing commands when the user explicitly needs token extraction, suppress command output, and report only non-secret status.
8. Treat `slack install`, `slack deploy`, deletion commands, trigger mutation, and any Web API write or user-visible action as workspace-changing actions.

## Run, Install, Deploy, And Hosting Decisions

| Task | Prefer | Notes |
| --- | --- | --- |
| Local development | `slack run` or the repository's Slack-backed dev command | Confirms the local project/runtime path. It is not proof that production hosting or OAuth install is configured. |
| Workspace installation | `slack install` or project-specific app install commands | Use only after confirming the target workspace, app, and environment. Installing a CLI-managed app is not a substitute for implementing OAuth install routes and persistent installation storage for distributed Bolt apps. |
| Slack Platform deployment | `slack deploy` | Use only when the selected project is deployable to the Slack Platform, such as supported Deno Slack SDK or Slack-hosted app shapes. |
| Externally hosted Bolt deployment | Repository or host-specific deployment commands | Ordinary HTTP Bolt apps usually need external hosting, request URL configuration, signing-secret handling, OAuth redirect routes when applicable, and persistent installation storage. |
| Web API checks | `slack api <method>` | Read-only methods can verify access. Mutating methods require explicit target workspace, channel, user, app, and expected side effect. |

## CI/CD Notes

- Prefer service-account-owned service tokens for shared automation.
- Never print service token values.
- Keep CI commands explicit and pin CLI versions when reproducibility matters.
- Separate validation jobs from install/deploy jobs when the repository's workflow supports that distinction.
- In Slack GitHub Action CLI usage, the action receives the command without the leading `slack` prefix, and a `token` input is passed to the CLI as `--token`.

## Web API Notes

- Use official Slack API method docs for parameters, scopes, pagination, rate limits, and error behavior.
- For repeated or scripted calls, handle pagination, `Retry-After`, duplicate work, and idempotency.
- Use `--json` for structured request bodies when it avoids quoting ambiguity.
- Treat methods such as `chat.postMessage`, `chat.update`, `conversations.create`, `files.upload`, `pins.add`, `reactions.add`, trigger mutation, and modal operations as writes even when invoked through `slack api`.
