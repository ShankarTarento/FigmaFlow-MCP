"""
Test LiteLLM configuration
"""
import asyncio
import sys
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.ai.client import AIClient


async def test_litellm():
    """Test connection to LiteLLM proxy"""
    
    print("=" * 80)
    print("TESTING LITELLM CONFIGURATION")
    print("=" * 80)
    
    try:
        # Initialize client (reads from .env)
        print("\n1. Initializing AI Client...")
        client = AIClient()
        print(f"   Model: {client.model}")
        print(f"   Base URL: {client.base_url or 'Default OpenAI'}")
        
        # Test simple code generation
        print("\n2. Testing code generation...")
        result = await client.generate_code(
            prompt='Create a simple Flutter Container widget with a blue background',
            system_prompt='You are a Flutter expert. Generate only code, no explanations.',
            temperature=0.3,
            max_tokens=500
        )
        
        print("\n✓ SUCCESS! LiteLLM connection is working.")
        print("\nGenerated code preview:")
        print("-" * 80)
        print(result[:300] + ("..." if len(result) > 300 else ""))
        print("-" * 80)
        
        await client.close()
        
        print("\n" + "=" * 80)
        print("✓ LITELLM CONFIGURED SUCCESSFULLY!")
        print("=" * 80)
        print("\nYou can now use FigmaFlow to generate widgets with gemini-pro.")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        print("\nTroubleshooting:")
        print("1. Check .env file has correct values")
        print("2. Verify AI_BASE_URL is accessible")
        print("3. Confirm AI_API_KEY is valid")
        return 1
    
    return 0


if __name__ == "__main__":
    exit_code = asyncio.run(test_litellm())
    sys.exit(exit_code)
