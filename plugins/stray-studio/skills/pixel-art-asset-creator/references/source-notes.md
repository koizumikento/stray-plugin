# Sources And Scope

Process references reviewed on 2026-09-13. These are examples from artists and tool documentation, not a claim that all artists use one method. The authored-motion and optional generated-appearance workflow is this skill's adaptation; its effectiveness must be tested, not inferred from human examples alone.

## Human Production

- [SLYNYRD — Human Walk Cycle](https://www.slynyrd.com/blog/2024/5/24/pixelblog-50-human-walk-cycle): select meaningful poses/timing from real footage, animate a simplified color-coded dummy, then dress it. Frame count is an artistic/production choice.
- [SLYNYRD — Side View Run 'N Gun](https://www.slynyrd.com/blog/2026/1/26/side-view-run-n-gun): use a dummy first; derive running expression through posture, stride, bounce and rhythm; add character details/secondary motion afterward.
- [Saint11 — Cluster Sketching and Painting](https://saint11.art/pixel_art_articles/article2/): work from connected color masses to contours/details; distinguish accidental orphan pixels from intentional tiny accents.
- [Saint11 — Basic Aseprite Animation](https://saint11.art/pixel_art_articles/article3/): straight-ahead and pose-to-pose methods, timing and preserving volume. This skill chooses pose-to-pose for articulated cycles; it is not the only valid animation method.
- [Saint11 — Basic Shading](https://saint11.art/pixel_art_articles/article4/): simplify lighting into readable surfaces and limited colors rather than copying reduced imagery literally.
- [Saint11 — Using 3D Reference](https://saint11.art/blog/3d-ref/): use a rough model for perspective, select frames and redraw; a render is reference, not finished pixel art.
- [Blender — Animation and Rigging](https://www.blender.org/features/animation/): controllable keys, constraints, rigs and shape keys for authored motion.
- [Blender — Background Python](https://docs.blender.org/api/5.0/info_tips_and_tricks.html): background script execution; verify the actual installed version and launcher.
- [Blender — Physics](https://docs.blender.org/manual/en/latest/physics/introduction.html): choose relevant simulation tools for deforming subjects/effects instead of imposing a humanoid rig.
- [FFmpeg — Documentation](https://ffmpeg.org/ffmpeg.html): frame extraction and preview encoding; preserve the selected timing.

Aseprite-titled artist material above is historical process evidence, not adoption of that editor. The selected toolchain excludes Aseprite.

No tutorial visual assets, recordings or paid source files are bundled. Attribute any selected external pose references separately in their actual run.

## sprite-gen Provenance

The original integration draws on [sprite-gen](https://github.com/aldegad/sprite-gen/tree/ed960ac2e8c61b34e34dd47650e4a7a0182cbc0f), rechecked on 2026-09-13 at `ed960ac2e8c61b34e34dd47650e4a7a0182cbc0f`: atlas planning, chroma cleanup, motion QA, pixel-grid and explicit recoloring guidance. Its shared palette is not semantic skin detection and its grid restoration cannot fix generated anatomy.

The isolated RGB background detection, soft-alpha unmix and small-cluster despill helpers in `scripts/_chroma_background.py` derive from `sprite_gen/frames/extract.py`. Preserve [Apache-2.0 license](sprite-gen-LICENSE.txt) and [modification notice](sprite-gen-NOTICE.txt). MIT-derived YCbCr, projection, mass-centroid and pixel-grid portions were not imported. Row segmentation/placement are local. No upstream visual assets are bundled.

## Actual Limits

1. Bundled tools provide single-row alpha-component extraction, common scaling, explicit stationary pixel lock, structural QA and uniform-duration previews. They do not recognize anatomy/materials, validate stage approval, enforce motion semantics or schedule reference-based intermediate poses.
2. Blender is the selected external motion tool and must actually run before claiming execution. Aseprite is excluded. The bundled scripts add no automatic rig builder, retargeter, per-frame timing player or semantic recoloring; author source locally and use the documented direct packaging handoff.
3. Arbitrary overlapping layouts, automatic pelvis anchors and pixel-grid estimation require demonstrated cases and acceptance checks before implementation. Engine timing/rectangle metadata and editable editor files require the actual requested consumer, not speculative formats.
4. Further upstream code integration requires license, dependency, Windows and run-safety review. The upstream generation providers, video pipeline, curation UI and Codex pet support remain outside this skill.
