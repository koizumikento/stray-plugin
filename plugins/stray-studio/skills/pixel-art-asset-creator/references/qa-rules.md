# QA Rules

Use this reference before accepting generated or packaged pixel-art assets.

## Transparency And Effects

- Prefer pose, expression, silhouette, and palette changes over decorative effects.
- Use transparent output when reliable; otherwise use a flat chroma-key color that is absent from the asset.
- Effects are allowed only when they are part of the asset, opaque, hard-edged, pixel-style, and attached to or overlapping the main silhouette.
- Avoid floating punctuation, loose sparkles, loose particles, separated smoke, detached shadows, floor patches, glow, aura, blur, smears, and action streaks by default.
- Do not accept outputs with white boxes, checkerboard backgrounds, visible grids, labels, frame numbers, watermarks, cropped body parts, edge slivers, or unrelated background scenery.

## Acceptance Checklist

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

## Repair Rules

- Repair the smallest failing unit first: one asset, one frame, one row, then the whole sheet only when the base identity is wrong.
- Use repair prompts that name the specific failure, the required preserved identity, and the exact output structure.
- Do not broaden a repair prompt into a new art direction unless the original identity is unusable.
- Do not claim pixel-perfect output from generative images unless geometry, transparency, and visual readability have been inspected and corrected.
- Do not substitute local transforms for meaningful missing poses or assets unless the user requested placeholder art.
