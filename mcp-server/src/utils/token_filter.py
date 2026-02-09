"""
Intelligent Token Filter for Figma Design Data
Reduces token consumption by filtering unnecessary properties while preserving essential design information
"""
from typing import Dict, Any, List, Optional
from enum import Enum
import json


class FilterLevel(Enum):
    """Token filtering strategies"""
    AGGRESSIVE = "aggressive"  # Max token reduction, keep only critical properties
    BALANCED = "balanced"      # Recommended: critical + important properties
    CONSERVATIVE = "conservative"  # Keep most properties, remove obvious waste


class TokenFilter:
    """Intelligently filter Figma design data to reduce token usage"""
    
    # Property classifications
    CRITICAL_PROPERTIES = {
        'name', 'type', 'bounds', 'text', 'children', 'visible',
        'width', 'height', 'x', 'y'
    }
    
    IMPORTANT_PROPERTIES = {
        'fills', 'strokes', 'backgroundColor', 'characters',
        'fontSize', 'fontWeight', 'fontFamily', 'textAlign',
        'cornerRadius', 'opacity', 'strokeWeight'
    }
    
    # Properties to always remove (Figma-specific metadata)
    UNWANTED_PROPERTIES = {
        'id', 'exportSettings', 'blendMode', 'layoutMode', 'layoutGrow',
        'constraints', 'transitionNodeID', 'prototypeDevice', 'reactions',
        'plugins', 'sharedPluginData', 'componentPropertyReferences',
        'boundVariables', 'resolvedVariableModes', 'inferredAutoLayout',
        'layoutPositioning', 'itemSpacing', 'paddingLeft', 'paddingRight',
        'paddingTop', 'paddingBottom', 'primaryAxisSizingMode',
        'counterAxisSizingMode', 'primaryAxisAlignItems', 'counterAxisAlignItems',
        'layoutWrap', 'layoutGrids', 'effects', 'isMask', 'preserveRatio',
        'layoutAlign', 'layoutGrow', 'clipsContent'
    }
    
    def __init__(self, filter_level: FilterLevel = FilterLevel.BALANCED):
        """
        Initialize token filter
        
        Args:
            filter_level: Filtering strategy to use
        """
        self.filter_level = filter_level
    
    def filter_design_data(
        self,
        data: Dict[str, Any],
        max_depth: int = 4,
        current_depth: int = 0
    ) -> Dict[str, Any]:
        """
        Filter Figma design data intelligently
        
        Args:
            data: Design data to filter
            max_depth: Maximum depth for children recursion
            current_depth: Current recursion depth
            
        Returns:
            Filtered design data
        """
        if not isinstance(data, dict):
            return data
        
        filtered = {}
        
        # Determine which properties to keep based on filter level
        if self.filter_level == FilterLevel.AGGRESSIVE:
            allowed_props = self.CRITICAL_PROPERTIES
        elif self.filter_level == FilterLevel.BALANCED:
            allowed_props = self.CRITICAL_PROPERTIES | self.IMPORTANT_PROPERTIES
        else:  # CONSERVATIVE
            allowed_props = None  # Keep all except unwanted
        
        # Filter properties
        for key, value in data.items():
            # Skip unwanted properties
            if key in self.UNWANTED_PROPERTIES:
                continue
            
            # Check if property is allowed (if filtering is active)
            if allowed_props is not None and key not in allowed_props and key != 'children':
                continue
            
            # Special handling for specific properties
            if key == 'children':
                filtered[key] = self._filter_children(value, max_depth, current_depth)
            elif key == 'fills':
                filtered[key] = self._filter_fills(value)
            elif key == 'strokes':
                filtered[key] = self._filter_strokes(value)
            elif key == 'bounds':
                filtered[key] = self._simplify_bounds(value)
            elif isinstance(value, dict):
                filtered[key] = self.filter_design_data(value, max_depth, current_depth)
            elif isinstance(value, (int, float)):
                filtered[key] = self._round_number(value)
            else:
                filtered[key] = value
        
        return filtered
    
    def _filter_children(
        self,
        children: List[Dict[str, Any]],
        max_depth: int,
        current_depth: int
    ) -> List[Dict[str, Any]]:
        """
        Intelligently filter child nodes
        
        Args:
            children: List of child nodes
            max_depth: Maximum recursion depth
            current_depth: Current depth
            
        Returns:
            Filtered children list
        """
        if current_depth >= max_depth:
            # At max depth, just indicate children exist
            return []
        
        filtered_children = []
        
        for child in children:
            # Skip invisible children
            if not child.get('visible', True):
                continue
            
            # Recursively filter child
            filtered_child = self.filter_design_data(child, max_depth, current_depth + 1)
            filtered_children.append(filtered_child)
        
        # Smart grouping for repetitive children
        if len(filtered_children) > 10:
            # Check if children are similar (e.g., list items)
            if self._are_children_repetitive(filtered_children):
                # Keep first 2 as examples + add note
                return filtered_children[:2] + [{
                    'type': '_note',
                    'text': f'... and {len(filtered_children) - 2} similar items'
                }]
        
        return filtered_children
    
    def _are_children_repetitive(self, children: List[Dict[str, Any]]) -> bool:
        """
        Check if children are repetitive (same type and similar structure)
        
        Args:
            children: List of child nodes
            
        Returns:
            True if children appear repetitive
        """
        if len(children) < 3:
            return False
        
        # Check if most children have the same type
        types = [child.get('type') for child in children]
        if len(set(types)) == 1:
            return True
        
        return False
    
    def _filter_fills(self, fills: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Filter fill properties, removing invisible or redundant fills
        
        Args:
            fills: List of fill objects
            
        Returns:
            Filtered fills
        """
        if not fills:
            return fills
        
        filtered = []
        for fill in fills:
            # Skip invisible fills
            if not fill.get('visible', True):
                continue
            
            # Skip fully transparent fills
            if fill.get('opacity', 1.0) == 0:
                continue
            
            # Simplify fill object
            simplified = {
                'type': fill.get('type', 'SOLID')
            }
            
            # Add color for solid fills
            if fill.get('type') == 'SOLID' and 'color' in fill:
                color = fill['color']
                # Color might be a string (from parser) or dict (raw Figma)
                if isinstance(color, str):
                    # Already processed by parser, keep as-is
                    simplified['color'] = color
                elif isinstance(color, dict):
                    # Raw Figma color dict, process it
                    simplified['color'] = {
                        'r': self._round_number(color.get('r', 0)),
                        'g': self._round_number(color.get('g', 0)),
                        'b': self._round_number(color.get('b', 0)),
                        'a': self._round_number(color.get('a', 1.0))
                    }
                else:
                    # Unknown format, keep as-is
                    simplified['color'] = color

            
            filtered.append(simplified)
        
        return filtered
    
    def _filter_strokes(self, strokes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Filter stroke properties
        
        Args:
            strokes: List of stroke objects
            
        Returns:
            Filtered strokes
        """
        if not strokes:
            return strokes
        
        filtered = []
        for stroke in strokes:
            if not stroke.get('visible', True):
                continue
            
            simplified = {
                'type': stroke.get('type', 'SOLID')
            }
            
            if stroke.get('type') == 'SOLID' and 'color' in stroke:
                color = stroke['color']
                # Color might be a string (from parser) or dict (raw Figma)
                if isinstance(color, str):
                    simplified['color'] = color
                elif isinstance(color, dict):
                    simplified['color'] = {
                        'r': self._round_number(color.get('r', 0)),
                        'g': self._round_number(color.get('g', 0)),
                        'b': self._round_number(color.get('b', 0)),
                        'a': self._round_number(color.get('a', 1.0))
                    }
                else:
                    simplified['color'] = color

            
            filtered.append(simplified)
        
        return filtered
    
    def _simplify_bounds(self, bounds: Dict[str, Any]) -> Dict[str, Any]:
        """
        Round bounds values to reduce token usage
        
        Args:
            bounds: Bounds dictionary
            
        Returns:
            Simplified bounds
        """
        return {
            key: self._round_number(value)
            for key, value in bounds.items()
            if key in ('x', 'y', 'width', 'height')
        }
    
    def _round_number(self, value: float, decimals: int = 1) -> float:
        """
        Round numbers to reduce token usage
        
        Args:
            value: Number to round
            decimals: Number of decimal places
            
        Returns:
            Rounded number
        """
        if isinstance(value, int):
            return value
        
        # Round to specified decimal places
        rounded = round(value, decimals)
        
        # Return as int if it's a whole number
        if rounded == int(rounded):
            return int(rounded)
        
        return rounded
    
    def estimate_tokens(self, data: Dict[str, Any]) -> int:
        """
        Estimate token count for design data
        
        Args:
            data: Design data
            
        Returns:
            Approximate token count
        """
        # Convert to JSON string
        json_str = json.dumps(data, indent=2)
        
        # Rough estimate: ~4 characters per token
        return len(json_str) // 4
    
    def get_filtering_stats(
        self,
        original_data: Dict[str, Any],
        filtered_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Get statistics about filtering effectiveness
        
        Args:
            original_data: Original design data
            filtered_data: Filtered design data
            
        Returns:
            Dictionary with filtering statistics
        """
        original_tokens = self.estimate_tokens(original_data)
        filtered_tokens = self.estimate_tokens(filtered_data)
        reduction = ((original_tokens - filtered_tokens) / original_tokens * 100) if original_tokens > 0 else 0
        
        return {
            'original_tokens': original_tokens,
            'filtered_tokens': filtered_tokens,
            'tokens_saved': original_tokens - filtered_tokens,
            'reduction_percentage': round(reduction, 1),
            'filter_level': self.filter_level.value
        }
