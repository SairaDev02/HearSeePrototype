"""
Utility functions for image processing and handling.

This module contains utilities for image operations including base64 conversion,
text extraction, captioning, and summarization. It provides a unified interface
for interacting with vision models through the ReplicateService.

Classes:
    ImageUtils: Static methods for various image processing operations.
"""

import time
import logging
from services.image_service import ImageService
from services.replicate_service import ReplicateService

# Get logger for this module
logger = logging.getLogger(__name__)

class ImageUtils:
    @staticmethod
    def extract_text(image, history=None):
        """
        Extract text from image using Qwen VL model.
        
        This function processes an image to extract any visible text content using
        a vision-language model. It handles image validation, conversion to base64,
        and error handling.
        
        Args:
            image: The image object to process (PIL.Image or similar)
            history: Optional chat history list of [user_msg, bot_msg] pairs. Defaults to None.
            
        Returns:
            tuple: (updated_history, metrics_message)
                - updated_history: List of conversation turns with the new extraction result
                - metrics_message: String with performance metrics or error message
                
        Raises:
            Exception: Passes through any exceptions from underlying services,
                       but catches them for graceful error handling
                       
        Example:
            >>> history, metrics = ImageUtils.extract_text(my_image)
            >>> print(metrics)
            'Latency: 2.34s | Words: 156'
        """
        logger.info("Starting text extraction from image")
        start_time = time.time()
        size_valid, size_msg = ImageService.verify_image_size(image)
        if not size_valid:
            logger.warning(f"Image size validation failed: {size_msg}")
            return [[None, size_msg]], "Error: Image too large"

        # Image validation is handled by verify_image_size which checks for None and size limits

        try:
            logger.debug("Converting image to base64")
            img_str = ImageService.image_to_base64(image)
            if img_str is None:
                logger.error("Failed to convert image to base64")
                return [[None, "Error processing the image."]], "Error: Metrics unavailable"

            # Craft specialized prompts for the vision model to optimize text extraction
            system_prompt = "You are a helpful AI assistant specializing in extracting text from images."
            user_prompt = "Extract and transcribe all text visible in this image. Be thorough and precise."
            
            logger.debug("Calling vision model for text extraction")
            result = ReplicateService.run_vision_model(
                f"{system_prompt}\n\n{user_prompt}", image_base64=img_str
            )

            # Calculate performance metrics to provide feedback to the user
            latency = time.time() - start_time
            word_count = len(result.split())
            metrics = f"Latency: {latency:.2f}s | Words: {word_count}"
            
            logger.info(f"Text extraction completed in {latency:.2f}s with {word_count} words")

            user_message = "Please extract the text from this image."
            history = [] if history is None else history
            return history + [[user_message, result]], metrics

        except Exception as e:
            logger.error(f"Error extracting text from image: {str(e)}", exc_info=True)
            error_message = f"Error extracting text: {str(e)}"
            
            # Check if the error is related to image validation
            if "Error checking image size" in str(e):
                error_message = f"Error extracting text: {str(e)}"
            history = [] if history is None else history
            return history + [[None, error_message]], "Error: Status unavailable. Please try again."

    @staticmethod
    def caption_image(image, history=None):
        """
        Generate detailed caption for image using Qwen VL model.
        
        This function processes an image to create a comprehensive description
        using a vision-language model. It handles image validation, conversion
        to base64, and error handling.
        
        Args:
            image: The image object to process (PIL.Image or similar)
            history: Optional chat history list of [user_msg, bot_msg] pairs. Defaults to None.
            
        Returns:
            tuple: (updated_history, metrics_message)
                - updated_history: List of conversation turns with the new caption
                - metrics_message: String with performance metrics or error message
                
        Raises:
            Exception: Passes through any exceptions from underlying services,
                       but catches them for graceful error handling
                       
        Example:
            >>> history, metrics = ImageUtils.caption_image(my_image)
            >>> print(metrics)
            'Latency: 3.12s | Words: 203'
        """
        logger.info("Starting image captioning")
        start_time = time.time()
        size_valid, size_msg = ImageService.verify_image_size(image)
        if not size_valid:
            logger.warning(f"Image size validation failed: {size_msg}")
            return [[None, size_msg]], "Error: Image too large"

        try:
            logger.debug("Converting image to base64")
            img_str = ImageService.image_to_base64(image)
            if img_str is None:
                logger.error("Failed to convert image to base64")
                return [[None, "Error processing the image."]], "Error: Status unavailable. Please try again."

            # Craft specialized prompts for the vision model to optimize conciseness and image description
            system_prompt = "You are a helpful AI assistant specializing in captioning images in a clear and concise manner."
            user_prompt = "Caption this image concisely, you may include objects, people, scenery, colors, and composition to your response."

            logger.debug("Calling vision model for image captioning")
            result = ReplicateService.run_vision_model(
                f"{system_prompt}\n\n{user_prompt}", image_base64=img_str
            )
            
            # Calculate metrics
            latency = time.time() - start_time
            word_count = len(result.split())
            metrics = f"Latency: {latency:.2f}s | Words: {word_count}"
            
            logger.info(f"Image captioning completed in {latency:.2f}s with {word_count} words")

            user_message = "Create a concise caption for this image."
            history = [] if history is None else history
            return history + [[user_message, result]], metrics

        except Exception as e:
            logger.error(f"Error generating image caption: {str(e)}", exc_info=True)
            error_message = f"Error generating caption: {str(e)}"
            history = [] if history is None else history
            return history + [[None, error_message]], "Error: Status unavailable. Please try again."

    @staticmethod
    def summarize_image(image, history=None):
        """
        Generate contextual summary for image using Qwen VL model.
        
        This function processes an image to create a comprehensive contextual
        summary using a vision-language model. It focuses on analyzing the
        image content and providing a concise summary of key elements.
        
        Args:
            image: The image object to process (PIL.Image or similar)
            history: Optional chat history list of [user_msg, bot_msg] pairs. Defaults to None.
            
        Returns:
            tuple: (updated_history, metrics_message)
                - updated_history: List of conversation turns with the new summary
                - metrics_message: String with performance metrics or error message
                
        Raises:
            Exception: Passes through any exceptions from underlying services,
                       but catches them for graceful error handling
                       
        Example:
            >>> history, metrics = ImageUtils.summarize_image(my_image)
            >>> print(metrics)
            'Latency: 2.87s | Words: 178'
        """
        logger.info("Starting image summarization")
        start_time = time.time()
        size_valid, size_msg = ImageService.verify_image_size(image)
        if not size_valid:
            logger.warning(f"Image size validation failed: {size_msg}")
            return [[None, size_msg]], "Error: Image too large"

        try:
            logger.debug("Converting image to base64")
            img_str = ImageService.image_to_base64(image)
            if img_str is None:
                logger.error("Failed to convert image to base64")
                return [[None, "Error processing the image."]], "Error: Metrics unavailable"

            # Single comprehensive and concise prompt for image summarization
            prompt = "Analyze this image and provide a concise contextual summary including objects, people, activities, environment, colors, and mood."

            logger.debug("Calling vision model for image summarization")
            result = ReplicateService.run_vision_model(prompt, image_base64=img_str)

            # Calculate metrics
            latency = time.time() - start_time
            word_count = len(result.split())
            metrics = f"Latency: {latency:.2f}s | Words: {word_count}"
            
            logger.info(f"Image summarization completed in {latency:.2f}s with {word_count} words")

            user_message = "Please provide a concise summary of this image."
            history = [] if history is None else history
            return history + [[user_message, result]], metrics

        except Exception as e:
            logger.error(f"Error summarizing image: {str(e)}", exc_info=True)
            error_message = f"Error summarizing image: {str(e)}"
            history = [] if history is None else history
            return history + [[None, error_message]], "Error: Status unavailable. Please try again."