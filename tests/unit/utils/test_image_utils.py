"""
Unit tests for the image_utils module.

This module contains tests for the ImageUtils class and its methods.
"""

import pytest
from unittest.mock import patch, MagicMock
import time

from utils.image_utils import ImageUtils
from services.image_service import ImageService
from services.replicate_service import ReplicateService


class TestImageUtils:
    """Test suite for ImageUtils class."""

    def test_extract_text_success(self, sample_image, mock_env_vars, mock_replicate):
        """Test successful text extraction from image."""
        # Configure mock
        mock_replicate.return_value = "This is extracted text from the image."
        
        # Call the method
        history, metrics = ImageUtils.extract_text(sample_image)
        
        # Verify the result
        assert len(history) == 1
        assert history[0][0] == "Please extract the text from this image."
        assert history[0][1] == "This is extracted text from the image."
        assert "Latency" in metrics
        assert "Words" in metrics

    def test_extract_text_invalid_size(self, sample_image):
        """Test text extraction with invalid image size."""
        # Patch verify_image_size to return invalid
        with patch.object(ImageService, 'verify_image_size', return_value=(False, "Image too large")):
            # Call the method
            history, metrics = ImageUtils.extract_text(sample_image)
            
            # Verify the result
            assert history[0][0] is None
            assert "Image too large" in history[0][1]
            assert "Error" in metrics

    def test_extract_text_base64_failure(self, sample_image):
        """Test text extraction with base64 conversion failure."""
        # Patch image_to_base64 to return None
        with patch.object(ImageService, 'image_to_base64', return_value=None):
            # Call the method
            history, metrics = ImageUtils.extract_text(sample_image)
            
            # Verify the result
            assert history[0][0] is None
            assert "Error processing the image" in history[0][1]
            assert "Error" in metrics

    def test_extract_text_api_exception(self, sample_image, mock_env_vars):
        """Test text extraction with API exception."""
        # Patch run_vision_model to raise an exception
        with patch.object(ReplicateService, 'run_vision_model', side_effect=Exception("API error")):
            # Call the method
            history, metrics = ImageUtils.extract_text(sample_image)
            
            # Verify the result
            assert "Error extracting text" in history[0][1]
            assert "Error" in metrics

    def test_caption_image_success(self, sample_image, mock_env_vars, mock_replicate):
        """Test successful image captioning."""
        # Configure mock
        mock_replicate.return_value = "This is a detailed caption for the image."
        
        # Call the method
        history, metrics = ImageUtils.caption_image(sample_image)
        
        # Verify the result
        assert len(history) == 1
        assert history[0][0] == "Please describe this image in detail."
        assert history[0][1] == "This is a detailed caption for the image."
        assert "Latency" in metrics
        assert "Words" in metrics

    def test_caption_image_invalid_size(self, sample_image):
        """Test image captioning with invalid image size."""
        # Patch verify_image_size to return invalid
        with patch.object(ImageService, 'verify_image_size', return_value=(False, "Image too large")):
            # Call the method
            history, metrics = ImageUtils.caption_image(sample_image)
            
            # Verify the result
            assert history[0][0] is None
            assert "Image too large" in history[0][1]
            assert "Error" in metrics

    def test_caption_image_base64_failure(self, sample_image):
        """Test image captioning with base64 conversion failure."""
        # Patch image_to_base64 to return None
        with patch.object(ImageService, 'image_to_base64', return_value=None):
            # Call the method
            history, metrics = ImageUtils.caption_image(sample_image)
            
            # Verify the result
            assert history[0][0] is None
            assert "Error processing the image" in history[0][1]
            assert "Error" in metrics

    def test_caption_image_api_exception(self, sample_image, mock_env_vars):
        """Test image captioning with API exception."""
        # Patch run_vision_model to raise an exception
        with patch.object(ReplicateService, 'run_vision_model', side_effect=Exception("API error")):
            # Call the method
            history, metrics = ImageUtils.caption_image(sample_image)
            
            # Verify the result
            assert "Error generating caption" in history[0][1]
            assert "Error" in metrics

    def test_summarize_image_success(self, sample_image, mock_env_vars, mock_replicate):
        """Test successful image summarization."""
        # Configure mock
        mock_replicate.return_value = "This is a comprehensive summary of the image."
        
        # Call the method
        history, metrics = ImageUtils.summarize_image(sample_image)
        
        # Verify the result
        assert len(history) == 1
        assert history[0][0] == "Please provide a comprehensive summary of this image."
        assert history[0][1] == "This is a comprehensive summary of the image."
        assert "Latency" in metrics
        assert "Words" in metrics

    def test_summarize_image_invalid_size(self, sample_image):
        """Test image summarization with invalid image size."""
        # Patch verify_image_size to return invalid
        with patch.object(ImageService, 'verify_image_size', return_value=(False, "Image too large")):
            # Call the method
            history, metrics = ImageUtils.summarize_image(sample_image)
            
            # Verify the result
            assert history[0][0] is None
            assert "Image too large" in history[0][1]
            assert "Error" in metrics

    def test_summarize_image_base64_failure(self, sample_image):
        """Test image summarization with base64 conversion failure."""
        # Patch image_to_base64 to return None
        with patch.object(ImageService, 'image_to_base64', return_value=None):
            # Call the method
            history, metrics = ImageUtils.summarize_image(sample_image)
            
            # Verify the result
            assert history[0][0] is None
            assert "Error processing the image" in history[0][1]
            assert "Error" in metrics

    def test_summarize_image_api_exception(self, sample_image, mock_env_vars):
        """Test image summarization with API exception."""
        # Patch run_vision_model to raise an exception
        with patch.object(ReplicateService, 'run_vision_model', side_effect=Exception("API error")):
            # Call the method
            history, metrics = ImageUtils.summarize_image(sample_image)
            
            # Verify the result
            assert "Error summarizing image" in history[0][1]
            assert "Error" in metrics

    def test_with_existing_history(self, sample_image, sample_chat_history, mock_env_vars, mock_replicate):
        """Test methods with existing chat history."""
        # Configure mock
        mock_replicate.return_value = "This is a test response."
        
        # Call the method with existing history
        history, metrics = ImageUtils.extract_text(sample_image, sample_chat_history)
        
        # Verify the result
        assert len(history) == len(sample_chat_history) + 1
        assert history[-1][1] == "This is a test response."