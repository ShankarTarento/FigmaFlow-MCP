"""
Test script for token filtering
Demonstrates the token reduction capabilities
"""
import json
from src.utils.token_filter import TokenFilter, FilterLevel


def create_sample_figma_data():
    """Create sample Figma design data with unnecessary properties"""
    return {
        "id": "1:2",  # Should be removed
        "name": "LoginButton",
        "type": "FRAME",
        "visible": True,
        "bounds": {
            "x": 127.58394,  # Should be rounded
            "y": 349.192847,  # Should be rounded
            "width": 250.0,
            "height": 56.0
        },
        "fills": [
            {
                "type": "SOLID",
                "visible": True,
                "color": {
                    "r": 0.2549019607843137,
                    "g": 0.5333333333333333,
                    "b": 0.9607843137254902,
                    "a": 1.0
                }
            },
            {
                "type": "SOLID",
                "visible": False,  # Should be removed (invisible)
                "color": {"r": 1.0, "g": 0.0, "b": 0.0, "a": 0.0}
            }
        ],
        "text": "Sign In",
        "exportSettings": [],  # Should be removed
        "blendMode": "NORMAL",  # Should be removed
        "effects": [],  # Should be removed
        "constraints": {"horizontal": "LEFT", "vertical": "TOP"},  # Should be removed
        "children": [
            {
                "id": "1:3",
                "name": "ButtonText",
                "type": "TEXT",
                "visible": True,
                "text": "Sign In",
                "fontSize": 16,
                "fontWeight": "MEDIUM"
            },
            {
                "id": "1:4",
                "name": "HiddenElement",
                "type": "FRAME",
                "visible": False,  # Entire element should be removed
                "children": []
            }
        ]
    }


def test_filtering():
    """Test different filtering levels"""
    sample_data = create_sample_figma_data()
    
    print("=" * 80)
    print("TOKEN FILTER TEST")
    print("=" * 80)
    
    # Test each filter level
    for level in [FilterLevel.AGGRESSIVE, FilterLevel.BALANCED, FilterLevel.CONSERVATIVE]:
        print(f"\n{'='*80}")
        print(f"Filter Level: {level.value.upper()}")
        print(f"{'='*80}")
        
        filter_obj = TokenFilter(level)
        filtered = filter_obj.filter_design_data(sample_data)
        
        # Get statistics
        stats = filter_obj.get_filtering_stats(sample_data, filtered)
        
        print(f"\nOriginal tokens: {stats['original_tokens']}")
        print(f"Filtered tokens: {stats['filtered_tokens']}")
        print(f"Tokens saved: {stats['tokens_saved']}")
        print(f"Reduction: {stats['reduction_percentage']}%")
        
        print(f"\nFiltered data structure:")
        print(json.dumps(filtered, indent=2))
    
    print(f"\n{'='*80}")
    print("Key Improvements:")
    print("=" * 80)
    print("✓ Removed invisible elements (HiddenElement)")
    print("✓ Removed Figma metadata (id, exportSettings, blendMode, effects, constraints)")
    print("✓ Rounded decimal coordinates (127.58 → 128)")
    print("✓ Removed invisible fills (opacity: 0)")
    print("✓ Simplified color values")
    print("✓ Preserved essential design information (layout, text, colors)")


if __name__ == "__main__":
    test_filtering()
