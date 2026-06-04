# Runtime Implementation

Use this reference for Slack app behavior implemented in a runtime such as Bolt for JavaScript, Bolt for Python, Deno Slack SDK, or an existing custom app. Keep runtime guidance tied to the selected Slack surface and the repository's existing patterns.

## Official Docs

Use current official Slack docs before relying on remembered framework behavior:

- Bolt for JavaScript overview: https://docs.slack.dev/tools/bolt-js/
- Bolt for JavaScript quickstart: https://docs.slack.dev/tools/bolt-js/getting-started/
- Bolt for JavaScript reference: https://docs.slack.dev/tools/bolt-js/reference/
- Bolt for Python overview: https://docs.slack.dev/tools/bolt-python/
- Bolt for Python creating an app: https://docs.slack.dev/tools/bolt-python/creating-an-app/
- Bolt for Python reference: https://docs.slack.dev/tools/bolt-python/reference/
- Bolt JS actions/interactivity: https://docs.slack.dev/tools/bolt-js/concepts/actions/
- Bolt Python actions/interactivity: https://docs.slack.dev/tools/bolt-python/concepts/actions/
- Bolt Python Web API usage: https://docs.slack.dev/tools/bolt-python/concepts/web-api/
- Slack app manifests: https://docs.slack.dev/app-manifests/
- Slack Web API methods: https://docs.slack.dev/reference/methods/
- Slack authentication overview: https://docs.slack.dev/authentication
- Slack token types: https://docs.slack.dev/authentication/tokens/
- Verifying Slack requests: https://docs.slack.dev/authentication/verifying-requests-from-slack/

## Scope

- slash commands, events, interactivity, shortcuts, modals, app home, workflow triggers, functions, and datastores
- handler implementation, request acknowledgement, retries, duplicate delivery, and side effects
- Slack Web API calls made from application code
- runtime secrets by name, such as `SLACK_BOT_TOKEN`, `SLACK_APP_TOKEN`, and `SLACK_SIGNING_SECRET`
- OAuth installation credentials such as `SLACK_CLIENT_ID`, `SLACK_CLIENT_SECRET`, state secrets, redirect paths, and installation stores

## Bolt For JavaScript Or Python

1. Follow the repository's existing package manager, app structure, handler style, and test commands.
2. Confirm required env var names without printing values.
3. Keep each handler path small and verifiable: command, event, action, modal submission, or Web API call.
4. Acknowledge Slack requests quickly; move slow work to an existing background mechanism when available.
5. Make repeated event or command side effects idempotent when duplicate delivery can create duplicate records or messages.
6. Keep OAuth scopes aligned with the manifest and actual Web API calls.

## Bolt Template Structure

Generated structure varies by selected template and version. Verify the local tree before editing:

```bash
find . \( -path './node_modules' -o -path './.venv' -o -path './.git' \) -prune -o -maxdepth 3 -type f -print | sort
```

Representative selected files from the Bolt for JavaScript starter observed from `slack create <name> -t slack-samples/bolt-js-starter-template` on 2026-06-04 with `slack v4.0.1`:

```text
.env.sample
.slack/config.json
.slack/hooks.json
README.md
app-oauth.js
app.js
assets/icon.png
listeners/actions/index.js
listeners/actions/sample-action.js
listeners/commands/index.js
listeners/commands/sample-command.js
listeners/events/app-home-opened.js
listeners/events/index.js
listeners/index.js
listeners/messages/index.js
listeners/messages/sample-message.js
listeners/shortcuts/index.js
listeners/shortcuts/sample-shortcut.js
listeners/views/index.js
listeners/views/sample-view.js
manifest.json
package.json
package-lock.json
```

Representative selected files from the Bolt for Python starter observed from `slack create <name> -t slack-samples/bolt-python-starter-template` on 2026-06-04 with `slack v4.0.1`:

```text
.slack/config.json
.slack/hooks.json
README.md
app.py
app_oauth.py
assets/icon.png
listeners/__init__.py
listeners/actions/__init__.py
listeners/actions/sample_action.py
listeners/commands/__init__.py
listeners/commands/sample_command.py
listeners/events/__init__.py
listeners/events/app_home_opened.py
listeners/messages/__init__.py
listeners/messages/sample_message.py
listeners/shortcuts/__init__.py
listeners/shortcuts/sample_shortcut.py
listeners/views/__init__.py
listeners/views/sample_view.py
manifest.json
pyproject.toml
requirements.txt
tests/__init__.py
```

Key files:

- `app.js` or `app.py`: runtime entry point. Current starter templates initialize the Bolt app, register listeners, and start Socket Mode.
- `listeners/`: handler modules grouped by Slack surface. Current starter templates split actions, commands, events, messages, shortcuts, and views.
- `manifest.json`: app manifest for scopes, slash commands, shortcuts, events, app home, interactivity, Socket Mode, and bot user settings.
- `app-oauth.js` or `app_oauth.py`: OAuth-oriented entry point in starter templates. Use only when the app's install/OAuth flow requires it.
- `package.json` or `requirements.txt`: runtime dependencies and local validation commands.
- `.slack/hooks.json`: Slack CLI hook integration. Bolt JavaScript starter templates use `@slack/cli-hooks`; Bolt Python starter templates use `slack-cli-hooks`.

## Credentials And Secrets Matrix

Do not assume every Bolt app only needs `SLACK_BOT_TOKEN` and `SLACK_APP_TOKEN`. Required values depend on how the app receives Slack traffic and whether it handles OAuth installation.

Common runtime values:

| Name | Typical use | Notes |
| --- | --- | --- |
| `SLACK_BOT_TOKEN` | Bot Web API calls for a single installed workspace | Usually an `xoxb-` bot token. Common in simple Socket Mode starters. Do not use as the only credential model for distributed OAuth installs. |
| `SLACK_APP_TOKEN` | Socket Mode connection | Usually an `xapp-` app-level token. Needed by current Bolt JS/Python Socket Mode starter templates. |
| `SLACK_SIGNING_SECRET` | HTTP request verification and OAuth receiver setup | Required when Slack sends HTTP requests to the app and in Bolt OAuth examples. Slack signing secrets replace deprecated verification tokens. |
| `SLACK_CLIENT_ID` | OAuth installation flow | Found in app Basic Information. Required for distributed or re-installable OAuth flows. |
| `SLACK_CLIENT_SECRET` | OAuth installation flow | Secret from app Basic Information. Rotate carefully; client secret rotation has deployment impact. |
| `SLACK_STATE_SECRET` | OAuth state generation/verification in Bolt JS examples | Bolt JS OAuth docs use this as the state secret. Some templates hardcode a development placeholder; production should use a secure config value. |
| `SLACK_SCOPES` | Optional env-driven OAuth bot scopes | Bolt Python OAuth internals can read comma-separated scopes from env when scopes are not passed explicitly. Many apps keep scopes in code or manifest instead. |
| `SLACK_USER_SCOPES` | Optional env-driven OAuth user scopes | Use only when the app intentionally needs user tokens. Keep bot and user scopes separate. |
| `SLACK_REDIRECT_URI` | Optional explicit OAuth redirect URI | Needed when overriding default redirect behavior or when deployment routes require an absolute redirect URI. |
| `SLACK_API_URL` | Optional Slack API base URL override | Present in generated Bolt JS starter client options. Rarely needed outside testing or special environments. |
| `PORT` | HTTP receiver port | Used by generated Bolt JS OAuth entry point. Python OAuth starter starts on `3000` unless changed. |

Token and secret categories:

- Bot token: app installation token used for bot-scoped Web API calls.
- User token: token for acting on behalf of a user; only request user scopes when the app behavior truly requires it.
- App-level token: app-wide token used by Socket Mode and select app-level APIs.
- Client secret: OAuth credential used during installation flows; never treat it as a runtime bot token.
- Signing secret: HMAC verification secret for Slack HTTP requests; do not use the deprecated verification token.
- State secret or state store: protects OAuth state verification during install; do not hardcode production state secrets.
- Service token: Slack CLI automation token for supported CLI workflows. Keep it separate from app runtime tokens.

For OAuth install flows:

- Bolt JS OAuth docs require `clientId`, `clientSecret`, `stateSecret`, `scopes`, and usually an `installationStore`; examples pass `signingSecret` too.
- Bolt Python OAuth docs use `OAuthSettings` with `client_id`, `client_secret`, `scopes`, `installation_store`, and `state_store`; `App` receives `signing_secret`.
- Production OAuth installs need persistent installation storage. File stores are development conveniences, not production storage.
- Redirect routes must match Slack app settings. Bolt Python defaults include `/slack/install` and `/slack/oauth_redirect`; Bolt JS defaults can be customized with `installerOptions`.
- Store installation data by team, enterprise, and user dimensions as needed; do not collapse multi-workspace installs into one token.
- CLI workspace installation is not the same as a distributed Bolt OAuth install flow. If the app must be installable by other workspaces, implement OAuth routes, state validation, and persistent installation storage.

## Bolt Runtime Defaults Observed In Starters

Treat these as template observations, not permanent API guarantees:

- Bolt JavaScript starter uses ESM, `@slack/bolt`, `dotenv`, Socket Mode, `SLACK_BOT_TOKEN`, and `SLACK_APP_TOKEN`.
- Bolt Python starter uses `slack_bolt.App`, `SocketModeHandler`, `SLACK_BOT_TOKEN`, and `SLACK_APP_TOKEN`.
- Bolt JavaScript OAuth starter path uses `SLACK_SIGNING_SECRET`, `SLACK_CLIENT_ID`, `SLACK_CLIENT_SECRET`, a state secret, OAuth scopes, and an installation store.
- Bolt Python OAuth starter path uses `SLACK_SIGNING_SECRET`, `SLACK_CLIENT_ID`, `SLACK_CLIENT_SECRET`, `OAuthSettings`, `FileInstallationStore`, and `FileOAuthStateStore`.
- Both starter manifests included app home, a global shortcut, `/sample-command`, `commands`, `chat:write`, `channels:history`, `app_home_opened`, `message.channels`, interactivity, and Socket Mode.
- Bolt JavaScript starter scripts included `npm run start`, `npm run dev`, `npm run lint`, and `npm test`.
- Bolt Python starter dependencies included `slack-bolt`, `slack-cli-hooks`, `pytest`, and `ruff`.

## Bolt Implementation Workflow

1. Identify the Slack surface first: command, action, view submission, shortcut, event, message, app home, or Web API call.
2. Find the matching listener group before adding a new pattern:
   - JavaScript: `listeners/commands`, `listeners/actions`, `listeners/events`, `listeners/messages`, `listeners/shortcuts`, `listeners/views`
   - Python: same grouping under Python packages in `listeners/`
3. Confirm the manifest declares the Slack surface:
   - slash command in `features.slash_commands`
   - shortcut in `features.shortcuts`
   - event in `settings.event_subscriptions.bot_events`
   - interactivity enabled in `settings.interactivity`
   - required scopes in `oauth_config.scopes.bot`
4. Confirm runtime env var names. For Socket Mode starter apps, expect `SLACK_BOT_TOKEN` and `SLACK_APP_TOKEN`. For HTTP receiver deployments, expect signing-secret handling such as `SLACK_SIGNING_SECRET`.
5. For OAuth installation flows, confirm client ID, client secret, state secret or state store, scopes, redirect routes, and persistent installation storage.
6. Keep listener IDs aligned with the manifest: slash command names, `callback_id`, `action_id`, event names, and view callback IDs.
7. Keep each handler path testable by isolating business logic from the Bolt listener wrapper when the change is non-trivial.
8. Use the injected or app-level Web API client rather than hand-rolled HTTP calls unless the repository has a clear reason.

## Request Handling And Reliability

- Acknowledge commands, actions, shortcuts, options, and view submissions quickly. In Bolt handlers this usually means calling `ack()` where the framework requires it.
- Do not perform slow LLM calls, network fan-out, or long database work before acknowledgement when the surface requires a fast response.
- Treat Events API deliveries and interactive submissions as retryable. Persist idempotency keys or dedupe by Slack identifiers when duplicate side effects matter.
- Preserve Slack request signature verification for HTTP receiver apps. Do not disable signature verification outside local test scaffolding.
- For Socket Mode apps, confirm the app token has the app-level scope required by the selected official docs and manifest.
- When posting messages or opening/updating modals, verify the manifest scopes match the Web API method being called.

## Validation

Prefer repository commands first, then Slack-specific checks:

```bash
slack manifest validate
slack api auth.test
slack run
```

For generated Bolt JavaScript starters, useful local commands may include:

```bash
npm run lint
npm test
npm run start
```

For generated Bolt Python starters, useful local commands may include:

```bash
python -m ruff check .
python -m pytest
python app.py
```

Use the actual repository's package manager and virtual environment. A generated Python project can exist even if dependency installation fails locally; separate scaffolding success from `pip`, `setuptools`, or virtualenv failures.

## Deno Slack SDK

1. Keep triggers, workflows, functions, datastores, and manifest changes consistent.
2. Prefer current official docs for platform behavior, because Deno Slack SDK details can move.
3. Validate manifest and trigger changes through the Slack CLI whenever possible.
4. Treat datastore writes and workflow steps as retryable where the platform can replay work.

## Custom Runtime Or Existing App

1. Preserve the existing HTTP routing, signature verification, deployment, and environment conventions.
2. Use Slack CLI for project inspection, manifest validation, authorization checks, API checks, install, and deploy where it fits.
3. Do not assume `slack deploy` deploys an externally hosted Bolt app. Ordinary HTTP Bolt apps need host-specific deployment plus Slack app request URL, OAuth redirect, and secret configuration.
4. Route broad non-Slack implementation changes to the general app builder; keep this reference focused on Slack app correctness.
