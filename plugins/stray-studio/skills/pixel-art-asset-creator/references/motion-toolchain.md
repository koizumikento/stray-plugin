# Motion Toolchain

Use Blender for authored motion, existing Python/Pillow/NumPy for processing, and FFmpeg/browser playback for verification. Aseprite is excluded. Do not build a custom editor or universal rig framework to complete one asset.

## Select The Method

1. Reuse suitable authored motion or selected footage when available. Record source, selected frames and timing; a tutorial name alone is not motion evidence.
2. Select the smallest controllable representation that fits the subject and action:

   | Subject/action | Preferred source | Review |
   | --- | --- | --- |
   | Articulated human, animal, multiple legs, wings or mechanism | Blender armature, constraints and keyed poses; plane-constrained for one view, 3D when perspective needs it | Segment lengths, joint limits, contact, effort and phase relationships |
   | Soft or changing shape | Keyed shape/deformation controls; simulation only when useful | Volume, silhouette, compression/release and timing |
   | Smoke, fire, particles or magic | Simple keyed shapes, reproducible simulation or reviewed drawn frames, according to the brief | Flow, rhythm, silhouette and loop seam |
   | Simple blink/stationary change | Explicit local edit/key scope or authored frames | Protected areas and holds; no unnecessary rig |
   | Static item/icon/tile | No motion tool | Skip motion production |

3. Do not impose humanoid anatomy, one character's measurements, eight frames or one gait on every subject. Do not build all branches in advance.
4. Stop modeling once the required proportions, joints, support surfaces and projected poses are readable. Add geometry only when it resolves a concrete motion/occlusion defect. Detailed faces, finished costumes, hair strands and a production character rig are not prerequisites for a motion reference. Retarget reusable motion to the approved proportions rather than inheriting the source actor's body as a new character.
5. After motion review, supply rendered poses to image generation together with the original approved design. Keep their roles separate: the render determines motion; the design determines appearance. Neutralize or omit temporary materials and design details that could contaminate the appearance prompt. Keep anatomical diagnostic colors when needed to distinguish overlapping limbs. A direct 3D render/downsample is a reference unless the user explicitly requested that final style/path.

## Execute Blender

1. Discover the installed executable/version and verify background Python execution plus a small keyed/interpolated property. Pin the tested version in the run record, not this reusable skill.
2. On Windows, try the discovered executable. For Store installs, inspect `Get-AppxPackage '*Blender*'` and the package manifest's execution aliases. A registered `blender-launcher.exe` alias can run background scripts when direct WindowsApps execution is denied. Do not hard-code a user's path/version or change ACLs. Use `Start-Process -WindowStyle Hidden` for a background launch; verify an output/result file because launcher exit alone may not prove success.
3. Use the equivalent of `blender --background --factory-startup --disable-autoexec --python-exit-code 1 --python <reviewed-script.py>`, adapted to the discovered launcher. Inspect the explicit script; disabling automatic scripts is not a sandbox for it. Load a selected trusted `.blend` only when needed.
4. Resolve output targets within the run root, reject traversal/symlink escapes and preserve existing files. Keep the actual script, parameters and editable `.blend`. Record camera/projection, scale, root/ground coordinates, frame range, timing and Blender version. For simulation, record seeds/settings and bake/cache when needed for reproducible renders.
5. Author keys and interpolation in the source; inspect intermediate poses and loop seams. Fixed bone lengths do not guarantee natural motion. Render frames at one camera/scale/canvas with alpha or a verified key. Material/object IDs may support exact color assignment later.
6. If Blender cannot run, reuse adequate reviewed footage/drawn frames or another already authorized controllable tool. Otherwise deliver the design and motion plan with execution unavailable. Do not replace missing tools with generated in-betweens or silently install another editor.

## Handoff

1. Preserve editable motion source, PNG frames, frame/time table, render parameters/version and hashes. A flattened strip alone is not a reproducible rig.
2. Use existing Python tools for alpha, shared palette or material-ID conversion, one common transform, packing and validation. Palette proximity cannot determine material identity. Do not resize individual limbs/frames or invent missing poses.
3. Use the authored-motion handoff in `script-workflow.md`. Do not record Blender renders or assembled strips as original image-generation results. The existing job scheduler neither executes Blender nor approves motion.
4. Use FFmpeg for source-frame extraction or preview encoding while preserving timing. Use the bundled browser player for supported uniform timing/stepping; any additional overlay or variable-hold player must actually be implemented and checked. Preserve frame/time data even if a preview format rounds durations.
5. Inspect native/final-size poses, normal/slow playback and adjacent/loop-boundary overlays where available. Separate execution success, geometry and naturalness. When continuous motion cannot be observed, mark naturalness unverified; do not approve final paint from snapshots alone.
