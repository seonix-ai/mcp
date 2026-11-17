# Changelog

All notable changes to the Seonix plugin and MCP client configuration.

## 1.1.0 - 2026-11-17

Protecting the traffic a site already has.

- `seonix-fix-site` opens with one rule: do not break what already ranks. The fix plan is worked by change risk (`safe` first, `careful` one template at a time, `ranking_sensitive` only on pages without traffic), and a ranking-sensitive change on a page with search traffic needs the site owner's yes for that page. A finding left alone on purpose is a valid outcome.
- `seonix-seo` carries the same rule and names the new `safe_change_protocol` playbook.
- The skills use what the server now returns: `change_risk`, `agent_note`, `pages_with_traffic` and `owner_approval_required` in `get_fix_plan`, the `safety` block, the `owner_confirmation_required` answer of `apply_fix`, and the new `get_page_changes` tool (what changed on the pages between two scans) for verifying an edit and for looking into a traffic drop.

## 1.0.0 - 2026-11-02

First packaged release.

- One plugin, `plugins/seonix`, with manifests for Claude Code (`.claude-plugin/plugin.json`), Codex / ChatGPT (portable `plugin.json` + `mcp.json`, `.codex-plugin/` compatibility manifest) and Cursor (`.cursor-plugin/plugin.json`); the repository root is a marketplace for all three (`.claude-plugin/marketplace.json`, `.agents/plugins/marketplace.json`, `.cursor-plugin/marketplace.json`).
- OAuth sign-in: the MCP entry is `https://api.seonix.ai/mcp` with no headers; clients discover the authorization server themselves. API keys remain a documented fallback.
- Three skills: `seonix-seo` (entry workflow), `seonix-fix-site` (Site Health to fix plan to fixes to rescan), `seonix-content` (clusters and calendar to draft to score to publish).
- Logo assets, `SECURITY.md`, a Makefile that validates the manifests and builds the Codex submission ZIP.
