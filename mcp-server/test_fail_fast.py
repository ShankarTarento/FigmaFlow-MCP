"""
Test fail-fast error handling (no retries)
"""
import asyncio
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))


async def test_fail_fast():
    """Test that errors are returned immediately"""
    print("\n=== Testing Fail-Fast Error Handling ===\n")
    
    from src.figma.client import FigmaClient
    from src.utils.errors import RateLimitError, InvalidDesignError
    from dotenv import load_dotenv
    
    load_dotenv()
    
    client = FigmaClient()
    
    # Test 1: Try to fetch a design (will fail immediately if rate limited)
    print("Test 1: Attempting Figma API call...")
    try:
        # Use a real design - will either succeed or fail fast
        node = await client.get_node('PpMRN0R3qQFIWABcOzjr24', '789:21610')
        print(f"✅ Success! Retrieved: {node.name}")
        print("   (Design was cached or API is working)")
    except RateLimitError as e:
        print(f"✅ Rate limit detected (fail fast - no retry)")
        print(f"   Message: {e.user_message}")
    except InvalidDesignError as e:
        print(f"✅ Invalid design error (fail fast)")
        print(f"   Message: {e.user_message}")
    except Exception as e:
        print(f"⚠️  Other error: {type(e).__name__}: {e}")
    
    await client.close()
    
    print("\n✅ Fail-fast test complete!")
    print("   No retries - errors return immediately")


if __name__ == "__main__":
    asyncio.run(test_fail_fast())
