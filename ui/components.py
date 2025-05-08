"""
UI Component Definitions for HearSee Application.

This module defines reusable UI components and their configurations.
"""

import gradio as gr
from config.settings import INIT_HISTORY, VOICE_TYPES

def create_chatbot_component():
    """
    Create the main chatbot Gradio component.
    
    Returns:
        gr.Chatbot: Configured chatbot component
    """
    return gr.Chatbot(
        value=INIT_HISTORY,
        container=True,
        autoscroll=True,
        show_copy_button=True,
        show_copy_all_button=True,
        min_height="500px",
        elem_classes="chatbox-style",
        layout="bubble"
    )

def create_image_instruction():
    """
    Create the image upload instruction HTML component.
    
    Returns:
        gr.HTML: Image instruction component
    """
    return gr.HTML(
        """<div style="padding: 8px; margin: 8px 0; color: #ff5500; background-color: rgba(0, 0, 0, 0.25); border-radius: 4px; text-align: center;">
        <b>⚠️ Please upload an image first to enable/renable chat functionality (Max 10MB size)</b>
        </div>"""
    )

def create_voice_type_dropdown():
    """
    Create the voice type dropdown for TTS.
    
    Returns:
        gr.Dropdown: Voice type selection component
    """
    return gr.Dropdown(
        choices=list(VOICE_TYPES.keys()),
        value=list(VOICE_TYPES.keys())[0],  # Default to first voice
        label="Voice Type"
    )

def create_speed_slider():
    """
    Create the speed slider for TTS.
    
    Returns:
        gr.Slider: Speed selection component
    """
    return gr.Slider(
        minimum=0.5,
        maximum=2.0,
        value=1.0,
        step=0.1,
        label="Playback Speed"
    )

def create_mllm_status():
    """
    Create the performance metrics textbox.
    
    Returns:
        gr.Textbox: Performance metrics display
    """
    return gr.Textbox(
        label="MLLM Status",
        value="Idle",
        interactive=False
    )

# Add more component creation functions as needed