---
name: "pixel-art-asset-creator"
description: "Use when the user wants to create, repair, adapt, or package pixel-art style assets for games, apps, docs, mascots, icons, sprites, tilesets, item sheets, or small animation loops from a concept, reference image, or asset brief. Do not use for Codex-compatible pet spritesheets that belong to hatch-pet, generic image editing, vector/logo design, full game implementation, screenshots, or broad brand identity work."
---

# Pixel Art Asset Creator

Create production-oriented pixel-art assets from a concept, visual reference, or asset brief. Keep the work focused on asset planning, image-generation prompts, frame or sheet consistency, transparent-background readiness, QA, and export guidance.

This skill generalizes the reliable parts of `hatch-pet`: canonical visual references, strict sprite-style contracts, row or sheet prompt planning, transparent-background discipline, forbidden artifact rules, and visual QA. It does not own Codex pet packaging, fixed pet atlas geometry, or `pet.json` creation.

## Generation Delegation

When the user wants actual visual assets produced, use the installed image generation capability for the visual work. Treat this skill's prompts as the authoritative visual specs: do not expand them into hero art, polished illustration, app-icon polish, marketing art, or generic image-generation embellishment.

The normal path does not require `OPENAI_API_KEY` in the repository environment. It should use the installed image generation capability, then record the selected output with `record_imagegen_result.py`.

Use deterministic tools only for work that is deterministic: organizing prompts, slicing generated sheets, composing contact sheets, resizing, converting formats, checking dimensions, or packaging files. Do not synthesize missing sprites, tiles, poses, or effects through local scripts as a substitute for image generation unless the user explicitly asks for procedural placeholder art.

If image generation is unavailable or blocked, stop and return the asset contract plus ready-to-run prompts. Do not claim that an asset was created.

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

## Inputs

Collect only the details that affect the asset. Infer reasonable defaults when the user is trying to move quickly.

- Asset type: sprite, icon, item, prop, tileset, character sheet, effect, avatar, or background tile.
- Target use: game engine, website, docs, app UI, social asset, placeholder, production asset, or exploration.
- Dimensions: exact size if known; otherwise choose a useful default such as `32x32`, `48x48`, `64x64`, `96x96`, or `192x192`.
- Sheet structure: standalone image, fixed grid, animation row, multi-row spritesheet, or tileset.
- Style constraints: palette, outline weight, resolution feel, perspective, lighting, mood, and allowed detail level.
- References: source images, sketches, screenshots, existing sprites, or brand colors.
- Export needs: transparent PNG/WebP, flat chroma-key background, contact sheet, frame list, or prompt pack.

## Default Style Contract

Use this style unless the user gives a stronger art direction:

```text
Pixel-art-adjacent game asset style: compact readable silhouette, low-resolution sprite logic, visible stepped edges, limited palette, crisp dark outline when appropriate, flat cel-style shading, one clear light direction, minimal texture, no tiny detail that disappears at target size, and clean transparent-background readiness.
```

Avoid:

- polished illustration, anime key art, 3D render, glossy app icon, vector mascot, painterly rendering, realistic fur or material texture, soft gradients, high-detail antialiasing, and excessive tiny accessories
- text, labels, UI panels, scenery, shadows, glows, halos, noisy particles, blurred motion, watermarks, visible grids, checkerboard transparency, and unrelated props
- colors close to the chroma key when a chroma-key workflow is being used

## Workflow

1. Define the asset contract.
   - Identify the asset type, target use, target dimensions, sheet structure, and reference sources.
   - Choose whether the asset should be a finished export, a prompt plan, or a repair pass.
   - Stop and ask one focused question only when the dimensions, frame count, or intended use would change the asset structure.

2. Establish the canonical look.
   - If references exist, use them as identity and design sources, not as images to copy literally.
   - If references are detailed, simplify them into the default pixel-art style before planning variants.
   - If no reference exists, create or specify one base asset first, then treat that base as the source of truth for every variant or frame.

3. Plan the sheet before generating.
   - For standalone assets, specify one centered asset with safe padding.
   - For icons or item sets, specify a consistent grid, scale, outline, palette, and lighting direction.
   - For animation, list each frame or row, the intended motion beat, and the exact frame count.
   - For tilesets, define tile size, edge behavior, repeatability, collision meaning when relevant, and which tiles connect to which neighbors.

4. Build generation prompts.
   - Use the prompt templates below as authoritative specs.
   - Attach reference images whenever the chosen generation path supports them.
   - Ask the image generation layer for clean assets only; use code or scripts only for deterministic assembly, slicing, resizing, contact sheets, or format conversion.
   - Do not create missing visual content through local scripts unless the user explicitly asks for procedural placeholder art.

5. Inspect and repair.
   - Check identity consistency, frame count, silhouette readability, palette consistency, transparency readiness, and target-size legibility.
   - Repair the smallest failing unit first: one asset, one frame, one row, then the whole sheet only when the base identity is wrong.
   - Treat geometry passing as necessary but not sufficient; visual identity and readability still decide acceptance.

6. Package the result.
   - Report final paths, dimensions, sheet structure, palette assumptions, and any known tradeoffs.
   - Include prompt files, contact sheets, or review notes when they are part of the requested deliverable.
   - If generation was blocked, return the asset contract and ready-to-run prompts instead of pretending the asset was produced.

## Bundled Scripts

Run these scripts with Pillow available. In this repository, prefer:

```bash
uv run --with pillow python <script> ...
```

The bundled scripts mirror the `hatch-pet` pipeline in a generic asset form:

- `prepare_asset_run.py`: create `asset_request.json`, prompt files, copied references, and `imagegen-jobs.json`
- `asset_job_status.py`: show ready and blocked visual generation jobs
- `record_imagegen_result.py`: record selected image generation outputs and create the canonical base reference
- `generate_asset_images.py`: secondary direct Image API fallback when the normal image generation skill cannot be used
- `extract_sheet_cells.py`: normalize chroma key or alpha, resize to the asset contract, and slice cells
- `inspect_asset_cells.py`: inspect extracted cells for empty cells, opaque backgrounds, clipping risk, and size outliers
- `compose_asset_sheet.py`: compose extracted cells into `final/asset.png` and `final/asset.webp`
- `validate_asset_sheet.py`: validate final dimensions, alpha, used cells, and unused cell transparency
- `make_contact_sheet.py`: create a labeled QA contact sheet
- `render_animation_preview.py`: create a GIF preview for sprite-row assets
- `queue_asset_repairs.py`: reopen the smallest relevant visual generation job with repair notes
- `package_asset_run.py`: one-step normalizer/packager for simpler runs
- `slice_asset_sheet.py`: export packaged cells as individual PNG files

## Default Script Workflow

1. Prepare the run.

```bash
uv run --with pillow python plugins/stray-studio/skills/pixel-art-asset-creator/scripts/prepare_asset_run.py \
  --asset-name "<Name>" \
  --description "<one sentence>" \
  --asset-type "<sprite|item-set|tileset|icon|prop>" \
  --target-size "64x64" \
  --sheet-structure "<standalone|sprite-row|item-set|tileset|sprite-sheet>" \
  --reference /absolute/path/to/reference.png
```

All arguments are optional except the ones needed to express the user's asset contract. If the user wants a quick standalone asset, omit sheet arguments. If the user wants animation, pass `--sheet-structure sprite-row --frame-count <n> --motion-beats "<beats>"`. If the user wants item or tile sets, pass `--item`, `--items`, `--tile`, or `--tiles`.

2. Inspect ready visual jobs.

```bash
uv run --with pillow python plugins/stray-studio/skills/pixel-art-asset-creator/scripts/asset_job_status.py \
  --run-dir /absolute/path/to/run
```

3. Generate each ready job with the installed image generation capability.
   - Use the prompt file listed by `asset_job_status.py`.
   - Attach every listed input image with its role label.
   - The `base` job may be prompt-only when no references exist.
   - Sheet jobs must use the canonical base reference created after the base job is recorded.

4. Record each selected generated output.

```bash
uv run --with pillow python plugins/stray-studio/skills/pixel-art-asset-creator/scripts/record_imagegen_result.py \
  --run-dir /absolute/path/to/run \
  --job-id <base|asset-sheet> \
  --source /absolute/path/to/generated-output.png
```

5. Finalize the run.

```bash
uv run --with pillow python plugins/stray-studio/skills/pixel-art-asset-creator/scripts/finalize_asset_run.py \
  --run-dir /absolute/path/to/run
```

Expected output:

```text
run/
  asset_request.json
  imagegen-jobs.json
  prompts/
  decoded/
  cells/
  final/asset.png
  final/asset.webp
  final/asset-manifest.json
  final/validation.json
  qa/contact-sheet.png
  qa/review.json
  qa/run-summary.json
  qa/previews/animation.gif
```

6. If QA fails, queue a targeted repair and regenerate only the reopened job.

```bash
uv run --with pillow python plugins/stray-studio/skills/pixel-art-asset-creator/scripts/queue_asset_repairs.py \
  --run-dir /absolute/path/to/run
```

Then repeat job status, image generation, result recording, and finalization.

Use the secondary fallback only when the installed image generation path is unavailable or blocked. This fallback calls the OpenAI Image API directly, so only this fallback requires `OPENAI_API_KEY`:

```bash
uv run --with pillow python plugins/stray-studio/skills/pixel-art-asset-creator/scripts/generate_asset_images.py \
  --run-dir /absolute/path/to/run \
  --model gpt-image-2
```

Do not use the fallback just because `OPENAI_API_KEY` is absent; absent API keys are fine for the normal installed-image-generation path.

## Prompt Templates

Use these templates directly or adapt them narrowly to the user's target. Keep prompts terse, asset-specific, and production-oriented.

### Base Asset

```text
Create a single clean pixel-art style asset for <asset-name>.

Asset: <one-sentence visual description>.
Target use: <game/app/docs/etc>.
Target size: <width>x<height>.
Style contract: <style contract>.

Use this prompt as an authoritative production asset spec. Do not expand it into a polished illustration, anime key art, 3D render, glossy icon, vector mascot, painterly image, or marketing artwork.

Output one centered complete asset only, with safe padding, on <transparent background or flat chroma-key background>. The asset must remain readable at <target size>. Do not include scenery, text, labels, borders, checkerboard transparency, detached effects, shadows, glows, or unrelated props.
```

### Sprite Or Animation Row

```text
Create a single horizontal pixel-art sprite strip for <asset-name> performing <state/action>.

Use the attached reference image(s) for identity and the attached base asset as the canonical design. Do not redesign the character, prop, palette, outline, material, or silhouette. Only change pose, expression, or action for this animation.

Output exactly <frame-count> separate animation frames arranged left-to-right in one single row. Treat the row as <frame-count> equal-width invisible frame slots. Fill every slot with exactly one complete centered pose. No pose may be cropped, overlap another pose, or cross into a neighboring slot.

Style contract: <style contract>.
Animation action: <motion beats>.
Background: <transparent or flat chroma-key>.

Do not include visible grid lines, borders, labels, frame numbers, scenery, checkerboard transparency, speed lines, motion blur, floor shadows, glows, dust, loose particles, or detached effects unless the brief explicitly requires an attached sprite effect.
```

### Tileset

```text
Create a pixel-art tileset for <environment/material>.

Tile size: <tile-size>.
Grid: <columns>x<rows>.
Tiles required: <list of terrain, edge, corner, transition, decoration, or collision-relevant tiles>.
Style contract: <style contract>.

Every tile must align to the same grid, use the same perspective and palette, and be readable at <tile-size>. Edge and transition tiles must connect cleanly to their neighbors. Do not include visible labels, UI, perspective drift, lighting drift, large shadows crossing tile boundaries, or non-repeatable seams unless the tile is explicitly decorative.
```

### Item Or Icon Set

```text
Create a pixel-art asset sheet of <count> <item/icon> assets for <use case>.

Grid: <columns>x<rows>.
Cell size: <cell-size>.
Items: <item list>.
Style contract: <style contract>.

Each cell must contain one centered complete asset with consistent scale, outline, lighting, palette discipline, and safe padding. Keep silhouettes distinct. Do not include text, labels, borders, scenery, shadows, glows, or duplicate-looking variants unless the brief asks for close variants.
```

## Transparency And Effects Rules

- Prefer pose, expression, silhouette, and palette changes over decorative effects.
- Use transparent output when reliable; otherwise use a flat chroma-key color that is absent from the asset.
- Effects are allowed only when they are part of the asset, opaque, hard-edged, pixel-style, and attached to or overlapping the main silhouette.
- Avoid floating punctuation, loose sparkles, loose particles, separated smoke, detached shadows, floor patches, glow, aura, blur, smears, and action streaks by default.
- Do not accept outputs with white boxes, checkerboard backgrounds, visible grids, labels, frame numbers, watermarks, cropped body parts, edge slivers, or unrelated background scenery.

## QA Checklist

Before calling the asset done, verify:

- dimensions and grid match the requested structure
- every used cell or frame contains exactly one complete asset or pose
- unused sheet space is transparent or intentionally empty
- the silhouette reads at the target size
- palette, outline, lighting, and material remain consistent
- references have been simplified rather than copied with too much detail
- animation frames create a readable motion instead of repeated near-duplicates
- tiles connect or repeat as required
- no forbidden detached effects, text, shadows, glows, labels, or backgrounds remain

## Output Expectations

- Final asset paths or, if not generated, a ready-to-use prompt pack.
- Asset contract: dimensions, grid, frame count, tile size, palette assumptions, and background strategy.
- QA notes describing what was inspected and what, if anything, remains risky.
- Repair notes when an asset was regenerated or narrowed.

## Guardrails

- Keep the job asset-specific; do not expand into full game design or broad brand identity.
- Do not claim exact pixel-perfect output from generative images unless it has been inspected and corrected.
- Do not substitute local transforms for meaningful missing poses or assets unless the user requested placeholder art.
- Do not upscale tiny generated art without checking that edges, transparency, and readability still hold.
- Do not use this skill for Codex pets; `hatch-pet` owns that specialized packaging and atlas contract.
