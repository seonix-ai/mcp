# Seonix MCP server

Connect AI agents — Claude Code, Cursor, Codex, VS Code, Windsurf — to your [Seonix](https://seonix.ai) SEO project.

Seonix is an SEO autopilot for a website: it crawls the site (Site Health), tracks every issue across scans, reads Google Search Console, researches keywords and clusters, scores drafts, and writes and publishes articles to WordPress, Shopify, Webflow, Ghost and Wix. This MCP server exposes that project data to your agent.

- **Endpoint:** `https://api.seonix.ai/mcp` (Streamable HTTP, remote, stateless)
- **Auth:** bearer API key, issued through a one-click device flow (no keys to copy by hand)
- **Access:** included in every paid Seonix plan (not available on the Free plan)
- **Agent instructions:** https://seonix.ai/mcp.md
- **Docs:** https://seonix.ai/mcp

This repository holds the client configuration and docs. The server itself runs at Seonix.

Looking for the free, open-source **local** auditor instead (audits any website, no account)? That is [seonix-ai/seonix-mcp](https://github.com/seonix-ai/seonix-mcp).

## Quick start

Paste this line into your agent:

```
Connect Seonix to this project over MCP: https://seonix.ai/mcp.md
```

The agent starts a connect session, shows you a link such as `https://app.seonix.ai/connect/agent?code=XXXX-XXXX`, you click **Connect** once in your Seonix account, and the agent writes the API key into its own config.

## Manual configuration

Create a key in Seonix: **Account → Agents** (`app.seonix.ai/account/agents`). Then:

**Claude Code**

```bash
claude mcp add --transport http seonix https://api.seonix.ai/mcp --header "Authorization: Bearer sx_mcp_…"
```

or copy [`.mcp.json`](.mcp.json) into your project and set `SEONIX_MCP_KEY` in your environment.

**Cursor**

Copy [`.cursor/mcp.json`](.cursor/mcp.json) into your project (or `~/.cursor/mcp.json`) and replace `sx_mcp_…` with your key.

**VS Code / Copilot, Windsurf, Codex**

Any client that supports remote Streamable HTTP servers with custom headers works: URL `https://api.seonix.ai/mcp`, header `Authorization: Bearer <key>`.

## What the agent can do

41 tools (36 read, 5 write) and 11 SEO playbooks as prompts.

| Area | Tools |
|---|---|
| Account & projects | `get_account`, `list_projects`, `get_project`, `get_plan_status`, `get_site_dna` |
| Site Health | `get_site_health`, `get_fix_plan`, `list_issues`, `get_issue`, `list_scans`, `get_scan_status`, `get_results`, `get_seo_progress`, `get_remediation_profile` |
| Search Console | `gsc_status`, `gsc_top_queries`, `gsc_top_pages`, `gsc_page_queries`, `gsc_opportunities`, `gsc_coverage`, `gsc_impact`, `gsc_timeseries` |
| Keywords & content | `list_keyword_candidates`, `list_clusters`, `get_cluster`, `list_articles`, `get_article`, `get_calendar`, `list_channels`, `analyze_seo`, `score_article`, `get_blog_integration_guide` |
| AI search | `get_ai_visibility` |
| Playbooks | `list_playbooks`, `get_playbook` |
| Write (scope `write`, confirmed per call) | `start_scan`, `apply_fix`, `get_fix_run`, `rollback_fix`, `acknowledge_issue`, `unacknowledge_issue` |

Everything that came from the website or the web is marked as untrusted data in tool results, so the agent never treats crawled page text as instructions.

## Limits

- 600 `tools/call` per hour per API key; handshakes and listings are free.
- Keys can be revoked at any time from **Account → Agents**; all keys are revoked on password change.
- Errors come back as JSON with an `error` code (`plan_required`, `project_required`, `rate_limited`, `not_connected`, …).

## Links

- Website: https://seonix.ai
- Pricing: https://seonix.ai/pricing
- API docs: https://seonix.ai/docs/api
- Official MCP Registry entry: `io.github.pahaa97/seonix`
- Support: info@seonix.ai
