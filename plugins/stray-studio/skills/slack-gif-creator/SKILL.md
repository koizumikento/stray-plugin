---
name: "slack-gif-creator"
description: "Use when the user wants a short animated GIF for a Slack emoji, message, or lightweight demo and needs loop design, crop, export, live constraint checks, and size optimization. Do not use for generic image editing, full video or motion-graphics production, static screenshots, or UI review."
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
   - Distinguish custom emoji upload from message/file upload; they can have different format, dimension, byte-size, duration, and workspace-policy limits.
   - Before final export, verify the current constraints in official Slack Help or developer documentation for the intended path and record the source and check date. Do not treat remembered numbers as platform guarantees.
   - If current official limits cannot be verified, use `128x128` for emoji-style drafts or `480x480` for message-sized drafts only as working targets, label compliance unverified, and do not claim the file is Slack-ready.
   - Use a practical `10-30 fps` working range and prefer short loops, then adjust to the verified upload limits and visual need.
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
   - Inspect and report actual pixel dimensions, encoded byte size, frame count, frame timing or total duration, and format; compare each measurable property with the live constraints for the selected Slack path.
   - Only when the user explicitly requests or approves an upload test, test the file in the intended Slack workspace without posting it publicly; otherwise treat the upload path as unverified.
   - If the result is too large or muddy, change only one variable at a time: crop, timing, or palette.

## Output Expectations

- State the intended Slack use case and the chosen dimensions.
- State the verified constraint source and check date, plus actual bytes, dimensions, frames, and duration; otherwise label platform compliance unverified.
- Return the final GIF and, if useful, a short note on the loop logic or export tradeoff.
- If source material is still missing, return the asset request and loop plan instead of pretending the GIF is ready.
- If the file still feels too heavy, name the specific constraint that needs to change.

## Guardrails

- Do not turn this into generic animation advice.
- Do not expand into video editing or motion design systems.
- Do not over-polish details that will disappear after Slack compression.
- Do not proceed without enough source material to define the loop clearly.
- Do not claim Slack compatibility from hardcoded dimensions alone or silently rely on stale upload limits.
- Do not upload a GIF to a Slack workspace merely to validate it; require an explicit request or approval for that external change.
