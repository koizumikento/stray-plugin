# Animation Production

Use for animation only. These are operator-reviewed stages, not a claim that the bundled scripts recognize anatomy or approve motion. For non-articulated effects, adapt the motion block to simple moving masses and mark anatomy-only checks not applicable. Choose the current stage and load its prompt block; keep downstream finish instructions out of motion generation.

## 1. Select Motion And Performance References

1. State the action's purpose, effort, mood, view and playback intent (loop or single action). Translate it into posture, center of weight, stride, torso response and timing. A sprint may lean strongly forward; a relaxed jog need not. Do not force one angle, frame count or maximum amplitude onto every subject.
2. Use real video, the user's recording, drawings or an established motion study. Select one complete cycle and representative poses manually, preserving their order and timing. Eight unique frames is a useful walking experiment, not an obligation. Select meaningful phases rather than uniformly dropping every Nth frame; record frame/time origins. If no usable reference can be inspected, use explicitly labelled pose planning and keep reference-derived mechanics unverified.
3. Plan both legs' contact, loading/down, passing and release/up or swing, with opposite arm motion. For running, plan compression, push-off and flight; do not impose flight on walking. Short stylized loops may combine phases but must still visibly convey support and passage under the body.
4. Keep a frame-index/duration table and loop intent in `qa/playback-plan.md`. Drawing count and playback timing are different. The intended duration need not be uniform; do not generate duplicate art just to hold a pose.

## 2. Motion Block — Required Before Character Finish

1. Generate simple color-coded dummy poses using the accepted proportions and motion reference. Use distinct diagnostic colors for head/torso and anatomical left/right limbs; colors follow the same limb even when its screen side changes. Show readable joints and shoe/foot volume. Omit final skin tones, costume texture, hair strands, optional shading and highlights.
2. Begin with both sides' contact and passing/support keys; inspect them, then fill the intermediate beats. Keys are actual viewed images, not just phase names in a prompt. Keep full-row jobs separate from partial key-pose studies.
3. Review the complete dummy loop at target size, normal speed, slow speed and frame stepping. Confirm foot passage under the pelvis, support/swing identity, limb proportions and the intended energy. A supporting foot moves back relative to the body during in-place motion; in world travel it stays planted against the ground until release.
4. Use previous/next-frame onion skin, including the last-to-first pair, to trace pelvis, knee, ankle and toe paths. Use an available editor's onion skin or an actual comparison capability. Keep all frames on the same coordinate system and common scale; overlaying already misaligned frames does not diagnose anatomy. Side-by-side stepping is a fallback; record missing overlays, and never claim the bundled HTML player supplies them.
5. Preserve planned sway, bounce, lean and compression. Do not freeze the upper body or minimize changed pixels to improve a consistency metric. Distinguish source row-spacing mistakes from intended body movement. Keep volumes/proportions consistent through justified deformation and occlusion; do not force constant visible pixel counts.
6. **Gate:** accept only when keys, complete playback, contact/pass continuity, proportions and intended impression pass. Record the output/reference hashes, settings, inspected frames and pass/fail/unverified in `qa/visual-review.md`. If failed, repair this block; do not proceed to paint.

## 3. Flat Character Color

1. Use the accepted dummy cycle as geometry/timing authority and the accepted design/base palette as appearance authority. Dress that same motion with simple flat material fills. Replace diagnostic limb colors with the approved skin/garment colors; retain depth through shape, overlap and outline.
2. Use one shared palette and explicit material roles. Omit optional shadow/highlight variation in this pass. Inspect face, hands and both legs together and compare material-relative interiors over the cycle; global palette count is insufficient.
3. Compare the painted cycle against the dummy at a common scale. Reject new foot shrinking, fused limbs, altered contacts, missing passing poses or reduced torso action, even when color looks improved.
4. **Gate:** base fills and retained motion must both pass before shading. If motion regressed, return to the last accepted dummy; if base fills drift, repair flat paint without regenerating the motion concept. Preserve originals and do not silently change the user's final style.

## 4. Finish And Secondary Motion

1. Add only the approved shading, coherent pixel clusters and essential details to the accepted flat cycle. Keep the palette fixed; simplify accidental isolated shades and contour jaggies without erasing intentional tiny features.
2. Let shadow regions follow changing surfaces and occlusion under the chosen light. Review color-role stability separately from shadow-boundary stability. A flat pass that is stable followed by a flickering shaded pass points to finish-stage paint, not a need for more global quantization.
3. Add hair/clothing overlap and follow-through with suitable delay, using the body's accepted motion as the driver. Hair can move after the torso; it must not compensate for missing body mechanics. Keep garment tension/folds sparse and tied to stable anatomical anchors.
4. Replay the whole cycle after every repaint or secondary-motion change. **Gate:** accept finish only when geometry, intended energy, base colors, shading, alpha and timing all pass. The final output hash and playback settings replace the previous verdict's scope.

## 5. Other Directions And 3D References

1. Accept one representative action/view first, then expand directions using the same design, palette, scale and phase convention. Inspect front, back, profile and oblique views for volume, silhouette and which limb is occluded. Do not horizontally mirror asymmetric clothing/accessories blindly.
   Generate and review one sprite row per action/view through the same gates; assemble a multi-row delivery grid afterward. A multi-row sheet is not a shortcut around motion/color review.
2. For difficult turns or foreshortening, use an available simple 3D model/reference to check perspective and pose. Block only the relevant volumes, select views/frames, reduce for reference and redraw/refine through the same motion → flat → finish gates. Do not present a reduced 3D render as finished pixel art.
3. If 3D tooling is unavailable or unnecessary, use observed video/drawing views and document that choice. Do not install tools or create a full rig as a prerequisite for a simple side-view cycle. Existing reference geometry must fit the target character's proportions before being adopted.

## Stationary Idle/Blink Branch

1. Use an accepted final-size base and explicitly name the mutable parts; skip the articulated dummy path for a genuinely stationary blink. Keep planned breathing/hair motion inside the intended scope.
2. Generate restricted edits and reuse suitable drawings for holds. Fix eye corners, width and lid weight; check the actual open/close/reopen timing. A long open hold with short lid beats is a starting point, not a fixed biological rule.
3. Use `registration: fixed` and optional pixel lock only for stationary planted contact. For locomotion, jumping or body travel use `free`; never use an idle lock to hide motion defects. Technical rectangle, palette and exact-copy behavior belongs to `script-workflow.md`.
4. Review the whole animation and background seams. Exact copying outside the edit regions does not prove natural motion or consistent pixels inside them.

## Stage Changes And Repairs

1. Record upstream accepted artifacts and the current failing stage. On a transition, create a fresh stage run/prompt and attach only its role-matched references; never append finishing commands to an old dummy prompt.
2. `--animation-stage` selects prompt context and records the stage. `--stage-reference` supplies the previous accepted cycle for flat/finish; its presence is not automated visual approval. Review gates above remain the operator's responsibility.
3. An accepted user-supplied rough or finished cycle can satisfy an earlier gate after inspection; it need not be regenerated. Package-only work does not require manufactured stage history. A request for a motion study ends at the motion gate; do not label it finished character art.
