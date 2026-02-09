"""
QA Test Case Generator
Generates manual QA test cases from design data
"""
import json
from typing import Dict, Any
from ..ai.client import AIClient
from ..ai.prompts import (
    QA_TEST_GENERATION_SYSTEM_PROMPT,
    QA_TEST_GENERATION_USER_PROMPT_TEMPLATE
)
from ..utils.token_filter import TokenFilter, FilterLevel


class QATestGenerator:
    """Generates QA test cases for manual testing"""
    
    def __init__(self, ai_client: AIClient, filter_level: FilterLevel = FilterLevel.BALANCED) -> None:
        """
        Initialize QA test generator
        
        Args:
            ai_client: AI client for test case generation
            filter_level: Token filtering strategy
        """
        self.ai_client = ai_client
        self.token_filter = TokenFilter(filter_level)
    
    async def generate_test_cases(
        self,
        design_data: Dict[str, Any],
        widget_code: str
    ) -> str:
        """
        Generate QA test cases
        
        Args:
            design_data: Parsed design data
            widget_code: Generated widget code
            
        Returns:
            QA test cases as formatted text
        """
        # Apply token filtering to design data
        filtered_data = self.token_filter.filter_design_data(design_data, max_depth=3)
        
        # Create design description from filtered data
        design_description = self._create_design_description(filtered_data)
        
        # Build user prompt
        user_prompt = QA_TEST_GENERATION_USER_PROMPT_TEMPLATE.format(
            design_description=design_description,
            widget_code=widget_code
        )
        
        # Generate test cases
        test_cases = await self.ai_client.generate_code(
            prompt=user_prompt,
            system_prompt=QA_TEST_GENERATION_SYSTEM_PROMPT,
            temperature=0.5  # Slightly higher for more varied test cases
        )
        
        return test_cases.strip()
    
    def _create_design_description(self, design_data: Dict[str, Any]) -> str:
        """
        Create human-readable description of design
        
        Args:
            design_data: Parsed design data
            
        Returns:
            Description string
        """
        description_parts = [
            f"Component: {design_data.get('name', 'Unknown')}",
            f"Type: {design_data.get('type', 'Widget')}",
        ]
        
        # Add dimensions if available
        if "bounds" in design_data:
            bounds = design_data["bounds"]
            description_parts.append(
                f"Size: {bounds['width']}x{bounds['height']}"
            )
        
        # Add text content if present
        if "text" in design_data:
            description_parts.append(f"Text: '{design_data['text']}'")
        
        # Add children count
        if "children" in design_data:
            description_parts.append(
                f"Children: {len(design_data['children'])} elements"
            )
        
        return "\n".join(description_parts)
