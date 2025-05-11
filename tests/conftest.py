"""
Global pytest fixtures for HearSee application testing.

This module contains fixtures that can be used across all test files.
"""

import os
import pytest
import json
from unittest.mock import MagicMock, patch
from io import BytesIO
import base64
from PIL import Image
import numpy as np

# No longer excluding any tests from collection
# All tests should now run successfully

# Mock environment variables
@pytest.fixture
def mock_env_vars(monkeypatch):
    """Mock environment variables used by the application."""
    monkeypatch.setenv("REPLICATE_API_TOKEN", "mock-api-token")
    yield


# Mock Replicate API
@pytest.fixture
def mock_replicate():
    """Mock the Replicate API client."""
    with patch("replicate.run") as mock_run:
        # Configure the mock to return a sample response
        mock_run.return_value = "This is a mock response from the Replicate API."
        yield mock_run


# Mock HTTP requests
@pytest.fixture
def mock_requests():
    """Mock HTTP requests."""
    with patch("requests.get") as mock_get:
        # Configure the mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b"Mock audio content"
        mock_get.return_value = mock_response
        yield mock_get


# Mock file system operations
@pytest.fixture
def mock_temp_file():
    """Mock temporary file creation."""
    with patch("tempfile.NamedTemporaryFile") as mock_temp:
        # Configure the mock to return a file-like object
        mock_file = MagicMock()
        mock_file.name = "mock_temp_file.wav"
        mock_temp.return_value.__enter__.return_value = mock_file
        yield mock_temp


# Sample test image
@pytest.fixture
def sample_image():
    """Create a sample test image."""
    # Create a simple 100x100 RGB image
    img = Image.new('RGB', (100, 100), color='red')
    img_array = np.array(img)
    return img_array

# Sample base64 image
@pytest.fixture
def sample_base64_image():
    """Create a sample base64 encoded image."""
    img = Image.new('RGB', (100, 100), color='blue')
    # Create a new BytesIO object for each test to avoid immutability issues
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_bytes = buffered.getvalue()
    return base64.b64encode(img_bytes).decode()



# Sample chat history
@pytest.fixture
def sample_chat_history():
    """Create a sample chat history."""
    return [
        ["Hello, can you analyze this image?", "I'd be happy to help analyze your image."],
        ["What can you see in it?", "I can see various elements in the image."]
    ]


# Mock logger
@pytest.fixture
def mock_logger():
    """Mock the logger to prevent actual logging during tests."""
    with patch("logging.getLogger") as mock_get_logger:
        mock_logger_instance = MagicMock()
        mock_get_logger.return_value = mock_logger_instance
        yield mock_logger_instance