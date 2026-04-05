# Rust Reference

Use this reference when the repository's primary app implementation language is Rust.

## Quality And Tooling Defaults

- Follow the repository's existing commands first.
- When no stronger repository convention exists, prefer `cargo fmt` for formatting, `cargo clippy` for linting and static checks, and `cargo test` for tests.
- Keep framework-specific test harnesses and integration setup aligned with the app already in use.

## Runtime And Package Management

- Prefer the standard Cargo toolchain already defined by the repository.
- Do not introduce alternate environment or package management layers unless the repository already depends on them.
- If the repository uses Nix or a pinned toolchain, follow that setup rather than working around it.

## Ecosystem Conventions

- Follow the repository's existing module, runtime, async, and FFI conventions instead of mixing patterns across frameworks or crates.
- Keep request, command, IPC, and persistence contracts explicit at the boundary where data enters the system.
- Prefer the surface-specific reference for browser rendering, mobile lifecycle, desktop windows, or packaging concerns.

## Common Risk Areas

- Check blocking work inside async contexts and confirm the runtime model still holds under load.
- Review error conversion paths so user-facing failures are explicit and logs still carry enough detail.
- Verify transaction handling, migration order, and data rollback assumptions on write paths.
- Treat native integration, filesystem access, and privileged OS calls as security-sensitive boundaries.
