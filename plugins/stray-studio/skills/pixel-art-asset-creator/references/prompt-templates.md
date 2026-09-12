# Prompt Templates

Use these templates directly or adapt them narrowly to the user's target. Keep prompts terse, asset-specific, and production-oriented.

## Default Exclusions

Avoid polished illustration, anime key art, 3D render, glossy app icon, vector mascot, painterly rendering, realistic fur or material texture, soft gradients, high-detail antialiasing, excessive tiny accessories, text, labels, UI panels, scenery, shadows, glows, halos, noisy particles, blurred motion, watermarks, visible grids, checkerboard transparency, unrelated props, and colors close to the chroma key when a chroma-key workflow is used.

## Base Asset

Choose the background before filling any template:

1. Prefer reliable transparent output. Otherwise inspect the intended subject palette, including small features such as eyes and gems, and choose a flat key color absent from it and its edge shades.
2. Consider green for pink/purple subjects and magenta for green subjects; check the entire palette before choosing. If neither is suitable, choose another absent color or request transparent output. Preserve the subject's colors rather than recoloring it to fit a key.
3. Specify the selected background in every prompt. The scripts do not choose a palette-safe key for you; chroma cleanup detects the painted background within the declared key family. If cleanup fails or damages the subject, revise the background strategy and regenerate the affected job.

```text
Create a single clean pixel-art style asset for <asset-name>.

Asset: <one-sentence visual description>.
Target use: <game/app/docs/etc>.
Target size: <width>x<height>.
Style contract: <style contract>.

Use this prompt as an authoritative production asset spec. Do not expand it into a polished illustration, anime key art, 3D render, glossy icon, vector mascot, painterly image, or marketing artwork.

Output one centered complete asset only, with safe padding, on <transparent background or flat chroma-key background>. The asset must remain readable at <target size>. Do not include scenery, text, labels, borders, checkerboard transparency, detached effects, shadows, glows, or unrelated props.
```

### Refine The Final-Size Base Before Variants

1. Inspect the extracted base at native size and nearest-neighbor enlargement. Count distinct RGB colors only where alpha is nonzero, and report alpha separately. Treat color count as a diagnostic, not a quality score.
2. For a compact sprite with noisy shading, compare a 32–64-color candidate with the original as a starting experiment, not a mandatory limit. Preserve small identity colors, eye highlights, outline contrast and material distinctions. Avoid dithering by default; it can turn smooth color noise into flickering pixel noise. Keep alpha and dimensions unchanged during color reduction.
3. Refine the base's disconnected noise pixels, stair-step contours and inconsistent line widths with an available image-editing capability. Keep intentional hair strands and highlights. Do not claim that nearest-neighbor shrinking or palette mapping repairs a pixel grid. Inspect the result before adopting it as the canonical final-size reference.
4. Preserve the original and record the chosen base hash, dimensions, palette target/actual count and protected details in a run-local QA note. Use the same accepted base for all variants. If that base changes, rebuild dependent frames and repeat pixel-lock and visual checks; do not mix versions or independently quantize each frame.

```text
Refine the attached base sprite at <final width>x<final height> before animation.
Preserve identity, silhouette, proportions, framing, alpha and these critical details: <details>.
Use <palette target or supplied palette> as a candidate, preserving separate readable colors for <materials/eyes/outline>.
Remove accidental speckled shading, group coherent pixel clusters, and keep consistent stepped contours and line weight. No dithering, blur, new texture or extra details.
Output one complete base frame. Do not create animation variants yet.
```

## Sprite Or Animation Row

For stationary idle/blink that needs exact pixel consistency, prefer the restricted-edit template below. Establish the accepted base at final cell size and select the edit rectangles visually before generating variants. A full-row prompt is still useful for actions with broader pose changes, but does not guarantee byte-identical unchanged areas.

```text
Create a single horizontal pixel-art sprite strip for <asset-name> performing <state/action>.

Use the attached reference image(s) for identity and the attached base asset as the canonical design. Do not redesign the character, prop, palette, outline, material, or silhouette. Only change pose, expression, or action for this animation.

Output exactly <frame-count> separate animation frames arranged left-to-right in one single row. Leave clear background gaps between complete poses. Keep roughly even spacing; honor the action's specified position changes relative to each nominal slot center. No pose may be cropped or overlap another pose. Final cell dimensions are an export contract: extraction finds whole poses before resizing, so do not draw separators or force limbs into exact equal-width cuts.

Keep orientation, body scale, pixel size, and safe margins consistent with the base. Use a shared baseline for ground contact; preserve intentional jump height or travel instead of recentering each pose. Show actual limb movement and stable contact during walking or running.

For stationary idle/blink, hold torso, clothing, face proportions and planted feet at the same coordinates; change only <named animated parts>. Declare registration as <fixed contact / free intentional travel>. Do not align by the overall silhouette: hair and accessories can move independently of the feet.

Style contract: <style contract>.
Animation action: <motion beats>.
Playback: <loop or single action>. For a loop, connect the final pose back to the first; for a single action, show a readable beginning, action, and ending without forcing a return to the first pose.
Background: <transparent or flat chroma-key>.

Do not include visible grid lines, borders, labels, frame numbers, scenery, checkerboard transparency, speed lines, motion blur, floor shadows, glows, dust, loose particles, or detached effects unless the brief explicitly requires an attached sprite effect.
```

## Stationary Idle/Blink Restricted Edit

Use only for fixed-contact stationary motion. Inspect the final-size reference and select the mutable rectangles yourself; the script does not recognize eyes, hair, or other body parts. Give each rectangle as `[left, top, right, bottom]` in final-cell pixels, with right and bottom excluded. Include the whole intended motion and enough room for its outline; do not select the whole canvas. Preserve the same accepted reference for every edit, rather than chaining edits from previously generated variants.

```text
Edit the attached accepted <width>x<height> base frame of <asset-name> for stationary <idle/blink>.

Keep the canvas, pixel scale, orientation, lighting, and the coordinates of the torso, clothing and planted feet unchanged. Do not redraw the character.
Only change <named animated parts> inside these final-cell rectangles: <mutable rectangles and what each contains>.
Frame beat: <the specific eye/expression/small local movement for this frame>.
For a blink, keep the inner and outer corner of each eye at <visually measured coordinates>; keep eye width, brow position and lid line weight consistent. Change lid coverage and the visible iris only as required by this beat. Do not shift the whole eye, cheek or bangs.
Use only colors already visible in the accepted base; preserve its outline weight and stepped pixel edges.
Keep all pixels outside the stated edit regions unchanged. Do not introduce motion or new details there.
Background: <the selected transparent or palette-safe flat chroma background>.
Output one complete frame with the same framing and padding as the reference; no labels, guides, grid, checkerboard, scenery or effects.
```

This is an editing prompt, not a new per-frame job runner. The bundled `asset-sheet` job still expects a complete row: adapt the output sentence and list all its frame beats when using this template for that job. Do not record a single-frame result as a completed multi-frame sheet.

Measure eye anchors from the accepted final-size base; omit the blink-specific sentence for other edits. Where a rectangular mask would include unrelated face or hair pixels, use smaller separate rectangles if they still enclose the complete moving lids. Anchors inside a mutable rectangle are prompt/visual constraints, not script-enforced locks. Check them in every extracted frame.

The generated edit may still change other pixels. After extraction and placement, verify cell 0 as the reference and use the opt-in pixel lock in `script-workflow.md` to copy unchanged regions from it. The script keeps generated pixels only inside the selected rectangles and maps their visible RGB to cell 0's nontransparent RGB palette while retaining alpha. It does not correct pixel-grid inconsistencies inside those rectangles. If an edit crosses their boundaries or needs a color absent from the base, revise the reference or edit contract and regenerate; do not hide the missing motion by copying the entire frame.

## Tileset

```text
Create a pixel-art tileset for <environment/material>.

Tile size: <tile-size>.
Grid: <columns>x<rows>.
Tiles required: <list of terrain, edge, corner, transition, decoration, or collision-relevant tiles>.
Style contract: <style contract>.

Every tile must align to the same grid, use the same perspective and palette, and be readable at <tile-size>. Edge and transition tiles must connect cleanly to their neighbors. Do not include visible labels, UI, perspective drift, lighting drift, large shadows crossing tile boundaries, or non-repeatable seams unless the tile is explicitly decorative.
```

## Item Or Icon Set

```text
Create a pixel-art asset sheet of <count> <item/icon> assets for <use case>.

Grid: <columns>x<rows>.
Cell size: <cell-size>.
Items: <item list>.
Style contract: <style contract>.

Each cell must contain one centered complete asset with consistent scale, outline, lighting, palette discipline, and safe padding. Keep silhouettes distinct. Do not include text, labels, borders, scenery, shadows, glows, or duplicate-looking variants unless the brief asks for close variants.
```
