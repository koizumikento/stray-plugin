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
- palette, outline, lighting, and material remain consistent; shared color count alone does not certify coherent shading
- orientation, body scale, and pixel size remain stable across frames; the ground-contact baseline is consistent without flattening intentional jump height or travel
- references have been simplified rather than copied with too much detail
- animation frames create a readable motion instead of repeated near-duplicates
- tiles connect or repeat as required
- no forbidden detached effects, text, detached or floor shadows, glows, labels, or backgrounds remain; intentional shading within the asset follows the material-color plan

## Motion Review

Before reviewing motion, verify the chosen final-size base: palette reduction must preserve alpha, critical colors, eye highlights, thin outlines and intentional isolated details. Compare the refined base to the original at native size. A lower color count alone is not a pass; record the palette count and base hash. All frames must use the same accepted base version and palette.

1. Read the playback intent and intended impression from the brief or motion prompt. Inspect representative key-pose silhouettes for the chosen posture, lean, weight placement and attitude at target size; record whether the requested performance reads, separately from technical correctness. Inspect each frame for identity, anatomy, clipping, and accidental position shifts, then watch the animated preview at its stated speed. Static checks alone cannot establish motion quality, and a technically valid cycle can still fail the intended impression.
2. For loops, check the last-to-first transition for a visible jump. For a single action, judge preparation, action, and ending within one pass; the preview's automatic repetition is not a requirement to connect its endpoints.
3. For walk/run cycles, identify the same near/far leg across frames and follow its contact, loading, passing, release and swing, including the opposite half-cycle. Check supporting-foot motion relative to the body and opposite arm swing; arm alternation alone does not prove leg continuity. Check weight transfer through hips/chest/head and shoulder/hip rotation. For humanlike running, require compression, push-off and flight; do not impose flight on walking. Reject a frozen upper body, random bobbing or unexplained limb-length changes. Judge effort in continuous normal-speed playback and support/swing transitions by slow playback and stepping. Merely opening an advancing player or inspecting isolated screenshots is not this review; record any untracked or ambiguous leg as unverified.
4. Record automated results separately from visual results in the handoff or a run-local QA note: background views inspected, motion intent, preview speed, pass/fail/unverified, and defects. If playback cannot be viewed, report motion as unverified. Do not conceal failed motion by changing playback speed or substituting repeated poses.
5. For a fixed-contact idle/blink, compare the midpoint of both planted feet and their baseline across frames, not the hair/body bounding-box center. The automated lowest-opaque-row anchor is only a hint (props, skirts or effects can be lower than feet); verify it visually. Do not enforce it for jumps or travel. Use the HTML player's guide and frame controls; it applies no alignment correction.
6. Keep automated JSON reports unchanged. Write the visual verdict in `qa/visual-review.md` with the final PNG's SHA-256, white/dark checks, motion checks and defects, so a later export cannot reuse a stale verdict. A failed or missing applicable check means failed or unverified acceptance. The finalizer always writes `visual_qa: unverified` and `accepted: false`; only the separate, current visual review can support the final handoff's acceptance claim.
7. For blinking, compare actual playback to the frame-index/duration plan: a long open hold and brief lid motion should read as the intended character behavior. Review eye-corner coordinates, eye width, lid thickness and brow stability at each beat. A static body does not excuse shifting eyes or missing opening motion. Record intended versus observed durations; uniform preview timing cannot verify an unequal-hold plan.
8. Review base-relative and adjacent-frame difference images when available, including the loop boundary. Unexpected changes inside the mutable regions remain defects even if the exact-copy check outside them passes. Record comparison scope and any unavailable difference-view tooling. Bind timing acceptance to the reviewed playback artifact/settings as well as the sprite hash; changing durations or sequence invalidates the previous timing verdict.
9. For locomotion placement repairs, compare the source and result: correct only demonstrated drift outside the planned root trajectory. Preserve intentional root sway, vertical bounce, torso lean and shoulder/hip motion; do not minimize changed pixels as a quality target. In run-in-place, a stance foot travels backward relative to the body; in world-space travel it stays planted against the ground until push-off. Check both phase and momentum at the loop boundary. When switching actions, compare character proportions and a declared common scale/pivot against the accepted base, not only canvas dimensions or maximum pose height.
   Review horizontal displacement across every frame, equivalent phases and last-to-first. Compare source spacing with the extractor's nominal slots and visually locate a waist/pelvis reference before attributing drift to weight transfer. Bounding-box centers or image-band registration can flag a common shift, but are not pelvis trajectories or contact-velocity measurements; record the comparison method and its limits. A constant Y correction does not resolve X spacing errors. Do not accept or suppress a trend merely because registration is free.

## Repair Rules

### Source-To-Export Proportions And Color

1. Compare the accepted base, original generation, native cleaned poses, resized cells and final color-mapped export. Use the declared common scale for comparisons, retain native originals for detail inspection, and never fit each pose independently to the same height. Record the first stage where the defect appears; do not blame resizing or chroma cleanup without before/after evidence.
2. For every humanoid frame, check limb length, knee/ankle articulation, heel/toe readability and boot volume, especially passing poses. Allow explained foreshortening, overlap and compression. Bounding-box height, ground-strip width, pixel area and component survival are diagnostics, not anatomical measurements or acceptance tests. Regenerate malformed source poses; do not stretch a foot or squeeze the whole character to conceal them.
3. Check outline and small features before and after sampling. Repeated noninteger nearest-neighbor resizing can drop different pixels; rebuild from the original source with one final resize and compare. A shared scale does not fix generated proportions. If no candidate preserves the required details at target size, repair the source's pixel density/detail rather than claiming automatic pixel-grid repair.
4. Track skin base/shadow roles on face, hands and limbs under the declared lighting, comparing equivalent surfaces across the cycle. Verify the actual generation inputs and export palette against the recorded accepted reference version/hash and explicit color plan; distinguish raw geometry references from final color authority. Record sampled regions and limits: a hand-selected window is not a semantic skin mask. Fixed palettes prevent palette recalculation drift but RGB nearest-color mapping does not identify materials. A palette-only pass does not establish stable skin tones.
5. After any partial visual replacement, inspect the join, retained regions and all affected frames in the current full-speed/stepped preview, including the loop seam. Record part-proportion, material-color, placement and motion verdicts separately in the hash-bound visual review. Leave the motion failed or unverified if any applicable verdict fails or is missing, even when the targeted defect and structural checks pass. Repeated incompatible edits require a return to verified base/key poses and a revised strategy within the authorized scope; do not preserve defects just because they lie outside the current repair region.

### Shading Consistency

1. Inspect the same material across paused final-size frames, then normal/slow playback and last-to-first. Look for accidental isolated shades, sparkling highlights or shadow regions that change without corresponding pose, occlusion or lighting changes. Judge material-relative surfaces, not exact screen-pixel matches, total changed pixels or equal shadow area across frames.
2. Check the material-color plan and light reference against the accepted base. Confirm large readable color regions while preserving intentional fine details, outline contrast and near/far limb distinctions. Report palette membership/count separately from the visual shading verdict; neither fewer colors nor zero palette violations proves temporal consistency. Record base-fill consistency and shadow-boundary consistency as separate verdicts for each affected material, with inspected frames/regions and reference/export hashes. For example, skin can retain its palette while switching from base to shadow without a pose or lighting reason.
3. Compare paint repairs to their geometry references. Reject lost limb articulation, changed proportions, damaged alpha or reduced lean/compression used to conceal flicker. Preserve the motion and repair the paint. Review backgrounds and replay the current export; bind the verdict to its hash and settings. If only palette mapping ran, do not report region consistency as repaired until visually verified.
4. For recurring drift, compare the flat diagnostic and shaded candidate described in `prompt-templates.md`. Passing the diagnostic only establishes the inspected base fills; it does not accept the full shaded animation or a changed art style. Record any unavailable material tracking or playback as unverified. Global histograms and fixed-coordinate differences mix pose, occlusion, outline and shading changes and must not be labelled semantic material checks. The bundled scripts do not infer material masks or enforce role-specific recoloring.

### Stationary Pixel-Lock Review

1. Verify that the action is stationary idle/blink, registration is `fixed`, and the placed final-size cell 0 is the accepted reference. Do not apply a stationary lock to walking, jumps, free/unspecified motion or an unapproved reference.
2. Inspect each explicit mutable rectangle in final-cell coordinates. It must include the complete intended change and moving outline without covering unrelated areas. Rectangles are manually chosen; neither prompts nor the script infer semantic parts.
3. Check the recorded reference hash and before/after mismatch counts. With pixel lock enabled, RGBA outside the union of the rectangles must be identical to cell 0 in every frame. Within the regions, visible RGB is restricted to cell 0's nontransparent RGB palette and the generated alpha is retained. This does not reduce the base palette or certify the pixel grid inside the edits.
4. View the output at native size and nearest-neighbor enlargement on white/dark backgrounds. Reject cut outlines, seams at rectangle boundaries, loss of eye or hair movement, unwanted palette substitutions and flickering alpha. Watch normal/slow playback and the loop boundary; a fully frozen row or empty edit is not an acceptable substitute for the requested motion.
5. Record both the exact-copy check and the visual verdict. If the regions are wrong, revise them; if the generated edits or reference are wrong, regenerate the affected visual. Do not treat zero unchanged-area mismatches as proof of an acceptable animation.

### Targeted Repairs

- Repair the smallest failing unit first: one asset, one frame, one row, then the whole sheet only when the base identity is wrong.
- Use repair prompts that name the specific failure, the required preserved identity, and the exact output structure.
- Name only verified properties as invariants. Do not preserve every pose's head position, height or spacing when those remain suspect. Recheck a repaired image before using it as another edit source; keep the accepted base/key poses authoritative and record new defects rather than treating the latest result as a new canonical reference.
- For repeated redraw or palette drift in stationary idle/blink, use an accepted final-size reference and restricted generated edits. The opt-in pixel lock may restore unchanged regions on an existing row, but it must preserve the requested motion and pass the review above.
- For a stiff walk/run, regenerate the failing poses with explicit upper-body and weight-transfer beats. Do not repair it by freezing the torso, suppressing all root movement, stretching individual frames, or changing playback speed alone. Record the remaining energy/body-mechanics defect even if geometry, palette and loop checks pass.
- When key removal starts erasing thin details or recoloring the asset, stop increasing tolerance and regenerate from the canonical reference with clean alpha or a more suitable background. For fixed-contact drift, request the same foot coordinates across the row; do not flatten intentional travel or substitute copied poses.
- Do not broaden a repair prompt into a new art direction unless the original identity is unusable.
- Do not claim pixel-perfect output from generative images unless geometry, transparency, and visual readability have been inspected and corrected.
- Do not substitute local transforms for meaningful missing poses or assets unless the user requested placeholder art.
- Follow the skill's default of three passes per repair strategy; report remaining failures and stop blind repetition. When further work is already authorized, diagnose and change strategy within that scope before continuing.

## Source And Deferred Capabilities

STR-318 draws on the production principles in [sprite-gen](https://github.com/aldegad/sprite-gen/tree/ed960ac2e8c61b34e34dd47650e4a7a0182cbc0f), rechecked on 2026-09-13 at the same commit `ed960ac2e8c61b34e34dd47650e4a7a0182cbc0f`:

- [Atlas workflow](https://github.com/aldegad/sprite-gen/blob/ed960ac2e8c61b34e34dd47650e4a7a0182cbc0f/docs/atlas-workflow.md): establish the base and verify extraction before delivery.
- [Chroma cleanup](https://github.com/aldegad/sprite-gen/blob/ed960ac2e8c61b34e34dd47650e4a7a0182cbc0f/docs/chroma-alpha.md): select the key against the palette and inspect material-color preservation.
- [Motion QA](https://github.com/aldegad/sprite-gen/blob/ed960ac2e8c61b34e34dd47650e4a7a0182cbc0f/docs/qa-motion.md): distinguish cyclic motion from single actions and inspect playback.
- [Pixel unfake](https://github.com/aldegad/sprite-gen/blob/ed960ac2e8c61b34e34dd47650e4a7a0182cbc0f/docs/pixel-unfake.md): restore a measurable pixel grid and preserve native logical detail instead of forcing equal pose heights. This grid pipeline is not implemented here and cannot repair generated anatomy.
- [Recolor](https://github.com/aldegad/sprite-gen/blob/ed960ac2e8c61b34e34dd47650e4a7a0182cbc0f/docs/recolor.md): explicit color substitutions with hit/miss reporting, not semantic skin detection. Upstream's pinned shared palette also does not enforce per-material color roles. These are limitations to respect, not claims of bundled capabilities.

The RGB background detection, soft-alpha unmix and small-cluster despill helpers are adapted from upstream's `sprite_gen/frames/extract.py` at that revision in `scripts/_chroma_background.py`. Preserve the bundled [Apache-2.0 license](sprite-gen-LICENSE.txt) and [source/modification notice](sprite-gen-NOTICE.txt). The MIT-derived YCbCr, projection, mass-centroid and pixel-grid portions are not imported. No upstream visual assets are bundled. Row segmentation and placement are local implementations.

Keep these capabilities deferred until their need and acceptance evidence exist:

| Candidate | Evidence required before implementation |
| --- | --- |
| Free-layout subject detection and semantic anchors | Separated single-row alpha components and common-scale placement are implemented; arbitrary layouts, occluded pixels and automatic recognition of feet remain unsupported. |
| Common pixel-grid estimation | Reproduce frame-to-frame grid drift and compare shape and outline preservation on every frame. |
| Runtime frame rectangles, timing, and loop metadata | Identify a consuming engine and define backward compatibility with the current manifest. |
| Aseprite-compatible JSON | Confirm an engine consumer; distinguish loader metadata from editable `.aseprite` files. |

Any later upstream integration needs a dependency, license, Windows compatibility, and run-safety review. Only the isolated RGB helpers and NumPy are included; the sprite-gen package, generation providers, video pipeline, curation UI and Codex pet support remain outside scope.
