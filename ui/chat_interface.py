"""
Chat Interface Construction for HearSee Application.

This module defines the layout and event handling for the main chat interface
of the HearSee application. It creates a Gradio-based UI with components for
chat interaction, image upload and processing, and text-to-speech functionality.

The interface is organized into logical sections:
- Chat and messaging components
- Image upload and processing controls
- Text-to-speech controls and output
- Status indicators
"""

import gradio as gr
from ui.components import (
    create_chatbot_component,
    create_image_instruction,
    create_voice_type_dropdown,
    create_speed_slider,
    create_mllm_status
)

# Module-level function for direct import
def create_interface():
    """
    Create the complete chat interface with all components and event handlers.
    
    This is a module-level convenience function that delegates to the
    ChatInterface class's static method.
    
    Returns:
        dict: A dictionary of Gradio components for the chat interface,
              keyed by component name for easy access and event binding.
    
    Example:
        components = create_interface()
        # Access specific component
        chatbot = components["chatbot"]
    """
    return ChatInterface.create_interface()

class ChatInterface:
    @staticmethod
    def create_interface():
        """
        Create the complete chat interface with all components and event handlers.
        
        This method constructs the entire UI layout using Gradio components,
        organizing them into a logical structure with appropriate styling and
        configuration.
        
        Returns:
            dict: A dictionary of Gradio components for the chat interface,
                  keyed by component name for easy access and event binding.
        
        Example:
            components = ChatInterface.create_interface()
            # Access specific component
            chatbot = components["chatbot"]
        """
        with gr.Column():
            # Main chat display and initial instruction message
            chatbot = create_chatbot_component()  # Main chat history display
            image_instruction = create_image_instruction()  # Warning to upload image first

            # User input section with text field and send button
            with gr.Row():
                msg = gr.Textbox(
                    label="Text Input",
                    placeholder="Enter text and press enter key/send button",
                    scale=9,
                    container=True,
                    show_label=False,
                )
                send_btn = gr.Button("Send", interactive=False)  # Initially disabled until image upload

            # Primary action buttons for image handling and chat management
            with gr.Row():
                upload_btn = gr.UploadButton("📁 Upload Image", file_types=["image"], file_count="single")
                regenerate_btn = gr.Button("🔄 Regenerate")
                clear_btn = gr.Button("🗑️ Clear History")

            # Specialized image processing action buttons
            # All initially disabled until an image is uploaded
            with gr.Row():
                extract_btn = gr.Button("📝 Extract Text", interactive=False)  # OCR functionality
                caption_btn = gr.Button("💭 Caption Image", interactive=False)  # Image description
                summarize_btn = gr.Button("📋 Summarize Image", interactive=False)  # Detailed analysis

            # Image display gallery
            # Uses 2 columns to allow for potential side-by-side comparison
            with gr.Row():
                gallery = gr.Gallery(
                    label="Uploaded Image",
                    show_label=True,
                    columns=2,  # Support for before/after comparisons
                    rows=1,
                    object_fit="scale-down",  # Maintains aspect ratio
                    show_share_button= False
                )

            # Text-to-Speech section header
            gr.Markdown("### Text-to-Speech Options")

            # Audio playback component for TTS output
            with gr.Row():
                audio_output = gr.Audio(label="Generated Speech", interactive=False, show_share_button=False)

            # TTS configuration controls
            with gr.Row():
                voice_type = create_voice_type_dropdown()  # Voice selection
                speed = create_speed_slider()  # Playback speed adjustment
                tts_btn = gr.Button("🔊 Play Last Response")  # Trigger TTS generation

            # System status indicators
            with gr.Row():
                tts_status = gr.Textbox(
                    label="TTS Status",
                    interactive=False,
                    value="Idle",  # Default state
                    scale=1  # Add scale parameter for responsive sizing
                )
                performance_metrics = create_mllm_status()  # Multimodal LLM performance tracking with scale parameter

            # Return all components in a dictionary for easy access and event binding in app.py
            # This allows the main application to connect these UI elements to backend functionality
            return {
                "chatbot": chatbot,
                "msg": msg,
                "send_btn": send_btn,
                "upload_btn": upload_btn,
                "regenerate_btn": regenerate_btn,
                "clear_btn": clear_btn,
                "extract_btn": extract_btn,
                "caption_btn": caption_btn,
                "summarize_btn": summarize_btn,
                "gallery": gallery,
                "voice_type": voice_type,
                "speed": speed,
                "tts_btn": tts_btn,
                "tts_status": tts_status,
                "performance_metrics": performance_metrics,
                "audio_output": audio_output,
                "image_instruction": image_instruction
            }