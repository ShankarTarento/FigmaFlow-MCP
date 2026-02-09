"""
Complete end-to-end test using real Figma URL
Mimics exactly what VS Code extension does
"""
import asyncio
import sys
import os
from dotenv import load_dotenv

load_dotenv()
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

async def test_complete_flow():
    """Test complete flow from Figma URL to widget generation"""
    from src.figma.client import FigmaClient
    from src.mcp.tools import ToolHandlers
    
    print("=" * 80)
    print("COMPLETE END-TO-END TEST")
    print("=" * 80)
    
    # Real Figma URL from user
    figma_url = "https://www.figma.com/design/J9en6JabZojwhL0gAbJrxe/Homepage---Reimagining?node-id=2867-15678"
    file_key = "J9en6JabZojwhL0gAbJrxe"
    node_id = "2867-15678"
    
    print(f"\n1. Fetching Figma design...")
    print(f"   File: {file_key}")
    print(f"   Node: {node_id}")
    
    try:
        figma_client = FigmaClient()
        node = await figma_client.get_node(file_key, node_id)
        print(f"   ✓ Got node: {node.name} (type: {node.type})")
        
        # Convert to dict (what VS Code sends)
        design_data = node.model_dump()
        await figma_client.close()
        
    except Exception as e:
        print(f"   ✗ Figma error: {e}")
        return 1
    
    print(f"\n2. Calling widget generation...")
    print(f"   Design data type: {type(design_data)}")
    print(f"   Design data keys: {list(design_data.keys())[:5]}...")
    
    # This is EXACTLY what VS Code sends
    args = {
        "designData": design_data,
        "widgetName": "TestWidget",
        "options": {
            "includeImports": True,
            "stateful": False
        }
    }
    
    print(f"   Args type: {type(args)}")
    print(f"   Args keys: {list(args.keys())}")
    
    try:
        handlers = ToolHandlers()
        result = await handlers.handle_generate_flutter_widget(args)
        
        print(f"\n✅ SUCCESS!")
        print(f"   Generated {len(result[0].text)} chars of code")
        print(f"   First 200 chars: {result[0].text[:200]}")
        return 0
        
    except Exception as e:
        print(f"\n❌ ERROR!")
        print(f"   Type: {type(e).__name__}")
        print(f"   Message: {str(e)}")
        print("\n   Full traceback:")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(test_complete_flow())
    sys.exit(exit_code)
