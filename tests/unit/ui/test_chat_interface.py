"""
Unit tests for the Chat Interface.

This module contains tests for the chat interface defined in ui/chat_interface.py.
These tests verify that the interface is created correctly with all required components.
"""

import pytest
from unittest.mock import patch, MagicMock
import gradio as gr

from ui.chat_interface import ChatInterface, create_interface


class TestChatInterface:
    """Test suite for the Chat Interface."""

    def test_create_interface_module_function(self):
        """Test that the module-level create_interface function delegates to the class method."""
        with patch('ui.chat_interface.ChatInterface.create_interface') as mock_create:
            # Configure the mock
            mock_create.return_value = {"test": "components"}
            
            # Call the function
            result = create_interface()
            
            # Verify the result
            assert result == {"test": "components"}
            mock_create.assert_called_once()

    def test_create_interface_components(self):
        """Test that the create_interface method returns all required components."""
        with patch('ui.components.create_chatbot_component') as mock_chatbot, \
             patch('ui.components.create_image_instruction') as mock_instruction, \
             patch('ui.components.create_voice_type_dropdown') as mock_dropdown, \
             patch('ui.components.create_speed_slider') as mock_slider, \
             patch('ui.components.create_mllm_status') as mock_status, \
             patch('gradio.Column'), \
             patch('gradio.Row'), \
             patch('gradio.Textbox'), \
             patch('gradio.Button'), \
             patch('gradio.UploadButton'), \
             patch('gradio.Gallery'), \
             patch('gradio.Markdown'), \
             patch('gradio.Audio'):
            
            # Configure the mocks
            mock_chatbot.return_value = MagicMock(name="chatbot")
            mock_instruction.return_value = MagicMock(name="image_instruction")
            mock_dropdown.return_value = MagicMock(name="voice_type")
            mock_slider.return_value = MagicMock(name="speed")
            mock_status.return_value = MagicMock(name="performance_metrics")
            
            # Call the method
            components = ChatInterface.create_interface()
            
            # Verify all required components are present
            required_components = [
                "chatbot", "msg", "send_btn", "upload_btn", "regenerate_btn", 
                "clear_btn", "extract_btn", "caption_btn", "summarize_btn", 
                "gallery", "voice_type", "speed", "tts_btn", "tts_status", 
                "performance_metrics", "audio_output", "image_instruction"
            ]
            
            for component in required_components:
                assert component in components, f"Missing component: {component}"

    def test_interface_structure(self):
        """Test the structure of the interface with context managers."""
        # This test verifies the structure of the interface using context managers
        # We'll use a custom context manager tracker to verify the nesting
        
        context_stack = []
        
        class MockContextManager:
            def __init__(self, name):
                self.name = name
            
            def __enter__(self):
                context_stack.append(self.name)
                return self
            
            def __exit__(self, exc_type, exc_val, exc_tb):
                if context_stack:
                    context_stack.pop()
        
        # Mock the context managers
        with patch('gradio.Column', return_value=MockContextManager("Column")), \
             patch('gradio.Row', return_value=MockContextManager("Row")), \
             patch('gradio.Markdown'), \
             patch('ui.components.create_chatbot_component', return_value=MagicMock()), \
             patch('ui.components.create_image_instruction', return_value=MagicMock()), \
             patch('ui.components.create_voice_type_dropdown', return_value=MagicMock()), \
             patch('ui.components.create_speed_slider', return_value=MagicMock()), \
             patch('ui.components.create_mllm_status', return_value=MagicMock()), \
             patch('gradio.Textbox', return_value=MagicMock()), \
             patch('gradio.Button', return_value=MagicMock()), \
             patch('gradio.UploadButton', return_value=MagicMock()), \
             patch('gradio.Gallery', return_value=MagicMock()), \
             patch('gradio.Audio', return_value=MagicMock()):
            
            # Call the method
            ChatInterface.create_interface()
            
            # Verify the context stack is empty at the end (all contexts properly exited)
            assert len(context_stack) == 0

    def test_button_initial_states(self):
        """Test that buttons have the correct initial states."""
        # Create a real interface with mocked components
        with patch('ui.components.create_chatbot_component', return_value=MagicMock()), \
             patch('ui.components.create_image_instruction', return_value=MagicMock()), \
             patch('ui.components.create_voice_type_dropdown', return_value=MagicMock()), \
             patch('ui.components.create_speed_slider', return_value=MagicMock()), \
             patch('ui.components.create_mllm_status', return_value=MagicMock()), \
             patch('gradio.Column', return_value=MagicMock()), \
             patch('gradio.Row', return_value=MagicMock()), \
             patch('gradio.Textbox', return_value=MagicMock()), \
             patch('gradio.UploadButton', return_value=MagicMock()), \
             patch('gradio.Gallery', return_value=MagicMock()), \
             patch('gradio.Markdown', return_value=MagicMock()), \
             patch('gradio.Audio', return_value=MagicMock()):
            
            # Track button creation with interactive parameter
            button_states = {}
            
            def mock_button(*args, **kwargs):
                if args and len(args) > 0:
                    name = args[0]
                else:
                    name = kwargs.get('value', 'unnamed')
                interactive = kwargs.get('interactive', True)
                button_states[name] = interactive
                return MagicMock()
            
            with patch('gradio.Button', side_effect=mock_button):
                # Call the method
                ChatInterface.create_interface()
                
                # Verify initial button states
                assert button_states.get('Send') is False, "Send button should be initially disabled"
                assert button_states.get('📝 Extract Text') is False, "Extract button should be initially disabled"
                assert button_states.get('💭 Caption Image') is False, "Caption button should be initially disabled"
                assert button_states.get('📋 Summarize Image') is False, "Summarize button should be initially disabled"

    def test_responsive_layout(self):
        """Test that the interface uses responsive layout techniques."""
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