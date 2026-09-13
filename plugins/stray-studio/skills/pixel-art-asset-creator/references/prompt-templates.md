# Prompt Assembly

This reference owns prompt selection, not design/animation/QA rules. Apply the design contract and current stage before filling the prompt. Do not concatenate all stages.

## Shared Prompt Blocks

The bundled preparer and repair queue read the same files below. For prompt-only work, read just the selected block and fill the contract around it; for generated runs inspect the emitted prompt before sending it.

| Current stage | Shared block | Input authority |
| --- | --- | --- |
| Authored motion study (execution brief) | `stage-prompts/motion.txt` | Proportion base + selected motion keys/reference |
| Flat character color | `stage-prompts/flat-color.txt` | Accepted authored cycle + design/palette |
| Finished character animation | `stage-prompts/finish.txt` | Accepted flat cycle + design/material plan |
| Stationary idle/blink | `stage-prompts/stationary.txt` | Accepted final-size base + edit scope |

For motion, use the selected block as a local execution brief under `motion-toolchain.md`; never dispatch it to image generation even if the legacy preparer emits it as an image job. The following image-prompt assembly applies to appearance stages.

1. Declare current stage, requested output and image-by-image roles: original approved design for identity; accepted authored poses for motion; optional approved pixel sample for rendering style. Name the design revision/current view and only relevant details. Explicitly exclude the rough motion model's face, costume and temporary materials from appearance authority. Read only the selected images; do not concatenate the complete design package.
2. Add geometry: logical size, used frames/cells, view, common scale, padding and exact frame order. For a row leave gaps between whole poses; the extractor finds poses before common scaling. Do not draw grid lines or force limbs into arbitrary cuts.
3. Add the selected block. Put the intended motion and timing into the motion/stationary prompt; flat/finish preserves the accepted sequence. Keep optional shading, costume detail and hair finish out of the dummy pass.
4. Add stage-relevant style/material choices and exactly one background directive from `design-contract.md`: genuine alpha, or one flat key. Never leave a conditional alpha/key fallback in a sent prompt. For flat color, request uniform material fills with no gradients, mottling, edge lighting or new far-limb skin tones; supply the accepted palette and outline roles. A dummy uses diagnostic part colors, not the final material palette; choose its key against those diagnostic colors too.
5. Exclude text, labels, frame numbers, watermarks, painted checkerboards, unintended scenery, detached/floor shadows, glow and blur. Allow only explicitly requested hard-edged attached sprite effects.
6. Attach and record the actual accepted images with role/version/hash. Map each requested output frame to its reference pose and duration. Name visible contact/passing or other essential action beats; a frame count alone does not constrain motion. Reconcile source geometry and final palette references before sending. Prompts are requests, not proof that the generator preserves geometry or exact colors.

## Base Or Static Asset Template

```text
Create <one base sprite / exact item set / tileset> for <asset name and description>.
Target: <use>, logical size <W×H>, <view/perspective>, <grid and used cells>.
Reference roles: <design candidate brief, or accepted design revision/current view with protected proportions/details>.
Style: compact readable pixel-art shapes, coherent color clusters and stepped contours,
<outline>, shared material palette <roles>, <lighting if relevant>.
Output: complete assets with safe padding on <verified alpha or selected flat key>.
No text, labels, painted checkerboard, unrelated scenery, glow or extra variants.
```

For tiles add explicit edges/corners/connections and repeat behavior. For item/icon sets name each asset and keep scale/palette consistent while preserving distinct silhouettes. These paths do not need animation stages.

For a character design candidate, use this same base template to request only the missing standing view or detail image. Specify proportions, identity details, palette and final-size readability from `design-contract.md`. Keep labels/measurements in the accompanying Markdown index or a separate review board, not in clean sprite references. Inspect the generated view against accepted views before adding it to the design package; generating a multi-view board does not approve its consistency.

## Repair Template

```text
Current stage: <stage>; observed defect: <specific defect and first failing artifact>.
Use <accepted references and roles>; preserve only <verified features>.
Repair <smallest failing unit>, returning <complete requested frame/row/grid>.
Retain the current stage's constraints and selected background.
Do not add a later stage's paint/detail or inherit unverified features from the last attempt.
```

After a local repair, review the current whole cycle. For a change of strategy or stage, prepare a fresh prompt and keep the old evidence; the queue does not diagnose stages or remove conflicting historical prose from legacy prompts.
