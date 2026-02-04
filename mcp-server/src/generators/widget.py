"""
Flutter Widget Generator
Generates Flutter widget code from Figma design data using AI
"""
import json
from typing import Dict, Any, Optional
from ..ai.client import AIClient
from ..ai.prompts import (
    WIDGET_GENERATION_SYSTEM_PROMPT,
    WIDGET_GENERATION_USER_PROMPT_TEMPLATE
)


class WidgetGenerator:
    """Generates Flutter widget code from design data"""
    
    def __init__(self, ai_client: AIClient) -> None:
        """
        Initialize widget generator
        
        Args:
            ai_client: AI client for code generation
        """
        self.ai_client = ai_client
    
    async def generate(
        self,
        design_data: Dict[str, Any],
        widget_name: str,
        options: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Generate Flutter widget code from design data
        
        Args:
            design_data: Parsed Figma design data
            widget_name: Name for the generated widget (PascalCase)
            options: Generation options (stateful, includeImports)
            
        Returns:
            Flutter widget code as string
        """
        options = options or {}
        
        # Format design data for prompt
        design_json = json.dumps(design_data, indent=2)
        
        # Build user prompt
        user_prompt = WIDGET_GENERATION_USER_PROMPT_TEMPLATE.format(
            widget_name=widget_name,
            design_json=design_json
        )
        
        # Generate code using AI
        code = await self.ai_client.generate_code(
            prompt=user_prompt,
            system_prompt=WIDGET_GENERATION_SYSTEM_PROMPT
        )
        
        # Post-process code
        code = self._clean_code(code)
        
        # Add imports if requested
        if options.get("includeImports", True):
            code = self._add_imports(code)
        
        return code
    
    def _clean_code(self, code: str) -> str:
        """
        Remove markdown code blocks and clean up formatting
        
        Args:
            code: Raw generated code
            
        Returns:
            Cleaned code
        """
        # Remove markdown code fences
        code = code.replace("```dart", "").replace("```", "")
        
        # Remove extra leading/trailing whitespace
        code = code.strip()
        
        return code
    
    def _add_imports(self, code: str) -> str:
        """
        Add necessary imports if not already present
        
        Args:
            code: Widget code
            
        Returns:
            Code with imports
        """
        required_imports = [
            "import 'package:flutter/material.dart';",
        ]
        
        # Check if imports are already present
        for import_line in required_imports:
            if import_line not in code:
                code = f"{import_line}\n\n{code}"
        
        return code
    
    def validate_widget_name(self, name: str) -> bool:
        """
        Validate widget name follows Flutter conventions
        
        Args:
            name: Widget name to validate
            
        Returns:
            True if valid, False otherwise
        """
        # Must be PascalCase and start with uppercase letter
        if not name:
            return False
        if not name[0].isupper():
            return False
        if not name.replace('_', '').isalnum():
            return False
        return True
