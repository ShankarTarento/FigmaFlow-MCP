#!/bin/bash
# Wrapper script to run MCP server with Poetry
# Must run as module (not script) for relative imports to work
cd "$(dirname "$0")"
# Redirect stderr to log file for debugging
exec poetry run python3 -m src.mcp.server "$@" 2>>/tmp/mcp_server_debug.log
