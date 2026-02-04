"""
MCP Server Core
Handles tool registration and request routing
"""
import asyncio
import os
from typing import Any, Dict
from dotenv import load_dotenv
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# Load environment variables
load_dotenv()


class FigmaFlowMCPServer:
    """Main MCP Server class"""
    
    def __init__(self) -> None:
        self.server = Server("figmaflow-mcp")
        self._register_handlers()
    
    def _register_handlers(self) -> None:
        """Register MCP tool handlers"""
        self.server.list_tools()(self._list_tools)
        self.server.call_tool()(self._call_tool)
    
    async def _list_tools(self) -> list[Tool]:
        """Return list of available tools"""
        return [
            Tool(
                name="get_figma_design",
                description="Fetch design data from a Figma file or node",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "fileUrl": {
                            "type": "string",
                            "description": "Figma file URL"
                        },
                        "nodeId": {
                            "type": "string",
                            "description": "Optional specific node ID"
                        },
                        "accessToken": {
                            "type": "string",
                            "description": "Figma API access token"
                        }
                    },
                    "required": ["fileUrl", "accessToken"]
                }
            ),
            Tool(
                name="generate_flutter_widget",
                description="Generate Flutter widget code from Figma design data",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "designData": {
                            "type": "object",
                            "description": "Parsed Figma design data"
                        },
                        "widgetName": {
                            "type": "string",
                            "description": "Name for the generated widget"
                        },
                        "options": {
                            "type": "object",
                            "properties": {
                                "stateful": {"type": "boolean"},
                                "includeImports": {"type": "boolean"}
                            }
                        }
                    },
                    "required": ["designData", "widgetName"]
                }
            ),
            Tool(
                name="generate_widget_tests",
                description="Generate Flutter widget tests from widget code",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "widgetCode": {
                            "type": "string",
                            "description": "Generated widget code"
                        },
                        "designData": {
                            "type": "object",
                            "description": "Design data for test scenarios"
                        }
                    },
                    "required": ["widgetCode", "designData"]
                }
            )
        ]
    
    async def _call_tool(self, name: str, arguments: Dict[str, Any]) -> list[TextContent]:
        """Route tool calls to appropriate handlers"""
        # Import handlers here to avoid circular imports
        from .tools import ToolHandlers
        
        handlers = ToolHandlers()
        
        if name == "get_figma_design":
            return await handlers.handle_get_figma_design(arguments)
        elif name == "generate_flutter_widget":
            return await handlers.handle_generate_flutter_widget(arguments)
        elif name == "generate_widget_tests":
            return await handlers.handle_generate_widget_tests(arguments)
        else:
            return [TextContent(
                type="text",
                text=f"Unknown tool: {name}"
            )]


async def main() -> None:
    """Main entry point for the MCP server"""
    server = FigmaFlowMCPServer()
    
    async with stdio_server() as (read_stream, write_stream):
        await server.server.run(
            read_stream,
            write_stream,
            server.server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
