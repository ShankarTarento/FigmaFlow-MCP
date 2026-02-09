"""
Direct test of widget generation to isolate the AttributeError
"""
import asyncio
import sys
import os
from dotenv import load_dotenv

load_dotenv()
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

async def test_widget_generation():
    """Test widget generation with sample data"""
    from src.mcp.tools import ToolHandlers
    
    print("=" * 80)
    print("DIRECT WIDGET GENERATION TEST")
    print("=" * 80)
    
    # Simulate what VS Code sends
    test_args = {
        "designData": {
            "name": "TestFrame",
            "type": "FRAME",
            "children": []
        },
        "widgetName": "TestWidget",
        "options": {
            "includeImports": True,
            "stateful": False
        }
    }
    
    print("\n1. Test Arguments:")
    print(f"   Type: {type(test_args)}")
    print(f"   Content: {test_args}")
    
    print("\n2. Calling ToolHandlers.handle_generate_flutter_widget()...")
    
    try:
        handlers = ToolHandlers()
        result = await handlers.handle_generate_flutter_widget(test_args)
        
        print("\n✅ SUCCESS!")
        print(f"   Result type: {type(result)}")
        print(f"   Result: {result}")
        
    except Exception as e:
        print("\n❌ ERROR!")
        print(f"   Error type: {type(e).__name__}")
        print(f"   Error message: {str(e)}")
        print("\n   Full traceback:")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = asyncio.run(test_widget_generation())
    sys.exit(exit_code)
