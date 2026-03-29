# Desktop Surface Reference

Use this reference when the primary user-facing surface is a desktop application.

## Surface Conventions

- Follow the repository's established window, menu, tray, updater, and packaging model.
- Keep IPC, command bridges, filesystem access, and shell integration behind explicit privileged boundaries.
- Treat install, update, and local persistence behavior as part of the shipped feature when the change depends on them.

## Common Risk Areas

- Check multi-window behavior, focus changes, and app restart or resume flows.
- Verify IPC validation, permission boundaries, and host integration paths before trusting renderer-side input.
- Watch for local file corruption, partial writes, or migration failures on app upgrade.
- Confirm signing, packaging, updater, or platform-specific runtime assumptions when the change touches release behavior.
