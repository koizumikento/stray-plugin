# Animation Production

Use for animation only, after accepting the applicable design from `design-contract.md`. These are operator-reviewed stages, not a claim that the bundled scripts recognize identity/anatomy or approve motion. For non-articulated effects, adapt the motion block to simple moving masses and mark anatomy-only checks not applicable. Choose the current stage and load its prompt block; keep downstream finish instructions out of motion generation.

## 1. Select Motion And Performance References

1. State the action's purpose, effort, mood, view and playback intent (loop or single action). Translate it into posture, center of weight, stride, torso response and timing. A sprint may lean strongly forward; a relaxed jog need not. Do not force one angle, frame count or maximum amplitude onto every subject.
2. Reuse suitable footage, captured motion, drawings or reviewed authored motion. Preserve the selected cycle/action's order and timing; distinguish captured evidence from locally authored poses. Select meaningful phases, not a habitual eight or twelve frames. Regular sampling is suitable only after confirming it retains the required beats. If no usable reference can be inspected, use explicitly labelled pose planning and keep reference-derived mechanics unverified.
3. Plan both legs' contact, loading/down, passing and release/up or swing, with opposite arm motion. For running, plan compression, push-off and flight; do not impose flight on walking. For jumping, include anticipation, extension, airborne height, landing compression and recovery. Adapt equivalent events to other subjects. Short stylized sequences may combine phases but must retain the action's essential mechanics.
4. Keep a frame-index/duration table and total cycle time in `qa/playback-plan.md`. Honor engine/user frame requirements first; otherwise choose drawing count from display size, meaningful phases and intended fluidity, and record the reason. Eight is not a universal standard. Drawing count and timing are separate; durations need not be uniform and held poses need no duplicate art. Compare frame-count variants at the same total cycle time unless tempo is the intended variable. Only claim a timing plan tested if the actual player supports and displays it.

## 2. Motion Block — Required Before Character Finish

1. Follow `motion-toolchain.md` to author a rig, keyed deformation, simulation or reviewed drawn source. Do not generate motion-block frames with image generation. Render simple color-coded dummy poses for articulated subjects using the accepted design's proportions, landmarks, scale and motion reference. Check against that design; resemblance between frames alone is insufficient. Diagnostic colors follow anatomical limbs across screen-side changes. Show readable joints and foot volume; omit final paint and detail.
2. Begin with the action's meaningful keys; for walking include both sides' contact and passing/support. Inspect them, then author interpolation and intermediate beats in the editable source. Keep the selected frame/time mapping. Keys and in-betweens must be viewed images, not just phase names in a prompt. Keep partial key studies distinct from complete cycles.
3. Review the complete dummy loop at target size, normal speed, slow speed and frame stepping. Trace pelvis, knee, ankle and toe through adjacent poses and the loop boundary; named contact/pass frames alone do not establish plausible in-betweens. Confirm support/swing identity, limb proportions and intended energy. A supporting foot moves back relative to the body during in-place motion; in world travel it stays planted against the ground until release.
4. Use previous/next-frame onion skin, including the last-to-first pair, to trace pelvis, knee, ankle and toe paths. Use an available editor's onion skin or an actual comparison capability. Keep all frames on the same coordinate system and common scale; overlaying already misaligned frames does not diagnose anatomy. Side-by-side stepping is a fallback; record missing overlays, and never claim the bundled HTML player supplies them.
5. Preserve planned sway, bounce, lean and compression. Do not freeze the upper body or minimize changed pixels to improve a consistency metric. Distinguish source row-spacing mistakes from intended body movement. Keep volumes/proportions consistent through justified deformation and occlusion; do not force constant visible pixel counts.
6. **Gate:** accept only when keys, complete playback, contact/pass continuity, proportions and intended impression pass. Record the output/reference hashes, settings, inspected frames and pass/fail/unverified in `qa/visual-review.md`. If failed, repair this block; do not proceed to paint.

## 3. Flat Character Color

1. For the image-generated asset path, generate character appearance with the installed image generator, attaching the accepted dummy cycle as geometry/timing authority and the original approved design sheet's current view/details as identity authority. Use the palette and any approved pixel sample for color and rendering style. Do not substitute recolored/downsampled mannequin renders for this appearance stage. Preserve the motion while drawing the original face, hair, costume and footwear; retain depth through shape, overlap and outline. An explicitly requested direct-render path still requires design, motion and color checks.
2. Use one shared palette and explicit material roles. Omit optional shadow/highlight variation in this pass. Inspect face, hands and both legs together and compare material-relative interiors over the cycle; global palette count is insufficient.
3. Compare the painted cycle against the dummy at a common scale. Reject new foot shrinking, fused limbs, altered contacts, missing passing poses or reduced torso action, even when color looks improved.
4. **Gate:** design identity, base fills and retained motion must pass before shading. If motion regressed, return to the last accepted dummy; if identity or fills drift, use the design sheet to repair the affected appearance without regenerating the motion concept. Preserve originals and do not silently change the user's final style.

## 4. Finish And Secondary Motion

1. Add only the approved shading, coherent pixel clusters and essential details to the accepted flat cycle. Keep the palette fixed; simplify accidental isolated shades and contour jaggies without erasing intentional tiny features.
2. Let shadow regions follow changing surfaces and occlusion under the chosen light. Review color-role stability separately from shadow-boundary stability. A flat pass that is stable followed by a flickering shaded pass points to finish-stage paint, not a need for more global quantization.
3. Add hair/clothing overlap and follow-through within the design sheet's deformation rules, using the body's accepted motion as the driver. Hair tips may lag while their attachment points stay on the head; garment movement must preserve its construction. Hair must not compensate for missing body mechanics. Keep folds sparse and tied to stable anatomical anchors.
4. Replay the whole cycle after every repaint or secondary-motion change. **Gate:** accept finish only when geometry, intended energy, base colors, shading, alpha and timing all pass. The final output hash and playback settings replace the previous verdict's scope.

## 5. Other Directions And 3D References

1. Accept one representative action/view first. Before animating another direction, establish and review that view in the design sheet using the same identity, palette and scale; retain the action's phase convention. Inspect front, back, profile and oblique views for volume, silhouette and which limb is occluded. Do not horizontally mirror asymmetric clothing/accessories blindly.
   Render and review one sprite row per action/view through the same gates; assemble a multi-row delivery grid afterward. A multi-row sheet is not a shortcut around motion/color review.
2. For difficult turns or foreshortening, use an available simple 3D model/reference to check perspective and pose. Block only the relevant volumes, select views/frames, reduce for reference and redraw/refine through the same motion → flat → finish gates. Do not present a reduced 3D render as finished pixel art.
3. Use plane-constrained controls or adequate observed video/drawing views for a simple side-view cycle; do not require a complete character model. Follow the toolchain's unavailable-tool behavior. Existing reference geometry must fit the target character's proportions before being adopted.

## Stationary Idle/Blink Branch

1. Use an accepted final-size base and explicitly name the mutable parts; skip the articulated dummy path for a genuinely stationary blink. Keep planned breathing/hair motion inside the intended scope.
2. Generate restricted edits and reuse suitable drawings for holds. Fix eye corners, width and lid weight; check the actual open/close/reopen timing. A long open hold with short lid beats is a starting point, not a fixed biological rule.
3. Use `registration: fixed` and optional pixel lock only for stationary planted contact. For locomotion, jumping or body travel use `free`; never use an idle lock to hide motion defects. Technical rectangle, palette and exact-copy behavior belongs to `script-workflow.md`.
4. Review the whole animation and background seams. Exact copying outside the edit regions does not prove natural motion or consistent pixels inside them.

## Stage Changes And Repairs

1. Record upstream accepted artifacts and the current failing stage. On a transition, create a fresh stage run/prompt and attach only its role-matched references; never append finishing commands to an old dummy prompt.
2. `--animation-stage` selects prompt context and records the stage. `--stage-reference` supplies the previous accepted cycle for flat/finish; its presence is not automated visual approval. Review gates above remain the operator's responsibility.
3. An accepted user-supplied rough or finished cycle can satisfy an earlier gate after inspection; it need not be regenerated. Package-only work does not require manufactured stage history. A request for a motion study ends at the motion gate; do not label it finished character art.
