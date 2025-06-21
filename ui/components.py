"""
UI Component Definitions for HearSee Application.

This module defines reusable UI components and their configurations for the
HearSee application. Each component is encapsulated in its own function to
promote reusability and maintainability across different interfaces.

The components include:
- Chatbot display
- Image upload instructions
- Voice type selection
- Speech speed controls
- Status indicators
"""

import gradio as gr
from config.settings import INIT_HISTORY, VOICE_TYPES

def create_chatbot_component():
    """
    Create the main chatbot Gradio component with predefined styling and configuration.
    
    The chatbot component displays the conversation history between the user and
    the AI assistant. It includes features like autoscrolling, copy buttons, and
    bubble-style layout for a modern chat appearance.
    
    Returns:
        gr.Chatbot: Configured chatbot component with initial history loaded
                    from settings.
    
    Example:
        chatbot = create_chatbot_component()
        # Can be used directly in a Gradio interface
        with gr.Blocks() as demo:
            chatbot_ui = chatbot
    
    Raises:
        ImportError: If Gradio is not installed or INIT_HISTORY is not defined
                     in settings.
    """
    return gr.Chatbot(
        value=INIT_HISTORY,  # Initial messages from settings
        container=True,  # Wrap in container for styling
        autoscroll=True,  # Automatically scroll to latest messages
        show_copy_button=True,  # Allow copying individual messages
        show_copy_all_button=True,  # Allow copying entire conversation
        min_height="500px",  # Ensure sufficient vertical space
        elem_classes="chatbox-style",  # Custom CSS class for styling
        layout="bubble",  # Modern chat bubble style
        show_share_button=False  # Disable sharing button - irrelevant for this use case
    )

def create_image_instruction():
    """
    Create the image upload instruction HTML component with warning styling.
    
    This component displays a prominent warning message to users, instructing
    them to upload an image before using the chat functionality. The message
    is styled with attention-grabbing colors and formatting.
    
    Returns:
        gr.HTML: Image instruction component with styled warning message
    
    Example:
        instruction = create_image_instruction()
        # Can be placed at the top of the interface
        with gr.Blocks() as demo:
            instruction_ui = instruction
    """
    return gr.HTML(
        """<div style="padding: 8px; margin: 8px 0; color: #ff5500; background-color: rgba(0, 0, 0, 0.25); border-radius: 4px; text-align: center;">
        <b>⚠️ Please upload an image first to enable chat functionality (Max 10MB size)</b>
        </div>"""  # Custom HTML with inline CSS for warning appearance
    )

def create_voice_type_dropdown():
    """
    Create the voice type dropdown for Text-to-Speech selection.
    
    This component allows users to select from predefined voice options
    for the text-to-speech functionality. Voice options are loaded from
    the application settings.
    
    Returns:
        gr.Dropdown: Voice type selection component with predefined options
    
    Example:
        voice_selector = create_voice_type_dropdown()
        # Can be used to get user voice preference
        selected_voice = voice_selector.value
    
    Raises:
        ImportError: If VOICE_TYPES is not defined in settings
    """
    return gr.Dropdown(
        choices=list(VOICE_TYPES.keys()),  # Available voice options from settings
        value=list(VOICE_TYPES.keys())[0],  # Default to first voice in the list
        label="Voice Type"  # User-friendly label
    )

def create_speed_slider():
    """
    Create the speed slider for Text-to-Speech playback rate control.
    
    This component provides a slider interface for users to adjust the
    playback speed of generated speech, ranging from half-speed (0.5x)
    to double-speed (2.0x).
    
    Returns:
        gr.Slider: Speed selection component with predefined range and step size
    
    Example:
        speed_control = create_speed_slider()
        # Can be used to get user speed preference
        playback_rate = speed_control.value
    """
    return gr.Slider(
        minimum=0.5,  # Half speed (slower)
        maximum=2.0,  # Double speed (faster)
        value=1.0,    # Default to normal speed
        step=0.1,     # Increment by 10% for fine control
        label="Playback Speed"  # User-friendly label
    )

def create_mllm_status():
    """
    Create the performance metrics textbox for Multimodal LLM status display.
    
    This component shows the current status and performance metrics of the
    multimodal language model, such as processing time, token usage, and
    operational state.
    
    Returns:
        gr.Textbox: Performance metrics display with default idle state
    
    Example:
        status_display = create_mllm_status()
        # Can be updated with performance data
        status_display.value = "Processing: 1.2s response time, 150 tokens"
    """
    return gr.Textbox(
        label="MLLM Status",  # Multimodal Language Model status
        value="Idle",         # Default state when no processing is happening
        interactive=False,    # Read-only display
        scale=1              # Add scale parameter for responsive sizing
    )

# Add more component creation functions as needed
# Each function should follow the pattern of creating a single, reusable UI component
# with appropriate configuration and documentation