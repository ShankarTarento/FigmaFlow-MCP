"""
Custom exceptions for FigmaFlow
Provides user-friendly error messages and categorization
"""


class FigmaFlowError(Exception):
    """Base exception for FigmaFlow"""
    
    def __init__(self, user_message: str, technical_details: str = None):
        """
        Initialize FigmaFlow error
        
        Args:
            user_message: User-friendly message to display
            technical_details: Technical error details for logging
        """
        self.user_message = user_message
        self.technical_details = technical_details or user_message
        super().__init__(user_message)


class RateLimitError(FigmaFlowError):
    """Figma API rate limit exceeded"""
    
    def __init__(self, retry_after: int = 60, attempt: int = 1, max_attempts: int = 1):
        # Cap unreasonable wait times (Figma shouldn't rate limit for more than 5 minutes)
        if retry_after > 300:  # More than 5 minutes
            retry_after = 60  # Default to 1 minute
        
        # Format time in human-readable way
        if retry_after < 60:
            time_str = f"{retry_after} seconds"
        elif retry_after < 3600:
            minutes = retry_after // 60
            seconds = retry_after % 60
            if seconds > 0:
                time_str = f"{minutes} minute{'s' if minutes != 1 else ''} and {seconds} seconds"
            else:
                time_str = f"{minutes} minute{'s' if minutes != 1 else ''}"
        else:
            hours = retry_after // 3600
            remaining = retry_after % 3600
            minutes = remaining // 60
            time_str = f"{hours} hour{'s' if hours != 1 else ''}"
            if minutes > 0:
                time_str += f" and {minutes} minute{'s' if minutes != 1 else ''}"
        
        user_message = (
            f"⚠️ Figma API rate limit exceeded.\n"
            f"   Please wait {time_str} and try again.\n\n"
            f"   💡 Tip: Previously fetched designs are cached for 24 hours.\n"
            f"   If you've used this design before, try clearing and refetching."
        )
        super().__init__(user_message, f"Rate limit hit, retry after {retry_after}s")


class InvalidDesignError(FigmaFlowError):
    """Invalid or inaccessible Figma design"""
    
    def __init__(self, file_key: str, reason: str = None):
        user_message = (
            f"❌ Unable to access Figma design.\n"
            f"   Please check:\n"
            f"   • Design URL is correct\n"
            f"   • Design is not private\n"
            f"   • Your Figma token has access to this file"
        )
        technical = f"Failed to fetch {file_key}: {reason}" if reason else f"Invalid design: {file_key}"
        super().__init__(user_message, technical)


class ConfigurationError(FigmaFlowError):
    """Configuration is invalid or missing"""
    
    def __init__(self, missing_keys: list = None):
        if missing_keys:
            keys_str = ", ".join(missing_keys)
            user_message = (
                f"⚙️ Configuration incomplete.\n"
                f"   Missing: {keys_str}\n"
                f"   Please update your .env file."
            )
        else:
            user_message = "⚙️ Configuration error. Please check your .env file."
        
        super().__init__(user_message, f"Missing config: {missing_keys}")


class AIGenerationError(FigmaFlowError):
    """AI code generation failed"""
    
    def __init__(self, reason: str = None):
        user_message = (
            f"🤖 Failed to generate code.\n"
            f"   This may be due to:\n"
            f"   • AI service temporarily unavailable\n"
            f"   • Design too complex\n"
            f"   • Invalid API key\n"
            f"   Please try again in a moment."
        )
        super().__init__(user_message, reason or "AI generation failed")


def handle_error(error: Exception) -> str:
    """
    Convert any exception to user-friendly message
    
    Args:
        error: The exception to handle
        
    Returns:
        User-friendly error message
    """
    if isinstance(error, FigmaFlowError):
        return error.user_message
    
    # Handle HTTP errors
    error_str = str(error)
    if "429" in error_str or "Too Many Requests" in error_str:
        return RateLimitError().user_message
    
    if "403" in error_str or "Forbidden" in error_str:
        return InvalidDesignError("unknown", "Access forbidden").user_message
    
    if "404" in error_str or "Not Found" in error_str:
        return InvalidDesignError("unknown", "Design not found").user_message
    
    # Generic error
    return (
        f"❌ An unexpected error occurred.\n"
        f"   {str(error)[:100]}\n"
        f"   Please try again or contact support."
    )
