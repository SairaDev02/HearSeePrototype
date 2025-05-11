"""
Validation utilities for HearSee application.

This module contains validation functions for various input types
and chat-related operations. It provides both a class-based interface
and convenience functions for common validation tasks.

Classes:
    Validators: Static methods for validating different types of inputs.

Functions:
    validate_message: Validate chat message input.
    validate_image_input: Validate image input.
    validate_history: Validate chat history format.
    get_last_bot_message: Extract the last bot message from chat history.
    validate_tts_input: Validate inputs for text-to-speech conversion.
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
        
        Checks if the message is not empty or just whitespace.
        
        Args:
            message (str): Message string to validate
        
        Returns:
            tuple: A (validity, error_message) pair where:
                - validity (bool): True if message is valid, False otherwise
                - error_message (str): Empty string if valid, error description if invalid
                
        Example:
            >>> valid, error = Validators.validate_message("Hello")
            >>> print(valid, error)
            True ''
            >>> valid, error = Validators.validate_message("")
            >>> print(valid, error)
            False 'Message cannot be empty'
        """
        # Check for None, empty string, or whitespace-only string
        if not message or message.strip() == "":
            logger.warning("Empty message validation failed")
            return False, "Message cannot be empty"
        logger.debug("Message validation passed")
        return True, ""

    @staticmethod
    def validate_image_input(image) -> Tuple[bool, str]:
        """
        Validate image input.
        
        Checks if an image object is provided (not None).
        
        Args:
            image: Image object to validate (PIL.Image or similar)
        
        Returns:
            tuple: A (validity, error_message) pair where:
                - validity (bool): True if image is valid, False otherwise
                - error_message (str): Empty string if valid, error description if invalid
                
        Example:
            >>> from PIL import Image
            >>> img = Image.open('test.jpg')
            >>> valid, error = Validators.validate_image_input(img)
            >>> print(valid, error)
            True ''
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
        
        Ensures the history is a valid list, returning an empty list
        if the input is None or not a list type.
        
        Args:
            history: Chat history to validate, expected to be a list of
                    [user_message, bot_response] pairs or None
        
        Returns:
            list: Validated chat history (original list if valid, empty list otherwise)
            
        Example:
            >>> history = [["Hello", "Hi there!"]]
            >>> validated = Validators.validate_history(history)
            >>> print(validated)
            [['Hello', 'Hi there!']]
            >>> validated = Validators.validate_history(None)
            >>> print(validated)
            []
        """
        # Handle None case
        if history is None:
            logger.debug("History validation: None provided, returning empty list")
            return []
            
        # Ensure history is a list type
        if not isinstance(history, list):
            logger.warning(f"History validation: Invalid type {type(history)}, returning empty list")
            return []
            
        logger.debug(f"History validation passed: {len(history)} entries")
        return history

    @staticmethod
    def get_last_bot_message(history: List) -> str:
        """
        Extract the last bot message from chat history.
        
        Retrieves the most recent bot response from the chat history.
        If history is empty, returns a default message.
        
        Args:
            history: Chat history list of [user_msg, bot_msg] pairs
        
        Returns:
            str: Last bot message or default message if history is empty
            
        Example:
            >>> history = [["Hello", "Hi there!"], ["How are you?", "I'm doing well!"]]
            >>> last_msg = Validators.get_last_bot_message(history)
            >>> print(last_msg)
            "I'm doing well!"
        """
        # Check if history exists and has entries
        if not history:
            logger.debug("No chat history found for TTS conversion")
            return "No messages to convert to speech."
            
        # Return the bot's message (second item) from the last history entry
        logger.debug("Retrieved last bot message for TTS conversion")
        return history[-1][1]  # history[-1] is the last conversation pair, [1] is the bot's response

    @staticmethod
    def validate_tts_input(text: str, voice_type: str = None, speed: float = None) -> Tuple[bool, str]:
        """
        Validate inputs for text-to-speech conversion.
        
        Checks if the text is not empty and validates the speech speed
        if provided, ensuring it's within acceptable range (0.5 to 2.0).
        Also validates that the voice type is one of the supported voices.
        
        Args:
            text (str): Text to convert to speech
            voice_type (str, optional): Voice type to use for conversion
            speed (float, optional): Speech speed multiplier
        
        Returns:
            tuple: A (validity, error_message) pair where:
                - validity (bool): True if all inputs are valid, False otherwise
                - error_message (str): Empty string if valid, error description if invalid
                
        Example:
            >>> valid, error = Validators.validate_tts_input("Hello world", "female", 1.5)
            >>> print(valid, error)
            True ''
            >>> valid, error = Validators.validate_tts_input("", "male", 3.0)
            >>> print(valid, error)
            False 'No text provided for speech conversion'
        """
        # Check text is not empty or whitespace-only
        if not text or text.strip() == "":
            logger.warning("TTS validation failed: No text provided")
            return False, "No text provided for speech conversion"

        # Validate voice type if provided
        if voice_type is not None:
            from config.settings import VOICE_TYPES
            if voice_type not in VOICE_TYPES:
                logger.warning(f"TTS validation failed: Invalid voice type '{voice_type}'")
                return False, f"Invalid voice type: {voice_type}. Valid options are: {', '.join(VOICE_TYPES.keys())}"

        # Validate speed if provided
        if speed is not None:
            try:
                # Convert to float in case it's passed as string
                speed_float = float(speed)
                
                # Check if speed is within acceptable range
                # Speech that's too slow or too fast becomes unintelligible
                if speed_float < 0.5 or speed_float > 2.0:
                    logger.warning(f"TTS validation failed: Speed {speed_float} out of range")
                    return False, "Speed must be between 0.5 and 2.0"
            except ValueError:
                # Handle case where speed can't be converted to float
                logger.warning(f"TTS validation failed: Invalid speed value '{speed}'")
                return False, "Invalid speed value"

        logger.debug(f"TTS validation passed: text length={len(text)}, voice={voice_type}, speed={speed}")
        return True, ""

def validate_message(message: str) -> Tuple[bool, str]:
    """
    Convenience function for message validation.
    
    Args:
        message (str): Message to validate
        
    Returns:
        tuple: (validity, error_message) pair
    """
    return Validators.validate_message(message)

def validate_image_input(image) -> Tuple[bool, str]:
    """
    Convenience function for image input validation.
    
    Args:
        image: Image to validate
        
    Returns:
        tuple: (validity, error_message) pair
    """
    return Validators.validate_image_input(image)

def validate_history(history: Union[List, None]) -> List:
    """
    Convenience function for history validation.
    
    Args:
        history: Chat history to validate
        
    Returns:
        list: Validated chat history
    """
    return Validators.validate_history(history)

def get_last_bot_message(history: List) -> str:
    """
    Convenience function for extracting last bot message.
    
    Args:
        history: Chat history
        
    Returns:
        str: Last bot message or default message
    """
    return Validators.get_last_bot_message(history)

def validate_tts_input(text: str, voice_type: str = None, speed: float = None) -> Tuple[bool, str]:
    """
    Convenience function for TTS input validation.
    
    Args:
        text (str): Text to convert
        voice_type (str, optional): Voice type to use
        speed (float, optional): Speech speed
        
    Returns:
        tuple: (validity, error_message) pair
    """
    return Validators.validate_tts_input(text, voice_type, speed)