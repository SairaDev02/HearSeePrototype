"""
Validation utilities for HearSee application.

This module contains validation functions for various input types
and chat-related operations.
"""

from typing import List, Union, Tuple
import logging

# Get logger for this module
logger = logging.getLogger(__name__)

class Validators:
    @staticmethod
    def validate_message(message: str) -> Tuple[bool, str]:
        """
        Validate chat message input.
        
        Args:
            message (str): Message to validate
        
        Returns:
            tuple: A boolean indicating validity and an error message if invalid
        """
        if not message or message.strip() == "":
            logger.warning("Empty message validation failed")
            return False, "Message cannot be empty"
        logger.debug("Message validation passed")
        return True, ""

    @staticmethod
    def validate_image_input(image) -> Tuple[bool, str]:
        """
        Validate image input.
        
        Args:
            image: Image to validate
        
        Returns:
            tuple: A boolean indicating validity and an error message if invalid
        """
        if image is None:
            logger.warning("Image validation failed: No image provided")
            return False, "An image is required. Please upload an image before sending a message."
        logger.debug("Image validation passed")
        return True, ""

    @staticmethod
    def validate_history(history: Union[List, None]) -> List:
        """
        Validate chat history format.
        
        Args:
            history: Chat history to validate
        
        Returns:
            list: Validated chat history
        """
        if history is None:
            logger.debug("History validation: None provided, returning empty list")
            return []
        if not isinstance(history, list):
            logger.warning(f"History validation: Invalid type {type(history)}, returning empty list")
            return []
        logger.debug(f"History validation passed: {len(history)} entries")
        return history

    @staticmethod
    def get_last_bot_message(history: List) -> str:
        """
        Extract the last bot message from chat history.
        
        Args:
            history: Chat history
        
        Returns:
            str: Last bot message or default message
        """
        if not history:
            logger.debug("No chat history found for TTS conversion")
            return "No messages to convert to speech."
        logger.debug("Retrieved last bot message for TTS conversion")
        return history[-1][1]

    @staticmethod
    def validate_tts_input(text: str, voice_type: str = None, speed: float = None) -> Tuple[bool, str]:
        """
        Validate inputs for text-to-speech conversion.
        
        Args:
            text (str): Text to convert
            voice_type (str, optional): Voice type to use
            speed (float, optional): Speech speed
        
        Returns:
            tuple: A boolean indicating validity and an error message if invalid
        """
        # Check text
        if not text or text.strip() == "":
            logger.warning("TTS validation failed: No text provided")
            return False, "No text provided for speech conversion"

        # Validate speed if provided
        if speed is not None:
            try:
                speed_float = float(speed)
                if speed_float < 0.5 or speed_float > 2.0:
                    logger.warning(f"TTS validation failed: Speed {speed_float} out of range")
                    return False, "Speed must be between 0.5 and 2.0"
            except ValueError:
                logger.warning(f"TTS validation failed: Invalid speed value '{speed}'")
                return False, "Invalid speed value"

        logger.debug(f"TTS validation passed: text length={len(text)}, voice={voice_type}, speed={speed}")
        return True, ""

def validate_message(message: str) -> Tuple[bool, str]:
    """Convenience function for message validation."""
    return Validators.validate_message(message)

def validate_image_input(image) -> Tuple[bool, str]:
    """Convenience function for image input validation."""
    return Validators.validate_image_input(image)

def validate_history(history: Union[List, None]) -> List:
    """Convenience function for history validation."""
    return Validators.validate_history(history)

def get_last_bot_message(history: List) -> str:
    """Convenience function for extracting last bot message."""
    return Validators.get_last_bot_message(history)

def validate_tts_input(text: str, voice_type: str = None, speed: float = None) -> Tuple[bool, str]:
    """Convenience function for TTS input validation."""
    return Validators.validate_tts_input(text, voice_type, speed)