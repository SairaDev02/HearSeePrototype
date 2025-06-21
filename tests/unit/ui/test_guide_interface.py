"""
Unit tests for the Guide Interface.

This module contains tests for the guide interface defined in ui/guide_interface.py.
These tests verify that the guide interface is created correctly with the proper content.
"""

import pytest
from unittest.mock import patch, MagicMock
import gradio as gr

from ui.guide_interface import GuideInterface, create_guide_interface


class TestGuideInterface:
    """Test suite for the Guide Interface."""

    def test_create_guide_interface_module_function(self):
        """Test that the module-level create_guide_interface function delegates to the class method."""
        with patch('ui.guide_interface.GuideInterface.create_guide') as mock_create:
            # Configure the mock
            mock_create.return_value = MagicMock()
            
            # Call the function
            result = create_guide_interface()
            
            # Verify the result
            assert result == mock_create.return_value
            mock_create.assert_called_once()

    def test_create_guide_content(self):
        """Test that the create_guide method returns a Markdown component with the correct content."""
        with patch('gradio.Markdown') as mock_markdown:
            # Configure the mock
            mock_instance = MagicMock()
            mock_markdown.return_value = mock_instance
            
            # Call the method
            result = GuideInterface.create_guide()
            
            # Verify the result
            assert result == mock_instance
            
            # Verify the component was created with correct content
            mock_markdown.assert_called_once()
            call_args = mock_markdown.call_args.args
            
            # Check for key sections in the guide content
            guide_content = call_args[0]
            assert "HearSee Web Application Guide" in guide_content
            assert "Image Upload & Analysis" in guide_content
            assert "Chat Functionality" in guide_content
            assert "Text-to-Speech Options" in guide_content
            assert "Performance Metrics" in guide_content
            assert "Technical Details" in guide_content
            assert "Privacy Note" in guide_content
            assert "Troubleshooting" in guide_content

    def test_guide_sections_completeness(self):
        """Test that all required sections are present in the guide."""
        with patch('gradio.Markdown', side_effect=lambda content: content) as mock_markdown:
            # Call the method
            guide_content = GuideInterface.create_guide()
            
            # Define required sections and features
            required_sections = [
                "Image Upload & Analysis",
                "Extract Text",
                "Caption Image",
                "Summarize Image",
                "Chat Functionality",
                "Text-to-Speech Options",
                "Performance Metrics",
                "Technical Details",
                "Privacy Note",
                "Troubleshooting"
            ]
            
            # Check each required section is present
            for section in required_sections:
                assert section in guide_content, f"Missing section: {section}"

    def test_guide_creation_with_actual_component(self):
        """Test creating the actual guide component without mocking."""
        # This test creates the actual component to ensure it works without errors
        guide = GuideInterface.create_guide()
        assert isinstance(guide, gr.Markdown)
        
        # Check the content of the guide
        guide_content = guide.value
        assert isinstance(guide_content, str)
        assert len(guide_content) > 0
        assert "HearSee Web Application Guide" in guide_content

    def test_guide_contains_all_features(self):
        """Test that the guide mentions all application features."""
        # Create the actual component
        guide = GuideInterface.create_guide()
        guide_content = guide.value
        
        # List of key features that should be mentioned
        key_features = [
            "Upload an Image",
            "Extract Text",
            "Caption Image",
            "Summarize Image",
            "chat",
            "Text-to-Speech",
            "voices",
            "speech speed",
            "Performance Metrics"
        ]
        
        # Check each key feature is mentioned
        for feature in key_features:
            assert feature.lower() in guide_content.lower(), f"Guide should mention feature: {feature}"

    def test_guide_contains_troubleshooting_info(self):
        """Test that the guide contains troubleshooting information."""
        # Create the actual component
        guide = GuideInterface.create_guide()
        guide_content = guide.value
        
        # Check for troubleshooting section
        assert "Troubleshooting" in guide_content
        
        # Check for common troubleshooting topics
        troubleshooting_topics = [
            "internet connection",
            "API key",
            "Refresh"
        ]
        
        # Check each troubleshooting topic is mentioned
        for topic in troubleshooting_topics:
            assert topic.lower() in guide_content.lower(), f"Guide should mention troubleshooting topic: {topic}"