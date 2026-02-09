"""
Test with the EXACT data from VS Code logs
"""
import asyncio
import sys
import os
from dotenv import load_dotenv

load_dotenv()
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

async def test_real_data():
    """Test with real Figma data that's causing the error"""
    from src.mcp.tools import ToolHandlers
    from src.figma.client import FigmaClient
    
    print("=" * 80)
    print("TEST WITH REAL FIGMA DATA")
    print("=" * 80)
    
    # Fetch the EXACT design that's failing
    file_key = "J9en6JabZojwhL0gAbJrxe"
    node_id = "2867-15678"
    
    print(f"\n1. Fetching real Figma design...")
    try:
        figma_client = FigmaClient()
        node = await figma_client.get_node(file_key, node_id)
        
        from src.figma.parser import DesignParser
        parser = DesignParser()
        design_data = parser.parse_layout(node)
        await figma_client.close()
        
        print(f"   ✓ Got design data")
        print(f"   Type: {type(design_data)}")
        print(f"   Keys: {list(design_data.keys())[:10]}")
        
    except Exception as e:
        print(f"   ✗ Figma fetch failed: {e}")
        # Use mock data instead
        design_data = {
            "id": "2867:15678",
            "name": "Frame 2106258399",
            "type": "Container",
            "visible": True,
            "bounds": {"x": -4597.0, "y": 4}
        }
        print(f"   Using mock data instead")
    
    print(f"\n2. Calling widget generation with REAL data...")
    
    args = {
        "designData": design_data,
        "widgetName": "Test",
        "options": {
            "includeImports": True,
            "stateful": False
        }
    }
    
    print(f"   Args type: {type(args)}")
    print(f"   Args['designData'] type: {type(args['designData'])}")
    
    try:
        handlers = ToolHandlers()
        result = await handlers.handle_generate_flutter_widget(args)
        
        print(f"\n✅ SUCCESS!")
        print(f"   Generated code: {len(result[0].text)} chars")
        return 0
        
    except Exception as e:
        print(f"\n❌ ERROR!")
        print(f"   Type: {type(e).__name__}")
        print(f"   Message: {str(e)}")
        print("\n   FULL TRACEBACK:")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(test_real_data())
    sys.exit(exit_code)
