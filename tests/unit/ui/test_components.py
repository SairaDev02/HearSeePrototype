"""
Unit tests for UI components.

This module contains tests for the UI components defined in ui/components.py.
These tests verify that each component is created with the correct configuration
and properties.
"""

import pytest
from unittest.mock import patch, MagicMock
import gradio as gr

from ui.components import (
    create_chatbot_component,
    create_image_instruction,
    create_voice_type_dropdown,
    create_speed_slider,
    create_mllm_status
)
from config.settings import INIT_HISTORY, VOICE_TYPES


class TestUIComponents:
    """Test suite for UI components."""

    def test_chatbot_component_creation(self):
        """Test that the chatbot component is created with correct properties."""
        with patch('gradio.Chatbot') as mock_chatbot:
            # Configure the mock
            mock_instance = MagicMock()
            mock_chatbot.return_value = mock_instance
            
            # Call the function
            result = create_chatbot_component()
            
            # Verify the result
            assert result == mock_instance
            
            # Verify the component was created with correct parameters
            mock_chatbot.assert_called_once()
            call_kwargs = mock_chatbot.call_args.kwargs
            assert call_kwargs['value'] == INIT_HISTORY
            assert call_kwargs['container'] is True
            assert call_kwargs['autoscroll'] is True
            assert call_kwargs['show_copy_button'] is True
            assert call_kwargs['show_copy_all_button'] is True
            assert call_kwargs['min_height'] == "500px"
            assert call_kwargs['elem_classes'] == "chatbox-style"
            assert call_kwargs['layout'] == "bubble"

    def test_image_instruction_creation(self):
        """Test that the image instruction component is created correctly."""
        with patch('gradio.HTML') as mock_html:
            # Configure the mock
            mock_instance = MagicMock()
            mock_html.return_value = mock_instance
            
            # Call the function
            result = create_image_instruction()
            
            # Verify the result
            assert result == mock_instance
            
            # Verify the component was created with correct parameters
            mock_html.assert_called_once()
            call_args = mock_html.call_args.args
            assert "Please upload an image first" in call_args[0]
            assert "warning" in call_args[0].lower() or "⚠️" in call_args[0]

    def test_voice_type_dropdown_creation(self):
        """Test that the voice type dropdown is created with correct options."""
        with patch('gradio.Dropdown') as mock_dropdown:
            # Configure the mock
            mock_instance = MagicMock()
            mock_dropdown.return_value = mock_instance
            
            # Call the function
            result = create_voice_type_dropdown()
            
            # Verify the result
            assert result == mock_instance
            
            # Verify the component was created with correct parameters
            mock_dropdown.assert_called_once()
            call_kwargs = mock_dropdown.call_args.kwargs
            assert call_kwargs['choices'] == list(VOICE_TYPES.keys())
            assert call_kwargs['value'] == list(VOICE_TYPES.keys())[0]
            assert call_kwargs['label'] == "Voice Type"

    def test_speed_slider_creation(self):
        """Test that the speed slider is created with correct range and default."""
        with patch('gradio.Slider') as mock_slider:
            # Configure the mock
            mock_instance = MagicMock()
            mock_slider.return_value = mock_instance
            
            # Call the function
            result = create_speed_slider()
            
            # Verify the result
            assert result == mock_instance
            
            # Verify the component was created with correct parameters
            mock_slider.assert_called_once()
            call_kwargs = mock_slider.call_args.kwargs
            assert call_kwargs['minimum'] == 0.5
            assert call_kwargs['maximum'] == 2.0
            assert call_kwargs['value'] == 1.0
            assert call_kwargs['step'] == 0.1
            assert call_kwargs['label'] == "Playback Speed"

    def test_mllm_status_creation(self):
        """Test that the MLLM status component is created correctly."""
        with patch('gradio.Textbox') as mock_textbox:
            # Configure the mock
            mock_instance = MagicMock()
            mock_textbox.return_value = mock_instance
            
            # Call the function
            result = create_mllm_status()
            
            # Verify the result
            assert result == mock_instance
            
            # Verify the component was created with correct parameters
            mock_textbox.assert_called_once()
            call_kwargs = mock_textbox.call_args.kwargs
            assert call_kwargs['label'] == "MLLM Status"
            assert call_kwargs['value'] == "Idle"
            assert call_kwargs['interactive'] is False

    def test_component_edge_cases(self):
        """Test edge cases for UI components."""
        # Test with actual Gradio components (no mocking)
        # This ensures the components can be created without errors
        chatbot = create_chatbot_component()
        assert isinstance(chatbot, gr.Chatbot)
        
        instruction = create_image_instruction()
        assert isinstance(instruction, gr.HTML)
        
        dropdown = create_voice_type_dropdown()
        assert isinstance(dropdown, gr.Dropdown)
        
        slider = create_speed_slider()
        assert isinstance(slider, gr.Slider)
        
        status = create_mllm_status()
        assert isinstance(status, gr.Textbox)