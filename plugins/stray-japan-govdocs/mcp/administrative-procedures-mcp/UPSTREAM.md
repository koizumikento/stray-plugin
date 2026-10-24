# Vendored upstream

This directory is a source snapshot of
[`digital-go-jp/administrative-procedures-mcp`](https://github.com/digital-go-jp/administrative-procedures-mcp).

- Upstream commit: `8d104339178f1aad8afbcee790eb541827574a74`
- Upstream package version: `0.3.0`
- Vendored on: `2026-08-14`
- License: MIT; see `LICENSE` and `NOTICE` in this directory

Local normalization: two whitespace-only test lines were stripped so repository
diff checks pass; executable content is unchanged.

Local security maintenance (2026-10-24): refreshed only the transitive `certifi`
lock entry from `2026.7.22` to `2026.10.19`, including distribution hashes, for
[GHSA-6q48-6c7w-9gw2](https://github.com/certifi/python-certifi/security/advisories/GHSA-6q48-6c7w-9gw2).
This is a local dependency update, not a new upstream snapshot; the upstream
commit, package version, Python `>=3.10` requirement, source, license, and notice
remain as recorded above. The containing plugin is version `0.1.7`.

The plugin starts this MCP with `uv run --locked --extra excel`; update the
installed plugin and resynchronize its environment to receive the refreshed
bundle. Existing installations and other Python environments are not updated by
this repository change. The government-download and OpenAI image-generation
helpers use `urllib` with Python's default SSL trust, so their OS/installer CA
stores remain a separate maintenance responsibility. Review Python installers,
pip/uv (including their bundled certificates), and system trust separately using
the [Python security release guidance](https://blog.python.org/2026/10/python-3151-3149-31317/).
This change does not modify system trust or address every Python vulnerability.

The snapshot includes the server, CLI, UI resources, dataset definition, lockfile,
tests, and upstream documentation. Published survey data is intentionally not
vendored. `apcli fetch procedures-survey-r6` retrieves it from the Digital Agency
source declared in `datasets/procedures-survey-r6/dataset.yaml`.

## Update policy

Update only from a reviewed immutable upstream commit. Preserve upstream license
and notice files, record the new commit and package version here, review changes to
network destinations and dataset definitions, run the upstream test suite, and
then bump the `stray-japan-govdocs` plugin version.
