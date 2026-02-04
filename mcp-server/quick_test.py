#!/usr/bin/env python3
"""
Quick test script for MCP server
Tests basic functionality without full integration
"""
import asyncio
import json
from src.figma.client import FigmaClient
from src.figma.parser import DesignParser


async def test_url_parsing():
    """Test Figma URL parsing"""
    print("🧪 Testing URL parsing...")
    
    test_cases = [
        {
            "url": "https://www.figma.com/file/ABC123/MyDesign",
            "expected_file": "ABC123",
            "expected_node": None
        },
        {
            "url": "https://www.figma.com/file/ABC123/MyDesign?node-id=1-2",
            "expected_file": "ABC123",
            "expected_node": "1:2"
        }
    ]
    
    for case in test_cases:
        file_key, node_id = FigmaClient.parse_file_url(case["url"])
        
        assert file_key == case["expected_file"], f"File key mismatch: {file_key} != {case['expected_file']}"
        assert node_id == case["expected_node"], f"Node ID mismatch: {node_id} != {case['expected_node']}"
        
        print(f"  ✅ {case['url']}")
    
    print("✅ URL parsing tests passed!\n")


async def test_design_parser():
    """Test design parser"""
    print("🧪 Testing design parser...")
    
    from src.figma.client import FigmaNode, BoundingBox, ColorRGBA
    
    # Create mock node
    node = FigmaNode(
        id="1:1",
        name="TestFrame",
        type="FRAME",
        absoluteBoundingBox=BoundingBox(x=0, y=0, width=100, height=50),
        backgroundColor=ColorRGBA(r=0.5, g=0.5, b=0.5, a=1.0),
        children=[]
    )
    
    parser = DesignParser()
    result = parser.parse_layout(node)
    
    assert result["name"] == "TestFrame"
    assert result["type"] == "Container"
    assert "bounds" in result
    assert result["bounds"]["width"] == 100
    
    print("  ✅ Design parser works")
    print(f"  Parsed: {json.dumps(result, indent=2)}\n")
    print("✅ Design parser tests passed!\n")


async def test_color_conversion():
    """Test color conversion"""
    print("🧪 Testing color conversion...")
    
    from src.figma.client import ColorRGBA
    parser = DesignParser()
    
    test_colors = [
        (ColorRGBA(r=1.0, g=0.0, b=0.0, a=1.0), "Color(0xFFFF0000)"),  # Red
        (ColorRGBA(r=0.0, g=1.0, b=0.0, a=1.0), "Color(0xFF00FF00)"),  # Green
        (ColorRGBA(r=0.0, g=0.0, b=1.0, a=1.0), "Color(0xFF0000FF)"),  # Blue
        (ColorRGBA(r=1.0, g=1.0, b=1.0, a=1.0), "Color(0xFFFFFFFF)"),  # White
    ]
    
    for color, expected in test_colors:
        result = parser._format_color(color)
        assert result == expected, f"Color mismatch: {result} != {expected}"
        print(f"  ✅ {expected}")
    
    print("✅ Color conversion tests passed!\n")


async def main():
    """Run all tests"""
    print("=" * 50)
    print("FigmaFlow-MCP Quick Tests")
    print("=" * 50 + "\n")
    
    try:
        await test_url_parsing()
        await test_design_parser()
        await test_color_conversion()
        
        print("=" * 50)
        print("✅ All quick tests passed!")
        print("=" * 50)
        
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        return 1
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)
