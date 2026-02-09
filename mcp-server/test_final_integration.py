#!/usr/bin/env python3
"""
Final integration test - simulates the exact MCP server flow
"""
import asyncio
import json
from dotenv import load_dotenv

# Load environment first
load_dotenv()

async def test_mcp_flow():
    """Test the complete MCP tool flow"""
    print("\n" + "="*70)
    print("FINAL INTEGRATION TEST - Complete MCP Flow")
    print("="*70)
    
    # Import after environment is loaded
    from src.mcp.tools import ToolHandlers
    
    # Sample design data
    sample_design = {
        "name": "Login Button",
        "type": "FRAME",
        "width": 200,
        "height": 50,
        "backgroundColor": {"r": 0.2, "g": 0.6, "b": 0.9, "a": 1.0},
        "children": [{
            "name": "Label",
            "type": "TEXT",
            "characters": "Sign In",
            "fontSize": 16,
            "fontWeight": 600
        }]
    }
    
    # Simulate extension call - NO AI config passed
    args = {
        "designData": sample_design,
        "widgetName": "LoginButton",
        "options": {
            "includeImports": True,
            "stateful": False
        }
    }
    
    print("\n1. Simulating Extension Call")
    print(f"   Widget Name: {args['widgetName']}")
    print(f"   Has Design Data: ✓")
    print(f"   AI Config Passed: ✗ (using server .env)")
    
    print("\n2. Calling MCP Tool Handler...")
    handlers = ToolHandlers()
    
    try:
        result = await handlers.handle_generate_flutter_widget(args)
        result_text = result[0].text
        
        # Check if error
        try:
            error_data = json.loads(result_text)
            if "error" in error_data:
                print(f"\n❌ GENERATION FAILED")
                print(f"   Error: {error_data['error']}")
                return False
        except json.JSONDecodeError:
            pass  # Not JSON - it's code!
        
        print(f"\n✓ GENERATION SUCCESSFUL!")
        print(f"   Code Length: {len(result_text)} characters")
        print(f"\n3. Generated Code Preview:")
        print("-" * 70)
        print(result_text[:600])
        if len(result_text) > 600:
            print("...")
        print("-" * 70)
        
        return True
        
    except Exception as e:
        print(f"\n❌ EXCEPTION: {type(e).__name__}")
        print(f"   {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    import sys
    success = asyncio.run(test_mcp_flow())
    print("\n" + "="*70)
    if success:
        print("✓ TEST PASSED - Extension should work now!")
    else:
        print("✗ TEST FAILED - Check error messages above")
    print("="*70 + "\n")
    sys.exit(0 if success else 1)
