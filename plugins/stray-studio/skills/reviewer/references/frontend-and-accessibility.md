# Frontend And Accessibility Review Aspects

Use this reference for UI, state management, design system, and client-side behavior.

## User-Visible Behavior

- Does the UI still behave correctly across loading, success, empty, and failure states?
- Are optimistic updates, transitions, or async state changes race-safe?
- Could the change produce flicker, stale data, or impossible states in the interface?
- Are mobile and narrow-layout behaviors still viable?

## Accessibility

- Is the change keyboard accessible?
- Are labels, names, roles, and focus order preserved?
- Are dynamic updates announced or otherwise perceivable when needed?
- Does color alone communicate state or meaning?

## State And Data Flow

- Is state derived in one place, or duplicated inconsistently?
- Could stale closures, dependency mistakes, or effect timing create bugs?
- Are input validation and form errors clear, recoverable, and correctly mapped to fields?
- Are permissions and feature flags enforced in data flow, not just visually hidden?

## Performance

- Does the change trigger unnecessary rerenders, refetches, or heavy work on input?
- Are large lists, expensive computations, or layout thrashing introduced?
- Are assets, bundles, or hydration costs increased materially?

## UX Quality

- Are destructive actions confirmable and reversible when appropriate?
- Does the interface communicate progress and failure without trapping the user?
- Is the chosen copy precise enough to prevent user error?
