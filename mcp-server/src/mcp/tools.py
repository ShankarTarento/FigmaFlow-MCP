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
        from ..utils.logger import setup_logger
        from ..utils.errors import handle_error, InvalidDesignError
        
        logger = setup_logger(__name__)
        
        try:
            from ..figma.client import FigmaClient
            from ..figma.parser import DesignParser
            
            figma_client = FigmaClient(args["accessToken"])
            
            # Parse URL to extract file key and node ID
            file_key, node_id = FigmaClient.parse_file_url(args["fileUrl"])
            
            if not file_key:
                error_msg = handle_error(InvalidDesignError("unknown", "Invalid Figma URL format"))
                return [TextContent(type="text", text=json.dumps({"error": error_msg}))]
            
            # Use provided nodeId if available
            if "nodeId" in args and args["nodeId"]:
                node_id = args["nodeId"]
            
            logger.info(f"Fetching Figma design: {file_key}:{node_id or 'root'}")
            
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
                    first_canvas = document["children"][0]
                    if first_canvas.get("children"):
                        first_frame = first_canvas["children"][0]
                        node = FigmaNode(**first_frame)
                        design_data = parser.parse_layout(node)
                    else:
                        design_data = {"error": "No frames found in design"}
                else:
                    design_data = {"error": "Empty document"}
            
            logger.info("✓ Successfully fetched Figma design")
            return [TextContent(type="text", text=json.dumps(design_data, indent=2))]
            
        except Exception as e:
            logger.error(f"Error fetching Figma design: {e}", exc_info=True)
            error_message = handle_error(e)
            return [TextContent(type="text", text=json.dumps({"error": error_message}))]
    
    async def handle_generate_flutter_widget(self, args: Dict[str, Any]) -> list[TextContent]:
        """
        Handle generate_flutter_widget tool call
        
        Args:
            args: Tool arguments containing designData, widgetName, options
            
        Returns:
            List of TextContent with generated widget code
        """
        from ..utils.logger import setup_logger
        from ..utils.errors import handle_error, AIGenerationError
        
        logger = setup_logger(__name__)
        
        try:
            from ..generators.widget import WidgetGenerator
            from ..ai.client import AIClient
            
            logger.info(f"Generating widget: {args.get('widgetName', 'Unknown')}")
            
            # Use API key from args (passed by extension)
            ai_client = AIClient(api_key=args.get("openaiApiKey"))
            generator = WidgetGenerator(ai_client)
            
            widget_code = await generator.generate(
                design_data=args["designData"],
                widget_name=args["widgetName"],
                options=args.get("options", {})
            )
            
            logger.info("✓ Successfully generated widget code")
            return [TextContent(type="text", text=widget_code)]
            
        except Exception as e:
            logger.error(f"Error generating widget: {e}", exc_info=True)
            error_message = handle_error(AIGenerationError(str(e)))
            return [TextContent(type="text", text=json.dumps({"error": error_message}))]
    
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
