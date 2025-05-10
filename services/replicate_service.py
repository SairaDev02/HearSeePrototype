"""Service for handling Replicate API interactions.

This module provides functionality for interacting with Replicate's API,
specifically for running vision and text-to-speech models. It handles
API validation, parameter preparation, and error handling.
"""

import os
import replicate
import logging
from dotenv import load_dotenv

from config.settings import (
    QWEN_VL_MODEL, 
    KOKORO_TTS_MODEL, 
    DEFAULT_MAX_TOKENS
)

# Load environment variables
load_dotenv()

# Get logger for this module
logger = logging.getLogger(__name__)

# Module level functions (exported directly)
def verify_api_available():
    """
    Check if the Replicate API token is available.
    
    Returns:
        tuple: A boolean indicating API availability and an error message if not available.
        
    Example:
        >>> available, error = verify_api_available()
        >>> if not available:
        >>>     print(error)
    """
    return ReplicateService.verify_api_available()

def run_vision_model(prompt, image_base64=None, max_tokens=DEFAULT_MAX_TOKENS):
    """
    Run the Qwen VL model with given prompt and optional image.
    
    Args:
        prompt (str): The text prompt for the model.
        image_base64 (str, optional): Base64 encoded image. Defaults to None.
        max_tokens (int, optional): Maximum number of tokens to generate. Defaults to DEFAULT_MAX_TOKENS.
    
    Returns:
        str: Model's text response.
        
    Raises:
        ValueError: If API token is not available.
        RuntimeError: If model execution fails.
        
    Example:
        >>> response = run_vision_model("Describe this image", image_base64_string)
        >>> print(response)
    """
    return ReplicateService.run_vision_model(prompt, image_base64, max_tokens)

def run_tts_model(text, voice_id, speed):
    """
    Run the Kokoro TTS model with given parameters.
    
    Args:
        text (str): Text to convert to speech.
        voice_id (str): Voice identifier.
        speed (float): Speech playback speed.
    
    Returns:
        str: URL of generated audio.
        
    Raises:
        ValueError: If API token is not available.
        RuntimeError: If model execution fails.
        
    Example:
        >>> audio_url = run_tts_model("Hello world", "male_1", 1.0)
        >>> print(f"Audio available at: {audio_url}")
    """
    return ReplicateService.run_tts_model(text, voice_id, speed)

class ReplicateService:
    @staticmethod
    def verify_api_available():
        """
        Check if the Replicate API token is available.
        
        Returns:
            tuple: A boolean indicating API availability and an error message if not available.
            
        Example:
            >>> available, error = ReplicateService.verify_api_available()
            >>> if not available:
            >>>     print(error)
        """
        if "REPLICATE_API_TOKEN" not in os.environ:
            logger.error("Replicate API token not found in environment variables")
            return False, "Error: Replicate API token not found. Set REPLICATE_API_TOKEN in your .env file."
        logger.debug("Replicate API token verified")
        return True, ""

    @staticmethod
    def run_vision_model(prompt, image_base64=None, max_tokens=DEFAULT_MAX_TOKENS):
        """
        Run the Qwen VL model with given prompt and optional image.
        
        Args:
            prompt (str): The text prompt for the model.
            image_base64 (str, optional): Base64 encoded image. Defaults to None.
            max_tokens (int, optional): Maximum number of tokens to generate. Defaults to DEFAULT_MAX_TOKENS.
        
        Returns:
            str: Model's text response.
            
        Raises:
            ValueError: If API token is not available.
            RuntimeError: If model execution fails.
            
        Example:
            >>> response = ReplicateService.run_vision_model("Describe this image", image_base64_string)
            >>> print(response)
        """
        # Validate API availability before running
        api_available, error_msg = ReplicateService.verify_api_available()
        if not api_available:
            logger.error(f"API not available: {error_msg}")
            raise ValueError(error_msg)

        # Prepare API parameters
        api_params = {
            "prompt": prompt,
            "max_new_tokens": max_tokens,
        }
        
        # Add image if provided
        if image_base64:
            api_params["media"] = f"data:image/png;base64,{image_base64}"
            logger.info("Image included in vision model request")
        else:
            logger.info("Running vision model without image")

        # Run the model
        try:
            logger.debug(f"Calling Replicate API with model: {QWEN_VL_MODEL}")
            output = replicate.run(QWEN_VL_MODEL, input=api_params)
            logger.info("Vision model API call completed successfully")
            
            # Replicate may return output as a list of string chunks or a single string
            # We join the chunks if it's a list, otherwise return as is
            return "".join(output) if isinstance(output, list) else output
        except Exception as e:
            logger.error(f"Error running vision model: {str(e)}", exc_info=True)
            raise RuntimeError(f"Error running vision model: {str(e)}")

    @staticmethod
    def run_tts_model(text, voice_id, speed):
        """
        Run the Kokoro TTS model with given parameters.
        
        Args:
            text (str): Text to convert to speech.
            voice_id (str): Voice identifier.
            speed (float): Speech playback speed.
        
        Returns:
            str: URL of generated audio.
            
        Raises:
            ValueError: If API token is not available.
            RuntimeError: If model execution fails.
            
        Example:
            >>> audio_url = ReplicateService.run_tts_model("Hello world", "male_1", 1.0)
            >>> print(f"Audio available at: {audio_url}")
        """
        # Validate API availability before running
        api_available, error_msg = ReplicateService.verify_api_available()
        if not api_available:
            logger.error(f"API not available: {error_msg}")
            raise ValueError(error_msg)

        try:
            logger.info(f"Running TTS model with voice: {voice_id}, speed: {speed}")
            logger.debug(f"Text length for TTS: {len(text)} characters")
            
            # Configure TTS model parameters
            output = replicate.run(
                KOKORO_TTS_MODEL,
                input={
                    "text": text,      # The text content to convert to speech
                    "voice": voice_id, # The voice identifier to use
                    "speed": speed     # The playback speed factor
                }
            )
            logger.info("TTS model API call completed successfully")
            return output
        except Exception as e:
            logger.error(f"Error running TTS model: {str(e)}", exc_info=True)
            raise RuntimeError(f"Error running TTS model: {str(e)}")