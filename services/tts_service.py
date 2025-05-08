"""Service for handling Text-to-Speech operations."""

import requests
from tempfile import NamedTemporaryFile
import os
import logging

from .replicate_service import ReplicateService
from config.settings import (
    VOICE_TYPES, 
    TTS_SPEED_RANGE, 
    DEFAULT_VOICE, 
    DEFAULT_SPEED
)

# Get logger for this module
logger = logging.getLogger(__name__)

# Module level functions (exported directly)
def validate_voice_type(voice_type=None):
    """
    Validate and get voice ID for given voice type.
    
    Args:
        voice_type (str, optional): Voice type to validate. Defaults to None.
    
    Returns:
        str: Validated voice ID.
    """
    return TTSService.validate_voice_type(voice_type)

def validate_speed(speed=None):
    """
    Validate and adjust speed to be within acceptable range.
    
    Args:
        speed (float, optional): Speed to validate. Defaults to None.
    
    Returns:
        float: Validated speed.
    """
    return TTSService.validate_speed(speed)

def process_audio(text, voice_type=None, speed=None):
    """
    Process text to speech conversion.
    
    Args:
        text (str): Text to convert to speech.
        voice_type (str, optional): Voice type to use. Defaults to None.
        speed (float, optional): Speech speed. Defaults to None.
    
    Returns:
        tuple: Temporary audio file path and status message.
    """
    return TTSService.process_audio(text, voice_type, speed)

class TTSService:
    @staticmethod
    def validate_voice_type(voice_type=None):
        """
        Validate and get voice ID for given voice type.
        
        Args:
            voice_type (str, optional): Voice type to validate. Defaults to None.
        
        Returns:
            str: Validated voice ID.
        """
        # If no voice type provided, use default
        if voice_type is None:
            voice_type = DEFAULT_VOICE
        
        # Return the voice ID, defaulting to default voice if not found
        return VOICE_TYPES.get(voice_type, VOICE_TYPES[DEFAULT_VOICE])

    @staticmethod
    def validate_speed(speed=None):
        """
        Validate and adjust speed to be within acceptable range.
        
        Args:
            speed (float, optional): Speed to validate. Defaults to None.
        
        Returns:
            float: Validated speed.
        """
        # If no speed provided, use default
        if speed is None:
            speed = DEFAULT_SPEED
        
        # Ensure speed is within the acceptable range
        min_speed, max_speed = TTS_SPEED_RANGE
        return max(min_speed, min(max_speed, float(speed)))

    @staticmethod
    def _create_temp_audio_file(content):
        """
        Create a temporary audio file with the given content.
        
        Args:
            content (bytes): Audio content to write to the file.
            
        Returns:
            str: Path to the temporary file.
        """
        with NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
            temp_file.write(content)
            return temp_file.name

    @staticmethod
    def process_audio(text, voice_type=None, speed=None):
        """
        Process text to speech conversion.
        
        Args:
            text (str): Text to convert to speech.
            voice_type (str, optional): Voice type to use. Defaults to None.
            speed (float, optional): Speech speed. Defaults to None.
        
        Returns:
            tuple: Temporary audio file path and status message.
        """
        # Check API availability
        api_available, error_msg = ReplicateService.verify_api_available()
        if not api_available:
            return None, error_msg

        # Validate inputs
        if not text or text.strip() == "":
            return None, "No text to convert to speech."

        try:
            # Get validated parameters
            voice_id = TTSService.validate_voice_type(voice_type)
            safe_speed = TTSService.validate_speed(speed)

            # Get audio URL from Replicate
            audio_url = ReplicateService.run_tts_model(text, voice_id, safe_speed)

            # Download and save audio
            response = requests.get(audio_url)
            if response.status_code == 200:
                # Create temporary file
                temp_path = TTSService._create_temp_audio_file(response.content)
                return temp_path, f"Generated audio using {voice_type or DEFAULT_VOICE} voice at {safe_speed}x speed"
            else:
                return None, f"Error downloading audio: HTTP status {response.status_code}"

        except Exception as e:
            return None, f"Error generating speech: {str(e)}"

    @staticmethod
    def cleanup_audio_file(file_path):
        """
        Clean up temporary audio file.
        
        Args:
            file_path (str): Path to the temporary audio file.
        """
        try:
            if file_path and os.path.exists(file_path):
                os.unlink(file_path)
        except Exception as e:
            logger.error(f"Error cleaning up audio file: {e}", exc_info=True)