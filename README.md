# Seonix for AI agents

Give Claude Code, Codex, Cursor and other AI agents your [Seonix](https://seonix.ai) SEO project: Site Health and the fix plan, Google Search Console, keywords, articles and eleven SEO playbooks — so the agent fixes the site in code, writes in your voice and ships content that shows up in Google, ChatGPT and Gemini.

Seonix grows organic and AI-search visibility for a website on autopilot: it crawls the site, tracks every issue across scans, reads Search Console, researches keywords, scores drafts, and writes and publishes articles. This repository is the plugin that connects an agent to that project through the hosted Seonix MCP server. The server itself runs at Seonix.

- **MCP endpoint:** `https://api.seonix.ai/mcp` (Streamable HTTP, remote)
- **Sign-in:** OAuth — the agent sends you to `app.seonix.ai` to approve once; no key to paste
- **Access:** included in every paid Seonix plan (not available on the Free plan)
- **Docs:** https://seonix.ai/mcp · agent-readable manifest: https://seonix.ai/mcp.md

Looking for the free, open-source **local** auditor instead (audits any website, no account)? That is [seonix-ai/seonix-mcp](https://github.com/seonix-ai/seonix-mcp).

## Install

### Claude Code

```bash
claude plugin marketplace add seonix-ai/mcp
claude plugin install seonix@seonix
```

Or both in one line (Claude Code 2.1.292+): `claude plugin install seonix --marketplace seonix-ai/mcp`. Inside a session: `/plugin marketplace add seonix-ai/mcp`, then `/plugin install seonix@seonix`. The first tool call opens the OAuth sign-in; `/mcp` shows the `seonix` server and lets you re-authenticate.

### Codex / ChatGPT

```bash
codex plugin marketplace add seonix-ai/mcp
codex plugin add seonix@seonix
```

The plugin is also submitted to the OpenAI plugin directory; once it is listed there, install it from the directory in ChatGPT or Codex instead.

### Cursor

[![Add Seonix to Cursor](https://cursor.com/deeplink/mcp-install-dark.svg)](cursor://anysphere.cursor-deeplink/mcp/install?name=seonix&config=eyJ1cmwiOiJodHRwczovL2FwaS5zZW9uaXguYWkvbWNwIn0%3D)

The button adds the `seonix` MCP server to Cursor; Cursor runs the OAuth sign-in on first use. The same config by hand — `.cursor/mcp.json` in your project or `~/.cursor/mcp.json`:

```json
{ "mcpServers": { "seonix": { "url": "https://api.seonix.ai/mcp" } } }
```

Cursor also loads this repository as a plugin marketplace (`.cursor-plugin/marketplace.json` → `plugins/seonix`); the directory listing is at https://cursor.directory/plugins/seonix.

### VS Code (Copilot)

`.vscode/mcp.json`:

```json
{ "servers": { "seonix": { "type": "http", "url": "https://api.seonix.ai/mcp" } } }
```

### Claude.ai and ChatGPT

Connect Seonix from the connector / plugin directories of each product once the listings are live. Until then, use one of the clients above.

### Any other MCP client

Add a remote Streamable HTTP server with URL `https://api.seonix.ai/mcp` and no headers. The client discovers the authorization server through `/.well-known/oauth-protected-resource`, registers itself (dynamic client registration) and runs the PKCE flow.

## How sign-in works

1. On the first call the client gets a `401` from the server, reads its OAuth metadata and opens `https://app.seonix.ai/connect/oauth` in your browser.
2. You see the client name, the requested scopes (`read`: Site Health, Search Console, keywords, articles; `write`: start scans, apply or roll back Seonix fixes, mark issues) and the requester's IP, and click **Approve**.
3. The client receives a short-lived token and refreshes it on its own. Revoke it any time at **Account → Agents** (`app.seonix.ai/account/agents`); changing your password revokes every grant.

### API key instead of OAuth

A client that cannot run OAuth (CI, a script, an older agent) can use a personal API key. Create one at **Account → Agents** and send it as a bearer token:

```json
{ "mcpServers": { "seonix": { "type": "http", "url": "https://api.seonix.ai/mcp", "headers": { "Authorization": "Bearer ${SEONIX_MCP_KEY}" } } } }
```

```bash
claude mcp add --transport http seonix https://api.seonix.ai/mcp --header "Authorization: Bearer ${SEONIX_MCP_KEY}"
```

An agent can also obtain a key by itself through the one-click device flow described at https://seonix.ai/mcp.md: it shows you a link such as `https://app.seonix.ai/connect/agent?code=XXXX-XXXX`, you click **Connect** once, and the agent writes the key into its own config. Keys are never part of this plugin; the manifests here carry no headers.

### One project per connection

Use `https://api.seonix.ai/mcp/p/<project id>` as the URL and every call is scoped to that project — no `project_id` argument needed. `list_projects` returns the ids.

## What the agent can do

41 tools (36 read, 5 write) and 11 SEO playbooks served as MCP prompts, resources and the `get_playbook` tool.

| Area | Tools |
|---|---|
| Account & projects | `get_account`, `list_projects`, `get_project`, `get_plan_status`, `get_site_dna`, `get_seo_progress` |
| Site Health | `get_site_health`, `get_fix_plan`, `list_issues`, `get_issue`, `get_remediation_profile`, `list_scans`, `get_scan_status`, `get_results` |
| Search Console | `gsc_status`, `gsc_top_queries`, `gsc_top_pages`, `gsc_page_queries`, `gsc_opportunities`, `gsc_coverage`, `gsc_impact`, `gsc_timeseries` |
| Keywords & content | `list_keyword_candidates`, `list_clusters`, `get_cluster`, `get_calendar`, `list_articles`, `get_article`, `analyze_seo`, `score_article`, `list_channels`, `get_blog_integration_guide` |
| AI search | `get_ai_visibility` |
| Playbooks | `list_playbooks`, `get_playbook` |
| Write (scope `write`, confirmed per call) | `start_scan`, `apply_fix`, `rollback_fix`, `acknowledge_issue`, `unacknowledge_issue` (`get_fix_run` reads a fix run) |

Playbooks: `seo_review` (the entry point: a full audit-and-plan of the project), `promote_site_playbook`, `work_through_page`, `work_through_all_pages`, `fix_issues_in_code`, `keyword_map_site`, `internal_linking_plan`, `write_article_for_brief`, `striking_distance_plan`, `monthly_seo_report`, `connect_blog_to_seonix`.

Resources: `seonix://guides` (index), `seonix://guides/seo-scoring`, `seonix://guides/title-style`, `seonix://guides/remediation/{code}`, `seonix://guides/blog-integration`, `seonix://playbooks/{name}`.

## Skills included

Three thin skills ship with the plugin; the detailed procedures stay on the server as playbooks, so they update without a new plugin version.

| Skill | When it triggers | What it does |
|---|---|---|
| `seonix-seo` | "improve SEO / traffic / content of my site", anything mentioning Seonix, Site Health or Search Console | The entry workflow: `get_account` → the right path (fix the site, traffic questions, writing), the untrusted-data and confirm-before-write rules, error codes |
| `seonix-fix-site` | "fix the SEO issues", "work through Site Health", "rescan" | `get_site_health` → `get_fix_plan` → fixes in the codebase or `apply_fix` on WordPress → `start_scan` → verify |
| `seonix-content` | "what should I write next", "score this draft", "publish through Seonix" | clusters and calendar → `get_site_dna` → draft → `analyze_seo` → publish through Seonix |

In Claude Code they are `/seonix:seonix-seo`, `/seonix:seonix-fix-site` and `/seonix:seonix-content`; the agent also picks them up on its own from their descriptions.

## Limits

- 600 tool calls per hour per connection (handshakes and listings are free); `rate_limited` carries `retry_after_seconds`.
- Responses are compact by default (for example `get_fix_plan` returns 10 items with 3 URLs each); every tool has flags to widen them.
- Errors come back as JSON with an `error` code: `unauthorized`, `plan_required` (with `upgrade_url`), `project_required`, `project_not_found`, `not_connected`, `not_available`, `scope_required`, `invalid_argument`, `not_found`, `conflict`, `rate_limited`, `internal`.

## Security

- **Untrusted data.** Anything that came from your website or from the web — crawled page evidence, page titles and URLs in the fix plan, article HTML, competitor-derived cluster insights, Search Console query strings typed by anonymous searchers — is marked in tool results with `"untrusted": true` or an `untrusted_source` field. The skills instruct the agent to treat it as data, never as instructions, and to tell you if a page contains instructions.
- **Confirm before any write.** `start_scan`, `apply_fix`, `rollback_fix`, `acknowledge_issue` and `unacknowledge_issue` need the `write` scope and, by the skills' rules, your explicit yes before each call. Read-only grants get `scope_required`.
- **No code runs locally.** The plugin is JSON manifests, Markdown skills and images. No hooks, no local server, no secrets.
- Report a vulnerability as described in [SECURITY.md](SECURITY.md).

## Repository layout

The repository is a marketplace with one plugin, `plugins/seonix`, in the layout all three platforms read:

```
.claude-plugin/marketplace.json     Claude Code marketplace "seonix"  -> ./plugins/seonix
.agents/plugins/marketplace.json    Codex marketplace "seonix"        -> ./plugins/seonix
.cursor-plugin/marketplace.json     Cursor marketplace "seonix"       -> plugins/seonix
.cursor/mcp.json                    project-level Cursor config, OAuth form (copy it)
plugins/seonix/
  plugin.json                       portable Agent Plugins manifest (Codex / ChatGPT, Cursor)
  mcp.json                          portable MCP config: the one remote server, OAuth via DCR
  .mcp.json                         Claude Code / Codex-compatible MCP config (type: http, no headers)
  .claude-plugin/plugin.json        Claude Code plugin manifest
  .codex-plugin/plugin.json         Codex compatibility manifest
  .cursor-plugin/plugin.json        Cursor plugin manifest
  skills/                           seonix-seo, seonix-fix-site, seonix-content
  assets/                           logo.svg, logo-512.png, logo-256.png, icon-128.png
scripts/                            build-codex-zip.sh, validate-schemas.py
```

`make validate` runs `claude plugin validate --strict` on the marketplace and the plugin and checks `plugin.json` / `mcp.json` against the Agent Plugins schemas; `make codex-zip` builds `dist/seonix-codex-plugin.zip` (plugin.json, mcp.json, skills/, assets/) for the OpenAI submission portal.

## Links

- Website: https://seonix.ai · Pricing: https://seonix.ai/pricing
- MCP docs: https://seonix.ai/mcp · API docs: https://seonix.ai/docs/api
- Privacy policy: https://seonix.ai/privacy-policy · Terms of use: https://seonix.ai/terms-of-use
- Support: info@seonix.ai · Issues: https://github.com/seonix-ai/mcp/issues
- Official MCP Registry entry: `io.github.pahaa97/seonix`
- Changelog: [CHANGELOG.md](CHANGELOG.md) · License: [MIT](LICENSE)
