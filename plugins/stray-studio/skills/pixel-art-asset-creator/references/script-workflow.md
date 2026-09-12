# Script Workflow And Catalog

Run these scripts with Pillow available. Chroma cleanup also requires NumPy; install it in the same Python environment as the finalizer (tested with Pillow 12.3.0 and NumPy 2.4.3). In this repository, prefer:

```bash
uv run --with pillow==12.3.0 --with numpy==2.4.3 python <script> ...
```

Resolve `skill_dir` to the absolute directory containing the loaded `SKILL.md`. Keep the working directory in the user's workspace and choose an absolute `run_dir` inside that workspace; do not write outputs into the plugin installation. The examples below use Bash notation; adapt quoting to the active shell.

```bash
skill_dir="/absolute/path/to/pixel-art-asset-creator"
run_dir="/absolute/path/to/user-workspace/output/pixel-art-assets/<run-name>"
```

Use deterministic tools for organizing prompts, slicing generated sheets, composing contact sheets, resizing, converting formats, checking dimensions, or packaging files. The opt-in stationary pixel lock below also preserves reference pixels and limits the palette of generated edits; it does not synthesize missing sprites, tiles, poses, or effects. Do not replace image generation with procedural content unless the user explicitly asks for procedural placeholder art.

## Bundled Scripts

- `prepare_asset_run.py`: create `asset_request.json`, prompt files, copied references, and `imagegen-jobs.json`
- `asset_job_status.py`: show ready and blocked visual generation jobs
- `record_imagegen_result.py`: record selected image generation outputs and create the canonical base reference
- `generate_asset_images.py`: explicit direct Image API path for a user-authorized, separately billed request; never an automatic fallback
- `extract_sheet_cells.py`: clean chroma at native resolution, extract row poses before common scaling, or slice declared grid cells; optionally preserve reference pixels outside selected stationary edit regions after placement
- `inspect_asset_cells.py`: inspect extracted cells for empty cells, opaque backgrounds, clipping risk, size outliers, key-colored edges, and fixed-contact drift hints
- `compose_asset_sheet.py`: compose extracted cells into `final/asset.png` and `final/asset.webp`
- `validate_asset_sheet.py`: validate final dimensions, alpha, used cells, and unused cell transparency
- `make_contact_sheet.py`: create a labeled QA contact sheet
- `render_animation_preview.py`: create GIF and portable interactive HTML previews for sprite-row assets
- `queue_asset_repairs.py`: reopen the smallest relevant visual generation job with repair notes
- `package_asset_run.py`: one-step normalizer/packager for simpler runs
- `slice_asset_sheet.py`: export packaged cells as individual PNG files

## Default Script Workflow

1. Prepare the run.

```bash
uv run --with pillow==12.3.0 --with numpy==2.4.3 python "$skill_dir/scripts/prepare_asset_run.py" \
  --asset-name "<Name>" \
  --description "<one sentence>" \
  --asset-type "<sprite|item-set|tileset|icon|prop>" \
  --target-size "64x64" \
  --sheet-structure "<standalone|sprite-row|item-set|tileset|sprite-sheet>" \
  --reference /absolute/path/to/reference.png \
  --output-dir "$run_dir"
```

The default run root is `output/pixel-art-assets/` in the current workspace. For repository work verify that generated `output/` files are ignored (this repository ignores `/output/`); do not silently change another repository's tracking policy. Always pass the selected `--output-dir`; use defaults for other arguments only when they match the user's asset contract. Omit `--reference` when none is supplied. Reference inputs must be valid PNG, JPEG, or WebP images no larger than 20 MiB; the workflow verifies their content instead of trusting the filename and records the copied reference hash in `asset_request.json`. For animation, pass `--sheet-structure sprite-row --frame-count <n> --motion-beats "<beats>"`. For item or tile sets, pass `--item`, `--items`, `--tile`, or `--tiles`.

Choose the background using `prompt-templates.md` before preparing. Pass `--background chroma-key --chroma-key "<selected #RRGGBB>"` or `--background transparent` explicitly. The default magenta is not an automatic palette check. For a pink subject without green details, for example, select `--chroma-key "#00FF00"`; if key colors conflict with required details, use transparent output or revise the brief.

Include playback intent in `--motion-beats`, for example `"loop: walking right with alternating foot contact and a smooth wrap"` or `"single action: crouch, jump to apex, descend, land; preserve jump height"`. The motion text is also recorded in `animation.motion_beats`. Pass `--registration fixed` for stationary idle/blink with planted feet, `--registration free` for intentional travel or jumps, or leave it `unspecified` when unknown. Only `fixed` enables the automated contact-drift warning. Use `--style-notes` for any specific scale, orientation, or baseline constraints. Check generated prompt files before sending them; `prepare_asset_run.py` builds its own prompts rather than reading the Markdown templates.

2. Inspect ready visual jobs.

```bash
uv run --with pillow==12.3.0 --with numpy==2.4.3 python "$skill_dir/scripts/asset_job_status.py" \
  --run-dir "$run_dir"
```

3. Generate each ready job with the installed image generation capability.
   - Use the prompt file listed by `asset_job_status.py`.
   - Attach every listed input image with its role label.
   - The `base` job may be prompt-only when no references exist.
   - Sheet jobs must use the canonical base reference created after the base job is recorded.

4. Record each selected generated output.

```bash
uv run --with pillow==12.3.0 --with numpy==2.4.3 python "$skill_dir/scripts/record_imagegen_result.py" \
  --run-dir "$run_dir" \
  --job-id <base|asset-sheet> \
  --source /absolute/path/to/generated-output.png
```

5. Finalize the run.

```bash
uv run --with pillow==12.3.0 --with numpy==2.4.3 python "$skill_dir/scripts/finalize_asset_run.py" \
  --run-dir "$run_dir"
```

Expected output:

```text
run/
  asset_request.json
  imagegen-jobs.json
  prompts/
  decoded/
  cells/
  final/asset.png
  final/asset.webp
  final/asset-manifest.json
  final/validation.json
  qa/contact-sheet.png
  qa/review.json
  qa/run-summary.json
  qa/previews/animation.gif
  qa/previews/animation.html
```

Inspect these outputs using `qa-rules.md` before delivery. The finalizer's `ok` and `automated_ok` describe automated execution only; it always reports `visual_qa: unverified` and `accepted: false`. Record actual visual acceptance separately in `qa/visual-review.md`, bound to the current final PNG hash. Never deliver a known visual failure as passed.

Open `qa/previews/animation.html` directly in a browser: its PNG is embedded, so it needs no server or external resources. Check play/pause, previous/next frame, frame time, zoom, white/dark/checker backgrounds and the adjustable baseline guide. Disable Loop for a single action. It uses the request's dimensions and row-major used cells without repositioning frames. GIF uses uniform 140 ms frames and infinite looping by default; neither preview nor the manifest specifies engine playback behavior. Use `render_animation_preview.py --duration <ms> --scale <integer>` to override defaults, `--html-output <run-relative.html>` to choose the HTML destination, and `--force-non-row` only for a grid that actually represents one row-major animation. Ordinary item sets are not animated. `--skip-preview` skips both previews during finalization.

### Playback Plan And Difference Review

1. Separate unique artwork from its playback sequence. For relaxed blinking, try open for 2000–4000 ms, half-closed for 60–100 ms, closed for 80–120 ms, then half-open for 60–100 ms before returning to open. These are adjustable art-direction starting points, not a biological rule. Reuse an existing suitable drawing for a hold or reopening beat; do not regenerate duplicate pictures merely to fill elapsed time.
2. Record an explicit frame-index/duration table and loop intent in `qa/playback-plan.md`, using only actual available frames. If an opening pose is unsuitable for reuse, generate the missing beat. Avoid adding both an end-of-cycle and start-of-cycle long open hold accidentally. Keep the unique-frame count and sheet contract consistent.
3. Verify timing in an available editor/player that supports individual holds. The bundled GIF/HTML renderer supports only one uniform duration and row-major frame order; `--duration` slows every frame. It does not read `qa/playback-plan.md` or implement per-frame timing fields. Until the intended schedule is rendered and watched, report timing as planned but unverified. Do not present a uniform-speed preview as the finished natural blink.
4. Use an available image comparison tool to show changed pixels both against cell 0 and against the previous frame, including last-to-first. Compare final-size cells without realigning them or scaling them separately. Count visible RGB or alpha changes; ignore RGB-only differences where both alpha values are zero. Keep this visual diagnostic distinct from pixel lock's stricter exact-RGBA check outside the mutable regions.
5. When available, save a labeled difference image under `qa/`, marking intended edit bounds separately from changed pixels, and record the source frame hashes. Inspect eye-anchor shifts, outline thickness and stray changed pixels inside as well as outside the regions. The bundled HTML player currently has no difference overlay; its guides show only center/baseline. If comparison tooling is unavailable, use its frame stepping and side-by-side cells, and state that a difference visualization was not produced.

### Native-Resolution Row Extraction

1. Use the new request's `sheet.extraction: components` for sprite rows. For an older row request, pass `--extraction components` to the finalizer or extractor. Tiles, items, multi-row grids and legacy requests retain `grid`; an explicit `--extraction grid` is only appropriate for an already verified fixed grid. Never use it silently after a component-count failure. `package_asset_run.py` refuses component requests; use the finalizer.
2. Clean chroma on the original image: detect the painted key from borders/corners, cut the hard background, unmix boundary blends into corrected RGB and partial alpha, and correct small trapped key-spill clusters. Native-alpha sources bypass chroma cleanup. `--chroma-tolerance` is an RGB Euclidean hard-cut radius (default 96, matching the reference extractor; previously an 8-per-channel binary cut); fringe threshold 180, tint delta 20 and reach 4 source pixels come from the imported RGB method. This is a heuristic: key-adjacent subject details and small colored accessories can still be damaged. Inspect material colors; do not blindly raise tolerance.
3. Segment the native alpha into separate poses before any resize. Group nearby disconnected details with their pose; stop on ambiguous grouping, count mismatch, overlapping pose bounds or source-edge clipping. Do not discard extra components or recover occluded body parts by guessing. This supports separated single rows, not arbitrary free layouts.
4. Crop each group by alpha, then use one common scale (never upscale) for all frames. For `fixed`, align the lowest opaque contact row to the common baseline after verifying that it represents planted feet. For `free`/`unspecified`, preserve source Y and each pose's X offset relative to its nominal source slot using one common transform. `--no-resize` requires a scale of 1 that fits; otherwise fail. No independent per-frame stretching or pixel-grid inference occurs.
5. Inspect the native cleaned `cells/source-normalized.png`, per-cell extraction metadata in `cells-manifest.json`, final PNG on white/dark backgrounds and animation playback. Heuristic segmentation and contact anchors still need visual approval. A successful extraction never makes a failed animation acceptable.

### Legacy Grid Trim And Align

1. Verify the base's extracted alpha and outline before sheet generation (native alpha or cleaned chroma). After generation, inspect all split cells for clean alpha and correct anatomy before alignment. RGB/color presence is not occupancy: use alpha greater than zero. A painted checkerboard or chroma residue must be resolved first; trimming cannot remove it.
2. For stationary idle/blink, set `animation.registration` to `fixed` (prepare with `--registration fixed`). After confirming the lowest opaque pixels really are the planted feet in every cell, run `finalize_asset_run.py --run-dir "$run_dir" --extraction grid --trim-align`, adding `--force` only to replace this run's previously derived outputs. `extract_sheet_cells.py` also exposes `--trim-align`; it cannot be combined with component extraction, which already performs placement. Free or unspecified registration and non-animation sheets are rejected with this flag; without it, offsets are preserved.
3. The extractor splits the normalized sheet, crops each used cell to its alpha bbox, and translates the crop onto a transparent canvas of the original cell size. It aligns the midpoint of the lowest row with alpha >=128 to the cell center and that row to height minus 2 (one bottom pixel of padding). Translation uses whole pixels, so odd/even contact widths can differ by at most half a pixel. It never rescales individual crops, deletes nonzero-alpha details, or fabricates poses. Empty/no-opaque-anchor cells, edge-touching content, and moves that would clip any visible pixels fail before the staged cell directory is published.
4. Inspect `cells/source-normalized.png` as the before image and the composed output as the after image. `cells-manifest.json` records each used cell's original alpha bbox, contact anchor and translation under `alignment`. The lowest-row estimate is unsuitable for dangling props, effects, or unplanted feet; do not use this option for those assets. Enlarge the shared contract or revise the source when it cannot fit, never shrink each pose independently. Review the resulting motion and alpha again; alignment is not visual acceptance.

### Optional Stationary Pixel Lock

1. Use this only for a `sprite-row` with `animation.registration: fixed` and stationary idle/blink motion whose changing parts fit explicit rectangles. Leave it absent for ordinary exports, walking, jumps, or free/unspecified motion. The code does not recognize body parts or decide which movement may be suppressed.
2. Prefer a final-size accepted base before generating new idle/blink edits, using `prompt-templates.md`'s restricted-edit template. Keep each generated edit in the same coordinate system as that reference. For an existing generated row, inspect the extracted and placed cells first. In both cases, confirm that the final-size `cell-00.png` is the intended reference: pixel lock uses that cell, not a separate high-resolution base file. If it differs from the accepted design, repair the reference before locking other frames to it.
3. Visually select final-cell pixel rectangles enclosing all intended changes and their moving outlines. Merge this opt-in field into the existing `animation` object in `asset_request.json`, preserving registration, motion beats and other fields:

```json
{"pixel_lock": {"mutable_rects": [[18, 16, 46, 30]]}}
```

   This is only an illustrative rectangle for a 64×64 cell; do not reuse its coordinates without inspecting the asset. Each rectangle is `[left, top, right, bottom]`, with right and bottom excluded. Empty selections, invalid or out-of-bounds rectangles, and coverage of the entire canvas are rejected. The operator chooses these regions; no automatic semantic detection or new command-line rectangle flag is implied.
4. Run the normal finalizer, adding `--force` only when replacing this run's existing derived outputs. Pixel lock runs after extraction and placement. Outside the rectangles, every frame receives cell 0's exact RGBA. Inside them, retain that frame's generated alpha and map visible RGB to the nearest color in the nontransparent RGB palette of cell 0. This restricts color drift without rebuilding the base palette or estimating a new pixel grid. It cannot supply an eye shape or other motion missing from the generated edit.
5. Inspect the recorded reference hash, selected regions and before/after unchanged-area mismatch counts in the extraction metadata. Then inspect the final PNG on white/dark backgrounds and replay the animation. Check for seams at rectangle boundaries, severed outlines, color substitutions and intended motion that was removed by too-small regions. A zero mismatch outside the rectangles is a narrowly scoped guarantee, not a visual-quality verdict. Revise the regions or regenerate affected edits when necessary, using the same repair budget.

### Targeted Repair Loop

If QA fails, queue a targeted repair and regenerate only the reopened job.

```bash
uv run --with pillow==12.3.0 --with numpy==2.4.3 python "$skill_dir/scripts/queue_asset_repairs.py" \
  --run-dir "$run_dir"
```

For a visual failure, pass repeated `--visual-defect` arguments with observed defects and preserved features, for example `--visual-defect "green fringe at left ribbon; preserve its red color" --visual-defect "idle planted feet slide 3px; keep contact coordinates fixed"`. These are appended to the repair prompt and recorded with the repair reason. The queue also reads automated errors from `qa/review.json` and `final/validation.json`; add `--repair-on-warnings` for warning hints you have inspected. It does not parse the separate visual QA note. Check the reopened job's `prompt_file` before resending it and keep automated reports unchanged. If background removal damages the outline or subject palette, regenerate with clean alpha or a better key instead of increasing tolerance repeatedly.

Then repeat job status, image generation, result recording, and finalization.

Before switching from chroma-key to transparent (or changing the key), synchronize `asset_request.json`'s `background.strategy` and `background.chroma_key` with every active background directive in the reopened prompt, including earlier repair notes. Recheck them before generation; an alpha image must not pass through stale chroma removal. Preserve source images and the canonical reference, and keep counting the same three-pass repair budget. The queue itself never changes the background contract.

When replacing derived `cells/`, `final/`, or `qa/` artifacts from the failed pass, rerun finalization with `--force`. The writer scripts still reject every symlink component; `--force` permits replacement only of contained regular outputs that the repair is expected to regenerate.

## Explicit Direct Image API Path

Do not select this path merely because installed image generation is unavailable. Use it only when the user specifically requests direct OpenAI Image API execution and authorizes sending the run's prompts and input images to that separately billed API. Otherwise, stop with the asset contract and ready-to-run prompts as described in `SKILL.md`.

After that authorization, set `OPENAI_API_KEY` in the environment and pass the required confirmation flag:

```bash
uv run --with pillow==12.3.0 --with numpy==2.4.3 python "$skill_dir/scripts/generate_asset_images.py" \
  --run-dir "$run_dir" \
  --model gpt-image-2 \
  --confirm-direct-api
```

The script sends credentials in an in-process HTTP header rather than a command-line argument, refuses HTTP redirects, and revalidates every input image and its prepared hash before the request. The direct path accepts at most eight input images, at most 60 MiB total input-image bytes, a prompt no larger than 1 MiB, and a complete request body no larger than 64 MiB. Never print, persist, or pass the API key as an argument. An absent API key is fine for the normal installed-image-generation path.
