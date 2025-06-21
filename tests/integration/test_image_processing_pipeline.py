"""
Integration tests for the image processing pipeline.

This module contains tests that verify the interaction between
image service, replicate service, and image utilities.
"""

import pytest
from unittest.mock import patch, MagicMock
import numpy as np
from PIL import Image

from services.image_service import ImageService
from services.replicate_service import ReplicateService
from utils.image_utils import ImageUtils


class TestImageProcessingPipeline:
    """Test suite for the image processing pipeline."""

    def test_extract_text_pipeline(self, sample_image, mock_env_vars, mock_replicate):
        """Test the complete text extraction pipeline."""
        # Configure mock to return a test response
        mock_replicate.return_value = "This is extracted text from the image."
        
        # Call the method that uses multiple components
        history, metrics = ImageUtils.extract_text(sample_image)
        
        # Verify the result
        assert len(history) == 1
        assert history[0][0] == "Please extract the text from this image."
        assert history[0][1] == "This is extracted text from the image."
        assert "Latency" in metrics
        assert "Words" in metrics

    def test_caption_image_pipeline(self, sample_image, mock_env_vars, mock_replicate):
        """Test the complete image captioning pipeline."""
        # Configure mock to return a test response
        mock_replicate.return_value = "This is a detailed caption for the image."
        
        # Call the method that uses multiple components
        history, metrics = ImageUtils.caption_image(sample_image)
        
        # Verify the result
        assert len(history) == 1
        assert history[0][0] == "Create a concise caption for this image."
        assert history[0][1] == "This is a detailed caption for the image."
        assert "Latency" in metrics
        assert "Words" in metrics

    def test_summarize_image_pipeline(self, sample_image, mock_env_vars, mock_replicate):
        """Test the complete image summarization pipeline."""
        # Configure mock to return a test response
        mock_replicate.return_value = "This is a comprehensive summary of the image."
        
        # Call the method that uses multiple components
        history, metrics = ImageUtils.summarize_image(sample_image)
        
        # Verify the result
        assert len(history) == 1
        assert history[0][0] == "Please provide a concise summary of this image."
        assert history[0][1] == "This is a comprehensive summary of the image."
        assert "Latency" in metrics
        assert "Words" in metrics

    def test_image_processing_with_api_unavailable(self, sample_image, monkeypatch):
        """Test image processing when API is unavailable."""
        # Remove the environment variable
        monkeypatch.delenv("REPLICATE_API_TOKEN", raising=False)
        
        # Call the method
        history, metrics = ImageUtils.extract_text(sample_image)
        
        # Verify the result indicates API unavailability
        assert "API token not found" in history[0][1]
        assert "Error" in metrics

    def test_end_to_end_image_processing(self, sample_image, mock_env_vars):
        """Test end-to-end image processing with minimal mocking."""
        # Only mock the actual API call, let the rest of the pipeline run normally
        with patch.object(ReplicateService, 'run_vision_model', return_value="Test response"):
            # Process the image
            history, metrics = ImageUtils.extract_text(sample_image)
            
            # Verify the result
            assert history[0][1] == "Test response"
            assert "Latency" in metrics
            assert "Words" in metrics

    def test_image_size_validation_integration(self):
        """Test image size validation in the processing pipeline."""
        # Create an image that's too large
        large_image = np.ones((5000, 5000, 3), dtype=np.uint8)  # 5000x5000 RGB image
        
        # Mock verify_image_size to simulate a large image without actually creating one
        with patch.object(ImageService, 'verify_image_size', 
                         return_value=(False, "Image size (75.0MB) exceeds maximum allowed size (10MB)")):
            
            # Call the method
            history, metrics = ImageUtils.extract_text(large_image)
            
            # Verify the result
            assert "exceeds maximum allowed size" in history[0][1]
            assert "Error" in metrics

    def test_image_processing_error_handling(self, sample_image, mock_env_vars):
        """Test error handling throughout the image processing pipeline."""
        # Mock the API to raise an exception
        with patch.object(ReplicateService, 'run_vision_model', side_effect=Exception("Test error")):
            # Call the method
            history, metrics = ImageUtils.extract_text(sample_image)
            
            # Verify the error is properly handled
            assert "Error extracting text" in history[0][1]
            assert "Test error" in history[0][1]
            assert "Error" in metrics

    def test_image_conversion_pipeline(self, sample_image):
        """Test the image conversion pipeline."""
        # Test the actual conversion without mocking
        img_str = ImageService.image_to_base64(sample_image)
        
        # Verify the result is a valid base64 string
        assert isinstance(img_str, str)
        assert len(img_str) > 0
        
        # Verify it can be used in the next step of the pipeline
        with patch.object(ReplicateService, 'run_vision_model', return_value="Test response"):
            # Use the converted image in the pipeline
            history, metrics = ImageUtils.extract_text(sample_image)
            
            # Verify the result
            assert history[0][1] == "Test response"