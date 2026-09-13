# Stage QA And Failure Diagnosis

Use before stage advancement or delivery. Design choices belong to `design-contract.md`; motion construction belongs to `animation-workflow.md`. Do not rebuild those plans inside a repair prompt.

## Evidence And Verdicts

1. Inspect the native source, cleaned poses and final-size output. Use white and dark backgrounds, native-size display and nearest-neighbor enlargement. Preserve originals and record reference/output SHA-256 values.
2. Record in `qa/visual-review.md`: stage; upstream reference paths/hashes; output hash; inspected frames/regions; preview path/settings/order/durations; automated results; geometry/motion/base-fill/shading/alpha verdicts; observed defects. Use pass/fail/unverified/not-applicable separately. Stage approval is an operator judgment, not automatically a user confirmation.
3. Only advance when every applicable check passes. A viewed key pose cannot accept a full cycle; a still screenshot or an advancing timer cannot prove that playback was inspected. If playback/tools are unavailable, leave the relevant verdict unverified.
4. Keep automated JSON unchanged. The finalizer reports `visual_qa: unverified` and `accepted: false`; its `ok` is execution success only. A motion or flat-color run's `final/` directory is a stage export, not proof of finished character art.
5. Changing an upstream reference, output bytes, frame order or duration invalidates dependent verdicts. Reopen only affected stages, then review the current whole cycle before handoff.

## Acceptance By Stage

| Stage | Required visual checks |
| --- | --- |
| Base/design | Identity, logical size, body/foot proportions, protected details, material roles, clear alpha |
| Motion block | Actual keys and full cycle, both legs' contact/pass continuity, knee/ankle/toe paths, volume, torso response, intended energy, loop/end behavior and observed timing |
| Flat color | Motion retained from accepted dummy, shared palette, stable material-relative base fills, skin consistent across face/hands/legs, depth readable without invented tones |
| Finish | All prior checks retained, coherent clusters/contours, justified shading boundaries, essential details, hair/clothing follow-through, no new flicker |
| Stationary | Accepted base, appropriate mutable scope, stable eye/foot anchors, complete intended edits, seams/alpha, actual hold schedule |
| Export | Exact dimensions/cells/order, no clipped/missing parts, clean alpha/unused cells, source details and intended offsets preserved |

## Motion Comparison

1. Trace the same anatomical leg across support and swing, including the opposite half-cycle. Diagnostic limb colors must not swap with screen side. Require the passing-under-body beat to be visible; do not accept only forward/back extremities. Evaluate joint proportions under explained foreshortening/overlap, not equal per-frame pixel area.
2. Review coordinated hips/chest/head and opposite arm motion. Running can include compression, push-off and flight; walking must not acquire an unintended flight phase. Match lean, stride and rhythm to the requested effort; changing speed alone cannot fix missing mechanics.
3. Use previous/next-frame onion skin or side-by-side stepping at a common scale to check joint trajectories and last-to-first. Record overlay availability. Do not realign each pose independently to manufacture a smooth path. Intentional root motion is valid; irregular source slot spacing is not automatically intentional.
4. Compare normal and slow playback against the frame-index/duration plan. Uniform-speed preview cannot verify unequal holds. Bind timing acceptance to the viewed settings as well as the sprite hash.
5. For other directions, check common proportions/palette and phase conventions while allowing projection changes. Preserve asymmetry; a mirror is not automatically a valid new view.

## First-Failure Diagnosis

First compare accepted design → motion block → flat color → finish to identify the earliest failing artistic stage. Within that stage compare raw generation → native cleanup → resized cells → final palette/export to distinguish a generation defect from processing damage. Locate the first actual defect, not an assumed cause.

| Observation | Repair target |
| --- | --- |
| Foot already shrinks or fuses in the dummy | Motion geometry/reference; regenerate the affected pose, never stretch a boot to hide it |
| Dummy is correct but dressed/painted foot changes | Flat/finish generation; return to accepted motion authority |
| Source toes/outline are good but export loses them | Sampling/cleanup; rebuild once from native source at common scale, inspect detail |
| Base fill changes in flat frames | Material assignment; repair affected regions with shared palette, not more global quantization |
| Flat pass is stable but shadows sparkle in finish | Surface-relative shading/clusters; preserve motion and flat fills |
| Key removal changes skin/outline | Background/cleanup; preserve subject colors and revise key/source rather than raising tolerance repeatedly |
| Loop jumps after free placement | Compare native source spacing to nominal slots and pelvis path; correct only demonstrated layout drift |

Do not treat body bbox, contact-strip width, component survival, total changed pixels, histograms or palette size as anatomy/material recognition. The scripts do not supply semantic masks, pelvis tracking or automatic grid restoration. A hand-selected sampling window is not a moving skin mask.

## Color And Transparency Checks

1. Compare the same material/surface across frames; allow pose/occlusion/lighting effects but reject unexplained base-to-shadow switching, accidental speckles and flashing highlights. Report base-fill and shadow-boundary verdicts separately.
2. Verify shared palette membership and actual reference version. Indexed colors prevent uncontrolled color creation only when the palette stays fixed; they do not decide which region should use which entry.
3. Preserve purposeful isolated eyes, hair tips and highlights while cleaning accidental orphan pixels and jaggies. Do not blur, delete all small components or freeze shading to canvas coordinates.
4. Inspect the whole background, including behind the body, on white/dark. Alpha can coexist with a painted checkerboard. Reject key fringes, damaged thin lines, required holes filled/erased, clipped parts and unwanted text/effects. Key-color counts are warning hints, not spill detection proof.

## Stationary Pixel Lock

1. Confirm genuine stationary motion, `registration: fixed`, accepted placed cell 0 and manually reviewed mutable rectangles. Reject use for locomotion/free motion.
2. Check exact RGBA copying outside the rectangles and the edited region's palette/alpha behavior against the script contract. Inspect inside/outside seams, eye anchors, outlines and intended motion; zero mismatch outside does not make a frozen animation acceptable.
3. If bounds or reference are wrong, repair those first; if the generated edit is wrong, regenerate it. Recheck normal/slow playback and the loop boundary after any change.

## Repairs And Delivery

1. Preserve only verified upstream features. Repair the smallest failing unit and inspect the current complete cycle afterward; do not promote the newest failed attempt to a canonical reference.
2. If repeated edits produce incompatible defects, return to accepted stage inputs and change the strategy within the user's scope. Three unchanged attempts trigger reassessment, not a reset of counters or deletion of evidence.
3. Export PNG/sheets/sequences and requested previews; verify actual dimensions and alpha. Keep an editable source with layers/palette/timing when available, and do not label JSON metadata as an editable `.aseprite` document.
4. Report the stage delivered and all remaining failed/unverified checks. Package-only input can be exported with missing provenance stated; do not invent passed earlier stages.
