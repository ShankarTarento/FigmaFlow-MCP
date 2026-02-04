"""
Input Validation Utilities
"""
import re
from typing import Optional, Tuple


def validate_figma_url(url: str) -> Tuple[bool, Optional[str]]:
    """
    Validate Figma URL format
    
    Args:
        url: URL to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not url:
        return False, "URL cannot be empty"
    
    if "figma.com" not in url:
        return False, "URL must be a Figma link"
    
    if "/file/" not in url:
        return False, "URL must be a Figma file link"
    
    # Check if file key can be extracted
    file_match = re.search(r'/file/([A-Za-z0-9]+)', url)
    if not file_match:
        return False, "Invalid Figma file URL format"
    
    return True, None


def validate_widget_name(name: str) -> Tuple[bool, Optional[str]]:
    """
    Validate Flutter widget name
    
    Args:
        name: Widget name to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not name:
        return False, "Widget name cannot be empty"
    
    if not name[0].isupper():
        return False, "Widget name must start with an uppercase letter (PascalCase)"
    
    if not name.replace('_', '').isalnum():
        return False, "Widget name must contain only letters, numbers, and underscores"
    
    if len(name) > 50:
        return False, "Widget name is too long (max 50 characters)"
    
    # Check for reserved Dart keywords
    reserved = ['class', 'void', 'return', 'if', 'else', 'for', 'while', 'do', 
                'switch', 'case', 'break', 'continue', 'default', 'new', 'this']
    if name.lower() in reserved:
        return False, f"'{name}' is a reserved Dart keyword"
    
    return True, None


def validate_api_token(token: str, token_type: str = "figma") -> Tuple[bool, Optional[str]]:
    """
    Validate API token format
    
    Args:
        token: Token to validate
        token_type: Type of token ('figma' or 'openai')
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not token:
        return False, f"{token_type.title()} token cannot be empty"
    
    if token_type == "figma":
        if not token.startswith("figd_"):
            return False, "Figma tokens typically start with 'figd_'"
        if len(token) < 20:
            return False, "Figma token appears to be too short"
    
    elif token_type == "openai":
        if not token.startswith("sk-"):
            return False, "OpenAI tokens typically start with 'sk-'"
        if len(token) < 20:
            return False, "OpenAI token appears to be too short"
    
    return True, None
