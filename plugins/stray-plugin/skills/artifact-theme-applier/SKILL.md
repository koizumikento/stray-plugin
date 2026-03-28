---
name: "artifact-theme-applier"
description: "Use when the user wants to apply a coherent visual theme to an existing artifact such as slides, docs, HTML pages, reports, or demos. Do not use for general UI review, brand strategy, or creating the artifact from scratch."
---

# Artifact Theme Applier

Apply one coherent visual theme to an existing artifact without changing the artifact's core content or structure. Treat the artifact as the source of truth and adjust styling, layout polish, and presentation details to make it feel intentional.

Use this skill when the user wants to restyle or unify an existing deliverable, especially when the request mentions:

- slides or pitch decks
- docs, reports, or one-pagers
- HTML pages or landing pages
- demos, artifacts, or shareable previews

## Do Not Use For

- reviewing code or UX quality as a critic
- creating a full artifact from a blank slate
- brand systems, marketing strategy, or identity design
- deep redesigns that change the artifact's purpose or content
- screenshot capture planning or single-image polish for launch assets
- styling work that should be handled by a site-wide design system instead of a one-off theme

## Workflow

1. Identify the artifact and the goal.
   - Determine the file type, audience, and where the artifact will be viewed.
   - Decide whether the user wants a theme applied, a theme adjusted, or a custom theme created from constraints.
   - Preserve the artifact's meaning, structure, and content unless the user explicitly asks for deeper changes.

2. Extract theme constraints.
   - Note any existing brand colors, fonts, spacing rules, tone, or visual references.
   - If no theme assets exist, infer a theme from the artifact's content, audience, and mood.
   - Keep the scope to a manageable theme system rather than inventing unrelated visual directions.

3. Choose or derive the theme.
   - Prefer an existing theme if one is already available and fits the artifact.
   - If no ready-made theme fits, define a custom theme with a small set of consistent tokens such as colors, typography, spacing, surfaces, and accent usage.
   - Make sure the theme supports readability and consistent contrast across the whole artifact.

4. Apply the theme consistently.
   - Update the artifact so headers, body text, backgrounds, accents, and highlights follow the same visual logic.
   - Keep component or slide structure intact unless a layout adjustment is needed to support readability.
   - Avoid mixing multiple visual styles unless the artifact intentionally has separate sections.

5. Check for fit and friction.
   - Look for low-contrast text, crowded spacing, mismatched fonts, and overused accent colors.
   - If the theme clashes with the artifact's content or format, simplify the design rather than layering on more effects.
   - Stop if the requested change would require a full redesign instead of theme application.

## Output Expectations

Return a concise summary that includes:

- the theme used or derived
- the main styling decisions applied
- any assumptions made because theme files or brand assets were missing
- the files or artifact areas changed

If no files were changed yet, explain what theme would be applied and what input is still needed.

## Guardrails

- Keep the work instruction-first and artifact-focused.
- Do not turn this into a general design critique.
- Do not overwrite the artifact's content unless the user asks for content edits.
- Do not expand the theme into unrelated product branding work.
- Do not add scripts or reference files unless a deterministic asset pipeline is actually needed.
