# Prompt Templates

Use these templates directly or adapt them narrowly to the user's target. Keep prompts terse, asset-specific, and production-oriented.

## Default Exclusions

Avoid polished illustration, anime key art, 3D render, glossy app icon, vector mascot, painterly rendering, realistic fur or material texture, soft gradients, high-detail antialiasing, excessive tiny accessories, text, labels, UI panels, scenery, detached or floor shadows, glows, halos, noisy particles, blurred motion, watermarks, visible grids, checkerboard transparency, unrelated props, and colors close to the chroma key when a chroma-key workflow is used. Simple shading within the asset is allowed under the material-color plan.

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

Output one centered complete asset only, with safe padding, on <transparent background or flat chroma-key background>. The asset must remain readable at <target size>. Do not include scenery, text, labels, borders, checkerboard transparency, detached effects, detached or floor shadows, glows, or unrelated props.
```

### Refine The Final-Size Base Before Variants

1. Inspect the extracted base at native size and nearest-neighbor enlargement. Count distinct RGB colors only where alpha is nonzero, and report alpha separately. Treat color count as a diagnostic, not a quality score.
2. For a compact sprite with noisy shading, compare a 32–64-color candidate with the original as a starting experiment, not a mandatory limit. Preserve small identity colors, eye highlights, outline contrast and material distinctions. Avoid dithering by default; it can turn smooth color noise into flickering pixel noise. Keep alpha and dimensions unchanged during color reduction.
3. Refine the base's disconnected noise pixels, stair-step contours and inconsistent line widths with an available image-editing capability. Keep intentional hair strands and highlights. Do not claim that nearest-neighbor shrinking or palette mapping repairs a pixel grid. Inspect the result before adopting it as the canonical final-size reference.
4. Preserve the original and record the chosen base hash, dimensions, palette target/actual count and protected details in a run-local QA note. Use the same accepted base for all variants. If that base changes, rebuild dependent frames and repeat pixel-lock and visual checks; do not mix versions or independently quantize each frame.
   Before generation, list the actual attached files and their version/hash: accepted design, final-size color/pixel-density authority, and any native geometry reference. A raw image may supplement the accepted base, but must not silently replace its refined color authority. Record how the export palette derives from that same accepted version.
5. Use that accepted base as the visual authority for proportions and pixel density; do not add competing textual redesigns or repeatedly reduce processed references. For articulated characters, note limb lengths, ankle/heel/toe shape and footwear volume where visible. Inspect source poses against the base at a common comparison scale before accepting them for extraction. Pose-driven foreshortening and occlusion are valid; unexplained shrinking, fused boots and missing joints are not.

```text
Refine the attached base sprite at <final width>x<final height> before animation.
Preserve identity, silhouette, proportions, framing, alpha and these critical details: <details>.
Use <palette target or supplied palette> as a candidate, preserving separate readable colors for <materials/eyes/outline>.
Remove accidental speckled shading, group coherent pixel clusters, and keep consistent stepped contours and line weight. No dithering, blur, new texture or extra details.
Output one complete base frame. Do not create animation variants yet.
```

### Material Colors And Stable Shading

1. Separate static mottling from temporal flicker. Inspect a paused frame for scattered near-identical shades, then compare the same hair lock, garment panel or body surface across adjacent frames and the loop boundary. Distinguish unwanted paint changes from pose, occlusion and intentional lighting changes; background spill requires the transparency repair path.
2. Record a compact material-color plan in the run's prompt and QA note: for each material, name its base color, optional shadow/highlight and where those colors may appear, plus the light direction and its frame of reference (for example screen-space upper-left). Sample actual colors from visually verified interiors of the accepted base, excluding outlines, antialiasing and key spill. Equal RGB values can belong to different materials; color alone does not identify a region. Reuse colors where appropriate and add shades only for readable form or identity. Preserve outline, eyes, trim and near/far limb readability; this is not a universal three-color cap.
3. Establish broad connected base and shadow regions on the accepted base at final size. Remove accidental speckles and dithering with the installed image-editing capability. Preserve intentional isolated details; do not apply blanket small-component deletion, blur or a spatial filter that erases eyes, hair tips or outlines.
4. Carry material roles and lighting through all poses. Keep shadow placement tied to the turning/bending surface, not fixed screen coordinates or a fixed percentage of each frame. Keep highlight shapes simple and sparse. Palette mapping alone cannot impose these regions; independent per-frame quantization can introduce additional color changes.
   For skin, specify actual base/shadow colors from the accepted reference, and compare face, hands and exposed limbs together. Preserve near/far contrast through consistent overlap and justified shading; do not invent a different skin tone whenever a limb changes phase. A fixed all-material palette still permits switching between its colors. Inspect raw colors before assuming cleanup or palette conversion caused the drift.
   Check explicit color values against the accepted export palette. If reduction changed them, reconcile the plan and reference before proceeding; record any intentional approximate mapping. Neither a color name in a prompt nor global nearest-RGB mapping enforces a material-specific color role.
5. For a paint-only repair, use the accepted poses as geometry references and explicitly preserve limb arrangement, lean, compression, silhouette, framing and timing. Regenerate/repaint the inconsistent material regions with the installed image-editing capability; verify geometry and motion again because generation can change them. Do not use stationary pixel lock on locomotion. Keep original frames and review white/dark backgrounds and normal/slow playback before accepting the new paint. If the canonical material plan changes, update the base and all dependent frames together.

```text
Paint using this shared material-color plan: <material: base, shadow, optional highlight>. Light direction and frame of reference: <choice>.
Use broad coherent color regions with simple shadow boundaries and sparse highlights. No accidental speckled shading or dithering. Preserve essential tiny details and near/far limb contrast.
Across poses, let shadows follow the changing surfaces and occlusion under the same lighting; do not freeze shadow pixels to the canvas or randomly change their coverage.
For this paint-only repair, preserve the accepted poses, silhouette, forward lean, compression, framing and frame sequence. Simplify inconsistent paint without reducing the action's energy. If the declared plan omits shadows/highlights for a material, keep it flat; do not add lighting variation to distinguish near and far legs.
```

### Flat-Color Diagnostic For Recurring Drift

1. Find the first failing stage using the source-to-export checks in `qa-rules.md`. If raw generation already changes a material's base color, stop repeating global palette reduction. If only cleanup/export introduces the change, repair that stage instead of repainting correct source art.
2. Select a small set of already accepted poses exposing the problem: for a walk, both sides' contact and passing poses are sufficient to start. Keep the accepted base and pose references; do not ask for new motion while testing paint. Generate a separate diagnostic candidate with one flat base color per affected material and no optional shadows/highlights there. Keep eyes, outlines, trim and overlap boundaries. Other materials may retain their accepted shading. This is a temporary diagnostic, not permission to replace the user's approved style.
3. Compare material-relative interiors in raw and final-size candidates, using the same reference version, background strategy and export palette. A matching palette count is insufficient. If base fills still change, repair the affected source regions and repeat this small probe; do not expand it into the full animation. Never infer moving skin masks from fixed screen rectangles or one RGB threshold, or paste one pose's skin pixels into other poses.
4. Once base fills are visually consistent, restore only the shadows needed by the approved style, with a clear anatomical/material boundary such as the underside of a hair lock. Check those boundaries through the same poses before proceeding to the full cycle. If the flat probe is stable but the shaded candidate flickers, the remaining defect is shading placement; reducing the global palette again is not a fix. Preserve the diagnostic and record which candidate is the final color authority. Repeat whole-motion review after any repaint.

```text
Diagnostic paint pass on these accepted complete poses; preserve geometry and frame order.
Affected materials: <skin: sampled base hex; hair: sampled base hex; ...>.
Use only each material's declared flat base fill in its interior. Omit optional shading/highlights on these materials for this diagnostic; preserve the approved colors and shading of other materials.
Keep eyes, outlines, trim, occlusion boundaries and full limb/boot shapes. Distinguish near/far limbs by overlap and outline, not a different skin base. No gradients, dithering or new texture.
```

## Sprite Or Animation Row

For stationary idle/blink that needs exact pixel consistency, prefer the restricted-edit template below. Establish the accepted base at final cell size and select the edit rectangles visually before generating variants. A full-row prompt is still useful for actions with broader pose changes, but does not guarantee byte-identical unchanged areas.

```text
Create a single horizontal pixel-art sprite strip for <asset-name> performing <state/action>.

Use the attached reference image(s) for identity and the attached base asset as the canonical design. Preserve proportions, costume, palette and outline style while changing pose, expression and silhouette as the action requires.

Output exactly <frame-count> separate animation frames arranged left-to-right in one single row. Leave clear background gaps between complete poses. Keep roughly even spacing; honor the action's specified position changes relative to each nominal slot center. No pose may be cropped or overlap another pose. Final cell dimensions are an export contract: extraction finds whole poses before resizing, so do not draw separators or force limbs into exact equal-width cuts.

Keep facing orientation, body scale, pixel size, and safe margins consistent with the base. Use a shared ground-contact baseline; preserve intentional jump height, body compression and travel. For locomotion, follow the whole-body motion plan below; a stable loop with moving legs alone is insufficient.
Preserve limb lengths and footwear proportions through joint articulation and justified foreshortening, not shrinking or fusing feet. Follow the accepted material base/shadow colors across face, hands and limbs. These are visual constraints to verify in every source and final frame, not guarantees supplied by a common scale or palette.

For stationary idle/blink, hold torso, clothing, face proportions and planted feet at the same coordinates; change only <named animated parts>. Declare registration as <fixed contact / free intentional travel>. Do not align by the overall silhouette: hair and accessories can move independently of the feet.

Style contract: <style contract>.
Animation action: <motion beats>.
Playback: <loop or single action>. For a loop, connect the final pose back to the first; for a single action, show a readable beginning, action, and ending without forcing a return to the first pose.
Background: <transparent or flat chroma-key>.

Do not include visible grid lines, borders, labels, frame numbers, scenery, checkerboard transparency, speed lines, motion blur, floor shadows, glows, dust, loose particles, or detached effects unless the brief explicitly requires an attached sprite effect.
```

### Action Design Before Motion Beats

1. Describe the intended impression in one sentence: who is acting, toward what purpose, with what effort, weight and emotion. Infer a sensible choice from the brief and record it; an action name such as "run" does not specify its performance.
2. Translate that impression into a few visible choices: the overall curve/direction through head, chest and pelvis (line of action), forward/backward lean, weight relative to supporting limbs, limb reach, and pose timing. Use animation judgment appropriate to anatomy and style, not a universal angle or a requirement that every body part move more. When the pose is unfamiliar or ambiguous, inspect a suitable motion reference before choosing the beats.
3. Use contrasts as design options, not biomechanical rules: an urgent accelerating run might lead with the chest and a pronounced forward lean; an easy jog might be more upright with compact swings; a heavy landing might show deeper compression and slower recovery. A jump can read through anticipation and extension, a strike through wind-up and follow-through, and a stop through braking and settling. Preserve the chosen character performance across the cycle instead of applying the same energetic-run recipe to every action.
4. Generate or select representative key poses and visually judge them at target size before requesting intermediate frames. For locomotion, establish both sides' contact and passing/support poses, then check the same leg's support-to-swing path, boot volume and opposite arms. Captions or a full-row phase list do not satisfy this check. Use accepted key poses to guide the row; revise posture and weight placement when the requested impression fails instead of adding bounce or speed.
5. Put these concrete choices in the generation prompt and review note. Distinguish stable design traits from expressive pose changes, and revise the chosen performance when the user says its impression is wrong even if technical QA passes.

### Locomotion Motion Plan

1. State run-in-place versus traveling motion and the requested energy (for example relaxed jog or forceful sprint). Use free registration for both. For humanlike running, plan contact/compression, push-off and flight over two alternating strides; adapt the beats to other anatomies and do not impose a flight phase on ordinary walking.
2. Describe the upper body at each beat: knees/hips absorb landing, chest responds to push-off, shoulders and hips counter-rotate with opposite arm swing, and the head follows the torso. Specify a readable change in lean and vertical position rather than identical head/chest coordinates. Match exaggeration to the brief; consistency means stable design and proportions, not a frozen torso.
3. Distinguish near/far limbs through consistent overlap or restrained shading. Follow one identified leg through contact, loading, passing and release, then the opposite leg; changing arm direction alone does not prove leg alternation. Let hair and clothing follow the body with appropriate delay, remaining attached.
4. Separate root trajectory from movement within the pose and from the row's drawn spacing. For motion in place, preserve planned sway/bounce without cumulative horizontal drift; for travel, preserve the requested trajectory. Compare corresponding phases and the loop using a visually identified waist/pelvis reference; silhouette centers are only warnings. During stance, the foot moves backward relative to the body. Never copy an idle upper body across running frames or align every head/foot to a constant point.
5. Replace the stationary paragraph in a hand-written row prompt with this motion plan. The preparation script omits stationary lock instructions for `--registration free`; check the actual prompt and add the character-specific beats before generation.

Example motion beats for an energetic humanlike run (adapt amplitude and frame count to the brief):

```text
Run in place facing right, two alternating strides. Land with knees/hips compressed and chest leaning forward; push off as the chest rises; show a distinct airborne pose before the opposite foot lands. Swing arms opposite their legs, with shoulder/hip counter-rotation. Let the head respond to the torso and twin tails follow a beat later. Preserve proportions but visibly change the upper-body pose. Keep the overall root near the same slot, with intentional sway and bounce; do not freeze head, chest or feet. Close the loop in pose and momentum, not just matching endpoints.
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

Each cell must contain one centered complete asset with consistent scale, outline, lighting, palette discipline, and safe padding. Keep silhouettes distinct. Do not include text, labels, borders, scenery, detached or floor shadows, glows, or duplicate-looking variants unless the brief asks for close variants.
```
