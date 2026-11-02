# Changelog

All notable changes to the Seonix plugin and MCP client configuration.

## 1.0.0 - 2026-11-02

First packaged release.

- One plugin, `plugins/seonix`, with manifests for Claude Code (`.claude-plugin/plugin.json`), Codex / ChatGPT (portable `plugin.json` + `mcp.json`, `.codex-plugin/` compatibility manifest) and Cursor (`.cursor-plugin/plugin.json`); the repository root is a marketplace for all three (`.claude-plugin/marketplace.json`, `.agents/plugins/marketplace.json`, `.cursor-plugin/marketplace.json`).
- OAuth sign-in: the MCP entry is `https://api.seonix.ai/mcp` with no headers; clients discover the authorization server themselves. API keys remain a documented fallback.
- Three skills: `seonix-seo` (entry workflow), `seonix-fix-site` (Site Health to fix plan to fixes to rescan), `seonix-content` (clusters and calendar to draft to score to publish).
- Logo assets, `SECURITY.md`, a Makefile that validates the manifests and builds the Codex submission ZIP.
