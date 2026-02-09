"""
Mock Figma Data for Demos
Use this when Figma API is rate-limited during demos
"""
import json
from typing import Dict, Any

# Sample Figma design data that you can use for demos
MOCK_DESIGNS = {
    "login_screen": {
        "name": "Login Screen",
        "type": "FRAME",
        "visible": True,
        "fills": [{"type": "SOLID", "color": {"r": 1, "g": 1, "b": 1, "a": 1}}],
        "children": [
            {
                "name": "Logo",
                "type": "FRAME",
                "visible": True,
                "width": 100,
                "height": 100,
                "fills": [{"type": "SOLID", "color": {"r": 0.2, "g": 0.4, "b": 0.8, "a": 1}}],
            },
            {
                "name": "Title",
                "type": "TEXT",
                "visible": True,
                "characters": "Welcome Back",
                "fontSize": 32,
                "fontWeight": 700,
                "fontFamily": "Inter",
                "fills": [{"type": "SOLID", "color": {"r": 0.1, "g": 0.1, "b": 0.1, "a": 1}}],
            },
            {
                "name": "Email Input",
                "type": "FRAME",
                "visible": True,
                "cornerRadius": 8,
                "fills": [{"type": "SOLID", "color": {"r": 0.95, "g": 0.95, "b": 0.95, "a": 1}}],
                "children": [
                    {
                        "name": "Placeholder",
                        "type": "TEXT",
                        "characters": "Email",
                        "fontSize": 16,
                        "fontFamily": "Inter",
                        "fills": [{"type": "SOLID", "color": {"r": 0.5, "g": 0.5, "b": 0.5, "a": 1}}],
                    }
                ],
            },
            {
                "name": "Login Button",
                "type": "FRAME",
                "visible": True,
                "cornerRadius": 8,
                "fills": [{"type": "SOLID", "color": {"r": 0.2, "g": 0.4, "b": 0.8, "a": 1}}],
                "children": [
                    {
                        "name": "Button Text",
                        "type": "TEXT",
                        "characters": "Login",
                        "fontSize": 18,
                        "fontWeight": 600,
                        "fontFamily": "Inter",
                        "fills": [{"type": "SOLID", "color": {"r": 1, "g": 1, "b": 1, "a": 1}}],
                    }
                ],
            },
        ],
    },
    
    "product_card": {
        "name": "Product Card",
        "type": "FRAME",
        "visible": True,
        "cornerRadius": 12,
        "fills": [{"type": "SOLID", "color": {"r": 1, "g": 1, "b": 1, "a": 1}}],
        "strokes": [{"type": "SOLID", "color": {"r": 0.9, "g": 0.9, "b": 0.9, "a": 1}}],
        "strokeWeight": 1,
        "children": [
            {
                "name": "Product Image",
                "type": "RECTANGLE",
                "fills": [{"type": "SOLID", "color": {"r": 0.9, "g": 0.9, "b": 0.9, "a": 1}}],
                "cornerRadius": 8,
            },
            {
                "name": "Product Name",
                "type": "TEXT",
                "characters": "Premium Product",
                "fontSize": 20,
                "fontWeight": 600,
                "fontFamily": "Inter",
                "fills": [{"type": "SOLID", "color": {"r": 0.1, "g": 0.1, "b": 0.1, "a": 1}}],
            },
            {
                "name": "Price",
                "type": "TEXT",
                "characters": "$99.99",
                "fontSize": 24,
                "fontWeight": 700,
                "fontFamily": "Inter",
                "fills": [{"type": "SOLID", "color": {"r": 0.2, "g": 0.6, "b": 0.3, "a": 1}}],
            },
        ],
    },
}


def get_mock_design(design_name: str = "login_screen") -> Dict[str, Any]:
    """
    Get mock design data for demos
    
    Args:
        design_name: Name of the mock design (login_screen, product_card)
        
    Returns:
        Mock Figma design data
    """
    return MOCK_DESIGNS.get(design_name, MOCK_DESIGNS["login_screen"])


def save_mock_to_cache(design_name: str = "login_screen", file_key: str = "demo"):
    """
    Save mock design to cache so it can be used in demos
    
    Args:
        design_name: Name of the mock design
        file_key: Cache key to use
    """
    from src.figma.cache import FigmaCache
    
    cache = FigmaCache()
    mock_data = get_mock_design(design_name)
    
    # Wrap in Figma's expected structure
    wrapped_data = {
        "nodes": {
            "demo": {
                "document": mock_data
            }
        }
    }
    
    cache.set(file_key, "demo", wrapped_data)
    print(f"✓ Saved {design_name} to cache as {file_key}")


if __name__ == "__main__":
    # Pre-populate cache with mock designs for demos
    print("Populating cache with mock designs for demos...")
    save_mock_to_cache("login_screen", "demo_login")
    save_mock_to_cache("product_card", "demo_product")
    print("\n✅ Demo cache ready!")
    print("Use file_key 'demo_login' or 'demo_product' in your demos")
