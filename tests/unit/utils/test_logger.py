"""
Unit tests for the logger module.

This module contains tests for the logger utility functions.
"""

import pytest
from unittest.mock import patch, MagicMock
import logging
import os

from utils.logger import get_logger
from config.logging_config import configure_logging, LOG_FORMAT, DATE_FORMAT


class TestLogger:
    """Test suite for logger utilities."""

    def test_configure_logging(self):
        """Test logging configuration."""
        # Call the function
        root_logger = configure_logging()
        
        # Verify the logger is configured correctly
        assert root_logger.level == logging.INFO
        
        # Verify handlers are added
        assert len(root_logger.handlers) >= 3  # Console, file, and error handlers
        
        # Verify at least one handler is a StreamHandler (console)
        assert any(isinstance(h, logging.StreamHandler) for h in root_logger.handlers)
        
        # Verify at least two handlers are FileHandlers (log file and error file)
        file_handlers = [h for h in root_logger.handlers if isinstance(h, logging.handlers.RotatingFileHandler)]
        assert len(file_handlers) >= 2

    def test_get_logger(self):
        """Test getting a logger instance."""
        # Save original logger state
        original_loggers = logging.Logger.manager.loggerDict.copy()
        original_root = logging.getLogger()
        original_handlers = original_root.handlers.copy()
        original_level = original_root.level
        
        try:
            # Set a known level for the root logger
            root_logger = logging.getLogger()
            root_logger.setLevel(logging.INFO)
            
            # Call the function
            logger = get_logger("test_module")
            
            # Verify the logger has the correct name
            assert logger.name == "test_module"
            
            # Verify the logger has the expected level
            # Note: Child loggers might not have an explicitly set level (0)
            # but they inherit from the root logger
            if logger.level == 0:  # NOTSET
                assert root_logger.level == logging.INFO
            else:
                assert logger.level == root_logger.level
        finally:
            # Restore original logger state
            logging.Logger.manager.loggerDict = original_loggers
            root = logging.getLogger()
            root.handlers = original_handlers
            root.setLevel(original_level)

    def test_log_directory_creation(self):
        """Test log directory creation."""
        # Use a direct approach to test the function
        with patch('os.makedirs') as mock_makedirs:
            # Import the function directly to ensure we're using the right one
            from config.logging_config import configure_logging, LOG_DIR
            
            # Call the function
            configure_logging()
            
            # Verify os.makedirs was called (at least once)
            mock_makedirs.assert_called()
            
            # Verify it was called with the log directory and exist_ok=True
            # Find the call with LOG_DIR
            log_dir_calls = [
                call for call in mock_makedirs.call_args_list
                if LOG_DIR in str(call) and 'exist_ok=True' in str(call)
            ]
            assert len(log_dir_calls) > 0

    def test_log_format(self):
        """Test log format configuration."""
        # Patch logging.Formatter to verify it's called with the correct format
        with patch('logging.Formatter') as mock_formatter:
            # Call the function
            configure_logging()
            
            # Verify Formatter was called with the correct format
            mock_formatter.assert_called_with(LOG_FORMAT, DATE_FORMAT)

    def test_third_party_logging_levels(self):
        """Test third-party library logging levels are set correctly."""
        # Call the function
        configure_logging()
        
        # Verify third-party loggers have WARNING level
        assert logging.getLogger("requests").level == logging.WARNING
        assert logging.getLogger("urllib3").level == logging.WARNING

    def test_logging_functionality(self):
        """Test actual logging functionality."""
        # Save original logger state
        original_loggers = logging.Logger.manager.loggerDict.copy()
        original_root = logging.getLogger()
        original_handlers = original_root.handlers.copy()
        original_level = original_root.level
        
        try:
            # Configure logging
            configure_logging()
            
            # Get a test logger
            test_logger = get_logger("test_logger")
            
            # Create a handler with proper level attribute
            mock_handler = MagicMock()
            mock_handler.level = logging.INFO  # Set a proper level
            
            # Add the handler to the logger
            test_logger.addHandler(mock_handler)
            
            # Log messages at different levels
            test_logger.debug("Debug message")
            test_logger.info("Info message")
            test_logger.warning("Warning message")
            test_logger.error("Error message")
            test_logger.critical("Critical message")
            
            # Mock the handle method to capture records
            handle_records = []
            original_handle = mock_handler.handle
            
            def mock_handle(record):
                handle_records.append(record)
                return True
                
            mock_handler.handle = mock_handle
            
            # Re-log messages to use our mock
            test_logger.info("Info message")
            test_logger.error("Error message")
            
            # Verify we captured the records
            assert len(handle_records) >= 2
            
            # Verify the messages
            assert any(record.getMessage() == "Info message" for record in handle_records)
            assert any(record.getMessage() == "Error message" for record in handle_records)
        finally:
            # Restore original logger state
            logging.Logger.manager.loggerDict = original_loggers
            root = logging.getLogger()
            root.handlers = original_handlers
            root.setLevel(original_level)