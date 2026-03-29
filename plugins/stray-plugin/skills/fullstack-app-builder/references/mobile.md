# Mobile Surface Reference

Use this reference when the primary user-facing surface is a mobile application.

## Surface Conventions

- Follow the repository's established screen navigation, lifecycle, state restoration, and native bridge patterns.
- Treat offline behavior, intermittent connectivity, and background or resume flows as part of correctness when the app depends on them.
- Keep platform permissions, deep links, notifications, and device capabilities explicit in the design.

## Common Risk Areas

- Check cold start, resume, backgrounding, and interrupted flows rather than validating only the happy path.
- Verify permission denial paths, degraded offline states, and retry behavior after reconnect.
- Watch for native module boundary issues, stale local caches, and duplicated sync writes.
- Confirm accessibility, touch targets, and platform-specific expectations on the target OS.
