"""
Chat Interface Construction for HearSee Application.

This module defines the layout and event handling for the main chat interface.
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
    
    Returns:
        dict: A dictionary of Gradio components for the chat interface
    """
    return ChatInterface.create_interface()

class ChatInterface:
    @staticmethod
    def create_interface():
        """
        Create the complete chat interface with all components and event handlers.
        
        Returns:
            dict: A dictionary of Gradio components for the chat interface
        """
        with gr.Column():
            # Chatbot and image instruction
            chatbot = create_chatbot_component()
            image_instruction = create_image_instruction()

            # Message input and send button
            with gr.Row():
                msg = gr.Textbox(
                    label="Text Input",
                    placeholder="Enter text and press enter key/send button",
                    scale=9,
                    container=True,
                    show_label=False,
                )
                send_btn = gr.Button("Send", interactive=False)

            # Image and functional buttons
            with gr.Row():
                upload_btn = gr.UploadButton("📁 Upload Image", file_types=["image"], file_count="single")
                regenerate_btn = gr.Button("🔄 Regenerate")
                clear_btn = gr.Button("🗑️ Clear History")

            # Image processing buttons
            with gr.Row():
                extract_btn = gr.Button("📝 Extract Text", interactive=False)
                caption_btn = gr.Button("💭 Caption Image", interactive=False)
                summarize_btn = gr.Button("📋 Summarize Image", interactive=False)

            # Image display
            with gr.Row():
                gallery = gr.Gallery(
                    label="Uploaded Image",
                    show_label=True,
                    columns=2,
                    rows=1,
                    object_fit="scale-down",
                )

            # TTS section
            gr.Markdown("### Text-to-Speech Options")

            # Audio output
            with gr.Row():
                audio_output = gr.Audio(label="Generated Speech", interactive=False)

            # Voice type and speed controls
            with gr.Row():
                voice_type = create_voice_type_dropdown()
                speed = create_speed_slider()
                tts_btn = gr.Button("🔊 Play Last Response")

            # Performance and status indicators
            with gr.Row():
                tts_status = gr.Textbox(
                    label="TTS Status",
                    interactive=False,
                    value="Idle"
                )
                performance_metrics = create_mllm_status()

            # Components to be returned for event binding
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