"""
Unit tests for the TTSService module.

This module contains tests for the TTSService class and its methods.
"""

import pytest
from unittest.mock import patch, MagicMock

from services.tts_service import TTSService
from config.settings import VOICE_TYPES, TTS_SPEED_RANGE, DEFAULT_VOICE, DEFAULT_SPEED


class TestTTSService:
    """Test suite for TTSService class."""

    def test_validate_voice_type_with_valid_voice(self):
        """Test voice type validation with a valid voice type."""
        # Get a valid voice type from the configuration
        valid_voice = list(VOICE_TYPES.keys())[0]
        
        # Call the method
        result = TTSService.validate_voice_type(valid_voice)
        
        # Should return the corresponding voice ID
        assert result == VOICE_TYPES[valid_voice]

    def test_validate_voice_type_with_invalid_voice(self):
        """Test voice type validation with an invalid voice type."""
        # Call the method with an invalid voice type
        result = TTSService.validate_voice_type("Invalid Voice")
        
        # Should return the default voice ID
        assert result == VOICE_TYPES[DEFAULT_VOICE]

    def test_validate_voice_type_with_none(self):
        """Test voice type validation with None."""
        # Call the method with None
        result = TTSService.validate_voice_type(None)
        
        # Should return the default voice ID
        assert result == VOICE_TYPES[DEFAULT_VOICE]

    def test_validate_speed_with_valid_speed(self):
        """Test speed validation with a valid speed."""
        # Call the method with a valid speed
        valid_speed = 1.5  # Within the range
        result = TTSService.validate_speed(valid_speed)
        
        # Should return the same speed
        assert result == valid_speed

    def test_validate_speed_below_minimum(self):
        """Test speed validation with a speed below the minimum."""
        # Call the method with a speed below the minimum
        min_speed, _ = TTS_SPEED_RANGE
        below_min = min_speed - 0.1
        
        result = TTSService.validate_speed(below_min)
        
        # Should return the minimum speed
        assert result == min_speed

    def test_validate_speed_above_maximum(self):
        """Test speed validation with a speed above the maximum."""
        # Call the method with a speed above the maximum
        _, max_speed = TTS_SPEED_RANGE
        above_max = max_speed + 0.1
        
        result = TTSService.validate_speed(above_max)
        
        # Should return the maximum speed
        assert result == max_speed

    def test_validate_speed_with_none(self):
        """Test speed validation with None."""
        # Call the method with None
        result = TTSService.validate_speed(None)
        
        # Should return the default speed
        assert result == DEFAULT_SPEED

    def test_process_audio_success(self, mock_env_vars, mock_replicate, mock_requests):
        """Test successful audio processing."""
        # Configure mocks
        mock_replicate.return_value = "https://mock-audio-url.com/sample.wav"
        
        # Create a proper mock for the content
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b"Mock audio content"
        mock_requests.return_value = mock_response
        
        # Mock the _create_temp_audio_file method
        with patch.object(TTSService, '_create_temp_audio_file', return_value="mock_temp_file.wav") as mock_create_file:
            # Call the method
            result, status = TTSService.process_audio("Test text", "Female River (American)", 1.0)
            
            # Verify the result
            assert result == "mock_temp_file.wav"
            assert "Generated audio" in status
            assert "Female River (American)" in status
            assert "1.0x speed" in status
            
            # Verify the mocks were called
            mock_replicate.assert_called_once()
            mock_requests.assert_called_once_with("https://mock-audio-url.com/sample.wav")
            mock_create_file.assert_called_once_with(b"Mock audio content")

    def test_process_audio_api_unavailable(self, monkeypatch):
        """Test audio processing when API is unavailable."""
        # Remove the environment variable
        monkeypatch.delenv("REPLICATE_API_TOKEN", raising=False)
        
        # Call the method
        result, status = TTSService.process_audio("Test text")
        
        # Verify the result
        assert result is None
        assert "API token not found" in status

    def test_process_audio_empty_text(self, mock_env_vars):
        """Test audio processing with empty text."""
        # Call the method with empty text
        result, status = TTSService.process_audio("")
        
        # Verify the result
        assert result is None
        assert "No text to convert to speech" in status

    def test_process_audio_request_error(self, mock_env_vars, mock_replicate, mock_requests):
        """Test audio processing with HTTP request error."""
        # Configure mocks
        mock_replicate.return_value = "https://mock-audio-url.com/sample.wav"
        mock_requests.return_value.status_code = 404
        
        # Call the method
        result, status = TTSService.process_audio("Test text")
        
        # Verify the result
        assert result is None
        assert "Error downloading audio" in status
        assert "404" in status

    def test_process_audio_exception(self, mock_env_vars, mock_replicate):
        """Test audio processing with exception."""
        # Configure mock to raise an exception
        mock_replicate.side_effect = Exception("API error")
        
        # Call the method
        result, status = TTSService.process_audio("Test text")
        
        # Verify the result
        assert result is None
        assert "Error generating speech" in status
        assert "API error" in status

    def test_cleanup_audio_file(self, tmp_path):
        """Test audio file cleanup."""
        # Create a temporary file
        test_file = tmp_path / "test_audio.wav"
        test_file.write_text("test content")
        
        # Verify the file exists
        assert test_file.exists()
        
        # Call the method
        TTSService.cleanup_audio_file(str(test_file))
        
        # Verify the file was deleted
        assert not test_file.exists()

    def test_cleanup_audio_file_nonexistent(self):
        """Test cleanup with nonexistent file."""
        # Call the method with a nonexistent file
        # This should not raise an exception
        TTSService.cleanup_audio_file("nonexistent_file.wav")
        
        # No assertion needed, just verifying no exception is raised

    def test_cleanup_audio_file_exception(self, tmp_path):
        """Test cleanup with exception."""
        # Create a temporary file
        test_file = tmp_path / "test_audio.wav"
        test_file.write_text("test content")
        
        # Patch the logger directly
        with patch('services.tts_service.logger') as mock_logger:
            # Patch os.unlink to raise an exception
            with patch('os.unlink') as mock_unlink:
                mock_unlink.side_effect = Exception("Permission denied")
                
                # Call the method
                TTSService.cleanup_audio_file(str(test_file))
                
                # Verify the logger was called with an error
                mock_logger.error.assert_called_once()
                assert "Error cleaning up audio file" in mock_logger.error.call_args[0][0]