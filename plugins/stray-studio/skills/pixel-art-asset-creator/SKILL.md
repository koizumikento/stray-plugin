---
name: "pixel-art-asset-creator"
description: "Use when the user wants to create, repair, adapt, or package pixel-art style assets for games, apps, docs, mascots, icons, sprites, tilesets, item sheets, or small animation loops from a concept, reference image, or asset brief. Do not use for Codex-compatible pet spritesheets that belong to hatch-pet, generic image editing, vector/logo design, full game implementation, screenshots, or broad brand identity work."
---

# Pixel Art Asset Creator

Create production-oriented pixel-art assets from a concept, visual reference, or asset brief. Keep the work focused on asset planning, image-generation prompts, frame or sheet consistency, transparent-background readiness, QA, and export guidance.

This skill generalizes the reliable parts of `hatch-pet`: canonical visual references, strict sprite-style contracts, row or sheet prompt planning, transparent-background discipline, forbidden artifact rules, and visual QA. It does not own Codex pet packaging, fixed pet atlas geometry, or `pet.json` creation.

## Use This Skill When

- the user wants pixel-art sprites, tiles, icons, props, items, UI badges, avatars, small mascots, effects, or animation frames
- the user provides reference art and wants it simplified into a pixel-art asset style
- the user needs a spritesheet, tileset, contact sheet, frame plan, or prompt set for image generation
- the user asks to repair pixel-art asset problems such as identity drift, inconsistent palettes, bad transparency, missing frames, or crowded sheets

## Do Not Use For

- Codex-compatible animated pet assets, `8x9` pet atlases, `pet.json`, or `${CODEX_HOME}/pets/`; use `hatch-pet`
- full game or app implementation; use an app-building skill
- brand strategy, logo design, or broad visual identity systems
- marketing screenshots, Slack GIF exports, or general image editing without pixel-art asset constraints
- exact hand-authored pixel art where the user explicitly wants every pixel placed manually

## Generation Delegation

When the user wants actual visual assets produced, use the installed image generation capability for the visual work. Treat this skill's prompts as authoritative visual specs: do not expand them into hero art, polished illustration, app-icon polish, marketing art, or generic image-generation embellishment.

The normal path does not require `OPENAI_API_KEY` in the repository environment. Use deterministic scripts only for organizing prompts, slicing generated sheets, composing contact sheets, resizing, converting formats, checking dimensions, and packaging files.

If image generation is unavailable or blocked, stop and return the asset contract plus ready-to-run prompts. Do not claim that an asset was created.

## Inputs

Collect only the details that affect the asset. Infer reasonable defaults when the user is trying to move quickly.

- Asset type: sprite, icon, item, prop, tileset, character sheet, effect, avatar, or background tile.
- Target use: game engine, website, docs, app UI, social asset, placeholder, production asset, or exploration.
- Dimensions: exact size if known; otherwise choose a useful default such as `32x32`, `48x48`, `64x64`, `96x96`, or `192x192`.
- Sheet structure: standalone image, fixed grid, animation row, multi-row spritesheet, or tileset.
- Style constraints: palette, outline weight, resolution feel, perspective, lighting, mood, and allowed detail level.
- References: source images, sketches, screenshots, existing sprites, or brand colors.
- Export needs: transparent PNG/WebP, flat chroma-key background, contact sheet, frame list, or prompt pack.

## Normal Path

1. Define the asset contract.
   - Identify the asset type, target use, target dimensions, sheet structure, and reference sources.
   - Choose whether the asset should be a finished export, a prompt plan, or a repair pass.
   - Ask one focused question only when dimensions, frame count, or intended use would change the asset structure.

2. Establish the canonical look.
   - If references exist, use them as identity and design sources, not as images to copy literally.
   - If references are detailed, simplify them into the default pixel-art style before planning variants.
   - If no reference exists, create or specify one base asset first, then treat that base as the source of truth for every variant or frame.

3. Plan the sheet before generating.
   - For standalone assets, specify one centered asset with safe padding.
   - For icons or item sets, specify a consistent grid, scale, outline, palette, and lighting direction.
   - For animation, list each frame or row, the intended motion beat, and exact frame count.
   - For tilesets, define tile size, edge behavior, repeatability, collision meaning when relevant, and neighbor connections.

4. Build generation prompts.
   - Load `references/prompt-templates.md` when writing or adapting prompts.
   - Attach reference images whenever the chosen generation path supports them.
   - Ask the image generation layer for clean assets only.
   - Do not create missing visual content through local scripts unless the user explicitly asks for procedural placeholder art.

5. Run deterministic packaging when needed.
   - Load `references/script-workflow.md` when the output needs prompt files, run directories, slicing, validation, contact sheets, animation previews, or packaged PNG/WebP exports.
   - Use scripts for deterministic assembly, slicing, resizing, contact sheets, validation, or format conversion.
   - Record selected generated outputs with `record_imagegen_result.py` when using the bundled workflow.

6. Inspect and repair.
   - Load `references/qa-rules.md` before accepting generated or packaged assets.
   - Check identity consistency, frame count, silhouette readability, palette consistency, transparency readiness, target-size legibility, and forbidden artifacts.
   - Repair the smallest failing unit first: one asset, one frame, one row, then the whole sheet only when the base identity is wrong.

7. Package and hand off.
   - Report final paths, dimensions, sheet structure, palette assumptions, background strategy, and any known tradeoffs.
   - Include prompt files, contact sheets, previews, or review notes when they are part of the requested deliverable.
   - If generation was blocked, return the asset contract and ready-to-run prompts instead of pretending the asset was produced.

## Default Style Contract

Use this style unless the user gives a stronger art direction:

```text
Pixel-art-adjacent game asset style: compact readable silhouette, low-resolution sprite logic, visible stepped edges, limited palette, crisp dark outline when appropriate, flat cel-style shading, one clear light direction, minimal texture, no tiny detail that disappears at target size, and clean transparent-background readiness.
```

## Reference Loading

- `references/prompt-templates.md`: default style exclusions and prompt templates for base assets, animation rows, tilesets, item sets, and icon sets.
- `references/script-workflow.md`: bundled script catalog, default run/finalize flow, fallback Image API flow, and expected output tree.
- `references/qa-rules.md`: transparency, effects, forbidden artifacts, acceptance checklist, and repair rules.

Load only the reference needed for the current path. A simple prompt-only answer may need only `prompt-templates.md`; a generated packaged spritesheet usually needs all three.

## Output Expectations

- Final asset paths or, if not generated, a ready-to-use prompt pack.
- Asset contract: dimensions, grid, frame count, tile size, palette assumptions, and background strategy.
- QA notes describing what was inspected and what remains risky.
- Repair notes when an asset was regenerated or narrowed.

## Guardrails

- Keep the job asset-specific; do not expand into full game design or broad brand identity.
- Do not claim exact pixel-perfect output from generative images unless it has been inspected and corrected.
- Do not substitute local transforms for meaningful missing poses or assets unless the user requested placeholder art.
- Do not upscale tiny generated art without checking that edges, transparency, and readability still hold.
- Do not use this skill for Codex pets; `hatch-pet` owns that specialized packaging and atlas contract.
