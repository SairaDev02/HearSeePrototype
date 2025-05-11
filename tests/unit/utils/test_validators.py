"""
Unit tests for the validators module.

This module contains tests for the validation functions in the validators module.
"""

import pytest
from unittest.mock import patch

from utils.validators import (
    validate_message,
    validate_image_input,
    validate_history,
    get_last_bot_message,
    validate_tts_input
)


class TestValidators:
    """Test suite for validator functions."""

    def test_validate_message_valid(self):
        """Test message validation with valid message."""
        valid, error = validate_message("Hello, this is a test message.")
        assert valid is True
        assert error == ""

    def test_validate_message_empty(self):
        """Test message validation with empty message."""
        valid, error = validate_message("")
        assert valid is False
        assert "Message cannot be empty" in error

    def test_validate_message_whitespace(self):
        """Test message validation with whitespace-only message."""
        valid, error = validate_message("   ")
        assert valid is False
        assert "Message cannot be empty" in error

    def test_validate_image_input_valid(self, sample_image):
        """Test image validation with valid image."""
        valid, error = validate_image_input(sample_image)
        assert valid is True
        assert error == ""

    def test_validate_image_input_none(self):
        """Test image validation with None."""
        valid, error = validate_image_input(None)
        assert valid is False
        assert "An image is required" in error

    def test_validate_history_valid(self, sample_chat_history):
        """Test history validation with valid history."""
        result = validate_history(sample_chat_history)
        assert result == sample_chat_history

    def test_validate_history_none(self):
        """Test history validation with None."""
        result = validate_history(None)
        assert result == []

    def test_validate_history_invalid_type(self):
        """Test history validation with invalid type."""
        result = validate_history("not a list")
        assert result == []

    def test_get_last_bot_message_valid(self, sample_chat_history):
        """Test getting last bot message with valid history."""
        result = get_last_bot_message(sample_chat_history)
        assert result == "I can see various elements in the image."

    def test_get_last_bot_message_empty(self):
        """Test getting last bot message with empty history."""
        result = get_last_bot_message([])
        assert "No messages" in result

    def test_validate_tts_input_valid(self):
        """Test TTS input validation with valid inputs."""
        # Use a voice type that exists in VOICE_TYPES
        from config.settings import VOICE_TYPES
        valid_voice = list(VOICE_TYPES.keys())[0]  # Get the first valid voice type
        valid, error = validate_tts_input("This is a test message.", valid_voice, 1.0)
        assert valid is True
        assert error == ""

    def test_validate_tts_input_empty_text(self):
        """Test TTS input validation with empty text."""
        valid, error = validate_tts_input("")
        assert valid is False
        assert "No text provided" in error

    def test_validate_tts_input_invalid_speed_value(self):
        """Test TTS input validation with invalid speed value."""
        valid, error = validate_tts_input("Test message", speed="not a number")
        assert valid is False
        assert "Invalid speed value" in error

    def test_validate_tts_input_speed_too_low(self):
        """Test TTS input validation with speed too low."""
        valid, error = validate_tts_input("Test message", speed=0.1)
        assert valid is False
        assert "Speed must be between" in error

    def test_validate_tts_input_speed_too_high(self):
        """Test TTS input validation with speed too high."""
        valid, error = validate_tts_input("Test message", speed=3.0)
        assert valid is False
        assert "Speed must be between" in error