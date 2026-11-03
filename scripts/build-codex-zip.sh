#!/usr/bin/env bash
# Build the ZIP for the OpenAI plugin submission portal
# (https://developers.openai.com/plugins/deploy/submission).
#
# The portable Agent Plugins package the portal expects is exactly:
#   plugin.json   root manifest with extensions.com.openai
#   mcp.json      the single remote MCP server
#   skills/       one folder per skill with SKILL.md
#   assets/       logo and composer icon referenced from plugin.json
# Nothing else goes in (no .claude-plugin/, no .codex-plugin/, no README).
set -euo pipefail

repo="$(cd "$(dirname "$0")/.." && pwd)"
plugin="$repo/plugins/seonix"
out_dir="$repo/dist"
out="$out_dir/seonix-codex-plugin.zip"

for f in plugin.json mcp.json; do
  [ -f "$plugin/$f" ] || { echo "missing plugins/seonix/$f" >&2; exit 1; }
done
[ -d "$plugin/skills" ] || { echo "missing plugins/seonix/skills/" >&2; exit 1; }
[ -d "$plugin/assets" ] || { echo "missing plugins/seonix/assets/" >&2; exit 1; }

mkdir -p "$out_dir"
rm -f "$out"

# The portal needs the OAuth declaration in mcp.json, but the plugin loader in
# Codex rejects `extensions` on a server entry and then drops the whole server.
# So the repo's mcp.json stays plain and only the ZIP carries the declaration.
stage="$(mktemp -d)"
trap 'rm -rf "$stage"' EXIT
python3 - "$plugin/mcp.json" "$stage/mcp.json" <<'PY'
import json, sys
mcp = json.load(open(sys.argv[1]))
for server in mcp["mcpServers"].values():
    server["extensions"] = {"com.openai": {"auth": {"type": "oauth", "client": {"mode": "dcr"}}}}
json.dump(mcp, open(sys.argv[2], "w"), indent=2)
PY

# -X drops macOS resource forks; .DS_Store is excluded explicitly.
(cd "$plugin" && zip -q -X -r "$out" plugin.json skills assets -x '*/.DS_Store' -x '.DS_Store')
(cd "$stage" && zip -q -X "$out" mcp.json)

echo "built $out"
unzip -l "$out"
