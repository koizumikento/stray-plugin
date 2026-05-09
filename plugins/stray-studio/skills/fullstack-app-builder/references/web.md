# Web Surface Reference

Use this reference when the primary user-facing surface is a browser-based application.

## Surface Conventions

- Follow the repository's established routing, rendering, hydration, and cache model.
- Treat SSR, CSR, static generation, and server actions as framework choices, not interchangeable patterns.
- Keep responsive layout, keyboard access, and browser navigation behavior part of the feature definition.
- For operational apps, keep the first screen focused on current objects, status, and likely next actions. Avoid turning app screens into landing pages unless the user explicitly asks for a marketing surface.
- Do not keep large forms permanently open in ordinary work screens. Prefer opening create, edit, bulk update, recovery, or settings forms only after explicit user intent, such as a button, selected row action, drawer, modal, bottom sheet, or routed edit state.
- When a form or action panel opens, provide a clear way to cancel or close it, preserve the user's current context, and prevent floating controls from covering submit or cancel actions.
- When the user points at the in-app browser or provides the current URL, treat that route, viewport, query string, route parameters, and selected object as part of the reproduction context.
- Preserve URL-driven state deliberately. Tabs, filters, selected rows, object IDs, and query parameters should not reset unexpectedly after edits, refreshes, or navigation unless that reset is the intended behavior.

## Common Risk Areas

- Check loading, error, empty, and retry states on real route transitions.
- Verify form behavior, focus management, scroll restoration, and URL-driven state.
- Watch for stale caches, duplicate submissions, and optimistic UI that can desync from server truth.
- Keep cookies, tokens, CSRF handling, and browser storage choices explicit.
- Confirm that primary actions show pending state, block duplicate submissions, and report success or failure visibly.
- Check that table, grid, card, drawer, modal, and bottom-sheet layouts do not hide required controls at mobile widths.
- Inspect dense screens for text overflow, overlapped controls, clipped localized or long labels, inaccessible icon-only buttons, and layout shifts caused by dynamic content.
- Prefer icon buttons only for familiar operations or when tooltips or accessible labels make the action clear.
- Avoid shipping placeholder sections, disabled controls, or "coming soon" paths inside the main workflow unless the product intentionally needs a visible staged state.
- After mutation, verify read-after-write behavior: updated local state, cache invalidation or revalidation, refreshed derived totals, and route state all need to match the server truth.
- For baseline-dependent review, comparison, or selection surfaces, verify what the baseline means. Missing baseline, current active item, candidate-only view, no-difference view, and one-candidate view often need different labels, columns, or actions.
- For read-only or locked domain states, verify both the UI affordance and server behavior: hidden or disabled controls are not enough if a direct request can still mutate protected data.
- For import, bulk edit, spreadsheet-like, and batch flows, verify dry-run or staging state separately from commit state, including row-level errors, duplicate rows, partial failures, paste behavior, and cancel/retry.
- Check local app config before running the browser path: env file name, ignored secret files, example env coverage, runtime bindings, API base URLs, auth origins, and seeded data assumptions.

## Browser Verification

- Start or reuse the local dev server when the app requires one, then visit the actual route or state that changed.
- If the in-app browser is already open on a relevant route, use that route as the first reproduction target before generalizing to other URLs.
- Check at least one normal desktop viewport and the smallest relevant mobile viewport when layout, navigation, forms, tables, or action panels changed.
- Capture or inspect the changed states that matter: default, loading, empty, error, editing, pending mutation, success, and failure.
- Capture or inspect the domain states that matter: no records, one record, many records, selected item missing, baseline missing, read-only or archived item, stale query parameter, and permission-denied response when they apply.
- For flows with bottom panels, drawers, popovers, dialogs, sticky headers, or floating actions, verify z-index, focus return, scroll locking, and that primary controls remain reachable.
- For mobile navigation, verify menu open and close behavior, active route indication, scroll position, touch target size, and whether primary work remains reachable after the menu changes.
- If browser verification is not possible, report the exact missing command, dependency, secret, service, or environment rather than replacing it with only a typecheck.
