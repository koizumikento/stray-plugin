# TypeScript And JavaScript Reference

Use this reference when the repository's primary app implementation language is TypeScript or JavaScript.

## Quality And Tooling Defaults

- Follow the repository's existing scripts and lockfile first.
- For greenfield or unsettled repositories, prefer `Vite+` as the baseline quality workflow when it fits the chosen surface.
- In practice, prefer `vp check` for formatting, linting, and type checking, and `vp test` for tests when that toolchain is in play.
- Do not replace an established stack with `Vite+` unless the user explicitly asks for that migration.

## Runtime And Package Management

- Keep one clear package manager and lockfile per app or workspace.
- Prefer the repository's existing Node, Bun, pnpm, npm, or Yarn workflow over introducing another.
- If the repository already uses Nix, follow it for shell and toolchain setup instead of bypassing it.

## Ecosystem Conventions

- Follow the repository's existing module boundary, workspace, bundler, and build conventions.
- Keep shared contracts, schema definitions, and validation logic explicit when code crosses client, server, worker, or desktop boundaries.
- Prefer the surface-specific reference for routing, SSR, native bridges, IPC, lifecycle, or packaging decisions instead of encoding all of that here.

## Common Risk Areas

- Watch for client and server validation drifting apart.
- Check shared type contracts for runtime mismatches hidden by compile-time assumptions.
- Avoid mixing incompatible runtimes, bundlers, or test environments inside one feature.
- Verify environment boundary handling for secrets, browser-only APIs, native modules, and server-only code.
