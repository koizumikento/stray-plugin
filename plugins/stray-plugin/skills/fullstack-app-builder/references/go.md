# Go Reference

Use this reference when the repository's primary app implementation language is Go.

## Quality And Tooling Defaults

- Follow the repository's existing commands first.
- When no stronger repository convention exists, prefer `gofmt` for formatting, `go test` for tests, and `go vet` for built-in static checks.
- If the repository already uses `golangci-lint`, follow it rather than introducing a parallel lint stack.

## Runtime And Package Management

- Prefer the standard Go toolchain and module system already defined by the repository.
- Do not add alternate environment or package management layers unless the repository already depends on them.
- If the repository already uses Nix or another reproducible shell, work inside that setup instead of bypassing it.

## Ecosystem Conventions

- Favor the repository's existing package layout, handler or service boundaries, and concurrency patterns.
- Keep auth, request validation, IPC, or background job checks close to the boundary where data enters privileged code.
- Prefer the surface-specific reference for browser rendering, mobile shells, desktop windows, or packaging concerns.

## Common Risk Areas

- Watch for implicit zero values masking validation mistakes.
- Check context cancellation, timeout, and error propagation paths on outbound calls and long-running requests.
- Review transaction boundaries, idempotency, and retry safety on write paths.
- Verify filesystem, OS integration, and local state handling when the feature touches the host environment.
