# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Alex Kim
# Adapted from aldegad/sprite-gen, commit ed960ac2e8c61b34e34dd47650e4a7a0182cbc0f.
# Modifications: isolated RGB matting helpers; replaced package dependency loader.
# See ../references/sprite-gen-NOTICE.txt and sprite-gen-LICENSE.txt.
"""RGB background detection, soft-alpha unmix, and small-cluster despill."""
from __future__ import annotations

import numpy as np
from PIL import Image

_KEY_CHANNEL_LIT = 192  # a channel the key saturates
_KEY_CHANNEL_DARK = 64  # a channel the key leaves dark — the one bar `is_key_family` / `is_border_key_candidate` reuse


def _key_channel_split(chroma_key: tuple[int, int, int]) -> tuple[list[int], list[int]]:
    """Which channels the key saturates, and which it leaves dark.

    Depends only on the key, so the whole-image path resolves it once instead of
    per pixel. Degenerate keys — no saturated channel, or no dark one — have no
    tint axis at all and come back as two empty lists; that emptiness is the one
    switch both callers read, and it turns off the unmix and spill passes.
    """
    keyed_channels = [index for index, value in enumerate(chroma_key) if value >= _KEY_CHANNEL_LIT]
    unkeyed_channels = [index for index, value in enumerate(chroma_key) if value < _KEY_CHANNEL_DARK]
    if not keyed_channels or not unkeyed_channels:
        return [], []
    return keyed_channels, unkeyed_channels


def key_tint_score(color: tuple[int, int, int], chroma_key: tuple[int, int, int]) -> float:
    keyed_channels, unkeyed_channels = _key_channel_split(chroma_key)
    if not keyed_channels:
        return 0.0
    keyed_average = sum(color[index] for index in keyed_channels) / len(keyed_channels)
    unkeyed_average = sum(color[index] for index in unkeyed_channels) / len(unkeyed_channels)
    return keyed_average - unkeyed_average



def despill_color(
    color: tuple[int, int, int],
    chroma_key: tuple[int, int, int],
    key_tint: float,
    tint: float,
) -> tuple[float, tuple[int, int, int]]:
    """Estimate the key fraction of a blend pixel and remove it from the RGB.

    Blend model: observed = (1-k)*subject + k*key. key_tint_score is linear in
    the channels and scores the key itself at `key_tint`, so k = tint/key_tint
    recovers a subject estimate whose own tint score is ~0. Returns the
    subject coverage (1-k) and the despilled color.
    """
    k = min(tint / key_tint, 1.0)
    coverage = 1.0 - k
    if coverage <= 0:
        return 0.0, (0, 0, 0)
    red, green, blue = (
        min(255, max(0, round((color[index] - k * chroma_key[index]) / coverage)))
        for index in range(3)
    )
    return coverage, (red, green, blue)


def unmix_key_blend(
    color: tuple[int, int, int],
    alpha: int,
    chroma_key: tuple[int, int, int],
    key_tint: float,
    tint: float,
) -> tuple[int, int, int, int]:
    """Separate a key/subject blend pixel into despilled RGB + partial alpha."""
    coverage, despilled = despill_color(color, chroma_key, key_tint, tint)
    out_alpha = round(alpha * coverage)
    if out_alpha <= 0:
        return (0, 0, 0, 0)
    return (*despilled, out_alpha)


# --- whole-image forms of the two primitives above ---------------------------
# remove_chroma_background asks `color_distance` and `key_tint_score` the same
# question of every pixel, which at 1.5 Mpx a row is where the extraction time
# went. These compute the identical float64 values one array at a time.
#
# "Identical" is the contract, not an aspiration: both quantities start as exact
# integer arithmetic on uint8 channels, and the one float operation in each
# (`math.sqrt`, `int / int`) is IEEE-754 correctly rounded, so the array form
# reproduces the scalar form bit for bit. tests/test_chroma_rcb_byte_identity.py
# holds the scalar side against a frozen pre-vectorization copy.


def _key_distance_field(rgb: np.ndarray, chroma_key: tuple[int, int, int]) -> np.ndarray:
    """`color_distance` for an (H, W, 3) integer array of colors.

    The squared differences accumulate in int64 on purpose. 255**2 * 3 = 195_075
    overflows uint16 as well as uint8, and a wrapped square does not raise — it
    returns a plausible distance for the wrong pixel.
    """
    diff = rgb - np.asarray(chroma_key, dtype=np.int32)
    return np.sqrt((diff * diff).sum(axis=-1, dtype=np.int64).astype(np.float64))


def _key_tint_field(rgb: np.ndarray, keyed_channels: list[int],
                    unkeyed_channels: list[int]) -> np.ndarray:
    """`key_tint_score` for an (H, W, 3) integer array of colors.

    Takes the channel split rather than the key, so the degenerate-key decision
    stays where `_key_channel_split` made it — one answer, read the same way here
    as in the scalar primitive.
    """
    if not keyed_channels:
        return np.zeros(rgb.shape[:2], dtype=np.float64)
    keyed_sum = rgb[..., keyed_channels].sum(axis=-1, dtype=np.int64)
    unkeyed_sum = rgb[..., unkeyed_channels].sum(axis=-1, dtype=np.int64)
    return keyed_sum / len(keyed_channels) - unkeyed_sum / len(unkeyed_channels)


def _grow_into(seed: np.ndarray, allowed: np.ndarray) -> np.ndarray:
    """Every `allowed` pixel 8-connected to `seed` through `allowed` pixels (seed included)."""
    reached = seed & allowed
    while True:
        grown = _grow_chebyshev(reached) & allowed
        if not (grown & ~reached).any():
            return reached
        reached = grown


def _grow_chebyshev(mask: np.ndarray) -> np.ndarray:
    """One step of 8-connected growth: the 3x3 neighborhood of every set pixel.

    Shifts are explicit slices, not `np.roll`, because roll wraps the far edge
    into the near one and would hand a bottom-row pixel the depth of the top
    row. The two axes are applied in sequence — a 3x3 dilation is separable, and
    Chebyshev distance is exactly what repeating this step counts.
    """
    grown = mask.copy()
    grown[:, 1:] |= mask[:, :-1]
    grown[:, :-1] |= mask[:, 1:]
    spread = grown.copy()
    spread[1:, :] |= grown[:-1, :]
    spread[:-1, :] |= grown[1:, :]
    return spread


# --- background key detection (RGB path) -------------------------------------
# Image models asked for #00FF00 / #FF00FF hand back a slightly different flat
# colour every run (measured 2026-09-11: Grok painted (8, 162, 24) for green).
# Its absolute distance to the pure key was 96.38 — a hair over the 96 hard-cut
# radius — so the whole background survived, while (7, 163, 24) at 95.34 keyed
# out. The rule below reads the *actual* background from the frame borders and,
# when that colour is the declared key's hue family, measures the hard cut from
# it as well. Raising the radius instead would only move the cliff to the next
# darker green; this removes the cliff for any brightness the model picks.
_KEY_FAMILY_MIN_KEYED = _KEY_CHANNEL_DARK  # a keyed channel must at least read as lit (the key split's dark bar)
_KEY_FAMILY_MAX_UNKEYED_RATIO = 0.35  # unkeyed channels stay below this fraction of the dimmest keyed one
_KEY_FAMILY_KEYED_BALANCE = 0.8  # for two-channel keys (magenta) the dimmer keyed channel keeps this share of the brighter
# Border candidate (2026-09-12): Grok paints #FF00FF as (216, 46, 147) / (225, 52, 155) /
# (236, 59, 161) — blue/red ≈ 0.68, under the 0.8 balance — so `is_key_family` said "not
# the key" for a colour that filled the whole border, the detector fell back to the
# declared key, and at ~120 from pure magenta the entire background survived. A flat
# border is already evidence of *background*; the balance rule exists to keep hot pink
# (250, 77, 150) and purple (213, 112, 246) inside the subject alive, and those two fail
# the border rule on a different axis: their unkeyed channel is lit (77, 112 >= 64), the
# painted keys' never is (46..59). So the border rule keeps the hue signature — keyed
# channels lit, unkeyed channels dark and saturated against the *brighter* keyed
# channel — and drops the balance between the keyed channels.
_BORDER_KEY_MAX_UNKEYED_RATIO = _KEY_FAMILY_MAX_UNKEYED_RATIO  # against the brightest keyed channel, not the dimmest
_KEY_DETECT_CORNER_DIV = 5  # corner patch = width/5 x height/5 (same sampling as the YCbCr path)
_KEY_DETECT_MIN_FRACTION = 0.12  # family share of the samples needed to trust the detection
_KEY_DETECT_BIN_SHIFT = 3  # RGB histogram bin width 8 — the mode bin, never a mean, picks the colour


def is_key_family(color: tuple[int, int, int], chroma_key: tuple[int, int, int]) -> bool:
    """True when `color` is the key's hue at any brightness — a *variant of the key*.

    The *interior* rule: what a pixel with no border evidence has to be before
    it counts as key (the border rule is `is_border_key_candidate`).
    Brightness is free; saturation and hue are not. Every channel the key
    saturates must read as lit (>= 64), the channels the key leaves dark must
    stay under 35% of the dimmest keyed channel, and a two-channel key keeps
    its keyed channels within 20% of each other. (8, 162, 24) and (170, 8, 180)
    are family; hot pink (250, 77, 150), purple (213, 112, 246) and cyan are
    subject colours, not keys. Degenerate keys have no family.
    """
    keyed_channels, unkeyed_channels = _key_channel_split(chroma_key)
    if not keyed_channels:
        return False
    keyed_min = min(color[index] for index in keyed_channels)
    keyed_max = max(color[index] for index in keyed_channels)
    unkeyed_max = max(color[index] for index in unkeyed_channels)
    return (
        keyed_min >= _KEY_FAMILY_MIN_KEYED
        and unkeyed_max <= keyed_min * _KEY_FAMILY_MAX_UNKEYED_RATIO
        and keyed_min >= keyed_max * _KEY_FAMILY_KEYED_BALANCE
    )


def is_border_key_candidate(color: tuple[int, int, int], chroma_key: tuple[int, int, int]) -> bool:
    """True when a colour *found on a flat border* can be the key as the model painted it.

    The border rule — one function for every entry point that classifies the
    border: `detect_background_key_rgb`, `cutout --key auto`, `video-canvas`
    and the `video-frames` edge-contact split. A superset of `is_key_family`:
    everything the interior rule admits, plus colours that carry the key's hue
    *signature* without the keyed channels balancing — every keyed channel lit
    (>= 64), every unkeyed channel dark (< 64, the key split's own bar) and
    under 35% of the *brightest* keyed channel. So Grok's (216, 46, 147)
    magenta is a candidate; hot pink (250, 77, 150) and purple (213, 112, 246)
    are not (their green channel is lit), nor are ivory and cyan. The interior
    rule stays `is_key_family` — a pixel *inside* the frame has no border evidence.
    """
    keyed_channels, unkeyed_channels = _key_channel_split(chroma_key)
    if not keyed_channels:
        return False
    keyed_min = min(color[index] for index in keyed_channels)
    keyed_max = max(color[index] for index in keyed_channels)
    unkeyed_max = max(color[index] for index in unkeyed_channels)
    return is_key_family(color, chroma_key) or (
        keyed_min >= _KEY_FAMILY_MIN_KEYED
        and unkeyed_max < _KEY_CHANNEL_DARK
        and unkeyed_max <= keyed_max * _BORDER_KEY_MAX_UNKEYED_RATIO
    )


def _key_family_field(rgb: np.ndarray, keyed_channels: list[int], unkeyed_channels: list[int]) -> np.ndarray:
    """Vector form of `is_key_family` — same three inequalities, same constants."""
    keyed_min = rgb[..., keyed_channels].min(axis=-1)
    keyed_max = rgb[..., keyed_channels].max(axis=-1)
    unkeyed_max = rgb[..., unkeyed_channels].max(axis=-1)
    return (
        (keyed_min >= _KEY_FAMILY_MIN_KEYED)
        & (unkeyed_max <= keyed_min * _KEY_FAMILY_MAX_UNKEYED_RATIO)
        & (keyed_min >= keyed_max * _KEY_FAMILY_KEYED_BALANCE)
    )


def _border_key_candidate_field(rgb: np.ndarray, keyed_channels: list[int], unkeyed_channels: list[int]) -> np.ndarray:
    """Vector form of `is_border_key_candidate` — same inequalities, same constants."""
    keyed_min = rgb[..., keyed_channels].min(axis=-1)
    keyed_max = rgb[..., keyed_channels].max(axis=-1)
    unkeyed_max = rgb[..., unkeyed_channels].max(axis=-1)
    signature = (
        (keyed_min >= _KEY_FAMILY_MIN_KEYED)
        & (unkeyed_max < _KEY_CHANNEL_DARK)
        & (unkeyed_max <= keyed_max * _BORDER_KEY_MAX_UNKEYED_RATIO)
    )
    return _key_family_field(rgb, keyed_channels, unkeyed_channels) | signature


def _key_detect_sample_mask(height: int, width: int) -> np.ndarray:
    """Corner patches (w/5 x h/5) plus the 1-px border — where the background lives."""
    mask = np.zeros((height, width), dtype=bool)
    if height == 0 or width == 0:
        return mask
    corner_w = width // _KEY_DETECT_CORNER_DIV
    corner_h = height // _KEY_DETECT_CORNER_DIV
    if corner_w < 2:
        corner_w = width
    if corner_h < 2:
        corner_h = height
    mask[:corner_h, :corner_w] = True
    mask[:corner_h, width - corner_w:] = True
    mask[height - corner_h:, :corner_w] = True
    mask[height - corner_h:, width - corner_w:] = True
    mask[0, :] = mask[-1, :] = True
    mask[:, 0] = mask[:, -1] = True
    return mask


def detect_background_key_rgb(
    image: Image.Image, chroma_key: tuple[int, int, int]
) -> tuple[int, int, int]:
    """The flat background colour as the model actually painted it, or the declared key.

    Samples the corner patches and the border, keeps the opaque pixels that
    carry the declared key's hue signature (`is_border_key_candidate` — the
    border rule, which unlike the interior `is_key_family` does not demand the
    keyed channels balance), and — when they make up at
    least 12% of the samples — returns the mean of the most populated 8-wide
    RGB histogram bin among them. The mode, never the mean of everything: a
    handful of antialiased fringe pixels on the border must not drag an
    exact-key background off the key, and a two-cluster border must resolve to
    the dominant cluster, not a midpoint that mattes neither. Otherwise — no
    such background, the subject crowds every border, a degenerate key — the
    declared key comes back unchanged, which keeps `remove_chroma_background`
    byte-identical to its pre-detection behaviour on exact-key backgrounds.
    """
    keyed_channels, unkeyed_channels = _key_channel_split(chroma_key)
    if not keyed_channels:
        return tuple(chroma_key)  # type: ignore[return-value]
    rgba = image if image.mode == "RGBA" else image.convert("RGBA")
    data = np.array(rgba, dtype=np.uint8)
    height, width = data.shape[:2]
    sample = _key_detect_sample_mask(height, width) & (data[..., 3] != 0)
    if not sample.any():
        return tuple(chroma_key)  # type: ignore[return-value]
    rgb = data[..., :3].astype(np.int32)
    family = sample & _border_key_candidate_field(rgb, keyed_channels, unkeyed_channels)
    family_count = int(np.count_nonzero(family))
    if family_count < int(np.count_nonzero(sample)) * _KEY_DETECT_MIN_FRACTION:
        return tuple(chroma_key)  # type: ignore[return-value]
    colors = rgb[family]  # (N, 3)
    bins = (colors >> _KEY_DETECT_BIN_SHIFT).astype(np.int64)
    slots = (bins[:, 0] << 16) | (bins[:, 1] << 8) | bins[:, 2]
    unique, inverse, counts = np.unique(slots, return_inverse=True, return_counts=True)
    mode = int(np.argmax(counts))  # first max = lowest slot on a tie: deterministic
    members = colors[inverse == mode]
    mean = members.sum(axis=0, dtype=np.int64) // len(members)
    return (int(mean[0]), int(mean[1]), int(mean[2]))


# remove_chroma_background pixel classes, decided once on the source colors.
_KEYED = 0  # erased: transparent input or hard key cut
_SUBJECT = 1  # not key-tinted — never touched
_BLEND_IN_BAND = 2  # key-tinted, within fringe_threshold of the key
_BLEND_OUT_OF_BAND = 3  # key-tinted, farther than fringe_threshold
_IN_BAND_UNMIX_KEY_DEPTH = 2

# A trapped-spill cluster must contain at least one strongly key-tinted pixel
# to be treated. This is the plan's visible-residue detector (every keyed
# channel clears every unkeyed channel by >40): warm subject colors (skin)
# score a marginal tint just above fringe_delta and must not be "corrected".
_SPILL_MIN_TINT = 40.0


def remove_chroma_background(
    image: Image.Image,
    chroma_key: tuple[int, int, int],
    threshold: float,
    fringe_threshold: float,
    fringe_delta: float,
    *,
    unmix_reach: int = 4,
    spill_max_fraction: float = 0.005,
    background_key: tuple[int, int, int] | None = None,
) -> Image.Image:
    """Key `chroma_key` out of `image` (hard cut + soft-alpha fringe unmix + trapped-spill despill).

    `background_key`: the background colour as actually painted. None (the
    default) detects it from the borders with `detect_background_key_rgb`;
    passing `chroma_key` itself pins the single-key behaviour (the frozen
    byte-identity gate does that).
    """
    rgba = image.convert("RGBA")
    width, height = rgba.size
    data = np.array(rgba, dtype=np.uint8)  # (H, W, 4); written back at the end
    source_rgb = data[..., :3].astype(np.int32)
    keyed_channels, unkeyed_channels = _key_channel_split(chroma_key)
    unseen = 255

    # The background as painted. Distances are taken to the declared key *and*
    # to the detected family colour and the smaller one wins, so an exact-key
    # background reproduces the single-key result bit for bit while a darker or
    # paler key of the same hue is cut from where it actually sits. The blend
    # model (despill / unmix) also mixes against the painted colour — that is
    # the colour the antialiased fringe was actually blended with. Which
    # channels count as "keyed" stays a property of the declared key.
    painted_key = (
        detect_background_key_rgb(rgba, chroma_key)
        if background_key is None
        else (int(background_key[0]), int(background_key[1]), int(background_key[2]))
    )

    # Classification, decided on the source colors before anything is erased.
    # np.select takes the first condition that holds, so the condlist order below
    # *is* the if/elif order it replaces — swapping the subject and in-band rows
    # changes the output wherever both hold at once (a wide --fringe-key-threshold
    # makes that reachable, and the gate has a case for it).
    key_distance = _key_distance_field(source_rgb, chroma_key)
    if painted_key != tuple(chroma_key):
        # The painted colour's authority is border evidence, and a pixel deep
        # inside the frame has none. So its ball erases the *background*: the
        # pixels that carry the key's hue signature themselves, plus whatever
        # else inside the ball touches that keyed region (the antialiased rim
        # of the subject, whose blend with a lit subject colour lifts the
        # unkeyed channel over the signature bar). An isolated patch inside
        # the subject that merely resembles the painted colour is left alone:
        # hot pink (250, 77, 150) sits 46 from Grok's (216, 46, 147) magenta
        # and would otherwise be cut out of the subject. The declared key's
        # ball stays what it always was — a colour ball, position-blind.
        painted_distance = _key_distance_field(source_rgb, painted_key)
        in_ball = painted_distance <= threshold
        painted_keyed = in_ball & _border_key_candidate_field(source_rgb, keyed_channels, unkeyed_channels)
        painted_keyed |= in_ball & (key_distance <= threshold)
        painted_keyed = _grow_into(painted_keyed, in_ball)
        key_distance = np.where(painted_keyed, np.minimum(key_distance, painted_distance), key_distance)
    source_tint = _key_tint_field(source_rgb, keyed_channels, unkeyed_channels)
    keyed_mask = (data[..., 3] == 0) | (key_distance <= threshold)
    classes = np.select(
        [keyed_mask, source_tint < fringe_delta, key_distance <= fringe_threshold],
        [_KEYED, _SUBJECT, _BLEND_IN_BAND],
        default=_BLEND_OUT_OF_BAND,
    ).astype(np.uint8)
    data[keyed_mask] = 0

    depths = np.full((height, width), unseen, dtype=np.uint8)  # chebyshev distance to keyed region
    depths[keyed_mask] = 0

    key_tint = key_tint_score(painted_key, chroma_key)
    max_reach = min(unseen - 1, unmix_reach if key_tint > 0 else 0)

    # Geometric distance to the nearest keyed-out pixel — outer background
    # *and* interior holes (hair gaps) alike. This walk is not blocked by
    # subject pixels, so an isolated key blend locked inside subject material
    # still gets a depth. Growing the keyed set one ring at a time numbers the
    # rings in the order a breadth-first walk would reach them.
    frontier = keyed_mask
    reached = keyed_mask
    depth = 0
    while frontier.any() and depth < max_reach:
        depth += 1
        frontier = _grow_chebyshev(frontier) & ~reached
        depths[frontier] = depth
        reached = reached | frontier

    # Soft-alpha unmix — binary erase cannot represent antialiased coverage.
    # Any key-tinted pixel within unmix_reach of the keyed region is separated
    # into despilled RGB + partial alpha instead:
    #   - out-of-band blends always (they are too subject-heavy to erase);
    #   - in-band blends only within the AA band nearest the key. Deeper
    #     key-tinted material stays byte-identical (v1.10.1 guardrail).
    # Only the selection is vectorized. The pixels that survive it are the AA
    # fringe — a thin minority — so the blend itself stays on the scalar
    # primitives that despill_color and unmix_key_blend already own.
    if key_tint > 0 and unmix_reach > 0:
        in_reach = (depths > 0) & (depths <= min(unmix_reach, unseen))
        unmixable = in_reach & (
            ((classes == _BLEND_IN_BAND) & (depths <= _IN_BAND_UNMIX_KEY_DEPTH))
            | (classes == _BLEND_OUT_OF_BAND)
        )
        rows, cols = np.nonzero(unmixable)
        for y, x in zip(rows.tolist(), cols.tolist()):
            red, green, blue, alpha = (int(value) for value in data[y, x])
            color = (red, green, blue)
            out_red, out_green, out_blue, out_alpha = unmix_key_blend(
                color, alpha, painted_key, key_tint, key_tint_score(color, chroma_key)
            )
            # The scalar path wrote this through `pixels[x, y] = (...)`, and PIL
            # clamped every channel to 0..255 on the way in. A uint8 array does
            # not — it raises — so the clamp has to be restored here or the
            # rewrite changes behavior instead of just its speed.
            #
            # Exactly one channel needs it. The three color channels leave
            # `despill_color` already squeezed by its own `min(255, max(0, …))`,
            # and re-clamping them here would put that bound in two places; the
            # alpha is the one value nothing bounds, because `coverage` exceeds
            # 1 whenever `tint` is negative (reachable with `--fringe-delta < 0`)
            # and `round(alpha * coverage)` then lands above `alpha`. It cannot
            # go the other way: `unmix_key_blend` returns a fully transparent
            # pixel for `out_alpha <= 0`, so the only unbounded direction is up.
            # Both premises are asserted in tests/test_chroma_rcb_byte_identity.py.
            data[y, x] = (out_red, out_green, out_blue, min(255, out_alpha))

    # Trapped-spill despill — generators paint key-colored spill *inside* the
    # subject (a green streak buried in crimson hair, key reflections between
    # strands) too far from any keyed pixel for depth-based treatment to
    # reach. Among the still-tinted pixels left after the passes above, a
    # small connected cluster is spill; a large one is intentional key-tinted
    # material (the hot-pink seed packet) and stays untouched. Spill keeps its
    # alpha — it sits inside opaque subject, so this is color correction, not
    # coverage: partial alpha here would punch pinholes through the sprite.
    if key_tint > 0 and keyed_mask.any() and spill_max_fraction > 0:
        subject_count = int(np.count_nonzero(~keyed_mask))
        spill_limit = max(32, round(subject_count * spill_max_fraction))
        # Re-scored on the *current* colors: the unmix pass above rewrote part of
        # the image, and a pixel it despilled is no longer a spill candidate.
        current_tint = _key_tint_field(data[..., :3].astype(np.int32),
                                       keyed_channels, unkeyed_channels)
        candidates = np.flatnonzero(
            ((data[..., 3] != 0) & (current_tint >= fringe_delta)).reshape(-1)
        )
        tints_left: dict[int, float] = dict(
            zip(candidates.tolist(), current_tint.reshape(-1)[candidates].tolist())
        )
        visited: set[int] = set()
        for start in tints_left:
            if start in visited:
                continue
            stack = [start]
            visited.add(start)
            cluster = []
            while stack:
                index = stack.pop()
                cluster.append(index)
                x = index % width
                y = index // width
                for dy in (-1, 0, 1):
                    for dx in (-1, 0, 1):
                        if 0 <= x + dx < width and 0 <= y + dy < height:
                            neighbor = (y + dy) * width + (x + dx)
                            if neighbor in tints_left and neighbor not in visited:
                                visited.add(neighbor)
                                stack.append(neighbor)
            if len(cluster) > spill_limit:
                continue
            if max(tints_left[index] for index in cluster) <= _SPILL_MIN_TINT:
                continue
            for index in cluster:
                x = index % width
                y = index // width
                red, green, blue, alpha = (int(value) for value in data[y, x])
                color = (red, green, blue)
                coverage, despilled = despill_color(
                    color, painted_key, key_tint, key_tint_score(color, chroma_key)
                )
                if coverage > 0:
                    data[y, x] = (*despilled, alpha)
    # Back into the converted copy rather than a fresh Image.fromarray, so the
    # returned image keeps the mode, size and `info` (icc profile, dpi) that
    # `convert` carried over from the caller's image.
    rgba.frombytes(data.tobytes())
    return rgba
