"""
Integration tests for error handling.

This module contains tests that verify the application's error handling capabilities
across different components and user interactions. These tests focus on validating
appropriate system responses to invalid inputs, network failures, and resource constraints.
"""

import pytest
from unittest.mock import patch, MagicMock
import numpy as np
import os
import requests

from services.image_service import ImageService
from services.replicate_service import ReplicateService
from services.tts_service import TTSService
from utils.image_utils import ImageUtils
from utils.validators import validate_image_input, validate_tts_input


class TestErrorHandling:
    """Test suite for error handling."""

    def test_oversized_image_handling(self):
        """Test handling of images that exceed the size limit."""
        # Mock the verify_image_size method to simulate an oversized image
        with patch.object(ImageService, 'verify_image_size', 
                         return_value=(False, "Image size (15.0MB) exceeds maximum allowed size (10MB)")):
            
            # Create a sample image (actual size doesn't matter due to the mock)
            sample_image = np.zeros((100, 100, 3), dtype=np.uint8)
            
            # Call the extract_text method which should handle the error
            history, metrics = ImageUtils.extract_text(sample_image)
            
            # Verify the error is properly handled
            assert "exceeds maximum allowed size" in history[0][1]
            assert "Error" in metrics

    def test_missing_api_token_handling(self):
        """Test handling of missing API token."""
        # Temporarily remove the environment variable
        with patch.dict(os.environ, {}, clear=True):
            # Call the method that requires the API token
            history, metrics = ImageUtils.extract_text(np.zeros((100, 100, 3), dtype=np.uint8))
            
            # Verify the error is properly handled
            assert "API token not found" in history[0][1]
            assert "Error" in metrics

    def test_api_error_handling(self):
        """Test handling of API errors."""
        # Mock the run_vision_model method to raise an exception
        with patch.object(ReplicateService, 'run_vision_model', 
                         side_effect=Exception("API rate limit exceeded")):
            
            # Create a sample image
            sample_image = np.zeros((100, 100, 3), dtype=np.uint8)
            
            # Call the method
            history, metrics = ImageUtils.extract_text(sample_image)
            
            # Verify the error is properly handled
            assert "Error extracting text" in history[0][1]
            assert "API rate limit exceeded" in history[0][1]
            assert "Error" in metrics

    def test_network_failure_handling_in_tts(self):
        """Test handling of network failures in text-to-speech service."""
        # Mock the API to return a URL but the download fails
        with patch.object(ReplicateService, 'run_tts_model', 
                         return_value="https://example.com/audio.wav"), \
             patch('requests.get') as mock_get:
            
            # Configure the mock to simulate a network error
            mock_get.side_effect = requests.exceptions.ConnectionError("Network error")
            
            # Call the method
            result, status = TTSService.process_audio("Test text")
            
            # Verify the error is properly handled
            assert result is None
            assert "Error downloading audio" in status
            assert "Network error" in status

    def test_invalid_voice_type_handling(self):
        """Test handling of invalid voice type."""
        # Call the validation function with an invalid voice type
        valid, error = validate_tts_input("Test text", "Invalid Voice", 1.0)
        
        # Verify the validation fails with appropriate error message
        assert valid is False
        assert "Invalid voice type" in error

    def test_invalid_speed_handling(self):
        """Test handling of invalid speed value."""
        # Test with speed below minimum
        valid1, error1 = validate_tts_input("Test text", "Female River (American)", 0.1)
        assert valid1 is False
        assert "Speed must be between" in error1
        
        # Test with speed above maximum
        valid2, error2 = validate_tts_input("Test text", "Female River (American)", 3.0)
        assert valid2 is False
        assert "Speed must be between" in error2

    def test_empty_text_handling_in_tts(self):
        """Test handling of empty text in text-to-speech service."""
        # Call the method with empty text
        result, status = TTSService.process_audio("")
        
        # Verify the error is properly handled
        assert result is None
        assert "No text to convert to speech" in status

    def test_missing_image_handling(self):
        """Test handling of missing image in image processing."""
        # Call the validation function with None as image
        valid, error = validate_image_input(None)
        
        # Verify the validation fails with appropriate error message
        assert valid is False
        assert "An image is required" in error

    def test_corrupted_image_handling(self):
        """Test handling of corrupted or invalid image data."""
        # Create an invalid image array (wrong shape)
        invalid_image = np.zeros((10, 10))  # Missing color channel dimension
        
        # Mock the image_to_base64 method to raise an exception when processing the invalid image
        with patch.object(ImageService, 'image_to_base64', 
                         side_effect=ValueError("Invalid image format")):
            
            # Call the method
            history, metrics = ImageUtils.extract_text(invalid_image)
            
            # Verify the error is properly handled
            assert "Error extracting text" in history[0][1] or "Error checking image size" in history[0][1]
            assert "Error" in metrics

    def test_server_error_handling(self):
        """Test handling of server errors from the API."""
        # Mock the API to return a 500 error
        with patch.object(ReplicateService, 'run_vision_model', 
                         side_effect=Exception("Server returned status code 500")):
            
            # Create a sample image
            sample_image = np.zeros((100, 100, 3), dtype=np.uint8)
            
            # Call the method
            history, metrics = ImageUtils.extract_text(sample_image)
            
            # Verify the error is properly handled
            assert "Error extracting text" in history[0][1]
            assert "Server returned status code 500" in history[0][1]
            assert "Error" in metrics

    def test_timeout_handling(self):
        """Test handling of timeout errors."""
        # Mock the API to time out
        with patch.object(ReplicateService, 'run_vision_model', 
                         side_effect=Exception("Request timed out after 30 seconds")):
            
            # Create a sample image
            sample_image = np.zeros((100, 100, 3), dtype=np.uint8)
            
            # Call the method
            history, metrics = ImageUtils.extract_text(sample_image)
            
            # Verify the error is properly handled
            assert "Error extracting text" in history[0][1]
            assert "Request timed out" in history[0][1]
            assert "Error" in metrics

    def test_resource_constraint_handling(self):
        """Test handling of resource constraints like memory limits."""
        # Mock the API to raise a memory error
        with patch.object(ReplicateService, 'run_vision_model', 
                         side_effect=MemoryError("Out of memory")):
            
            # Create a sample image
            sample_image = np.zeros((100, 100, 3), dtype=np.uint8)
            
            # Call the method
            history, metrics = ImageUtils.extract_text(sample_image)
            
            # Verify the error is properly handled
            assert "Error extracting text" in history[0][1]
            assert "Out of memory" in history[0][1] or "Memory" in history[0][1]
            assert "Error" in metrics