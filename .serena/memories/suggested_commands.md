Useful commands for this repo:
- List skill files: find plugins/stray-plugin/skills -maxdepth 2 -type f | sort
- Read plugin manifest: sed -n '1,240p' plugins/stray-plugin/.codex-plugin/plugin.json
- Read marketplace: sed -n '1,220p' .agents/plugins/marketplace.json
- Validate JSON after manifest/marketplace edits:
python3 - <<'PY'
import json
json.load(open('.agents/plugins/marketplace.json'))
json.load(open('plugins/stray-plugin/.codex-plugin/plugin.json'))
print('json-ok')
PY
- Search files quickly: rg --files
- Search text quickly: rg "pattern" plugins/stray-plugin/skills