---
name: "slack-gif-creator"
description: "Use when the user wants a Slack-friendly animated GIF from scratch or from provided images/screenshots, and needs guidance on Slack export constraints, loop timing, crop decisions, and file-size optimization. Do not use for generic image editing, video production, or UI review."
---

# Slack GIF Creator

Create short GIFs that read clearly inside Slack and stay small enough to share without friction. Keep the work focused on one loop, one message, and one export target.

Use this skill when the user asks for:

- a GIF for Slack emoji or a channel message
- an animated reaction, loop, or quick visual explanation
- a GIF built from screenshots, existing images, or a simple screen capture

## Do Not Use For

- general image editing or illustration
- full video editing, audio, or subtitle work
- UI critique, code review, or product design review
- static screenshot planning or artifact-wide theme work
- long-form motion graphics or marketing video production

## Workflow

1. Define the target and the message.
   - Ask whether the GIF is for emoji, a message, or a lightweight demo.
   - Ask what the GIF must communicate in one sentence.
   - If the source material is missing, stop and request the image, screenshot, or a concrete scene description.

2. Set Slack-specific constraints first.
   - Use `128x128` for emoji-style GIFs and `480x480` for message-sized GIFs unless the user asks for something else.
   - Aim for `10-30 fps`, with short loops preferred over long sequences.
   - Keep emoji-style loops under about `3 seconds`.
   - Reduce colors aggressively and assume no audio.

3. Plan a simple loop.
   - Choose one action, one beat, and one ending state.
   - Prefer cuts, zooms, highlights, or a single motion path over busy animation.
   - If starting from screenshots, crop out everything that does not support the loop.

4. Build the frames.
   - If creating from scratch, sketch the frame sequence before editing.
   - If using screenshots or source images, normalize spacing and remove clutter before animating.
   - Keep small details, thin text, and subtle UI decorations to a minimum.

5. Optimize the export.
   - Trim frame count before relying on compression.
   - Test palette reduction and verify the motion still reads at Slack size.
   - Make sure the first and last frames connect smoothly.
   - Favor a compact, readable loop over a high-resolution file with visual noise.

6. Validate the result.
   - Confirm the GIF is readable at its intended display size.
   - Confirm the loop lands within the first second and loops cleanly.
   - If the result is too large or muddy, change only one variable at a time: crop, timing, or palette.

## Output Expectations

- State the intended Slack use case and the chosen dimensions.
- Return the final GIF and, if useful, a short note on the loop logic or export tradeoff.
- If source material is still missing, return the asset request and loop plan instead of pretending the GIF is ready.
- If the file still feels too heavy, name the specific constraint that needs to change.

## Guardrails

- Do not turn this into generic animation advice.
- Do not expand into video editing or motion design systems.
- Do not over-polish details that will disappear after Slack compression.
- Do not proceed without enough source material to define the loop clearly.
