"""
Logger utility for the HearSee application.
This module provides a convenient interface for logging throughout the application.
"""

import logging
import inspect
import os
from functools import wraps
import traceback

from config.logging_config import get_logger

def get_module_logger(module_name=None):
    """
    Get a logger for the specified module.
    If module_name is not provided, it will be determined from the call stack.
    
    Args:
        module_name (str, optional): The name of the module. Defaults to None.
        
    Returns:
        logging.Logger: A configured logger instance.
    """
    if module_name is None:
        # Get the caller's module name
        frame = inspect.stack()[1]
        module = inspect.getmodule(frame[0])
        module_name = module.__name__ if module else "unknown"
    
    return get_logger(module_name)

def log_exception(logger=None, level=logging.ERROR, exc_info=True):
    """
    Decorator to log exceptions raised in a function.
    
    Args:
        logger (logging.Logger, optional): The logger to use. If None, a logger will be created.
        level (int, optional): The logging level for the exception. Defaults to logging.ERROR.
        exc_info (bool, optional): Whether to include exception info. Defaults to True.
        
    Returns:
        function: The decorated function.
    """
    def decorator(func):
        # Get the module logger if not provided
        nonlocal logger
        if logger is None:
            module = inspect.getmodule(func)
            logger = get_logger(module.__name__ if module else "unknown")
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                # Get function details
                func_name = func.__name__
                module_name = func.__module__
                
                # Log the exception
                logger.log(
                    level,
                    f"Exception in {module_name}.{func_name}: {str(e)}",
                    exc_info=exc_info
                )
                
                # Re-raise the exception
                raise
        
        return wrapper
    
    return decorator

def log_function_call(logger=None, level=logging.DEBUG):
    """
    Decorator to log function calls with arguments and return values.
    
    Args:
        logger (logging.Logger, optional): The logger to use. If None, a logger will be created.
        level (int, optional): The logging level. Defaults to logging.DEBUG.
        
    Returns:
        function: The decorated function.
    """
    def decorator(func):
        # Get the module logger if not provided
        nonlocal logger
        if logger is None:
            module = inspect.getmodule(func)
            logger = get_logger(module.__name__ if module else "unknown")
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            func_name = func.__name__
            args_repr = [repr(a) for a in args]
            kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
            signature = ", ".join(args_repr + kwargs_repr)
            
            logger.log(level, f"Calling {func_name}({signature})")
            
            try:
                result = func(*args, **kwargs)
                logger.log(level, f"{func_name} returned {result!r}")
                return result
            except Exception as e:
                logger.log(logging.ERROR, f"{func_name} raised {e!r}")
                raise
        
        return wrapper
    
    return decorator

# Create module-level logger
logger = get_module_logger(__name__)

# Export common logging functions at module level for convenience
def debug(msg, *args, **kwargs):
    """Log a debug message."""
    logger.debug(msg, *args, **kwargs)

def info(msg, *args, **kwargs):
    """Log an info message."""
    logger.info(msg, *args, **kwargs)

def warning(msg, *args, **kwargs):
    """Log a warning message."""
    logger.warning(msg, *args, **kwargs)

def error(msg, *args, **kwargs):
    """Log an error message."""
    logger.error(msg, *args, **kwargs)

def critical(msg, *args, **kwargs):
    """Log a critical message."""
    logger.critical(msg, *args, **kwargs)

def exception(msg, *args, **kwargs):
    """Log an exception message with traceback."""
    kwargs['exc_info'] = True
    logger.error(msg, *args, **kwargs)