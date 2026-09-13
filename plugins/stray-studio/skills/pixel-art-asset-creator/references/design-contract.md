# Design Contract

Use this before creating a base or evaluating supplied assets. It owns the character design sheet, identity, proportions and color; animation sequencing belongs to `animation-workflow.md`.

## Run Context

1. For an execution run, keep a short `run-context.md` beside the run manifest, or use an existing equivalent note. Record the requested deliverable, current stage, next check and selected production path. This is human-readable execution context, not a new required script schema.
2. Link the approved design, motion and optional pixel-style references with their roles and revisions/hashes. Point to existing palette, frame/time and export manifests for details rather than copying their values into several documents.
3. Record the chosen action/view, dimensions, scale/ground/travel intent, loop versus single action, and what has passed or remains unverified. Keep subject-specific anatomy, local tool paths and trial results here, outside reusable instructions. Replace superseded choices in the active note; preserve rejected outputs separately as evidence.

## Character Design Sheet — Before Animation

1. For a character or mascot, create or inspect a small reusable design package before authoring motion. Reuse suitable user art; fill only missing information needed for the requested action/view. For prompt-only work, deliver a design brief and reference prompts with acceptance unverified. Package-only work documents supplied art without inventing a passed design history. Non-character icons, items and tiles skip this section.
2. Save the package under the asset workspace's `design/`: a `character-sheet.md` index plus selected reference images and palette. Record revision, accepted/candidate status, image paths and hashes, required views and unresolved details. These are operator-authored artifacts, not a new machine-validated schema or mandatory composite board.
3. Establish the following together, using actual viewed images and measured final-pixel examples rather than prose alone:

   | Design element | Record and inspect |
   | --- | --- |
   | Base and silhouette | One final-size standing sprite; face, head-to-body ratio, recognizable silhouette and outline weight |
   | Required views | Current view first; add front, side, back or oblique only when needed. Compare proportions and costume between views before accepting each; a generated turnaround is not automatically consistent |
   | Proportions and coordinates | Cell dimensions, body scale, neutral pelvis and ground coordinates; head, shoulder, waist, knee and ankle landmarks; thigh/shin lengths, boot shaft, heel and toe dimensions |
   | Identity details | Eye shape/placement, fringe shape, hair attachment points and length, accessories, garment seams/hem, footwear construction and anatomical left/right asymmetry; include close-ups only where ambiguous |
   | Material palette | Actual RGB/index entries and base/shadow/highlight roles from the palette section below |
   | Deformation | Features to retain versus permitted motion: hair tips and cloth may lag, but attachment points, garment construction and footwear identity remain recognizable. Allow justified perspective, overlap and squash/stretch |

4. Inspect the base at native logical size and nearest-neighbor enlargement on white/dark. Essential eyes, outline, boot toe and thin details must survive the intended export transform; revise the design if they rely on lines thinner than a final pixel. Enlargement is a display aid, not permission to create finer detail. Do not let a polished large illustration stand in for an accepted final-size sprite.
5. Resolve conflicting views, palette and details before declaring the revision accepted. Record operator evidence in `qa/visual-review.md`; follow an explicit user design-approval gate if present, otherwise perform routine review without adding one. If identity is ambiguous enough to change the requested character, ask for that missing choice while continuing independent checks.
6. For each subsequent production stage, select only the accepted current-view image, relevant detail crops and palette/proportion notes. Motion receives proportion/landmark evidence without costume or paint instructions; flat/finish receives identity details as well as the accepted cycle. If a dummy contradicts the design's proportions, repair the dummy before dressing it. Do not attach all views, rejected candidates or a whole research history by default.

## Contract And Reference Roles

1. Record asset type/use, final logical cell size, camera/view, pixel density, outline, sheet structure and protected details. Select a practical size such as 32×32 or 64×64 only when unspecified; larger sprites and more details increase animation work.
2. Identify references by role, path/source URL, version/hash and inspected scope:
   - **Design authority:** accepted design-sheet revision and selected view/detail images for character identity, body proportions, costume and asymmetry.
   - **Motion authority:** selected video poses, reviewed sketches or accepted authored rig/deformation/simulation and its rendered cycle; does not supply final skin/clothing colors.
   - **Color authority:** accepted final-size base and explicit material palette; does not override approved motion.
   - **Pixel-style authority:** an optional accepted pixel sample for outline weight, cluster size, pixel density and finish; it must not override the design's identity or the motion's poses.
   - **Perspective authority:** an optional rough 3D/reference view; does not supply final pixel texture or automatic shading.
   A file can serve multiple roles only when they are compatible. A motion actor or mannequin is not permission to replace the approved character's proportions, appearance or identity. Resolve contradictions before generating; do not attach every historical attempt.
3. Use selected, permitted reference material. Record provenance and select only useful frames/views; do not copy unrelated creator artwork or send unrelated files. A tutorial URL is process evidence, not itself an attached pose reference.
4. Keep the same logical body scale and coordinate contract across views and production stages. Neutral landmarks are references, not a lock on moving joints: retain planned bob, lean and travel. Use ranges or annotated examples rather than identical visible pixel areas; foreshortening and occlusion change projections. Record any global source-gutter crop and scale; do not independently fit each stage's silhouette to its cell or silently change its baseline.
5. When accepted design changes, revise the design-sheet index, affected view/detail images, palette and generation inputs together, then recheck dependent stages. A later generated costume or hairstyle variation must not silently become the new design. Do not use a refined base only during export while supplying an older raw image to generation.

## Palette And Color Regions

1. Define material roles from verified base interiors: material → base color, optional shadow/highlight, where each is allowed, light direction and its frame of reference. Include skin across face/hands/legs, hair, clothing, footwear, outline and tiny identity colors. Record actual RGB values or indexed palette entries. Color alone is not a semantic region mask.
2. Reuse one accepted palette across the family. For flat color, choose one base entry per material plus necessary outline/eye/detail entries before generating the cycle; derive them from the accepted design/base, not a newly noisy sheet. Use Python with that palette file or explicit material-ID mapping and verify actual pixels. Material-ID masks must come from a verified source, not nearest-color guesses. Do not independently quantize each frame. A prompt containing hex colors is a request, not exact-color enforcement; record and review any palette revision instead of silently adopting generated colors.
3. Build broad connected color regions, then refine contours and details. Avoid accidental orphan pixels and incoherent stair steps, but preserve intentional eyes, hair tips, highlights and texture. Never delete all small components or blur the image to reduce noise.
4. For a noisy base, first locate the variation in the raw generation, cleanup or sampling. Correct that stage before palette conversion. Use the smallest palette that represents the accepted material/detail roles; neither 9 nor 32–64 colors is a universal quota. Disable dithering for flat-color export and compare before/after at final size. Nearest-color mapping cannot determine whether a pixel belongs to skin or clothing: reject new speckles, colored outlines or merged hair/boot/skin identities. Use verified region assignments or a targeted generation repair when similar colors collide; do not repeatedly reduce the color count.
5. A shaded base may define the final style target. Introduce shading into new articulated animation frames only after the flat-color gate. Let shadow boundaries follow surfaces/occlusion under the declared lighting; do not fix shadow positions to the canvas or force equal shadow area per frame. Omit unnecessary detail. Retain the user's intended final style; flat color can be final when that is the brief.

## Background

1. Prefer native transparency when the selected tool produces it reliably. Record observed behavior in the run context: if the same generation path has already painted checkerboards, use a verified flat key from the outset where the tool permits it instead of repeating the failed request. Choose the key against the entire subject, including edge shades and small details; a related hue can trigger despill even when its RGB differs. Cyan is not automatically safe for teal clothing, nor magenta for coral accessories. Do not universalize one run's key or tolerance.
2. Select exactly one background strategy per generation call. Do not ask for "transparent, or a key if unavailable". Specify either actual alpha with no transparency visualization, or one uniform exact key with no texture/gradient/shadow. Do not recolor the subject to accommodate the key. Keep checkerboards in the viewer only; do not attach checker-composited previews as style references when a clean source is available.
3. Inspect the returned file's mode and alpha values and composite it over light/dark before extraction. RGB, or RGBA with only opaque alpha, is not transparent; partial alpha alone does not exclude a painted checkerboard. For baked checks, preserve the source and repair only the background with image generation using the selected key, then recheck pose coordinates and foreground colors because a background-only edit may redraw them. Never erase white/gray globally when the subject contains those colors.
4. Clean at native size before extracting alpha components and applying a common scale; technical details belong to `script-workflow.md`. If cleanup damages colors/outlines, repair its demonstrated cause or revise the key/source instead of repeatedly raising tolerance. Record the successful background choice for subsequent calls in this run.

## Static Assets

1. For icons/items, choose distinct readable silhouettes with common apparent scale, palette and padding.
2. For tiles, specify tile size, perspective, required edges/corners/transitions and neighbor connections. Review tiling in context.
3. Generate only the requested assets. No animation dummy, motion reference or per-frame timing is required for static work.
