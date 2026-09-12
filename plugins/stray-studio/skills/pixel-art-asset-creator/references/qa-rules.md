# QA Rules

Use this reference before accepting generated or packaged pixel-art assets.

## Transparency And Effects

- Prefer pose, expression, silhouette, and palette changes over decorative effects.
- Use transparent output when reliable; otherwise use a flat chroma-key color that is absent from the asset.
- Inspect final PNG/WebP edges on both white and dark backgrounds at target size and enlarged with nearest-neighbor display. Reject colored fringes, holes in required details, lost thin outlines, or altered subject colors; compare against the base and source image. Increasing the key tolerance is not evidence that these defects are fixed.
- Alpha presence is not proof of a clean background: an RGBA image can contain an opaque painted checkerboard, including behind a subject with transparent margins. Inspect the whole background as well as the edge. Key-colored edge counts are warnings, not proof of spill; legitimate palette colors can trigger them, and subtle or gray spill can be missed.
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
- orientation, body scale, and pixel size remain stable across frames; the ground-contact baseline is consistent without flattening intentional jump height or travel
- references have been simplified rather than copied with too much detail
- animation frames create a readable motion instead of repeated near-duplicates
- tiles connect or repeat as required
- no forbidden detached effects, text, shadows, glows, labels, or backgrounds remain

## Motion Review

Before reviewing motion, verify the chosen final-size base: palette reduction must preserve alpha, critical colors, eye highlights, thin outlines and intentional isolated details. Compare the refined base to the original at native size. A lower color count alone is not a pass; record the palette count and base hash. All frames must use the same accepted base version and palette.

1. Read the playback intent from the brief or motion prompt. Inspect each frame for identity, anatomy, clipping, and accidental position shifts, then watch the animated preview at its stated speed. Static checks alone cannot establish motion quality.
2. For loops, check the last-to-first transition for a visible jump. For a single action, judge preparation, action, and ending within one pass; the preview's automatic repetition is not a requirement to connect its endpoints.
3. For walk/run cycles, check alternating limb movement, body rhythm, and foot contact during stance. Reject stationary bobbing presented as walking, sliding planted feet, or unexplained changes in limb length. Treat locomotion as unverified until this review passes.
4. Record automated results separately from visual results in the handoff or a run-local QA note: background views inspected, motion intent, preview speed, pass/fail/unverified, and defects. If playback cannot be viewed, report motion as unverified. Do not conceal failed motion by changing playback speed or substituting repeated poses.
5. For a fixed-contact idle/blink, compare the midpoint of both planted feet and their baseline across frames, not the hair/body bounding-box center. The automated lowest-opaque-row anchor is only a hint (props, skirts or effects can be lower than feet); verify it visually. Do not enforce it for jumps or travel. Use the HTML player's guide and frame controls; it applies no alignment correction.
6. Keep automated JSON reports unchanged. Write the visual verdict in `qa/visual-review.md` with the final PNG's SHA-256, white/dark checks, motion checks and defects, so a later export cannot reuse a stale verdict. A failed or missing applicable check means failed or unverified acceptance. The finalizer always writes `visual_qa: unverified` and `accepted: false`; only the separate, current visual review can support the final handoff's acceptance claim.
7. For blinking, compare actual playback to the frame-index/duration plan: a long open hold and brief lid motion should read as the intended character behavior. Review eye-corner coordinates, eye width, lid thickness and brow stability at each beat. A static body does not excuse shifting eyes or missing opening motion. Record intended versus observed durations; uniform preview timing cannot verify an unequal-hold plan.
8. Review base-relative and adjacent-frame difference images when available, including the loop boundary. Unexpected changes inside the mutable regions remain defects even if the exact-copy check outside them passes. Record comparison scope and any unavailable difference-view tooling. Bind timing acceptance to the reviewed playback artifact/settings as well as the sprite hash; changing durations or sequence invalidates the previous timing verdict.

## Repair Rules

### Stationary Pixel-Lock Review

1. Verify that the action is stationary idle/blink, registration is `fixed`, and the placed final-size cell 0 is the accepted reference. Do not apply a stationary lock to walking, jumps, free/unspecified motion or an unapproved reference.
2. Inspect each explicit mutable rectangle in final-cell coordinates. It must include the complete intended change and moving outline without covering unrelated areas. Rectangles are manually chosen; neither prompts nor the script infer semantic parts.
3. Check the recorded reference hash and before/after mismatch counts. With pixel lock enabled, RGBA outside the union of the rectangles must be identical to cell 0 in every frame. Within the regions, visible RGB is restricted to cell 0's nontransparent RGB palette and the generated alpha is retained. This does not reduce the base palette or certify the pixel grid inside the edits.
4. View the output at native size and nearest-neighbor enlargement on white/dark backgrounds. Reject cut outlines, seams at rectangle boundaries, loss of eye or hair movement, unwanted palette substitutions and flickering alpha. Watch normal/slow playback and the loop boundary; a fully frozen row or empty edit is not an acceptable substitute for the requested motion.
5. Record both the exact-copy check and the visual verdict. If the regions are wrong, revise them; if the generated edits or reference are wrong, regenerate the affected visual. Do not treat zero unchanged-area mismatches as proof of an acceptable animation.

### Targeted Repairs

- Repair the smallest failing unit first: one asset, one frame, one row, then the whole sheet only when the base identity is wrong.
- Use repair prompts that name the specific failure, the required preserved identity, and the exact output structure.
- For repeated redraw or palette drift in stationary idle/blink, use an accepted final-size reference and restricted generated edits. The opt-in pixel lock may restore unchanged regions on an existing row, but it must preserve the requested motion and pass the review above.
- When key removal starts erasing thin details or recoloring the asset, stop increasing tolerance and regenerate from the canonical reference with clean alpha or a more suitable background. For fixed-contact drift, request the same foot coordinates across the row; do not flatten intentional travel or substitute copied poses.
- Do not broaden a repair prompt into a new art direction unless the original identity is unusable.
- Do not claim pixel-perfect output from generative images unless geometry, transparency, and visual readability have been inspected and corrected.
- Do not substitute local transforms for meaningful missing poses or assets unless the user requested placeholder art.
- Follow the skill's maximum of three targeted repair passes; report remaining failures and the best candidate when that limit is reached.

## Source And Deferred Capabilities

STR-318 draws on the production principles in [sprite-gen](https://github.com/aldegad/sprite-gen/tree/ed960ac2e8c61b34e34dd47650e4a7a0182cbc0f), reviewed on 2026-09-12 at commit `ed960ac2e8c61b34e34dd47650e4a7a0182cbc0f`:

- [Atlas workflow](https://github.com/aldegad/sprite-gen/blob/ed960ac2e8c61b34e34dd47650e4a7a0182cbc0f/docs/atlas-workflow.md): establish the base and verify extraction before delivery.
- [Chroma cleanup](https://github.com/aldegad/sprite-gen/blob/ed960ac2e8c61b34e34dd47650e4a7a0182cbc0f/docs/chroma-alpha.md): select the key against the palette and inspect material-color preservation.
- [Motion QA](https://github.com/aldegad/sprite-gen/blob/ed960ac2e8c61b34e34dd47650e4a7a0182cbc0f/docs/qa-motion.md): distinguish cyclic motion from single actions and inspect playback.

The RGB background detection, soft-alpha unmix and small-cluster despill helpers are adapted from upstream's `sprite_gen/frames/extract.py` at that revision in `scripts/_chroma_background.py`. Preserve the bundled [Apache-2.0 license](sprite-gen-LICENSE.txt) and [source/modification notice](sprite-gen-NOTICE.txt). The MIT-derived YCbCr, projection, mass-centroid and pixel-grid portions are not imported. No upstream visual assets are bundled. Row segmentation and placement are local implementations.

Keep these capabilities deferred until their need and acceptance evidence exist:

| Candidate | Evidence required before implementation |
| --- | --- |
| Free-layout subject detection and semantic anchors | Separated single-row alpha components and common-scale placement are implemented; arbitrary layouts, occluded pixels and automatic recognition of feet remain unsupported. |
| Common pixel-grid estimation | Reproduce frame-to-frame grid drift and compare shape and outline preservation on every frame. |
| Runtime frame rectangles, timing, and loop metadata | Identify a consuming engine and define backward compatibility with the current manifest. |
| Aseprite-compatible JSON | Confirm an engine consumer; distinguish loader metadata from editable `.aseprite` files. |

Any later upstream integration needs a dependency, license, Windows compatibility, and run-safety review. Only the isolated RGB helpers and NumPy are included; the sprite-gen package, generation providers, video pipeline, curation UI and Codex pet support remain outside scope.
