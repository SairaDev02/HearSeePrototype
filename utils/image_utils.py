"""
Utility functions for image processing and handling.

This module contains utilities for image operations including base64 conversion,
text extraction, captioning, and summarization.
"""

import time
from services.image_service import ImageService
from services.replicate_service import ReplicateService

class ImageUtils:
    @staticmethod
    def extract_text(image, history=None):
        """
        Extract text from image using Qwen VL model.
        
        Args:
            image: Image to process
            history: Optional chat history
            
        Returns:
            tuple: Updated history and status message
        """
        start_time = time.time()
        size_valid, size_msg = ImageService.verify_image_size(image)
        if not size_valid:
            return [[None, size_msg]], "Error: Image too large"

# Removed redundant check for `image is None` as `verify_image_size` already handles this case.

        try:
            img_str = ImageService.image_to_base64(image)
            if img_str is None:
                return [[None, "Error processing the image."]], "Error: Metrics unavailable"

            system_prompt = "You are a helpful AI assistant specializing in extracting text from images."
            user_prompt = "Extract and transcribe all text visible in this image. Be thorough and precise."
            
            result = ReplicateService.run_vision_model(
                f"{system_prompt}\n\n{user_prompt}", image_base64=img_str
            )

            # Calculate metrics
            latency = time.time() - start_time
            word_count = len(result.split())
            metrics = f"Latency: {latency:.2f}s | Words: {word_count}"

            user_message = "Please extract the text from this image."
            history = [] if history is None else history
            return history + [[user_message, result]], metrics

        except Exception as e:
            error_message = f"Error extracting text: {str(e)}"
            return history + [[None, error_message]], "Error: Status unavailable. Please try again."

    @staticmethod
    def caption_image(image, history=None):
        """
        Generate caption for image using Qwen VL model.
        
        Args:
            image: Image to process
            history: Optional chat history
            
        Returns:
            tuple: Updated history and status message
        """
        start_time = time.time()
        size_valid, size_msg = ImageService.verify_image_size(image)
        if not size_valid:
            return [[None, size_msg]], "Error: Image too large"

        try:
            img_str = ImageService.image_to_base64(image)
            if img_str is None:
                return [[None, "Error processing the image."]], "Error: Status unavailable. Please try again."

            system_prompt = "You are a helpful AI assistant specializing in describing images in detail."
            user_prompt = "Describe this image in detail, including objects, people, scenery, colors, and composition."

            result = ReplicateService.run_vision_model(
                f"{system_prompt}\n\n{user_prompt}", image_base64=img_str
            )
            
            # Calculate metrics
            latency = time.time() - start_time
            word_count = len(result.split())
            metrics = f"Latency: {latency:.2f}s | Words: {word_count}"

            user_message = "Please describe this image in detail."
            history = [] if history is None else history
            return history + [[user_message, result]], metrics

        except Exception as e:
            error_message = f"Error generating caption: {str(e)}"
            return history + [[None, error_message]], "Error: Status unavailable. Please try again."

    @staticmethod
    def summarize_image(image, history=None):
        """
        Generate summary for image using Qwen VL model.
        
        Args:
            image: Image to process
            history: Optional chat history
            
        Returns:
            tuple: Updated history and status message
        """
        start_time = time.time()
        size_valid, size_msg = ImageService.verify_image_size(image)
        if not size_valid:
            return [[None, size_msg]], "Error: Image too large"

        try:
            img_str = ImageService.image_to_base64(image)
            if img_str is None:
                return [[None, "Error processing the image."]], "Error: Metrics unavailable"

            prompt = "Analyze this image and provide a comprehensive contextual summary including objects, people, activities, environment, colors, and mood."

            result = ReplicateService.run_vision_model(prompt, image_base64=img_str)

            # Calculate metrics
            latency = time.time() - start_time
            word_count = len(result.split())
            metrics = f"Latency: {latency:.2f}s | Words: {word_count}"

            user_message = "Please provide a comprehensive summary of this image."
            history = [] if history is None else history
            return history + [[user_message, result]], metrics

        except Exception as e:
            error_message = f"Error summarizing image: {str(e)}"
            return history + [[None, error_message]], "Error: Status unavailable. Please try again."