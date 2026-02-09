#!/usr/bin/env python3
"""
Test MCP protocol directly to find the exact error
"""
import json
import sys

# Simulate what MCP client sends
mcp_request = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
        "name": "generate_flutter_widget",
        "arguments": {
            "designData": {"name": "Test", "type": "FRAME"},
            "widgetName": "TestWidget"
        }
    }
}

print("Sending MCP request:", file=sys.stderr)
print(json.dumps(mcp_request, indent=2), file=sys.stderr)
print(json.dumps(mcp_request))
sys.stdout.flush()
