# Design Contract

Use this before creating a base or evaluating supplied assets. It owns design and color decisions; animation sequencing belongs to `animation-workflow.md`.

## Contract And Reference Roles

1. Record asset type/use, final logical cell size, camera/view, pixel density, outline, sheet structure and protected details. Select a practical size such as 32×32 or 64×64 only when unspecified; larger sprites and more details increase animation work.
2. Identify references by role, path/source URL, version/hash and inspected scope:
   - **Design authority:** character identity, body proportions, costume and asymmetry.
   - **Motion authority:** selected video poses, sketches or an accepted dummy cycle; does not supply final skin/clothing colors.
   - **Color authority:** accepted final-size base and explicit material palette; does not override approved motion.
   - **Perspective authority:** an optional rough 3D/reference view; does not supply final pixel texture or automatic shading.
   A file can serve multiple roles only when they are compatible. Resolve contradictions before generating; do not attach every historical attempt.
3. Use selected, permitted reference material. Record provenance and select only useful frames/views; do not copy unrelated creator artwork or send unrelated files. A tutorial URL is process evidence, not itself an attached pose reference.
4. Accept one final-size base. Check silhouette and alpha on white/dark backgrounds, inspect pixel clusters and essential details, and compare against the source. Record visible thigh/shin/foot proportions, knee/ankle/heel/toe landmarks and costume asymmetry. Use ranges or annotated examples rather than assuming identical visible pixel area in every pose: foreshortening and occlusion change projections.
5. When the base changes, update its version, attached references and palette together, then recheck dependent stages. Do not use a refined base only during export while supplying an older raw image to generation.

## Palette And Color Regions

1. Define material roles from verified base interiors: material → base color, optional shadow/highlight, where each is allowed, light direction and its frame of reference. Include skin across face/hands/legs, hair, clothing, footwear, outline and tiny identity colors. Record actual RGB values or indexed palette entries. Color alone is not a semantic region mask.
2. Reuse one accepted palette across the family. In an available editor, Indexed mode stores palette indices; keep that palette stable across frames. Otherwise use a shared palette file and verify actual pixels. Do not independently quantize each frame. A prompt containing hex colors is a request, not exact-color enforcement.
3. Build broad connected color regions, then refine contours and details. Avoid accidental orphan pixels and incoherent stair steps, but preserve intentional eyes, hair tips, highlights and texture. Never delete all small components or blur the image to reduce noise.
4. For a noisy base, compare a modest palette-reduction candidate with the original; 32–64 colors can be a starting experiment, not a universal quota. Preserve alpha, essential color distinctions and detail. Nearest-color mapping cannot determine whether a pixel belongs to skin or clothing; a shared palette can still flicker by switching between valid colors.
5. A shaded base may define the final style target. Introduce shading into new articulated animation frames only after the flat-color gate. Let shadow boundaries follow surfaces/occlusion under the declared lighting; do not fix shadow positions to the canvas or force equal shadow area per frame. Omit unnecessary detail. Retain the user's intended final style; flat color can be final when that is the brief.

## Background

1. Prefer reliable native transparency. Otherwise choose a flat key absent from the entire subject palette, including eye/accessory colors and edge shades. Select green/magenta only after inspection, or choose another absent color.
2. Specify that exact background in the request and each active prompt. Do not recolor the subject to accommodate the key. A painted checkerboard fails transparency; checker display belongs only in the viewer.
3. Preserve native sources. Clean before extracting alpha components and applying a common scale; technical details belong to `script-workflow.md`. If cleanup damages colors/outlines, revise the key or source instead of repeatedly raising tolerance.

## Static Assets

1. For icons/items, choose distinct readable silhouettes with common apparent scale, palette and padding.
2. For tiles, specify tile size, perspective, required edges/corners/transitions and neighbor connections. Review tiling in context.
3. Generate only the requested assets. No animation dummy, motion reference or per-frame timing is required for static work.
