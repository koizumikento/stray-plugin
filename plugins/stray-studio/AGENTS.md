# Stray Studio Guidance

## Script Changes

- Resolve all output paths before writing. Reject absolute paths, `..` traversal, and symlink escapes from the declared run root.
- Do not overwrite or delete existing files unless the skill contract names an explicit authorization gate.
- Keep credentials out of process arguments, logs, manifests, and generated artifacts.
- Treat network calls, publishing, installation, and other external sends as separately authorized side effects.
- Add regression tests under the changed skill's `tests/` directory for every safety invariant.

## Validation

- Run `PYTHONDONTWRITEBYTECODE=1 uv run --with pytest==9.1.1 python -m pytest -q -p no:cacheprovider plugins/stray-studio/skills/change-readiness-review/tests` after changing the change-readiness state helpers, contracts, or safety boundaries.
- Run `PYTHONDONTWRITEBYTECODE=1 uv run --with pytest==9.1.1 --with pillow==12.3.0 python -m pytest -q -p no:cacheprovider plugins/stray-studio/skills/corporate-site-builder/tests plugins/stray-studio/skills/pixel-art-asset-creator/tests` after changing their scripts.
- Run the repository routing validator after changing `SKILL.md`, companion metadata, or plugin discovery text.
