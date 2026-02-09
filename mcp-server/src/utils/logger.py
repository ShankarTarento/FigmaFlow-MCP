"""
Structured logging for FigmaFlow
Provides consistent logging across all components
"""
import logging
import os
import sys
from datetime import datetime


def setup_logger(name: str) -> logging.Logger:
    """
    Setup structured logger
    
    Args:
        name: Logger name (usually __name__)
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    
    # Get log level from environment
    level_name = os.getenv("LOG_LEVEL", "INFO").upper()
    level = getattr(logging, level_name, logging.INFO)
    logger.setLevel(level)
    
    # Avoid duplicate handlers
    if logger.handlers:
        return logger
    
    # Console handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)
    
    # Format with timestamp and level
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler.setFormatter(formatter)
    
    logger.addHandler(handler)
    
    return logger


# Convenience function for quick logging
def log_info(message: str, logger_name: str = "figmaflow"):
    """Quick info log"""
    logger = setup_logger(logger_name)
    logger.info(message)


def log_warning(message: str, logger_name: str = "figmaflow"):
    """Quick warning log"""
    logger = setup_logger(logger_name)
    logger.warning(message)


def log_error(message: str, logger_name: str = "figmaflow", exc_info: bool = False):
    """Quick error log"""
    logger = setup_logger(logger_name)
    logger.error(message, exc_info=exc_info)
