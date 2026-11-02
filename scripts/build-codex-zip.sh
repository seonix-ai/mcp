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

# -X drops macOS resource forks; .DS_Store is excluded explicitly.
(cd "$plugin" && zip -q -X -r "$out" plugin.json mcp.json skills assets -x '*/.DS_Store' -x '.DS_Store')

echo "built $out"
unzip -l "$out"
