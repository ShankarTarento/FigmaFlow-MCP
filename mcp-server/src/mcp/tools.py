"""
MCP Tool Handlers
Implements the logic for each MCP tool
"""
import json
from typing import Any, Dict
from mcp.types import TextContent


class ToolHandlers:
    """Handlers for MCP tools"""
    
    def __init__(self) -> None:
        """Initialize tool handlers"""
        # Lazy imports to avoid circular dependencies
        pass
    
    async def handle_get_figma_design(self, args: Dict[str, Any]) -> list[TextContent]:
        """
        Handle get_figma_design tool call
        
        Args:
            args: Tool arguments containing fileUrl, nodeId (optional), accessToken
            
        Returns:
            List of TextContent with design data or error
        """
        try:
            from ..figma.client import FigmaClient
            from ..figma.parser import DesignParser
            
            figma_client = FigmaClient(args["accessToken"])
            
            # Parse URL to extract file key and node ID
            file_key, node_id = FigmaClient.parse_file_url(args["fileUrl"])
            
            if not file_key:
                return [TextContent(
                    type="text",
                    text=json.dumps({"error": "Invalid Figma URL"})
                )]
            
            # Use provided nodeId if available
            if "nodeId" in args and args["nodeId"]:
                node_id = args["nodeId"]
            
            # Fetch design data
            if node_id:
                node = await figma_client.get_node(file_key, node_id)
                parser = DesignParser()
                design_data = parser.parse_layout(node)
            else:
                file_data = await figma_client.get_file(file_key)
                from ..figma.client import FigmaNode
                parser = DesignParser()
                # Parse first canvas from document
                document = file_data.get("document", {})
                if document.get("children"):
                    # Get first canvas/page
                    first_canvas = document["children"][0]
                    if first_canvas.get("children"):
                        # Get first frame on canvas
                        first_frame = first_canvas["children"][0]
                        node = FigmaNode(**first_frame)
                        design_data = parser.parse_layout(node)
                    else:
                        design_data = {"error": "No frames found in design"}
                else:
                    design_data = {"error": "Empty document"}
            
            return [TextContent(
                type="text",
                text=json.dumps(design_data, indent=2)
            )]
            
        except Exception as e:
            return [TextContent(
                type="text",
                text=json.dumps({"error": str(e)})
            )]
    
    async def handle_generate_flutter_widget(self, args: Dict[str, Any]) -> list[TextContent]:
        """
        Handle generate_flutter_widget tool call
        
        Args:
            args: Tool arguments containing designData, widgetName, options
            
        Returns:
            List of TextContent with generated widget code
        """
        try:
            from ..generators.widget import WidgetGenerator
            from ..ai.client import AIClient
            
            # Use API key from args (passed by extension)
            ai_client = AIClient(api_key=args.get("openaiApiKey"))
            generator = WidgetGenerator(ai_client)
            
            widget_code = await generator.generate(
                design_data=args["designData"],
                widget_name=args["widgetName"],
                options=args.get("options", {})
            )
            
            return [TextContent(
                type="text",
                text=widget_code
            )]
            
        except Exception as e:
            return [TextContent(
                type="text",
                text=json.dumps({"error": str(e)})
            )]
    
    async def handle_generate_widget_tests(self, args: Dict[str, Any]) -> list[TextContent]:
        """
        Handle generate_widget_tests tool call
        
        Args:
            args: Tool arguments containing widgetCode, designData
            
        Returns:
            List of TextContent with generated test code
        """
        try:
            from ..generators.test import TestGenerator
            from ..ai.client import AIClient
            
            ai_client = AIClient()
            generator = TestGenerator(ai_client)
            
            test_code = await generator.generate_widget_tests(
                widget_code=args["widgetCode"],
                design_data=args["designData"]
            )
            
            return [TextContent(
                type="text",
                text=test_code
            )]
            
        except Exception as e:
            return [TextContent(
                type="text",
                text=json.dumps({"error": str(e)})
            )]
