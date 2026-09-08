# Client State Reference

Read this when ownership, identity scope, or lifetime of client state needs a decision, including drafts, navigation, caches, pending operations, stale responses, optimistic updates, and restoration. A presentation-only edit with settled behavior may skip it. Use the surface reference for platform APIs and rendering checks.

Sources were checked on 2026-09-08. React and TanStack examples describe their documented versions, not universal library defaults; inspect the installed framework before choosing APIs. The workflow and failure cases are application-design guidance, not a requirement for a global store or state-machine library.

## Workflow

1. Identify the affected state and its owner.
   - For each relevant value, name its authoritative input, owning component/screen/window/account, resource identity, writers, and required lifetime. Reuse existing framework state rather than duplicating it in another store.
   - Separate these meanings; do not force every flow to use every category. Avoid contradictory flags and separately stored values that can be derived reliably. See [React state structure](https://react.dev/learn/choosing-the-state-structure).

   | State | Decision |
   |---|---|
   | Local UI | Which component or window owns selection, focus, expansion, or an open dialog? |
   | Navigation | Must filters, sort, page, or selected IDs survive a link, reload, or Back/Forward? |
   | Fetched snapshot/cache | Which context identifies the result, when may it be stale, and who refreshes it? |
   | Edit draft | Which resource is being edited, and when is unsaved input kept, reset, or committed? |
   | Derived value | Can totals, selected objects, or filtered lists be calculated from existing state? |
   | Pending operation | What was requested, which attempt is pending, and what proves its result? |

2. Define preservation and reset before wiring updates.
   - If navigation state belongs in the URL, read it through the existing router rather than keeping an unsynchronized copy. Handle invalid values and missing targets. See [router state management](https://reactrouter.com/explanation/state-management).
   - Keep an edit draft's lifetime distinct from the fetched snapshot. Decide what happens on resource change, refetch, save, failure, and navigation; do not overwrite dirty input on every refetch or carry resource A's draft into B. Track a base version when concurrent editing needs conflict detection, not for every form. See [state preservation and reset](https://react.dev/learn/preserving-and-resetting-state).
3. Make response application match the current operation and context.
   - Associate a result with its requested resource, filters, and identity context before applying it. Use existing query identity, cancellation, or generation checks as appropriate; unmounting alone does not prove work or cache population stopped.
   - Distinguish abandoning a result from cancelling transport or undoing server work. Use [api-communication.md](api-communication.md) when cancellation or a lost write response needs a contract decision. TanStack Query's default unused-query behavior can retain completed results; consuming its AbortSignal changes cancellation behavior. See [query cancellation](https://tanstack.com/query/latest/docs/framework/react/guides/query-cancellation).
4. Define cache identity, freshness, and retention separately.
   - Include inputs that change the result in the key or cache-owner scope, including account/tenant when relevant. Use stable identifiers, not raw credentials, as cache keys. Reuse framework key conventions. See [query keys](https://github.com/TanStack/query/blob/main/docs/framework/react/guides/query-keys.md).
   - Decide when cached data is usable, when to refetch, and how long inactive or persisted data remains. Check mount, focus, reconnect, and mutation invalidation behavior. For example, TanStack Query v5 documents that `staleTime: 'static'` blocks invalidation-triggered refetch, unlike `Infinity`; verify the installed version rather than assuming invalidation always refreshes. See [important defaults](https://tanstack.com/query/latest/docs/framework/react/guides/important-defaults).
   - For account/tenant or permission changes, use [identity-access.md](identity-access.md) to determine the validity boundary. Retire or isolate prior-context requests, subscriptions, cache entries, and drafts so late results cannot restore old data. Include persisted caches and other windows when the app shares them; cache freshness never grants access.
5. Reconcile mutations without erasing unrelated work.
   - Distinguish a pending visual change from committed data. Choose local pending UI or a cache update according to which readers need the optimistic result; pessimistic confirmation is acceptable when speculation would complicate correctness.
   - Plan for overlapping mutations and completion out of order. Example: from `[A]`, optimistically add B; C then succeeds; B fails. Restoring B's entire starting snapshot `[A]` would also remove C. Use operation-specific rollback, constrained concurrency, or reconstruction from confirmed results as appropriate, and preserve newer edits.
   - Treat that example as a concurrency check, not a guarantee supplied by a library's simple rollback recipe. Handle refetch failure and unknown write outcomes explicitly. Client serialization does not prove database atomicity; use [data-persistence.md](data-persistence.md) for the storage guarantee. See [optimistic updates](https://tanstack.com/query/latest/docs/framework/react/guides/optimistic-updates) and [mutation ordering](https://tanstack.com/query/latest/docs/framework/react/guides/mutations).
6. Check additional lifetimes only when the target uses them.
   - For SSR, isolate user-specific request state and ensure server output and client hydration start from the intended snapshot. Use framework-supported serialization and transfer only authorized fields; do not put a shared user-specific QueryClient at module scope. React server `cache()` has request scope, which is not the lifetime of every framework cache. See [SSR and hydration](https://tanstack.com/query/latest/docs/framework/react/guides/ssr) and [React cache](https://react.dev/reference/react/cache).
   - For mobile/desktop, distinguish component removal, navigation, window/scene closure, backgrounding, process death, and explicit restart. Restore only the required identity, selection, input, or durable data, with invalid/missing targets handled. Android ViewModel survives configuration changes but not process death; saved-state mechanisms are not a general durable database. See [Android UI state saving](https://developer.android.com/topic/libraries/architecture/saving-states).
   - Separate shared models from window/scene-specific selections and drafts. Apple describes these ownership scopes in [Data Essentials in SwiftUI](https://developer.apple.com/videos/play/wwdc2020/10040/); use the 2020 talk for concepts and current platform docs for API choices.
   - For offline-first flows, distinguish the local source used by UI readers from server acceptance and cross-device conflict resolution. Show local persistence, pending sync, confirmation, or conflict when relevant. If unsent work must survive restart, use [data-persistence.md](data-persistence.md) and [async-workflows.md](async-workflows.md); a UI cache alone is not that guarantee. See [Android offline-first design](https://developer.android.com/topic/architecture/data-layer/offline-first).
7. Verify combinations that can break the changed flow.
   - Select relevant cases below; a label-only edit does not require this matrix. Report what was proven on the actual surface and what remains unverified across network, identity, persistence, or lifecycle boundaries.

| Case | Required observation |
|---|---|
| Search A then B; responses B then A | Current B state remains correct |
| Dirty draft during refetch or resource A/B navigation | Input is preserved or reset according to the declared policy |
| Mutation M2 succeeds before M1 fails | M1 recovery preserves M2 and any newer user edit |
| Logout or tenant switch before a response/subscription event arrives | Old-context results do not repopulate current state |
| Two simultaneous SSR users or two windows with different selections | Shared data and local state follow their declared scopes |
| Process death with pending offline edits | Promised local durability holds; pending work is not shown as server-confirmed |
