"""
Guide Interface Module for HearSee Application.

This module provides a comprehensive guide and documentation for the HearSee
application. It creates a Markdown-based help interface that explains all
features, functionality, and technical details of the application to users.

The guide includes sections on:
- Image upload and analysis features
- Chat functionality
- Text-to-speech options
- Technical details and troubleshooting
"""

import gradio as gr

# Module-level function for direct import
def create_guide_interface():
    """
    Create the guide interface for the application.
    
    This is a module-level convenience function that delegates to the
    GuideInterface class's static method.
    
    Returns:
        gr.Markdown: Markdown guide component with formatted documentation
    
    Example:
        guide = create_guide_interface()
        # Can be added to a Gradio interface
        with gr.Blocks() as demo:
            guide_tab = gr.Tab("Help")
            with guide_tab:
                guide
    """
    return GuideInterface.create_guide()

class GuideInterface:
    @staticmethod
    def create_guide():
        """
        Create the guide interface with detailed information about the application.
        
        This method generates a comprehensive Markdown document that serves as
        the user manual for the HearSee application. It includes instructions
        for all features, technical details, and troubleshooting information.
        
        Returns:
            gr.Markdown: Markdown component with formatted application guide
        
        Example:
            guide = GuideInterface.create_guide()
            # Can be added to a Gradio interface
            with gr.Blocks() as demo:
                with gr.Tab("Help"):
                    guide
        """
        # Create a comprehensive user guide with markdown formatting
        # The guide is structured in sections with clear headings and emoji for visual appeal
        return gr.Markdown("""
        # HearSee Web Application Guide

        ## Welcome to HearSee: Your Multimodal Learning Tool

        ### 🖼️ Image Upload & Analysis
        1. **Upload an Image**
           - Click the "Upload Image" button (supports only one image at a time)
           - Select an image file (JPG, PNG, etc.)
           - Maximum file size: 10MB

        2. **Image Analysis Features**
           - **Extract Text**: Automatically detect and transcribe text in images
           - **Caption Image**: Generate detailed image descriptions
           - **Summarize Image**: Provide comprehensive contextual analysis

        ### 💬 Chat Functionality
        - After uploading an image, type your message in the chat box
        - AI will respond based on the uploaded image
        - Regenerate responses or clear chat history as needed

        ### 🔊 Text-to-Speech Options
        - Convert AI responses to speech
        - Choose from multiple voices:
          * Female: River (American), Bella (American), Emma (British)
          * Male: Michael (American), Fenrir (American), George (British)
        - Adjust speech speed from 0.5x to 2.0x

        ### 📊 Performance Metrics
        - View real-time processing details
        - Track response latency and word count

        ## Technical Details
        - Gradio-based interface
        - Qwen 2 VL 7B for vision and language understanding
        - Kokoro TTS for speech synthesis
        - Python backend with Replicate API integration

        ## Privacy Note
        - No data is stored persistently
        - All interactions are session-based
        - Compliant with privacy regulations

        ## Troubleshooting
        - Ensure a stable internet connection
        - Check Replicate API key is valid
        - Refresh page if experiencing issues

        ### Enjoy HearSee - Your Learning Assistant! 🙉🙈✨
        """)