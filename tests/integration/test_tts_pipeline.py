"""
Integration tests for the text-to-speech pipeline.

This module contains tests that verify the interaction between
TTS service, replicate service, and related components.
"""

import pytest
from unittest.mock import patch, MagicMock
import os

from services.tts_service import TTSService
from services.replicate_service import ReplicateService
from utils.validators import validate_tts_input, get_last_bot_message


class TestTTSPipeline:
    """Test suite for the text-to-speech pipeline."""

    def test_tts_pipeline_success(self, mock_env_vars, mock_replicate, mock_requests):
        """Test the complete TTS pipeline with successful execution."""
        # Configure mocks
        mock_replicate.return_value = "https://mock-audio-url.com/sample.wav"
        
        # Create a proper mock for the content
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b"Mock audio content"
        mock_requests.return_value = mock_response
        
        # Mock the _create_temp_audio_file method
        with patch.object(TTSService, '_create_temp_audio_file', return_value="mock_temp_file.wav") as mock_create_file:
            # Sample text to convert
            text = "This is a test message for text-to-speech conversion."
            
            # Call the method that uses multiple components
            result, status = TTSService.process_audio(text, "Female River (American)", 1.0)
            
            # Verify the result
            assert result == "mock_temp_file.wav"
            assert "Generated audio" in status
            assert "Female River (American)" in status
            assert "1.0x speed" in status
        
            # Verify the mocks were called in the correct sequence
            mock_replicate.assert_called_once()
            mock_requests.assert_called_once_with("https://mock-audio-url.com/sample.wav")
            mock_create_file.assert_called_once_with(b"Mock audio content")

    def test_tts_pipeline_with_validation(self, mock_env_vars, mock_replicate, mock_requests):
        """Test the TTS pipeline including input validation."""
        # Configure mocks
        mock_replicate.return_value = "https://mock-audio-url.com/sample.wav"
        
        # Create a proper mock for the content
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b"Mock audio content"
        mock_requests.return_value = mock_response
        
        # Mock the _create_temp_audio_file method
        with patch.object(TTSService, '_create_temp_audio_file', return_value="mock_temp_file.wav") as mock_create_file:
            # Sample text to convert
            text = "This is a test message for text-to-speech conversion."
            
            # First validate the input
            valid, error = validate_tts_input(text, "Female River (American)", 1.0)
            assert valid is True
            assert error == ""
            
            # Then process the audio
            result, status = TTSService.process_audio(text, "Female River (American)", 1.0)
            
            # Verify the result
            assert result == "mock_temp_file.wav"
            assert "Generated audio" in status
            assert "Female River (American)" in status
            assert "1.0x speed" in status
            
            # Verify the mock was called with the correct content
            mock_create_file.assert_called_once_with(b"Mock audio content")

    def test_tts_pipeline_with_chat_history(self, sample_chat_history, mock_env_vars, mock_replicate, mock_requests):
        """Test the TTS pipeline with chat history integration."""
        # Configure mocks
        mock_replicate.return_value = "https://mock-audio-url.com/sample.wav"
        
        # Create a proper mock for the content
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b"Mock audio content"
        mock_requests.return_value = mock_response
        
        # Mock the _create_temp_audio_file method
        with patch.object(TTSService, '_create_temp_audio_file', return_value="mock_temp_file.wav") as mock_create_file:
            # Get the last bot message from chat history
            text = get_last_bot_message(sample_chat_history)
            assert text == "I can see various elements in the image."
            
            # Process the audio
            result, status = TTSService.process_audio(text, "Female River (American)", 1.0)
            
            # Verify the result
            assert result == "mock_temp_file.wav"
            assert "Generated audio" in status
            assert "Female River (American)" in status
            assert "1.0x speed" in status
            
            # Verify the mock was called with the correct content
            mock_create_file.assert_called_once_with(b"Mock audio content")

    def test_tts_pipeline_api_unavailable(self, monkeypatch):
        """Test TTS pipeline when API is unavailable."""
        # Remove the environment variable
        monkeypatch.delenv("REPLICATE_API_TOKEN", raising=False)
        
        # Sample text to convert
        text = "This is a test message for text-to-speech conversion."
        
        # Call the method
        result, status = TTSService.process_audio(text)
        
        # Verify the result indicates API unavailability
        assert result is None
        assert "API token not found" in status

    def test_tts_pipeline_empty_text(self, mock_env_vars):
        """Test TTS pipeline with empty text."""
        # Call the method with empty text
        result, status = TTSService.process_audio("")
        
        # Verify the result
        assert result is None
        assert "No text to convert to speech" in status

    def test_tts_pipeline_api_error(self, mock_env_vars):
        """Test TTS pipeline with API error."""
        # Mock the API to raise an exception
        with patch.object(ReplicateService, 'run_tts_model', side_effect=Exception("API error")):
            # Call the method
            result, status = TTSService.process_audio("Test text")
            
            # Verify the result
            assert result is None
            assert "Error generating speech" in status
            assert "API error" in status

    def test_tts_pipeline_download_error(self, mock_env_vars, mock_replicate):
        """Test TTS pipeline with download error."""
        # Configure mocks
        mock_replicate.return_value = "https://mock-audio-url.com/sample.wav"
        
        # Mock requests.get to return an error status code
        with patch('requests.get') as mock_get:
            mock_response = MagicMock()
            mock_response.status_code = 404
            mock_get.return_value = mock_response
            
            # Call the method
            result, status = TTSService.process_audio("Test text")
            
            # Verify the result
            assert result is None
            assert "Error downloading audio" in status
            assert "404" in status

    def test_tts_pipeline_file_cleanup(self, mock_env_vars, mock_replicate, mock_requests, tmp_path):
        """Test TTS pipeline file cleanup."""
        # Configure mocks
        mock_replicate.return_value = "https://mock-audio-url.com/sample.wav"
        
        # Create a temporary file
        test_file = tmp_path / "test_audio.wav"
        test_file.write_text("test content")
        
        # Mock _create_temp_audio_file to return our test file
        with patch.object(TTSService, '_create_temp_audio_file', return_value=str(test_file)):
            # Call the method
            result, status = TTSService.process_audio("Test text")
            
            # Verify the result
            assert result == str(test_file)
            assert "Generated audio" in status
            
            # Clean up the file
            TTSService.cleanup_audio_file(result)
            
            # Verify the file was deleted
            assert not os.path.exists(result)

    def test_end_to_end_tts_pipeline(self, mock_env_vars):
        """Test end-to-end TTS pipeline with minimal mocking."""
        # Only mock the actual API call and HTTP request, let the rest of the pipeline run normally
        with patch.object(ReplicateService, 'run_tts_model', return_value="https://mock-audio-url.com/sample.wav"), \
             patch('requests.get') as mock_get, \
             patch.object(TTSService, '_create_temp_audio_file', return_value="mock_temp_file.wav") as mock_create_file:
            
            # Configure mocks
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.content = b"Mock audio content"
            mock_get.return_value = mock_response
            
            # Process the audio
            result, status = TTSService.process_audio("Test text")
            
            # Verify the result
            assert result == "mock_temp_file.wav"
            assert "Generated audio" in status
            
            # Verify the mock was called with the correct content
            mock_create_file.assert_called_once_with(b"Mock audio content")