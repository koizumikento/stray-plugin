# UI Review

Use this reference when reviewing screens, frontend flows, visual interaction, accessibility, responsive behavior, or user-facing product surfaces.

## Review Focus

1. Identify the workflow:
   - primary user goal
   - entry and exit points
   - critical states: loading, empty, error, success, disabled, offline, permission denied
2. Check usability and correctness:
   - information hierarchy supports the task
   - controls match their expected behavior
   - state transitions are predictable
   - destructive or irreversible actions are guarded
   - form validation is clear and server-backed when needed
3. Check accessibility:
   - keyboard navigation and focus order
   - labels, names, and target sizes
   - contrast and readable text
   - motion or animation does not block use
4. Check responsive and visual quality:
   - text does not overlap or overflow containers
   - fixed-format elements have stable dimensions
   - layout works across relevant viewport sizes
   - visual hierarchy fits the product context

## Output

- Findings first, tied to screen, state, or component.
- Prioritize workflow blockers, accessibility issues, and misleading UI over taste.
- Include verification gaps when no browser or screenshot evidence was available.

## Guardrails

- Do not convert UI review into implementation unless requested.
- Do not judge only the static happy path when the workflow has important states.
- Do not use aesthetic preference as a blocker without user impact.
