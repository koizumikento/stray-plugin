# Vendored upstream

This directory is a source snapshot of
[`digital-go-jp/administrative-procedures-mcp`](https://github.com/digital-go-jp/administrative-procedures-mcp).

- Upstream commit: `8d104339178f1aad8afbcee790eb541827574a74`
- Upstream package version: `0.3.0`
- Vendored on: `2026-08-14`
- License: MIT; see `LICENSE` and `NOTICE` in this directory

Local normalization: two whitespace-only test lines were stripped so repository
diff checks pass; executable content is unchanged.

The snapshot includes the server, CLI, UI resources, dataset definition, lockfile,
tests, and upstream documentation. Published survey data is intentionally not
vendored. `apcli fetch procedures-survey-r6` retrieves it from the Digital Agency
source declared in `datasets/procedures-survey-r6/dataset.yaml`.

## Update policy

Update only from a reviewed immutable upstream commit. Preserve upstream license
and notice files, record the new commit and package version here, review changes to
network destinations and dataset definitions, run the upstream test suite, and
then bump the `stray-japan-govdocs` plugin version.
