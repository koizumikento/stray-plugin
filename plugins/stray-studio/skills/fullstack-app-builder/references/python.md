# Python Reference

Use this reference when the repository's primary app implementation language is Python.

## Quality And Tooling Defaults

- Follow the repository's existing commands first.
- Before settling on validation commands, inspect the repo for Python workflow signals in scripts, docs, config, lockfiles, or CI.
- When the repository does not have a clear quality baseline, prefer `ruff` for linting and formatting checks, `ty` for static type checking, and `pytest` for tests.
- If those tools are not used, record the existing command source instead: package scripts, task runner, framework CLI, tox/nox, make targets, or CI workflow.
- Keep migrations, fixture setup, and app startup commands consistent with the framework already in use.

## Runtime And Package Management

- Prefer `uv` for environment and package management when the repository is greenfield or the workflow is still unsettled.
- Before adding or running dependency commands, check for `uv.lock`, `pyproject.toml`, Poetry, pip-tools, plain `requirements.txt`, virtualenv conventions, Nix, or framework-specific setup docs.
- If the repository already uses Poetry, pip-tools, plain `venv`, or Nix, follow that established workflow instead of migrating it during feature work.

## Ecosystem Conventions

- Prefer the repository's established application framework, job runner, and packaging approach before adding parallel libraries.
- Keep validation, persistence, and background work boundaries explicit instead of hiding business logic inside glue code.
- Prefer the surface-specific reference for navigation, UI lifecycle, native packaging, or browser behavior.

## Common Risk Areas

- Check ORM query behavior for N+1 issues, transaction boundaries, and partial writes when persistence is involved.
- Treat migrations and data backfills as operational changes with rollout implications.
- Verify background tasks, external calls, and retries separately from the foreground interaction path when user-visible behavior depends on them.
- Keep secrets, local file access, and permission-sensitive operations explicit.
