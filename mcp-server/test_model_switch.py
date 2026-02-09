"""
Quick test to switch between different AI models
Usage: python3 test_model_switch.py gpt-5
       python3 test_model_switch.py claude-3-5-sonnet
       python3 test_model_switch.py gemini-pro
"""
import asyncio
import sys
import os
from dotenv import load_dotenv

# Load environment
load_dotenv()
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.ai.client import AIClient


async def test_model(model_name: str):
    """Test a specific model"""
    
    print("=" * 80)
    print(f"TESTING MODEL: {model_name}")
    print("=" * 80)
    
    try:
        # Override model from command line
        client = AIClient(model=model_name)
        
        print(f"\n✓ Initialized AI Client")
        print(f"  Model: {client.model}")
        print(f"  Endpoint: {client.base_url or 'Default OpenAI'}")
        
        # Test code generation
        print(f"\n⏳ Generating Flutter code with {model_name}...")
        
        result = await client.generate_code(
            prompt='Create a simple Flutter Text widget that says "Hello World"',
            system_prompt='You are a Flutter expert. Generate only code.',
            temperature=0.3,
            max_tokens=300
        )
        
        print(f"\n✅ SUCCESS! {model_name} is working!\n")
        print("Generated code:")
        print("-" * 80)
        print(result[:200] + ("..." if len(result) > 200 else ""))
        print("-" * 80)
        
        await client.close()
        
        print(f"\n✓ {model_name} configured successfully!")
        return 0
        
    except Exception as e:
        print(f"\n❌ ERROR with {model_name}: {e}")
        print("\nTroubleshooting:")
        print(f"1. Check if {model_name} is available on your LiteLLM proxy")
        print("2. Verify API key has access to this model")
        print("3. Check AI_BASE_URL is correct")
        return 1


async def test_multiple_models():
    """Test switching between multiple models"""
    
    print("\n" + "=" * 80)
    print("MULTI-MODEL TEST - Demonstrating LLM Agnostic Platform")
    print("=" * 80)
    
    models = [
        "gemini-pro",
        "gpt-4o", 
        "claude-3-5-sonnet"
    ]
    
    results = {}
    
    for model in models:
        print(f"\n\n{'='*80}")
        print(f"Testing: {model}")
        print('='*80)
        
        try:
            client = AIClient(model=model)
            result = await client.generate_code(
                prompt='Create a Flutter Container with red background',
                system_prompt='Generate only code.',
                max_tokens=200
            )
            results[model] = "✅ Working"
            print(f"✅ {model}: Working!")
            await client.close()
        except Exception as e:
            results[model] = f"❌ {str(e)[:50]}"
            print(f"❌ {model}: {e}")
    
    # Summary
    print("\n\n" + "=" * 80)
    print("MODEL COMPATIBILITY SUMMARY")
    print("=" * 80)
    for model, status in results.items():
        print(f"  {model:30} {status}")
    
    print("\n✓ Platform is LLM-agnostic - switch models anytime in .env!")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Test specific model from command line
        model = sys.argv[1]
        exit_code = asyncio.run(test_model(model))
        sys.exit(exit_code)
    else:
        # Test multiple models
        asyncio.run(test_multiple_models())
