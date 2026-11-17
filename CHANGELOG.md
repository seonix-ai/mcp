# Changelog

All notable changes to the Seonix plugin and MCP client configuration.

## 1.2.0 - 2026-11-17

The site owner decides; the agent reports.

- `seonix-fix-site` is one pass, not a loop: read the findings, put the ranking-sensitive ones to the owner, apply what they approve, rescan, check what changed with `get_page_changes`, report and stop. A finding that is gone after a scan is not proof of a fix.
- Any canonical, noindex, robots, redirect or deletion change needs the owner's yes on every page, with or without traffic: a canonicalised, noindexed or redirected page has no traffic of its own. "Fix everything" is not that yes, and an unattended run changes none of them.
- The risk classes are `low`, `careful` and `ranking_sensitive` (the first was `safe`), the traffic window is 90 days (`search_console_90d`), and the item's `fix` text is the one to follow. `apply_fix` needs `confirm_ranking_sensitive` and `issue_ids` for ranking-sensitive codes (`pages_required` otherwise).
- `seonix-content`: a published article that gets search clicks is not a draft; its title, H1 and text are not changed to pass a check.
- Descriptions no longer promise that the agent "fixes the site in code".

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
