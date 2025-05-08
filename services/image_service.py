"""Service for handling image processing operations."""

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
        image (numpy.ndarray): Image array to convert.
    
    Returns:
        str or None: Base64 encoded image string, or None if conversion fails.
    """
    return ImageService.image_to_base64(image)

def verify_image_size(image):
    """
    Verify that the image size is within acceptable limits.
    
    Args:
        image (numpy.ndarray): Image to check.
    
    Returns:
        tuple: A boolean indicating if the image is valid, and an error message if not.
    """
    return ImageService.verify_image_size(image)

class ImageService:
    @staticmethod
    def image_to_base64(image):
        """
        Convert numpy image array to base64 string.
        
        Args:
            image (numpy.ndarray): Image array to convert.
        
        Returns:
            str or None: Base64 encoded image string, or None if conversion fails.
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
            image (numpy.ndarray): Image to check.
        
        Returns:
            tuple: A boolean indicating if the image is valid, and an error message if not.
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
            image (numpy.ndarray): Input image.
        
        Returns:
            numpy.ndarray: Preprocessed image.
        """
        # Add any necessary preprocessing steps
        # For example, resizing, normalization, etc.
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
            dict: Image metadata.
        """
        if image is None:
            return {}
        
        # Ensure image is a PIL Image
        if not isinstance(image, Image.Image):
            image = Image.fromarray(image)
        
        return {
            'format': image.format,
            'mode': image.mode,
            'size': image.size
        }