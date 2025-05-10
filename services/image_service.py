"""Service for handling image processing operations.

This module provides functionality for image conversion, validation, and metadata extraction.
It includes both module-level functions and a class-based implementation.
"""

from PIL import Image
import io
import base64
import numpy as np
import logging

from config.settings import MAX_IMAGE_SIZE

# Get logger for this module
logger = logging.getLogger(__name__)

# Module level functions (exported directly)
def image_to_base64(image):
    """
    Convert numpy image array to base64 string.
    
    Args:
        image (numpy.ndarray or PIL.Image): Image to convert.
    
    Returns:
        str or None: Base64 encoded image string, or None if conversion fails.
        
    Raises:
        Exception: If image conversion or encoding fails.
        
    Example:
        >>> img = np.array([[[255, 0, 0]]])  # Simple red pixel
        >>> encoded = image_to_base64(img)
    """
    return ImageService.image_to_base64(image)

def verify_image_size(image):
    """
    Verify that the image size is within acceptable limits.
    
    Args:
        image (numpy.ndarray or PIL.Image): Image to check.
    
    Returns:
        tuple: A boolean indicating if the image is valid, and an error message if not.
        
    Raises:
        Exception: If image validation fails.
        
    Example:
        >>> is_valid, message = verify_image_size(large_image)
        >>> if not is_valid:
        >>>     print(message)
    """
    return ImageService.verify_image_size(image)

class ImageService:
    @staticmethod
    def image_to_base64(image):
        """
        Convert numpy image array to base64 string.
        
        Args:
            image (numpy.ndarray or PIL.Image): Image to convert.
        
        Returns:
            str or None: Base64 encoded image string, or None if conversion fails.
            
        Raises:
            Exception: If image conversion or encoding fails.
            
        Example:
            >>> img = np.array([[[255, 0, 0]]])  # Simple red pixel
            >>> encoded = ImageService.image_to_base64(img)
        """
        if image is None:
            return None
        
        try:
            buffered = io.BytesIO()
            # Ensure the image is in the correct format
            if not isinstance(image, Image.Image):
                img = Image.fromarray(image)
            else:
                img = image
            
            img.save(buffered, format="PNG")
            return base64.b64encode(buffered.getvalue()).decode()
        except Exception as e:
            logger.error(f"Error converting image to base64: {e}", exc_info=True)
            return None

    @staticmethod
    def verify_image_size(image):
        """
        Verify that the image size is within acceptable limits.
        
        Args:
            image (numpy.ndarray or PIL.Image): Image to check.
        
        Returns:
            tuple: A boolean indicating if the image is valid, and an error message if not.
            
        Raises:
            Exception: If image validation fails.
            
        Example:
            >>> is_valid, message = ImageService.verify_image_size(large_image)
            >>> if not is_valid:
            >>>     print(message)
        """
        if image is None:
            return False, "No image provided"

        try:
            buffered = io.BytesIO()
            # Ensure the image is in the correct format
            if not isinstance(image, Image.Image):
                img = Image.fromarray(image)
            else:
                img = image
            
            img.save(buffered, format="PNG")
            size = len(buffered.getvalue())
            
            # Convert bytes to MB for human-readable error message
            if size > MAX_IMAGE_SIZE:
                return False, f"Image size ({size/1024/1024:.1f}MB) exceeds maximum allowed size (10MB)"
            
            return True, ""
        except Exception as e:
            return False, f"Error checking image size: {str(e)}"

    @staticmethod
    def preprocess_image(image):
        """
        Perform basic preprocessing on the image.
        
        Args:
            image (numpy.ndarray or PIL.Image): Input image.
        
        Returns:
            numpy.ndarray: Preprocessed image.
            
        Raises:
            None: Returns None if input image is None.
            
        Example:
            >>> processed_img = ImageService.preprocess_image(raw_image)
            >>> display(processed_img)
        """
        # This is a placeholder for future preprocessing steps
        # Could include resizing, normalization, color correction, etc.
        if image is None:
            return None
        
        # Convert to PIL Image if it's a numpy array
        if not isinstance(image, Image.Image):
            image = Image.fromarray(image)
        
        return np.array(image)

    @staticmethod
    def extract_image_metadata(image):
        """
        Extract metadata from the image.
        
        Args:
            image (numpy.ndarray or PIL.Image): Input image.
        
        Returns:
            dict: Image metadata including format, mode, and size.
            
        Raises:
            None: Returns empty dict if input image is None.
            
        Example:
            >>> metadata = ImageService.extract_image_metadata(img)
            >>> print(f"Image size: {metadata['size']}")
        """
        if image is None:
            return {}
        
        # Ensure image is a PIL Image
        if not isinstance(image, Image.Image):
            image = Image.fromarray(image)
        
        # Extract basic metadata properties from the PIL Image
        return {
            'format': image.format,  # Image format (PNG, JPEG, etc.)
            'mode': image.mode,      # Color mode (RGB, RGBA, etc.)
            'size': image.size       # Width and height in pixels
        }