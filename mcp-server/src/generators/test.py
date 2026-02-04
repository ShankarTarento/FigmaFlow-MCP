"""
Widget Test Generator
Generates Flutter widget tests from widget code using AI
"""
from typing import Dict, Any
from ..ai.client import AIClient
from ..ai.prompts import (
    TEST_GENERATION_SYSTEM_PROMPT,
    TEST_GENERATION_USER_PROMPT_TEMPLATE
)


class TestGenerator:
    """Generates Flutter widget tests"""
    
    def __init__(self, ai_client: AIClient) -> None:
        """
        Initialize test generator
        
        Args:
            ai_client: AI client for test generation
        """
        self.ai_client = ai_client
    
    async def generate_widget_tests(
        self,
        widget_code: str,
        design_data: Dict[str, Any]
    ) -> str:
        """
        Generate widget tests from widget code
        
        Args:
            widget_code: Generated widget code
            design_data: Original design data for context
            
        Returns:
            Flutter test code as string
        """
        # Build user prompt
        user_prompt = TEST_GENERATION_USER_PROMPT_TEMPLATE.format(
            widget_code=widget_code
        )
        
        # Generate tests using AI
        test_code = await self.ai_client.generate_code(
            prompt=user_prompt,
            system_prompt=TEST_GENERATION_SYSTEM_PROMPT
        )
        
        # Clean and format test code
        test_code = self._clean_code(test_code)
        test_code = self._add_imports(test_code)
        
        return test_code
    
    def _clean_code(self, code: str) -> str:
        """
        Remove markdown code blocks and clean formatting
        
        Args:
            code: Raw generated test code
            
        Returns:
            Cleaned test code
        """
        # Remove markdown code fences
        code = code.replace("```dart", "").replace("```", "")
        
        # Remove extra whitespace
        code = code.strip()
        
        return code
    
    def _add_imports(self, code: str) -> str:
        """
        Add necessary test imports if not present
        
        Args:
            code: Test code
            
        Returns:
            Code with imports
        """
        required_imports = [
            "import 'package:flutter_test/flutter_test.dart';",
            "import 'package:flutter/material.dart';",
        ]
        
        for import_line in required_imports:
            if import_line not in code:
                code = f"{import_line}\n{code}"
        
        return code
