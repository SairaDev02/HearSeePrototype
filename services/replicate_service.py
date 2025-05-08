"""Service for handling Replicate API interactions."""

import os
import replicate
from dotenv import load_dotenv

from config.settings import (
    QWEN_VL_MODEL, 
    KOKORO_TTS_MODEL, 
    DEFAULT_MAX_TOKENS
)

# Load environment variables
load_dotenv()

# Module level functions (exported directly)
def verify_api_available():
    """
    Check if the Replicate API token is available.
    
    Returns:
        tuple: A boolean indicating API availability and an error message if not available.
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
    """
    return ReplicateService.run_tts_model(text, voice_id, speed)

class ReplicateService:
    @staticmethod
    def verify_api_available():
        """
        Check if the Replicate API token is available.
        
        Returns:
            tuple: A boolean indicating API availability and an error message if not available.
        """
        if "REPLICATE_API_TOKEN" not in os.environ:
            return False, "Error: Replicate API token not found. Set REPLICATE_API_TOKEN in your .env file."
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
        """
        # Validate API availability before running
        api_available, error_msg = ReplicateService.verify_api_available()
        if not api_available:
            raise ValueError(error_msg)

        # Prepare API parameters
        api_params = {
            "prompt": prompt,
            "max_new_tokens": max_tokens,
        }
        
        # Add image if provided
        if image_base64:
            api_params["media"] = f"data:image/png;base64,{image_base64}"

        # Run the model
        try:
            output = replicate.run(QWEN_VL_MODEL, input=api_params)
            return "".join(output) if isinstance(output, list) else output
        except Exception as e:
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
        """
        # Validate API availability before running
        api_available, error_msg = ReplicateService.verify_api_available()
        if not api_available:
            raise ValueError(error_msg)

        try:
            output = replicate.run(
                KOKORO_TTS_MODEL,
                input={
                    "text": text,
                    "voice": voice_id,
                    "speed": speed
                }
            )
            return output
        except Exception as e:
            raise RuntimeError(f"Error running TTS model: {str(e)}")