"""
Unit tests for the ReplicateService module.

This module contains tests for the ReplicateService class and its methods.
"""

import pytest
from unittest.mock import patch, MagicMock
import os

from services.replicate_service import ReplicateService
from tests.test_config import MOCK_VISION_RESPONSE, MOCK_TTS_RESPONSE, MOCK_API_PARAMS


class TestReplicateService:
    """Test suite for ReplicateService class."""

    def test_verify_api_available_success(self, mock_env_vars):
        """Test API verification when token is available."""
        # Test with mock environment variable set
        available, error_msg = ReplicateService.verify_api_available()
        assert available is True
        assert error_msg == ""

    def test_verify_api_available_failure(self, monkeypatch):
        """Test API verification when token is not available."""
        # Remove the environment variable
        monkeypatch.delenv("REPLICATE_API_TOKEN", raising=False)
        
        available, error_msg = ReplicateService.verify_api_available()
        assert available is False
        assert "API token not found" in error_msg

    def test_run_vision_model(self, mock_env_vars, mock_replicate):
        """Test running the vision model."""
        # Configure mock to return our test response
        mock_replicate.return_value = MOCK_VISION_RESPONSE
        
        # Call the method
        result = ReplicateService.run_vision_model(
            MOCK_API_PARAMS["vision"]["prompt"],
            image_base64="mock_base64_string",
            max_tokens=MOCK_API_PARAMS["vision"]["max_new_tokens"]
        )
        
        # Verify the result
        assert result == MOCK_VISION_RESPONSE
        
        # Verify the mock was called with expected parameters
        mock_replicate.assert_called_once()
        # We don't check exact parameters here as they include model IDs that might change

    def test_run_vision_model_api_unavailable(self, monkeypatch):
        """Test running vision model when API is unavailable."""
        # Remove the environment variable
        monkeypatch.delenv("REPLICATE_API_TOKEN", raising=False)
        
        # Expect ValueError when API is unavailable
        with pytest.raises(ValueError) as excinfo:
            ReplicateService.run_vision_model("test prompt")
        
        assert "API token not found" in str(excinfo.value)

    def test_run_vision_model_exception(self, mock_env_vars, mock_replicate):
        """Test handling exceptions from the API."""
        # Configure mock to raise an exception
        mock_replicate.side_effect = Exception("API error")
        
        # Expect RuntimeError when API raises exception
        with pytest.raises(RuntimeError) as excinfo:
            ReplicateService.run_vision_model("test prompt")
        
        assert "Error running vision model" in str(excinfo.value)

    def test_run_tts_model(self, mock_env_vars, mock_replicate):
        """Test running the TTS model."""
        # Configure mock to return our test response
        mock_replicate.return_value = MOCK_TTS_RESPONSE
        
        # Call the method
        result = ReplicateService.run_tts_model(
            MOCK_API_PARAMS["tts"]["text"],
            MOCK_API_PARAMS["tts"]["voice"],
            MOCK_API_PARAMS["tts"]["speed"]
        )
        
        # Verify the result
        assert result == MOCK_TTS_RESPONSE
        
        # Verify the mock was called with expected parameters
        mock_replicate.assert_called_once()