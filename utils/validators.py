"""
Validation utilities for HearSee application.

This module contains validation functions for various input types
and chat-related operations.
"""

from typing import List, Union, Tuple

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
            return False, "Message cannot be empty"
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
            return False, "An image is required. Please upload an image before sending a message."
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
            return []
        if not isinstance(history, list):
            return []
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
            return "No messages to convert to speech."
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
            return False, "No text provided for speech conversion"

        # Validate speed if provided
        if speed is not None:
            try:
                speed_float = float(speed)
                if speed_float < 0.5 or speed_float > 2.0:
                    return False, "Speed must be between 0.5 and 2.0"
            except ValueError:
                return False, "Invalid speed value"

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