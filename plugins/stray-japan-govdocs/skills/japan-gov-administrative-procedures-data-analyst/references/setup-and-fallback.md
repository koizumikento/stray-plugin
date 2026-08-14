# Setup and fallback

Resolve the MCP directory from the installed plugin root. Relative to this skill
directory it is `../../mcp/administrative-procedures-mcp/`; in this repository it
is:

`plugins/stray-japan-govdocs/mcp/administrative-procedures-mcp/`

Run all commands below with that directory as the working directory. Do not assume
the repository path when the plugin is installed in a cache or another workspace.

## Runtime states

1. **MCP and data available** — use `list_datasets`, `inspect_dataset`,
   `summarize_records`, and `query_records`.
2. **MCP available, data missing** — announce the first official fetch, then run:

   ```text
   uv run --locked --extra excel apcli fetch procedures-survey-r6 --allowed-host www.digital.go.jp
   ```

3. **MCP unavailable, shell available** — use the equivalent CLI operations:

   ```text
   uv run --locked --extra excel apcli list
   uv run --locked --extra excel apcli inspect procedures-survey-r6
   uv run --locked --extra excel apcli summarize procedures-survey-r6 ...
   uv run --locked --extra excel apcli query procedures-survey-r6 ...
   ```

   Label results `bundled CLI fallback`; they use the same registry and query
   implementation but are not an MCP tool call.
4. **Neither MCP nor shell available** — report that the bundled server could not
   be started and provide the required `uv` command. Do not replace the requested
   analysis with guessed values.

## Effects and destinations

- Dependency environment: `.venv/` in the bundled MCP directory.
- Downloaded dataset: `datasets/procedures-survey-r6/data.parquet`.
- Retrieval metadata: `datasets/procedures-survey-r6/.fetch.json`.
- Temporary source downloads are managed by the upstream fetcher and are not a
  durable citation target.

The upstream `.gitignore` excludes these generated artifacts. Do not add them to
version control. Leave them for reuse after success or failure; remove them only
on the user's explicit cleanup request.

## Failure handling

- Missing `uv`: report the missing executable and stop.
- Lock or dependency failure: preserve the error summary; retry once only if the
  correction is concrete and remains locked.
- Official page/asset failure: report the page URL, allowlisted host, and last
  verified stage. Retry once; do not broaden to arbitrary hosts.
- Parse/schema failure: do not edit the downloaded workbook or relax the schema to
  force success. Report that the upstream source or parser needs review.
- Missing data during an MCP call: fetch once, then restart/reconnect the MCP so it
  rebuilds the registry before retrying the tool.
