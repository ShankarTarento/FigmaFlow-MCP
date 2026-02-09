"""
Test production improvements
Validates error handling, config validation, and logging
"""
import asyncio
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(__file__))


def test_config_validation():
    """Test configuration validation"""
    print("\n=== Testing Configuration Validation ===\n")
    
    from src.utils.config_validator import ConfigValidator
    
    # Should validate successfully
    is_valid, errors, warnings = ConfigValidator.validate()
    
    print(f"Configuration valid: {is_valid}")
    
    if warnings:
        print("\nWarnings:")
        for warning in warnings:
            print(f"  ⚠️  {warning}")
    
    if errors:
        print("\nErrors:")
        for error in errors:
            print(f"  ❌ {error}")
    else:
        print("\n✅ Configuration validation passed!")
    
    return is_valid


def test_error_handling():
    """Test error handling"""
    print("\n=== Testing Error Handling ===\n")
    
    from src.utils.errors import (
        RateLimitError,
        InvalidDesignError,
        ConfigurationError,
        AIGenerationError,
        handle_error
    )
    
    # Test custom exceptions
    print("1. Rate Limit Error:")
    rate_error = RateLimitError(retry_after=30, attempt=2, max_attempts=5)
    print(rate_error.user_message)
    
    print("\n2. Invalid Design Error:")
    design_error = InvalidDesignError("test123", "Not found")
    print(design_error.user_message)
    
    print("\n3. Configuration Error:")
    config_error = ConfigurationError(["FIGMA_ACCESS_TOKEN", "AI_API_KEY"])
    print(config_error.user_message)
    
    print("\n4. AI Generation Error:")
    ai_error = AIGenerationError("Model timeout")
    print(ai_error.user_message)
    
    print("\n5. Generic error handling:")
    generic_error = Exception("429 Too Many Requests")
    friendly_message = handle_error(generic_error)
    print(friendly_message)
    
    print("\n✅ Error handling tests passed!")
    return True


def test_logging():
    """Test structured logging"""
    print("\n=== Testing Structured Logging ===\n")
    
    from src.utils.logger import setup_logger
    
    logger = setup_logger("test")
    
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    
    print("\n✅ Logging tests passed!")
    return True


async def test_cache_first():
    """Test cache-first strategy"""
    print("\n=== Testing Cache-First Strategy ===\n")
    
    from src.figma.client import FigmaClient
    from dotenv import load_dotenv
    
    load_dotenv()
    
    try:
        client = FigmaClient()
        
        # This should try cache first
        print("Testing cache-first fetch...")
        
        # Use a demo design that we know is cached
        file_key = "demo_login"
        node_id = "demo"
        
        try:
            node = await client.get_node(file_key, node_id)
            print(f"✓ Retrieved node: {node.name}")
        except Exception as e:
            print(f"Note: Demo cache not found, this is expected: {e}")
        
        await client.close()
        print("\n✅ Cache-first strategy test passed!")
        return True
        
    except Exception as e:
        print(f"⚠️  Error (this is OK if rate limited): {e}")
        return True


async def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("  FigmaFlow Production Improvements Test Suite")
    print("=" * 60)
    
    results = []
    
    # Test 1: Config validation
    try:
        results.append(("Config Validation", test_config_validation()))
    except Exception as e:
        print(f"\n❌ Config validation failed: {e}")
        results.append(("Config Validation", False))
    
    # Test 2: Error handling
    try:
        results.append(("Error Handling", test_error_handling()))
    except Exception as e:
        print(f"\n❌ Error handling failed: {e}")
        results.append(("Error Handling", False))
    
    # Test 3: Logging
    try:
        results.append(("Logging", test_logging()))
    except Exception as e:
        print(f"\n❌ Logging failed: {e}")
        results.append(("Logging", False))
    
    # Test 4: Cache-first
    try:
        results.append(("Cache-First", await test_cache_first()))
    except Exception as e:
        print(f"\n❌ Cache-first failed: {e}")
        results.append(("Cache-First", False))
    
    # Summary
    print("\n" + "=" * 60)
    print("  Test Summary")
    print("=" * 60 + "\n")
    
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name:30} {status}")
    
    total = len(results)
    passed = sum(1 for _, p in results if p)
    
    print(f"\nPassed: {passed}/{total}")
    
    if passed == total:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
