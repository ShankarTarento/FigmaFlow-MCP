"""
Figma Design Parser
Converts Figma design data to Flutter-friendly structure
"""
from typing import Dict, Any, List, Optional
from .client import FigmaNode, ColorRGBA, BoundingBox


class DesignParser:
    """Parse Figma design data into Flutter-compatible structure"""
    
    def parse_layout(self, node: FigmaNode) -> Dict[str, Any]:
        """
        Extract layout information from Figma node
        
        Args:
            node: Figma node to parse
            
        Returns:
            Dictionary with Flutter-friendly layout data
        """
        layout_data = {
            "id": node.id,
            "name": node.name,
            "type": self._map_node_type(node.type),
            "visible": node.visible,
        }
        
        # Add bounding box if available
        if node.absolute_bounding_box:
            layout_data["bounds"] = {
                "x": node.absolute_bounding_box.x,
                "y": node.absolute_bounding_box.y,
                "width": node.absolute_bounding_box.width,
                "height": node.absolute_bounding_box.height,
            }
        
        # Add background color if available
        if node.background_color:
            layout_data["backgroundColor"] = self._format_color(node.background_color)
        
        # Add text content if it's a text node
        if node.characters:
            layout_data["text"] = node.characters
        
        # Add fills (for backgrounds, shapes)
        if node.fills:
            layout_data["fills"] = self._parse_fills(node.fills)
        
        # Add strokes (borders)
        if node.strokes:
            layout_data["strokes"] = self._parse_strokes(node.strokes)
        
        # Recursively parse children
        if node.children:
            layout_data["children"] = [
                self.parse_layout(child) for child in node.children
            ]
        
        return layout_data
    
    def _map_node_type(self, figma_type: str) -> str:
        """
        Map Figma node types to Flutter widget types
        
        Args:
            figma_type: Figma node type
            
        Returns:
            Suggested Flutter widget type
        """
        type_mapping = {
            "FRAME": "Container",
            "RECTANGLE": "Container",
            "TEXT": "Text",
            "COMPONENT": "Widget",
            "INSTANCE": "Widget",
            "GROUP": "Column",
            "VECTOR": "Icon",
            "ELLIPSE": "CircleAvatar",
            "LINE": "Divider",
        }
        return type_mapping.get(figma_type, "Widget")
    
    def _format_color(self, color: ColorRGBA) -> str:
        """
        Convert Figma RGBA color to Flutter Color format
        
        Args:
            color: ColorRGBA object
            
        Returns:
            Flutter Color string (e.g., "Color(0xFFRRGGBB)")
        """
        r = int(color.r * 255)
        g = int(color.g * 255)
        b = int(color.b * 255)
        a = int(color.a * 255)
        
        # Format as 0xAARRGGBB
        hex_color = f"0x{a:02X}{r:02X}{g:02X}{b:02X}"
        return f"Color({hex_color})"
    
    def _parse_fills(self, fills: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Parse Figma fills
        
        Args:
            fills: List of fill objects
            
        Returns:
            Parsed fills data
        """
        parsed_fills = []
        for fill in fills:
            if fill.get("visible", True):
                fill_data = {
                    "type": fill.get("type", "SOLID")
                }
                
                # Add color for solid fills
                if fill["type"] == "SOLID" and "color" in fill:
                    color = ColorRGBA(**fill["color"])
                    fill_data["color"] = self._format_color(color)
                
                parsed_fills.append(fill_data)
        
        return parsed_fills
    
    def _parse_strokes(self, strokes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Parse Figma strokes (borders)
        
        Args:
            strokes: List of stroke objects
            
        Returns:
            Parsed stroke data
        """
        parsed_strokes = []
        for stroke in strokes:
            if stroke.get("visible", True):
                stroke_data = {
                    "type": stroke.get("type", "SOLID")
                }
                
                if stroke["type"] == "SOLID" and "color" in stroke:
                    color = ColorRGBA(**stroke["color"])
                    stroke_data["color"] = self._format_color(color)
                
                parsed_strokes.append(stroke_data)
        
        return parsed_strokes
    
    def get_widget_hierarchy_summary(self, layout_data: Dict[str, Any], indent: int = 0) -> str:
        """
        Generate a human-readable summary of widget hierarchy
        
        Args:
            layout_data: Parsed layout data
            indent: Current indentation level
            
        Returns:
            Multi-line string showing hierarchy
        """
        summary = "  " * indent + f"- {layout_data['type']}: {layout_data['name']}\n"
        
        if "children" in layout_data:
            for child in layout_data["children"]:
                summary += self.get_widget_hierarchy_summary(child, indent + 1)
        
        return summary
