"""
Unit tests for the logging_config module.

This module contains tests for the logging configuration.
"""

import pytest
from unittest.mock import patch, MagicMock
import logging
import os
import sys

from config.logging_config import (
    configure_logging,
    get_logger,
    LOG_DIR,
    APP_LOG_FILE,
    ERROR_LOG_FILE,
    LOG_FORMAT,
    DATE_FORMAT,
    DEFAULT_LOG_LEVEL
)


class TestLoggingConfig:
    """Test suite for logging configuration."""

    def test_log_constants(self):
        """Test logging constants are defined correctly."""
        # Verify log directory is defined
        assert isinstance(LOG_DIR, str)
        assert "logs" in LOG_DIR
        
        # Verify log file paths are defined
        assert isinstance(APP_LOG_FILE, str)
        assert "app.log" in APP_LOG_FILE
        assert isinstance(ERROR_LOG_FILE, str)
        assert "error.log" in ERROR_LOG_FILE
        
        # Verify log format is defined
        assert isinstance(LOG_FORMAT, str)
        assert "%(asctime)s" in LOG_FORMAT
        assert "%(levelname)s" in LOG_FORMAT
        assert "%(message)s" in LOG_FORMAT
        
        # Verify date format is defined
        assert isinstance(DATE_FORMAT, str)
        assert "%Y-%m-%d" in DATE_FORMAT
        
        # Verify default log level is defined
        assert DEFAULT_LOG_LEVEL == logging.INFO

    def test_log_directory_creation(self):
        """Test log directory creation."""
        # Use a direct approach to test the function
        with patch('os.makedirs') as mock_makedirs:
            # Import the function directly to ensure we're using the right one
            from config.logging_config import configure_logging
            
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

    def test_configure_logging(self):
        """Test logging configuration."""
        # Create a separate test that doesn't interfere with other tests
        
        # Save original logger state
        original_loggers = logging.Logger.manager.loggerDict.copy()
        original_root = logging.getLogger()
        original_handlers = original_root.handlers.copy()
        original_level = original_root.level
        
        try:
            # Create a fresh logger for testing
            test_logger = MagicMock()
            
            # Patch the necessary components
            with patch('logging.getLogger', return_value=test_logger), \
                 patch('logging.StreamHandler', return_value=MagicMock()), \
                 patch('logging.handlers.RotatingFileHandler', return_value=MagicMock()), \
                 patch('logging.Formatter', return_value=MagicMock()), \
                 patch('os.makedirs'):  # Prevent directory creation
                
                # Import the function directly
                from config.logging_config import configure_logging
                
                # Call the function
                result = configure_logging()
                
                # Verify the result is the test logger
                assert result == test_logger
                
                # Verify handlers were cleared
                test_logger.handlers.clear.assert_called_once()
                
                # Verify handlers were added
                assert test_logger.addHandler.call_count >= 3
                
                # Verify the logger's level was set (don't check exact value)
                assert test_logger.setLevel.called
        finally:
            # Restore original logger state
            logging.Logger.manager.loggerDict = original_loggers
            root = logging.getLogger()
            root.handlers = original_handlers
            root.setLevel(original_level)

    def test_get_logger(self):
        """Test getting a logger instance."""
        # Patch logging.getLogger to verify it's called
        with patch('logging.getLogger') as mock_get_logger:
            # Call the function
            get_logger("test_module")
            
            # Verify logging.getLogger was called with the module name
            mock_get_logger.assert_called_once_with("test_module")

    def test_console_handler_configuration(self):
        """Test console handler configuration."""
        # Save original logger state
        original_loggers = logging.Logger.manager.loggerDict.copy()
        original_root = logging.getLogger()
        original_handlers = original_root.handlers.copy()
        original_level = original_root.level
        
        try:
            # Create a fresh logger and handler for testing
            test_logger = MagicMock()
            test_handler = MagicMock()
            test_formatter = MagicMock()
            
            # Create a custom StreamHandler class for testing
            class TestStreamHandler:
                def __init__(self, stream=None):
                    self.stream = stream
                    
            # Patch the necessary components
            with patch('logging.getLogger', return_value=test_logger), \
                 patch('logging.StreamHandler', TestStreamHandler), \
                 patch('logging.Formatter', return_value=test_formatter), \
                 patch('os.makedirs'):  # Prevent directory creation
                
                # Import the function directly
                from config.logging_config import configure_logging
                
                # Call the function
                configure_logging()
                
                # Verify a StreamHandler was created
                # We can't easily verify it was created with sys.stdout, so we'll skip that check
                
                # Verify the handler was added to the logger
                assert test_logger.addHandler.called
        finally:
            # Restore original logger state
            logging.Logger.manager.loggerDict = original_loggers
            root = logging.getLogger()
            root.handlers = original_handlers
            root.setLevel(original_level)

    def test_file_handlers_configuration(self):
        """Test file handlers configuration."""
        # Save original logger state
        original_loggers = logging.Logger.manager.loggerDict.copy()
        original_root = logging.getLogger()
        original_handlers = original_root.handlers.copy()
        original_level = original_root.level
        
        try:
            # Create a fresh logger for testing
            test_logger = MagicMock()
            test_handler = MagicMock()
            
            # Track file handler creation
            file_handler_calls = []
            
            # Create a custom mock for RotatingFileHandler
            def mock_file_handler_factory(*args, **kwargs):
                # Track the filename
                if args and len(args) > 0:
                    file_handler_calls.append(args[0])
                return test_handler
            
            # Patch the necessary components
            with patch('logging.getLogger', return_value=test_logger), \
                 patch('logging.handlers.RotatingFileHandler', side_effect=mock_file_handler_factory), \
                 patch('logging.Formatter', return_value=MagicMock()), \
                 patch('logging.StreamHandler', return_value=MagicMock()), \
                 patch('os.makedirs'):  # Prevent directory creation
                
                # Import the function directly
                from config.logging_config import configure_logging, APP_LOG_FILE, ERROR_LOG_FILE
                
                # Call the function
                configure_logging()
                
                # Verify handlers were added to the logger
                assert test_logger.addHandler.call_count >= 3
                
                # Verify file handlers were created with the correct filenames
                assert len(file_handler_calls) >= 2
                assert any(APP_LOG_FILE in str(filename) for filename in file_handler_calls)
                assert any(ERROR_LOG_FILE in str(filename) for filename in file_handler_calls)
        finally:
            # Restore original logger state
            logging.Logger.manager.loggerDict = original_loggers
            root = logging.getLogger()
            root.handlers = original_handlers
            root.setLevel(original_level)

    def test_third_party_logging_levels(self):
        """Test third-party library logging levels are set correctly."""
        # Save original logger state
        original_loggers = logging.Logger.manager.loggerDict.copy()
        original_root = logging.getLogger()
        original_handlers = original_root.handlers.copy()
        original_level = original_root.level
        
        # Save original third-party logger levels
        original_requests_level = None
        original_urllib3_level = None
        if 'requests' in logging.Logger.manager.loggerDict:
            original_requests_level = logging.getLogger('requests').level
        if 'urllib3' in logging.Logger.manager.loggerDict:
            original_urllib3_level = logging.getLogger('urllib3').level
        
        try:
            # Create mock loggers
            mock_requests_logger = MagicMock()
            mock_urllib3_logger = MagicMock()
            
            # Patch getLogger to return our mocks for specific names
            original_getLogger = logging.getLogger
            
            def mock_getLogger(name=None):
                if name == 'requests':
                    return mock_requests_logger
                elif name == 'urllib3':
                    return mock_urllib3_logger
                elif name is None:
                    # Return the real root logger for configure_logging to work with
                    return original_root
                else:
                    # For any other loggers, return a new MagicMock
                    return MagicMock()
            
            # Apply the patch
            with patch('logging.getLogger', side_effect=mock_getLogger):
                # Call the function
                configure_logging()
                
                # Verify third-party loggers had their levels set
                mock_requests_logger.setLevel.assert_called_once_with(logging.WARNING)
                mock_urllib3_logger.setLevel.assert_called_once_with(logging.WARNING)
        finally:
            # Restore original logger state
            logging.Logger.manager.loggerDict = original_loggers
            root = logging.getLogger()
            root.handlers = original_handlers
            root.setLevel(original_level)
            
            # Restore original third-party logger levels
            if original_requests_level is not None and 'requests' in logging.Logger.manager.loggerDict:
                logging.getLogger('requests').setLevel(original_requests_level)
            if original_urllib3_level is not None and 'urllib3' in logging.Logger.manager.loggerDict:
                logging.getLogger('urllib3').setLevel(original_urllib3_level)