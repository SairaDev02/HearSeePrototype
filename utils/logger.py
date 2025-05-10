"""
Logger utility for the HearSee application.

This module provides a convenient interface for logging throughout the application.
It includes functions for obtaining loggers, decorators for logging exceptions and
function calls, and convenience functions for common logging operations.

Functions:
    get_module_logger: Get a logger for a specific module
    log_exception: Decorator to log exceptions raised in a function
    log_function_call: Decorator to log function calls with arguments and return values
    debug, info, warning, error, critical, exception: Convenience logging functions
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
    
    If module_name is not provided, it will be automatically determined from the call stack,
    making it convenient to use without explicitly passing the module name.
    
    Args:
        module_name (str, optional): The name of the module. Defaults to None.
        
    Returns:
        logging.Logger: A configured logger instance with appropriate handlers and formatters.
        
    Example:
        >>> logger = get_module_logger()
        >>> logger.info("This is an info message")
    """
    if module_name is None:
        # Get the caller's module name by inspecting the call stack
        # This allows automatic module name detection without explicit passing
        frame = inspect.stack()[1]  # Get the frame of the caller
        module = inspect.getmodule(frame[0])  # Get the module object
        module_name = module.__name__ if module else "unknown"  # Extract module name or use "unknown"
    
    return get_logger(module_name)

def log_exception(logger=None, level=logging.ERROR, exc_info=True):
    """
    Decorator to log exceptions raised in a function.
    
    This decorator wraps a function to catch any exceptions it raises, log them
    with the specified logger and level, and then re-raise the exception.
    
    Args:
        logger (logging.Logger, optional): The logger to use. If None, a logger will be
                                          created based on the function's module.
        level (int, optional): The logging level for the exception. Defaults to logging.ERROR.
        exc_info (bool, optional): Whether to include exception traceback info. Defaults to True.
        
    Returns:
        function: The decorated function that will log exceptions when they occur.
        
    Example:
        >>> @log_exception()
        >>> def risky_function():
        >>>     # This will be logged if it raises an exception
        >>>     return 1/0
    """
    def decorator(func):
        # Get the module logger if not provided
        # This ensures we always have a logger even if none was passed
        nonlocal logger
        if logger is None:
            module = inspect.getmodule(func)
            logger = get_logger(module.__name__ if module else "unknown")
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                # Get function details for more informative logging
                func_name = func.__name__
                module_name = func.__module__
                
                # Log the exception with function context
                logger.log(
                    level,
                    f"Exception in {module_name}.{func_name}: {str(e)}",
                    exc_info=exc_info
                )
                
                # Re-raise the exception to maintain original behavior
                # This ensures the decorator doesn't swallow exceptions
                raise
        
        return wrapper
    
    return decorator

def log_function_call(logger=None, level=logging.DEBUG):
    """
    Decorator to log function calls with arguments and return values.
    
    This decorator logs when a function is called, what arguments it received,
    and what value it returned (or if it raised an exception). This is useful
    for debugging and tracing program execution.
    
    Args:
        logger (logging.Logger, optional): The logger to use. If None, a logger will be
                                          created based on the function's module.
        level (int, optional): The logging level. Defaults to logging.DEBUG.
        
    Returns:
        function: The decorated function that will log its calls and returns.
        
    Example:
        >>> @log_function_call()
        >>> def add(a, b):
        >>>     return a + b
        >>>
        >>> # When called, will log something like:
        >>> # "Calling add(1, 2)"
        >>> # "add returned 3"
    """
    def decorator(func):
        # Get the module logger if not provided
        # This ensures we always have a logger even if none was passed
        nonlocal logger
        if logger is None:
            module = inspect.getmodule(func)
            logger = get_logger(module.__name__ if module else "unknown")
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Create a readable representation of the function call
            func_name = func.__name__
            # Convert positional args to string representations
            args_repr = [repr(a) for a in args]
            # Convert keyword args to key=value string representations
            kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
            # Combine all arguments into a signature string
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
    """
    Log a debug message.
    
    Args:
        msg (str): The message to log
        *args: Variable length argument list passed to the logger
        **kwargs: Arbitrary keyword arguments passed to the logger
    """
    logger.debug(msg, *args, **kwargs)

def info(msg, *args, **kwargs):
    """
    Log an info message.
    
    Args:
        msg (str): The message to log
        *args: Variable length argument list passed to the logger
        **kwargs: Arbitrary keyword arguments passed to the logger
    """
    logger.info(msg, *args, **kwargs)

def warning(msg, *args, **kwargs):
    """
    Log a warning message.
    
    Args:
        msg (str): The message to log
        *args: Variable length argument list passed to the logger
        **kwargs: Arbitrary keyword arguments passed to the logger
    """
    logger.warning(msg, *args, **kwargs)

def error(msg, *args, **kwargs):
    """
    Log an error message.
    
    Args:
        msg (str): The message to log
        *args: Variable length argument list passed to the logger
        **kwargs: Arbitrary keyword arguments passed to the logger
    """
    logger.error(msg, *args, **kwargs)

def critical(msg, *args, **kwargs):
    """
    Log a critical message.
    
    Args:
        msg (str): The message to log
        *args: Variable length argument list passed to the logger
        **kwargs: Arbitrary keyword arguments passed to the logger
    """
    logger.critical(msg, *args, **kwargs)

def exception(msg, *args, **kwargs):
    """
    Log an exception message with traceback.
    
    This is a convenience function that ensures exc_info=True
    to include the exception traceback in the log.
    
    Args:
        msg (str): The message to log
        *args: Variable length argument list passed to the logger
        **kwargs: Arbitrary keyword arguments passed to the logger
    """
    kwargs['exc_info'] = True  # Always include exception info
    logger.error(msg, *args, **kwargs)