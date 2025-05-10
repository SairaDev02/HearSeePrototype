"""
Logging configuration for the HearSee application.

This module provides a centralized configuration for the application's logging system.
It sets up console and file-based logging with rotation capabilities, configures
formatting, and provides utility functions to obtain properly configured loggers.

Constants:
    LOG_DIR (str): Directory where log files are stored
    APP_LOG_FILE (str): Path to the main application log file
    ERROR_LOG_FILE (str): Path to the error-only log file
    LOG_FORMAT (str): Format string for log messages
    DATE_FORMAT (str): Format string for timestamps in log messages
    DEFAULT_LOG_LEVEL (int): Default logging level (INFO)
"""

import os
import logging
from logging.handlers import RotatingFileHandler
import sys

# Define log directory - navigates up from config dir to project root, then to logs
LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs")

# Create logs directory if it doesn't exist - prevents FileNotFoundError on first run
os.makedirs(LOG_DIR, exist_ok=True)

# Log file paths for main application logs and error-specific logs
APP_LOG_FILE = os.path.join(LOG_DIR, "app.log")
ERROR_LOG_FILE = os.path.join(LOG_DIR, "error.log")

# Standard log format with timestamp, logger name, level, and message
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# Default logging level - INFO captures normal operational messages but not debug details
DEFAULT_LOG_LEVEL = logging.INFO

def configure_logging():
    """
    Configure the logging system for the application.
    
    Sets up the root logger with three handlers:
    1. Console handler (stdout) for all logs at DEFAULT_LOG_LEVEL
    2. File handler for all logs at DEFAULT_LOG_LEVEL with rotation
    3. File handler for ERROR level logs only with rotation
    
    Also configures third-party libraries to log at WARNING level to reduce noise.
    
    Returns:
        logging.Logger: The configured root logger instance.
        
    Example:
        >>> logger = configure_logging()
        >>> logger.info("Application started")
    """
    # Create formatter with the defined format and date format
    formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)
    
    # Get and configure the root logger - affects all loggers in the application
    root_logger = logging.getLogger()
    root_logger.setLevel(DEFAULT_LOG_LEVEL)
    
    # Clear any existing handlers to prevent duplicate logs when called multiple times
    if root_logger.handlers:
        root_logger.handlers.clear()
    
    # Console handler outputs to stdout for immediate visibility during development
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(DEFAULT_LOG_LEVEL)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # File handler for all logs with 10MB size limit and 5 backup files
    # This creates app.log, app.log.1, app.log.2, etc. as files rotate
    file_handler = RotatingFileHandler(
        APP_LOG_FILE,
        maxBytes=10*1024*1024,  # 10MB size limit before rotation
        backupCount=5           # Keep 5 backup files
    )
    file_handler.setLevel(DEFAULT_LOG_LEVEL)
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)
    
    # Separate file handler for errors only - helps with quick error diagnosis
    error_file_handler = RotatingFileHandler(
        ERROR_LOG_FILE,
        maxBytes=10*1024*1024,  # 10MB size limit before rotation
        backupCount=5           # Keep 5 backup files
    )
    error_file_handler.setLevel(logging.ERROR)  # Only capture ERROR and CRITICAL
    error_file_handler.setFormatter(formatter)
    root_logger.addHandler(error_file_handler)
    
    # Reduce noise from commonly verbose third-party libraries
    # Only show their WARNING, ERROR, and CRITICAL messages
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    
    return root_logger

def get_logger(name):
    """
    Get a logger with the specified name.
    
    This function returns a logger that inherits the configuration from the root logger.
    It's recommended to use this function with __name__ as the parameter to create
    module-specific loggers.
    
    Args:
        name (str): The name of the logger, typically __name__ of the module.
        
    Returns:
        logging.Logger: A configured logger instance.
        
    Raises:
        TypeError: If name is not a string.
        
    Example:
        >>> logger = get_logger(__name__)
        >>> logger.info("Function X completed successfully")
    """
    if not isinstance(name, str):
        raise TypeError("Logger name must be a string")
    return logging.getLogger(name)