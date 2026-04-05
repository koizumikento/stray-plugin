---
name: "marketing-screenshot-creator"
description: "Use when the user wants to plan or produce app screenshots for docs, landing pages, release notes, demos, or social posts, especially when they need polished captures with consistent framing, sizing, and annotations. Do not use for general frontend review, design critique, or Playwright debugging."
---

# Marketing Screenshot Creator

Plan and produce polished screenshots that present a product clearly and consistently. Focus on deciding what to capture, how to frame it, and how to export the final images for the intended channel.

Use this skill when the user needs screenshots for:

- documentation
- marketing pages
- release notes
- launch posts
- product demos

## Do Not Use For

- general UI or frontend code review
- visual design critique that does not end in screenshots
- Playwright troubleshooting or browser automation debugging
- image editing beyond preparing the capture itself
- artifact-wide theming or restyling of full docs, slides, or reports
- test strategy for app behavior

## Workflow

1. Identify the screenshot brief.
   - Confirm the target surface, audience, destination, and format.
   - Ask for missing details only when they affect the capture plan: viewport size, device type, theme, crop ratio, overlays, and whether text callouts are needed.
   - Stop if the user wants a redesign instead of a screenshot plan.

2. Choose the smallest useful capture set.
   - Prefer a few representative shots over many redundant ones.
   - Decide which state each screenshot must show.
   - Include empty, loading, error, or comparison states only if they are part of the message.

3. Define the framing before capturing.
   - Set viewport, zoom, and layout constraints to match the destination.
   - Decide what to hide, crop, blur, or annotate.
   - Keep spacing, alignment, and browser chrome consistent across the set.

4. Capture the screenshots.
   - Use the app or page state that best demonstrates the requested message.
   - Re-run captures when the framing is off, the content is cut off, or the composition is distracting.
   - Prefer repeatable capture steps over manual one-off tweaking.

5. Polish only what improves clarity.
   - Add annotations, callouts, or crops only when they help the viewer understand the point quickly.
   - Keep styling minimal and consistent with the destination.
   - Avoid turning the task into a design exercise.

6. Verify the final set.
   - Check readability, cropping, focus, and consistency.
   - Confirm the files are named and organized for the target use.
   - Stop once the screenshots communicate the intended story cleanly.

## Output Expectations

- State the chosen capture plan and the intended use of each screenshot.
- Report the final file names or export locations.
- If the screenshots were not captured yet, return the planned shot list, framing choices, and missing prerequisites instead.
- Call out any assumptions that were necessary.
- Note any unresolved capture constraints, such as unavailable app states or missing assets.

## Guardrails

- Do not expand into general UI review or product design advice.
- Do not debug browser automation unless the user explicitly asked for that work.
- Do not overproduce variants when one clear capture will do.
- Do not change application code unless the user explicitly asks for capture support changes.
- Do not add extra files or tooling unless they materially improve reproducibility.
