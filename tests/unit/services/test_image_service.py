"""
Unit tests for the ImageService module.

This module contains tests for the ImageService class and its methods.
"""

import pytest
from unittest.mock import patch, MagicMock
import base64
from PIL import Image
import io
import numpy as np

from services.image_service import ImageService
from config.settings import MAX_IMAGE_SIZE


class TestImageService:
    """Test suite for ImageService class."""

    def test_image_to_base64_with_numpy_array(self, sample_image):
        """Test converting a numpy array image to base64."""
        # Call the method
        result = ImageService.image_to_base64(sample_image)
        
        # Verify the result is a non-empty string
        assert isinstance(result, str)
        assert len(result) > 0
        
        # Verify it's valid base64
        try:
            decoded = base64.b64decode(result)
            # Verify it's a valid image
            img = Image.open(io.BytesIO(decoded))
            assert img.size == (100, 100)  # Our sample image size
        except Exception as e:
            pytest.fail(f"Failed to decode base64 or open image: {e}")

    def test_image_to_base64_with_pil_image(self):
        """Test converting a PIL Image to base64."""
        # Create a PIL Image
        pil_image = Image.new('RGB', (100, 100), color='green')
        
        # Call the method
        result = ImageService.image_to_base64(pil_image)
        
        # Verify the result is a non-empty string
        assert isinstance(result, str)
        assert len(result) > 0

    def test_image_to_base64_with_none(self):
        """Test handling None input."""
        result = ImageService.image_to_base64(None)
        assert result is None

    def test_image_to_base64_with_exception(self):
        """Test handling exceptions during conversion."""
        # Create an invalid "image" that will cause an exception
        invalid_image = "not an image"
        
        # Call the method
        result = ImageService.image_to_base64(invalid_image)
        
        # Should return None on exception
        assert result is None

    def test_verify_image_size_success(self, sample_image):
        """Test image size verification with valid image."""
        # Call the method
        valid, error_msg = ImageService.verify_image_size(sample_image)
        
        # Should be valid
        assert valid is True
        assert error_msg == ""

    def test_verify_image_size_none(self):
        """Test image size verification with None."""
        valid, error_msg = ImageService.verify_image_size(None)
        assert valid is False
        assert "No image provided" in error_msg

    def test_verify_image_size_too_large(self):
        """Test image size verification with oversized image."""
        # Create a custom BytesIO class for testing
        class MockBytesIO(io.BytesIO):
            def getvalue(self):
                # Return a byte string larger than MAX_IMAGE_SIZE
                return b'x' * (MAX_IMAGE_SIZE + 1)
        
        # Patch BytesIO to use our custom class
        with patch('io.BytesIO', MockBytesIO):
            # Create a small image that will pass the initial checks
            img = Image.new('RGB', (100, 100), color='red')
            
            # Call the method
            valid, error_msg = ImageService.verify_image_size(np.array(img))
            
            # Should be invalid due to size
            assert valid is False
            assert "exceeds maximum allowed size" in error_msg

    def test_preprocess_image(self, sample_image):
        """Test image preprocessing."""
        # Call the method
        result = ImageService.preprocess_image(sample_image)
        
        # Should return a numpy array
        assert isinstance(result, np.ndarray)
        assert result.shape == sample_image.shape

    def test_preprocess_image_none(self):
        """Test preprocessing with None input."""
        result = ImageService.preprocess_image(None)
        assert result is None

    def test_extract_image_metadata(self, sample_image):
        """Test extracting image metadata."""
        # Call the method
        metadata = ImageService.extract_image_metadata(sample_image)
        
        # Verify the metadata
        assert isinstance(metadata, dict)
        assert 'size' in metadata
        assert metadata['size'] == (100, 100)  # Our sample image size
        assert 'mode' in metadata
        assert metadata['mode'] == 'RGB'

    def test_extract_image_metadata_none(self):
        """Test extracting metadata with None input."""
        metadata = ImageService.extract_image_metadata(None)
        assert metadata == {}