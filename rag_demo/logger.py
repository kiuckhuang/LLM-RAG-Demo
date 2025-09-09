import logging
import sys
from .config import Config

def setup_logger():
    """Set up logger based on configuration"""
    if not Config.ENABLE_LOGGING:
        # Return a null logger that doesn't output anything
        logger = logging.getLogger("rag_demo_null")
        logger.addHandler(logging.NullHandler())
        return logger
    
    # Create logger
    logger = logging.getLogger("rag_demo")
    logger.setLevel(getattr(logging, Config.LOG_LEVEL.upper()))
    
    # Prevent adding multiple handlers if logger already exists
    if logger.handlers:
        return logger
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, Config.LOG_LEVEL.upper()))
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(formatter)
    
    # Add handler to logger
    logger.addHandler(console_handler)
    
    return logger

def debug_log(logger, message):
    """Log debug message if debug mode is enabled"""
    if Config.DEBUG_MODE:
        logger.debug(message)

# Initialize logger
logger = setup_logger()
