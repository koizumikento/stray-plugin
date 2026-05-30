# Prompt Templates

Use these templates directly or adapt them narrowly to the user's target. Keep prompts terse, asset-specific, and production-oriented.

## Default Exclusions

Avoid polished illustration, anime key art, 3D render, glossy app icon, vector mascot, painterly rendering, realistic fur or material texture, soft gradients, high-detail antialiasing, excessive tiny accessories, text, labels, UI panels, scenery, shadows, glows, halos, noisy particles, blurred motion, watermarks, visible grids, checkerboard transparency, unrelated props, and colors close to the chroma key when a chroma-key workflow is used.

## Base Asset

```text
Create a single clean pixel-art style asset for <asset-name>.

Asset: <one-sentence visual description>.
Target use: <game/app/docs/etc>.
Target size: <width>x<height>.
Style contract: <style contract>.

Use this prompt as an authoritative production asset spec. Do not expand it into a polished illustration, anime key art, 3D render, glossy icon, vector mascot, painterly image, or marketing artwork.

Output one centered complete asset only, with safe padding, on <transparent background or flat chroma-key background>. The asset must remain readable at <target size>. Do not include scenery, text, labels, borders, checkerboard transparency, detached effects, shadows, glows, or unrelated props.
```

## Sprite Or Animation Row

```text
Create a single horizontal pixel-art sprite strip for <asset-name> performing <state/action>.

Use the attached reference image(s) for identity and the attached base asset as the canonical design. Do not redesign the character, prop, palette, outline, material, or silhouette. Only change pose, expression, or action for this animation.

Output exactly <frame-count> separate animation frames arranged left-to-right in one single row. Treat the row as <frame-count> equal-width invisible frame slots. Fill every slot with exactly one complete centered pose. No pose may be cropped, overlap another pose, or cross into a neighboring slot.

Style contract: <style contract>.
Animation action: <motion beats>.
Background: <transparent or flat chroma-key>.

Do not include visible grid lines, borders, labels, frame numbers, scenery, checkerboard transparency, speed lines, motion blur, floor shadows, glows, dust, loose particles, or detached effects unless the brief explicitly requires an attached sprite effect.
```

## Tileset

```text
Create a pixel-art tileset for <environment/material>.

Tile size: <tile-size>.
Grid: <columns>x<rows>.
Tiles required: <list of terrain, edge, corner, transition, decoration, or collision-relevant tiles>.
Style contract: <style contract>.

Every tile must align to the same grid, use the same perspective and palette, and be readable at <tile-size>. Edge and transition tiles must connect cleanly to their neighbors. Do not include visible labels, UI, perspective drift, lighting drift, large shadows crossing tile boundaries, or non-repeatable seams unless the tile is explicitly decorative.
```

## Item Or Icon Set

```text
Create a pixel-art asset sheet of <count> <item/icon> assets for <use case>.

Grid: <columns>x<rows>.
Cell size: <cell-size>.
Items: <item list>.
Style contract: <style contract>.

Each cell must contain one centered complete asset with consistent scale, outline, lighting, palette discipline, and safe padding. Keep silhouettes distinct. Do not include text, labels, borders, scenery, shadows, glows, or duplicate-looking variants unless the brief asks for close variants.
```
