# Web Surface Reference

Use this reference when the primary user-facing surface is a browser-based application.

## Surface Conventions

- Follow the repository's established routing, rendering, hydration, and cache model.
- Treat SSR, CSR, static generation, and server actions as framework choices, not interchangeable patterns.
- Keep responsive layout, keyboard access, and browser navigation behavior part of the feature definition.

## Common Risk Areas

- Check loading, error, empty, and retry states on real route transitions.
- Verify form behavior, focus management, scroll restoration, and URL-driven state.
- Watch for stale caches, duplicate submissions, and optimistic UI that can desync from server truth.
- Keep cookies, tokens, CSRF handling, and browser storage choices explicit.
