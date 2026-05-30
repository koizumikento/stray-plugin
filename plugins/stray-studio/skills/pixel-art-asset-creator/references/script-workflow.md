# Script Workflow And Catalog

Run these scripts with Pillow available. In this repository, prefer:

```bash
uv run --with pillow python <script> ...
```

Use deterministic tools only for organizing prompts, slicing generated sheets, composing contact sheets, resizing, converting formats, checking dimensions, or packaging files. Do not synthesize missing sprites, tiles, poses, or effects through local scripts as a substitute for image generation unless the user explicitly asks for procedural placeholder art.

## Bundled Scripts

- `prepare_asset_run.py`: create `asset_request.json`, prompt files, copied references, and `imagegen-jobs.json`
- `asset_job_status.py`: show ready and blocked visual generation jobs
- `record_imagegen_result.py`: record selected image generation outputs and create the canonical base reference
- `generate_asset_images.py`: secondary direct Image API fallback when the normal image generation skill cannot be used
- `extract_sheet_cells.py`: normalize chroma key or alpha, resize to the asset contract, and slice cells
- `inspect_asset_cells.py`: inspect extracted cells for empty cells, opaque backgrounds, clipping risk, and size outliers
- `compose_asset_sheet.py`: compose extracted cells into `final/asset.png` and `final/asset.webp`
- `validate_asset_sheet.py`: validate final dimensions, alpha, used cells, and unused cell transparency
- `make_contact_sheet.py`: create a labeled QA contact sheet
- `render_animation_preview.py`: create a GIF preview for sprite-row assets
- `queue_asset_repairs.py`: reopen the smallest relevant visual generation job with repair notes
- `package_asset_run.py`: one-step normalizer/packager for simpler runs
- `slice_asset_sheet.py`: export packaged cells as individual PNG files

## Default Script Workflow

1. Prepare the run.

```bash
uv run --with pillow python plugins/stray-studio/skills/pixel-art-asset-creator/scripts/prepare_asset_run.py \
  --asset-name "<Name>" \
  --description "<one sentence>" \
  --asset-type "<sprite|item-set|tileset|icon|prop>" \
  --target-size "64x64" \
  --sheet-structure "<standalone|sprite-row|item-set|tileset|sprite-sheet>" \
  --reference /absolute/path/to/reference.png
```

All arguments are optional except the ones needed to express the user's asset contract. For animation, pass `--sheet-structure sprite-row --frame-count <n> --motion-beats "<beats>"`. For item or tile sets, pass `--item`, `--items`, `--tile`, or `--tiles`.

2. Inspect ready visual jobs.

```bash
uv run --with pillow python plugins/stray-studio/skills/pixel-art-asset-creator/scripts/asset_job_status.py \
  --run-dir /absolute/path/to/run
```

3. Generate each ready job with the installed image generation capability.
   - Use the prompt file listed by `asset_job_status.py`.
   - Attach every listed input image with its role label.
   - The `base` job may be prompt-only when no references exist.
   - Sheet jobs must use the canonical base reference created after the base job is recorded.

4. Record each selected generated output.

```bash
uv run --with pillow python plugins/stray-studio/skills/pixel-art-asset-creator/scripts/record_imagegen_result.py \
  --run-dir /absolute/path/to/run \
  --job-id <base|asset-sheet> \
  --source /absolute/path/to/generated-output.png
```

5. Finalize the run.

```bash
uv run --with pillow python plugins/stray-studio/skills/pixel-art-asset-creator/scripts/finalize_asset_run.py \
  --run-dir /absolute/path/to/run
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
```

6. If QA fails, queue a targeted repair and regenerate only the reopened job.

```bash
uv run --with pillow python plugins/stray-studio/skills/pixel-art-asset-creator/scripts/queue_asset_repairs.py \
  --run-dir /absolute/path/to/run
```

Then repeat job status, image generation, result recording, and finalization.

## Secondary Image API Fallback

Use the fallback only when the installed image generation path is unavailable or blocked. This fallback calls the OpenAI Image API directly, so only this fallback requires `OPENAI_API_KEY`:

```bash
uv run --with pillow python plugins/stray-studio/skills/pixel-art-asset-creator/scripts/generate_asset_images.py \
  --run-dir /absolute/path/to/run \
  --model gpt-image-2
```

Do not use the fallback just because `OPENAI_API_KEY` is absent; absent API keys are fine for the normal installed-image-generation path.
