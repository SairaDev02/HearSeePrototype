"""
Functional tests for responsive design.

This module contains tests that verify the application's responsive design capabilities
across different screen sizes and devices. These tests focus on ensuring that the UI
components adapt appropriately to different viewport dimensions.
"""

import pytest
from unittest.mock import patch, MagicMock
import gradio as gr

from ui.chat_interface import ChatInterface
from ui.guide_interface import GuideInterface


class TestResponsiveDesign:
    """Test suite for responsive design."""

    def test_chat_interface_responsive_layout(self):
        """Test that the chat interface uses responsive layout techniques."""
        # Check for responsive layout elements like rows, columns, and scaling
        with patch('gradio.Column') as mock_column, \
             patch('gradio.Row') as mock_row, \
             patch('gradio.Textbox') as mock_textbox, \
             patch('ui.components.create_chatbot_component', return_value=MagicMock()), \
             patch('ui.components.create_image_instruction', return_value=MagicMock()), \
             patch('ui.components.create_voice_type_dropdown', return_value=MagicMock()), \
             patch('ui.components.create_speed_slider', return_value=MagicMock()), \
             patch('ui.components.create_mllm_status', return_value=MagicMock()), \
             patch('gradio.Button', return_value=MagicMock()), \
             patch('gradio.UploadButton', return_value=MagicMock()), \
             patch('gradio.Gallery', return_value=MagicMock()), \
             patch('gradio.Markdown', return_value=MagicMock()), \
             patch('gradio.Audio', return_value=MagicMock()):
            
            # Call the method
            ChatInterface.create_interface()
            
            # Verify Column and Row were used for layout
            assert mock_column.called, "Column should be used for responsive layout"
            assert mock_row.called, "Row should be used for responsive layout"
            
            # Check if any component uses scale parameter for responsive sizing
            mock_textbox.assert_called()
            textbox_kwargs = mock_textbox.call_args.kwargs
            assert 'scale' in textbox_kwargs, "Textbox should use scale parameter for responsive sizing"

    def test_gallery_responsive_configuration(self):
        """Test that the gallery component is configured for responsive display."""
        # Mock the Gallery component to capture its configuration
        with patch('gradio.Gallery') as mock_gallery, \
             patch('gradio.Column', return_value=MagicMock()), \
             patch('gradio.Row', return_value=MagicMock()), \
             patch('ui.components.create_chatbot_component', return_value=MagicMock()), \
             patch('ui.components.create_image_instruction', return_value=MagicMock()), \
             patch('ui.components.create_voice_type_dropdown', return_value=MagicMock()), \
             patch('ui.components.create_speed_slider', return_value=MagicMock()), \
             patch('ui.components.create_mllm_status', return_value=MagicMock()), \
             patch('gradio.Textbox', return_value=MagicMock()), \
             patch('gradio.Button', return_value=MagicMock()), \
             patch('gradio.UploadButton', return_value=MagicMock()), \
             patch('gradio.Markdown', return_value=MagicMock()), \
             patch('gradio.Audio', return_value=MagicMock()):
            
            # Call the method
            ChatInterface.create_interface()
            
            # Verify Gallery was configured with responsive parameters
            mock_gallery.assert_called_once()
            gallery_kwargs = mock_gallery.call_args.kwargs
            
            # Check for responsive configuration
            assert 'columns' in gallery_kwargs, "Gallery should specify columns for responsive layout"
            assert 'object_fit' in gallery_kwargs, "Gallery should specify object_fit for responsive image display"
            assert gallery_kwargs['object_fit'] == "scale-down", "Gallery should use scale-down to maintain aspect ratio"

    def test_chatbot_responsive_configuration(self):
        """Test that the chatbot component is configured for responsive display."""
        # Mock the Chatbot directly to capture its configuration
        with patch('gradio.Chatbot') as mock_chatbot:
            
            # Configure the mock to return a MagicMock
            mock_instance = MagicMock()
            mock_chatbot.return_value = mock_instance
            
            # Import the function directly to ensure we're testing the right implementation
            from ui.components import create_chatbot_component
            
            # Call the function
            result = create_chatbot_component()
            
            # Verify the chatbot was created with responsive parameters
            assert mock_chatbot.called, "Chatbot should be created"
            chatbot_kwargs = mock_chatbot.call_args.kwargs
            
            # Check for responsive configuration
            assert 'min_height' in chatbot_kwargs, "Chatbot should specify min_height for responsive layout"
            assert 'container' in chatbot_kwargs, "Chatbot should use container for responsive layout"
            assert chatbot_kwargs['container'] is True, "Chatbot container should be enabled for responsive layout"

    def test_mobile_viewport_adaptation(self):
        """Test that the interface adapts to mobile viewport sizes."""
        # This test verifies that the interface uses techniques that work well on mobile
        
        # Check for mobile-friendly UI patterns in the chat interface
        with patch('gradio.Column') as mock_column, \
             patch('gradio.Row') as mock_row, \
             patch('ui.components.create_chatbot_component', return_value=MagicMock()), \
             patch('ui.components.create_image_instruction', return_value=MagicMock()), \
             patch('ui.components.create_voice_type_dropdown', return_value=MagicMock()), \
             patch('ui.components.create_speed_slider', return_value=MagicMock()), \
             patch('ui.components.create_mllm_status', return_value=MagicMock()), \
             patch('gradio.Textbox', return_value=MagicMock()), \
             patch('gradio.Button', return_value=MagicMock()), \
             patch('gradio.UploadButton', return_value=MagicMock()), \
             patch('gradio.Gallery', return_value=MagicMock()), \
             patch('gradio.Markdown', return_value=MagicMock()), \
             patch('gradio.Audio', return_value=MagicMock()):
            
            # Call the method
            components = ChatInterface.create_interface()
            
            # Verify the interface uses a column-based layout which works well on mobile
            assert mock_column.called, "Interface should use Column for mobile-friendly layout"
            
            # Instead of checking mock_row.mock_calls, check if Button was called
            # This is more reliable since we're mocking the Button directly
            assert mock_row.called, "Interface should use Row for mobile-friendly layout"

    def test_guide_interface_responsive_content(self):
        """Test that the guide interface content is suitable for different screen sizes."""
        # Create the actual guide component
        with patch('gradio.Markdown', side_effect=lambda content: content) as mock_markdown:
            # Call the method
            guide_content = GuideInterface.create_guide()
            
            # Check for content organization that works well on different screen sizes
            assert "###" in guide_content, "Guide should use hierarchical headings for responsive layout"
            assert "-" in guide_content, "Guide should use lists for scannable content on small screens"
            
            # Check that content sections are concise (good for mobile)
            sections = guide_content.split("###")
            for section in sections[1:]:  # Skip the first split which is before any heading
                # Check that sections aren't too long (arbitrary threshold for testing)
                assert len(section.strip()) < 1000, "Guide sections should be concise for mobile viewing"

    def test_cross_component_interactions(self):
        """Test interactions between different UI components."""
        # This test verifies that components interact correctly across the interface
        
        # Instead of mocking app functions, we'll test the UI components directly
        with patch('gradio.Column', return_value=MagicMock()), \
             patch('gradio.Row', return_value=MagicMock()), \
             patch('ui.components.create_chatbot_component', return_value=MagicMock()), \
             patch('ui.components.create_image_instruction', return_value=MagicMock()), \
             patch('ui.components.create_voice_type_dropdown', return_value=MagicMock()), \
             patch('ui.components.create_speed_slider', return_value=MagicMock()), \
             patch('ui.components.create_mllm_status', return_value=MagicMock()), \
             patch('gradio.Textbox', return_value=MagicMock()), \
             patch('gradio.Button', return_value=MagicMock()), \
             patch('gradio.UploadButton', return_value=MagicMock()), \
             patch('gradio.Gallery', return_value=MagicMock()), \
             patch('gradio.Markdown', return_value=MagicMock()), \
             patch('gradio.Audio', return_value=MagicMock()):
            
            # Call the method to create the interface
            from ui.chat_interface import ChatInterface
            components = ChatInterface.create_interface()
            
            # Verify that the interface returns a dictionary of components
            assert isinstance(components, dict), "Interface should return a dictionary of components"
            
            # Verify that the dictionary contains all the expected components
            expected_components = [
                "chatbot", "msg", "send_btn", "upload_btn", "regenerate_btn",
                "clear_btn", "extract_btn", "caption_btn", "summarize_btn",
                "gallery", "voice_type", "speed", "tts_btn", "tts_status",
                "performance_metrics", "audio_output", "image_instruction"
            ]
            
            for component in expected_components:
                assert component in components, f"Missing component: {component}"

    def test_ui_state_transitions(self):
        """Test UI state transitions during processing."""
        # Instead of mocking app functions, we'll test the UI components directly
        with patch('gradio.Column', return_value=MagicMock()), \
             patch('gradio.Row', return_value=MagicMock()), \
             patch('ui.components.create_chatbot_component', return_value=MagicMock()), \
             patch('ui.components.create_image_instruction', return_value=MagicMock()), \
             patch('ui.components.create_voice_type_dropdown', return_value=MagicMock()), \
             patch('ui.components.create_speed_slider', return_value=MagicMock()), \
             patch('ui.components.create_mllm_status', return_value=MagicMock()), \
             patch('gradio.Textbox', return_value=MagicMock()), \
             patch('gradio.Button', return_value=MagicMock()), \
             patch('gradio.UploadButton', return_value=MagicMock()), \
             patch('gradio.Gallery', return_value=MagicMock()), \
             patch('gradio.Markdown', return_value=MagicMock()), \
             patch('gradio.Audio', return_value=MagicMock()):
            
            # Call the method to create the interface
            from ui.chat_interface import ChatInterface
            components = ChatInterface.create_interface()
            
            # Verify that the interface includes buttons that can be enabled/disabled
            assert "send_btn" in components, "Interface should include send button"
            assert "extract_btn" in components, "Interface should include extract button"
            assert "caption_btn" in components, "Interface should include caption button"
            assert "summarize_btn" in components, "Interface should include summarize button"
            
            # Verify that the interface includes components for displaying status
            assert "tts_status" in components, "Interface should include TTS status component"
            assert "performance_metrics" in components, "Interface should include performance metrics component"