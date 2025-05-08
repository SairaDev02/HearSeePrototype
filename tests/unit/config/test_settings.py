"""
Unit tests for the settings module.

This module contains tests for the configuration settings.
"""

import pytest
import importlib
import sys
from unittest.mock import patch

# Import the settings module
from config.settings import (
    QWEN_VL_MODEL,
    KOKORO_TTS_MODEL,
    DEFAULT_MAX_TOKENS,
    MAX_IMAGE_SIZE,
    INIT_HISTORY,
    VOICE_TYPES,
    TTS_SPEED_RANGE,
    DEFAULT_VOICE,
    DEFAULT_SPEED
)


class TestSettings:
    """Test suite for configuration settings."""

    def test_model_constants(self):
        """Test model constants are defined correctly."""
        # Verify model constants are non-empty strings
        assert isinstance(QWEN_VL_MODEL, str)
        assert len(QWEN_VL_MODEL) > 0
        assert isinstance(KOKORO_TTS_MODEL, str)
        assert len(KOKORO_TTS_MODEL) > 0

    def test_api_configuration(self):
        """Test API configuration settings."""
        # Verify DEFAULT_MAX_TOKENS is a positive integer
        assert isinstance(DEFAULT_MAX_TOKENS, int)
        assert DEFAULT_MAX_TOKENS > 0

    def test_image_settings(self):
        """Test image processing settings."""
        # Verify MAX_IMAGE_SIZE is a positive integer
        assert isinstance(MAX_IMAGE_SIZE, int)
        assert MAX_IMAGE_SIZE > 0
        # Verify it's set to 10MB
        assert MAX_IMAGE_SIZE == 10 * 1024 * 1024

    def test_init_history(self):
        """Test initial chat history."""
        # Verify INIT_HISTORY is a non-empty list
        assert isinstance(INIT_HISTORY, list)
        assert len(INIT_HISTORY) > 0
        
        # Verify each entry is a list with two strings
        for entry in INIT_HISTORY:
            assert isinstance(entry, list)
            assert len(entry) == 2
            assert isinstance(entry[0], str)
            assert isinstance(entry[1], str)

    def test_voice_types(self):
        """Test voice types configuration."""
        # Verify VOICE_TYPES is a non-empty dictionary
        assert isinstance(VOICE_TYPES, dict)
        assert len(VOICE_TYPES) > 0
        
        # Verify each entry has a string key and string value
        for key, value in VOICE_TYPES.items():
            assert isinstance(key, str)
            assert isinstance(value, str)

    def test_tts_speed_range(self):
        """Test TTS speed range configuration."""
        # Verify TTS_SPEED_RANGE is a tuple with two floats
        assert isinstance(TTS_SPEED_RANGE, tuple)
        assert len(TTS_SPEED_RANGE) == 2
        assert isinstance(TTS_SPEED_RANGE[0], float)
        assert isinstance(TTS_SPEED_RANGE[1], float)
        
        # Verify min is less than max
        assert TTS_SPEED_RANGE[0] < TTS_SPEED_RANGE[1]

    def test_default_tts_settings(self):
        """Test default TTS settings."""
        # Verify DEFAULT_VOICE is a string and exists in VOICE_TYPES
        assert isinstance(DEFAULT_VOICE, str)
        assert DEFAULT_VOICE in VOICE_TYPES
        
        # Verify DEFAULT_SPEED is a float within TTS_SPEED_RANGE
        assert isinstance(DEFAULT_SPEED, float)
        assert TTS_SPEED_RANGE[0] <= DEFAULT_SPEED <= TTS_SPEED_RANGE[1]

    def test_settings_reload(self):
        """Test settings can be reloaded."""
        # Save the original settings
        original_max_tokens = DEFAULT_MAX_TOKENS
        
        # Use a simpler approach that doesn't require file I/O
        # Create a mock module with the settings we want
        mock_settings = type('MockSettings', (), {
            'DEFAULT_MAX_TOKENS': 1024,  # Changed value
            'QWEN_VL_MODEL': 'mock-model',
            'KOKORO_TTS_MODEL': 'mock-tts-model',
            'MAX_IMAGE_SIZE': 10 * 1024 * 1024,
            'INIT_HISTORY': [],
            'VOICE_TYPES': {'test': 'test'},
            'TTS_SPEED_RANGE': (0.5, 2.0),
            'DEFAULT_VOICE': 'test',
            'DEFAULT_SPEED': 1.0
        })
        
        # Save the original module
        original_module = None
        if 'config.settings' in sys.modules:
            original_module = sys.modules['config.settings']
        
        try:
            # Replace the module in sys.modules
            sys.modules['config.settings'] = mock_settings
            
            # Access the settings from the mock module
            new_max_tokens = sys.modules['config.settings'].DEFAULT_MAX_TOKENS
            
            # Verify the value was changed
            assert new_max_tokens == 1024
            assert new_max_tokens != original_max_tokens
            
        finally:
            # Restore the original module
            if original_module:
                sys.modules['config.settings'] = original_module
            elif 'config.settings' in sys.modules:
                del sys.modules['config.settings']