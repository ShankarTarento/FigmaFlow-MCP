"""
Configuration validation for FigmaFlow
Validates environment configuration on startup
"""
import os
from typing import List, Tuple
from dotenv import load_dotenv


class ConfigValidator:
    """Validates FigmaFlow configuration"""
    
    @staticmethod
    def validate() -> Tuple[bool, List[str], List[str]]:
        """
        Validate configuration
        
        Returns:
            Tuple of (is_valid, errors, warnings)
        """
        load_dotenv()
        
        errors = []
        warnings = []
        
        # Required: Figma token
        figma_token = os.getenv("FIGMA_ACCESS_TOKEN")
        if not figma_token:
            errors.append("FIGMA_ACCESS_TOKEN is required")
        elif not figma_token.startswith("figd_"):
            warnings.append("FIGMA_ACCESS_TOKEN may be invalid (should start with 'figd_')")
        
        # Required: AI API key (either format)
        ai_key = os.getenv("AI_API_KEY") or os.getenv("OPENAI_API_KEY")
        if not ai_key:
            errors.append("AI_API_KEY or OPENAI_API_KEY is required")
        
        # Optional but recommended
        if not os.getenv("AI_BASE_URL"):
            warnings.append("AI_BASE_URL not set - using direct OpenAI endpoint")
        
        if not os.getenv("AI_MODEL"):
            warnings.append("AI_MODEL not set - using default (gpt-4o)")
        
        # Cache configuration
        cache_ttl = os.getenv("FIGMA_CACHE_TTL_HOURS")
        if cache_ttl and not cache_ttl.isdigit():
            warnings.append(f"FIGMA_CACHE_TTL_HOURS should be a number, got: {cache_ttl}")
        
        return (len(errors) == 0, errors, warnings)
    
    @staticmethod
    def validate_and_report():
        """
        Validate and print results
        Exits if validation fails
        """
        is_valid, errors, warnings = ConfigValidator.validate()
        
        if warnings:
            print("⚠️  Configuration warnings:")
            for warning in warnings:
                print(f"   • {warning}")
            print()
        
        if errors:
            print("❌ Configuration errors:")
            for error in errors:
                print(f"   • {error}")
            print("\nPlease update your .env file and try again.")
            print("See .env.example for reference.\n")
            raise SystemExit(1)
        
        print("✓ Configuration validated successfully")
        return True
