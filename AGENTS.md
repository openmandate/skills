# OpenMandate Agent Reference

This repo contains skills and MCP server configuration for OpenMandate.

## Quick Start

1. Set `OPENMANDATE_API_KEY` environment variable
2. Use MCP tools (auto-configured) or shell commands via `scripts/openmandate.py`

## Skills

- `openmandate` — Full workflow: create mandates, answer intake, manage matches

## MCP Server

Auto-configured via `.mcp.json`. Server URL: `https://mcp.openmandate.ai/mcp`

Tools: `create_mandate`, `get_mandate`, `list_mandates`, `submit_answers`, `close_mandate`, `list_matches`, `get_match`, `respond_to_match`
