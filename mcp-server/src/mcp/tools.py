"""
MCP Tool Handlers
Implements the logic for each MCP tool
"""
import json
import os
import sys
from typing import Any, Dict, Optional
from mcp.types import TextContent

from ..utils.logger import setup_logger
from ..utils.errors import handle_error, InvalidDesignError, AIGenerationError
from ..figma.client import FigmaClient, FigmaNode
from ..figma.parser import DesignParser
from ..generators.widget import WidgetGenerator
from ..ai.client import AIClient


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
        logger = setup_logger(__name__)
        
        try:
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
        logger = setup_logger(__name__)
        
        print("[MCP] ========== GENERATE WIDGET CALLED ==========", file=sys.stderr)
        print(f"[MCP] Args type: {type(args)}", file=sys.stderr)
        print(f"[MCP] Args content: {str(args)[:200]}", file=sys.stderr)
        
        try:
            print("[MCP] STEP 1: Imports successful", file=sys.stderr)
            
            # Validate args is a dictionary
            if not isinstance(args, dict):
                print(f"[MCP] ERROR: Args is not dict! Type: {type(args)}", file=sys.stderr)
                raise TypeError(
                    f"Invalid arguments format. Expected dict, got {type(args).__name__}. "
                    f"Arguments: {str(args)[:200]}"
                )
            
            print("[MCP] STEP 2: Args is dict - validating fields", file=sys.stderr)
            
            # Validate required arguments exist
            if "designData" not in args:
                raise ValueError("Missing required argument: designData")
            if "widgetName" not in args:
                raise ValueError("Missing required argument: widgetName")
            
            print(f"[MCP] STEP 3: Required fields present", file=sys.stderr)
            print(f"[MCP] Widget name: {args.get('widgetName')}", file=sys.stderr)
            
            # Always use environment variables from mcp-server/.env
            # The server runs as a separate process with its own .env loaded at startup
            print("[MCP] STEP 4: Loading AI configuration", file=sys.stderr)
            logger.info("Using AI configuration from server environment (.env file)")
            
            try:
                print("[MCP] STEP 5: Initializing AIClient", file=sys.stderr)
                ai_client = AIClient()
                print(f"[MCP] STEP 6: AIClient initialized successfully", file=sys.stderr)
                logger.info(f"✓ AIClient initialized - Model: {ai_client.model}, Base URL: {ai_client.base_url or 'default'}")
            except ValueError as e:
                print(f"[MCP] ERROR in AIClient init: {e}", file=sys.stderr)
                logger.error(f"Failed to initialize AIClient: {e}")
                raise AIGenerationError(
                    "AI configuration error. Please check mcp-server/.env file has:\n"
                    "  - AI_API_KEY\n"
                    "  - AI_BASE_URL (optional)\n"
                    "  - AI_MODEL (optional)"
                )
            
            print(f"[MCP] STEP 7: Creating WidgetGenerator", file=sys.stderr)
            generator = WidgetGenerator(ai_client)
            print(f"[MCP] STEP 8: WidgetGenerator created", file=sys.stderr)
            
            print(f"[MCP] STEP 9: Calling generator.generate()", file=sys.stderr)
            print(f"[MCP] - designData type: {type(args['designData'])}", file=sys.stderr)
            print(f"[MCP] - widgetName type: {type(args['widgetName'])}", file=sys.stderr)
            print(f"[MCP] - options type: {type(args.get('options', {}))}", file=sys.stderr)
            
            widget_code = await generator.generate(
                design_data=args["designData"],
                widget_name=args["widgetName"],
                options=args.get("options", {})
            )
            
            print(f"[MCP] STEP 10: Code generated", file=sys.stderr)
            print(f"[MCP] - Code length: {len(widget_code)}", file=sys.stderr)
            print(f"[MCP] - Code lines: {len(widget_code.splitlines())}", file=sys.stderr)
            print(f"[MCP] - First 100 chars: {widget_code[:100]}", file=sys.stderr)
            print(f"[MCP] - Last 100 chars: {widget_code[-100:]}", file=sys.stderr)
            sys.stderr.flush()
            
            logger.info(f"✓ Successfully generated widget code - {len(widget_code)} chars, {len(widget_code.splitlines())} lines")
            
            print(f"[MCP] STEP 11: Creating TextContent response", file=sys.stderr)
            result = [TextContent(type="text", text=widget_code)]
            print(f"[MCP] STEP 12: Returning response", file=sys.stderr)
            sys.stderr.flush()
            
            return result
            
        except Exception as e:
            logger.error(f"Error generating widget: {e}", exc_info=True)
            # Include actual error details for debugging
            error_details = f"{type(e).__name__}: {str(e)}"
            logger.error(f"Error details: {error_details}")
            
            # Log environment status for debugging
            logger.error(f"Environment check - API Key present: {bool(os.getenv('AI_API_KEY'))}")
            logger.error(f"Environment check - Base URL: {os.getenv('AI_BASE_URL') or 'not set'}")
            logger.error(f"Environment check - Model: {os.getenv('AI_MODEL') or 'not set'}")
            
            # Return actual error details to user (not generic message)
            detailed_error = (
                f"🤖 Widget Generation Failed\n\n"
                f"Error Type: {type(e).__name__}\n"
                f"Error Message: {str(e)}\n\n"
                f"Environment Status:\n"
                f"  • AI_API_KEY: {'✓ Present' if os.getenv('AI_API_KEY') else '✗ Missing'}\n"
                f"  • AI_BASE_URL: {os.getenv('AI_BASE_URL') or 'Not set (using OpenAI default)'}\n"
                f"  • AI_MODEL: {os.getenv('AI_MODEL') or 'gpt-4o (default)'}\n\n"
                f"If this error persists, check the MCP server logs for details."
            )
            return [TextContent(type="text", text=json.dumps({"error": detailed_error}))]
    
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
