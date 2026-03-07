# OpenMandate — Agent Skills

Say what you need. An agent finds the match.

[OpenMandate](https://openmandate.ai) helps founders find cofounders and early teammates beyond their network. Describe what you need and what you offer. OpenMandate keeps evaluating fit over time and introduces both sides when there is real mutual match.

## Install

```bash
npx skills add openmandate/skills
```

Works with Claude Code, Cursor, VS Code, Windsurf, Codex, Gemini CLI, and 30+ other agents.

This installs the OpenMandate skill **and** auto-configures the [MCP server](https://mcp.openmandate.ai/mcp) for full API access.

## Setup

1. Sign up at [openmandate.ai](https://openmandate.ai)
2. Create an API key at [openmandate.ai/api-keys](https://openmandate.ai/api-keys)
3. Set the environment variable:

```bash
export OPENMANDATE_API_KEY="om_live_..."
```

## What's Included

| Component | Purpose |
|-----------|---------|
| **Skill** (`skills/openmandate/SKILL.md`) | Teaches your coding agent the OpenMandate workflow, API patterns, and best practices |
| **MCP Server** (`.mcp.json`) | Auto-configures the hosted MCP server — 14 tools for full API access |
| **Shell Helper** (`scripts/openmandate.py`) | Stdlib-only Python CLI for agents without MCP support |
| **References** (`references/`) | API reference, intake workflow, matching guide, SDK docs |

## Also Available

| Integration | Install |
|-------------|---------|
| Python SDK | `pip install openmandate` — [GitHub](https://github.com/openmandate/openmandate-python) |
| JavaScript SDK | `npm install openmandate` — [GitHub](https://github.com/openmandate/openmandate-js) |
| MCP Server (manual) | `https://mcp.openmandate.ai/mcp` |
| ClawHub | `clawhub install openmandate` |

## Links

- [openmandate.ai](https://openmandate.ai)
- [API Keys](https://openmandate.ai/api-keys)
- [Python SDK](https://github.com/openmandate/openmandate-python)
- [JavaScript SDK](https://github.com/openmandate/openmandate-js)
