"""
AI Client for code generation
Handles communication with OpenAI API
"""
import os
from typing import Optional
from openai import AsyncOpenAI


class AIClient:
    """Client for AI model interactions"""
    
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None) -> None:
        """
        Initialize AI client
        
        Args:
            api_key: OpenAI API key (defaults to env var)
            model: Model to use (defaults to env var or gpt-4o)
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model or os.getenv("AI_MODEL", "gpt-4o")
        
        if not self.api_key:
            raise ValueError("OpenAI API key not found. Set OPENAI_API_KEY environment variable.")
        
        self.client = AsyncOpenAI(api_key=self.api_key)
        self.temperature = float(os.getenv("AI_TEMPERATURE", "0.3"))
        self.max_tokens = int(os.getenv("AI_MAX_TOKENS", "2000"))
    
    async def generate_code(
        self,
        prompt: str,
        system_prompt: str,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> str:
        """
        Generate code using AI model
        
        Args:
            prompt: User prompt with specific requirements
            system_prompt: System prompt defining behavior
            temperature: Generation temperature (0-2)
            max_tokens: Maximum tokens to generate
            
        Returns:
            Generated code as string
        """
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature or self.temperature,
            max_tokens=max_tokens or self.max_tokens
        )
        
        return response.choices[0].message.content or ""
    
    async def close(self) -> None:
        """Close the client connection"""
        await self.client.close()
