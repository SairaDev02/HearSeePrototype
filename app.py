"""
HearSee - Multimodal Chat Application with Vision and Voice Capabilities

This is the main entry point for the HearSee application, which integrates
image understanding and text-to-speech capabilities.
"""

import gradio as gr
import time
import os
from tempfile import NamedTemporaryFile
import requests
from dotenv import load_dotenv
import logging

# Import from our modular components
from config.settings import INIT_HISTORY
from config.logging_config import configure_logging
from services.image_service import ImageService
from services.replicate_service import ReplicateService
from services.tts_service import TTSService
from utils.validators import get_last_bot_message, validate_image_input
from utils.image_utils import ImageUtils
from ui import ChatInterface, GuideInterface, UIStateManager

# Load environment variables and configure logging
load_dotenv()
configure_logging()
logger = logging.getLogger(__name__)

def create_app():
    """
    Create and configure the HearSee application.
    
    Returns:
        gr.Blocks: Configured Gradio application
    """
    # Create custom theming with compatibility for different Gradio versions
    try:
        # Try to create theme with the new method (for newer Gradio versions)
        system_theme = gr.themes.Soft(
            primary_hue="blue",
            secondary_hue="blue",
            neutral_hue="gray",
            text_size=gr.themes.sizes.text_md,
            font="system-ui",
        ).set(
            # Force light mode by setting these properties
            body_background_fill="white",
            background_fill_primary="white",
            background_fill_secondary="#f7f7f7",
            block_title_text_color="black",
            block_label_text_color="black",
            input_background_fill="#ffffff",
            body_text_color="black",
        )
    except (TypeError, AttributeError):
        # Fallback for older Gradio versions
        system_theme = gr.themes.Soft(
            primary_hue="blue",
            secondary_hue="blue",
            neutral_hue="gray",
            text_size=gr.themes.sizes.text_md,
            font="system-ui",
        )
    
    # Create the main application with theme
    with gr.Blocks(theme=system_theme, title="HearSee") as hearsee:
        gr.Markdown("# HearSee: Multimodal Chat Application Tool with Vision and Voice")
        
        # Shared state
        image_uploaded_state = gr.State(value=False)
        processing_status = gr.State(value=False)
        
        with gr.Tabs():
            with gr.Tab("Chat"):
                # Get chat components
                components = ChatInterface.create_interface()
                
                # Extract components for event handling
                chatbot = components["chatbot"]
                msg = components["msg"]
                send_btn = components["send_btn"]
                upload_btn = components["upload_btn"]
                regenerate_btn = components["regenerate_btn"]
                clear_btn = components["clear_btn"]
                extract_btn = components["extract_btn"]
                caption_btn = components["caption_btn"]
                summarize_btn = components["summarize_btn"]
                gallery = components["gallery"]
                voice_type = components["voice_type"]
                speed = components["speed"]
                tts_btn = components["tts_btn"]
                tts_status = components["tts_status"]
                performance_metrics = components["performance_metrics"]
                audio_output = components["audio_output"]
                image_instruction = components["image_instruction"]
                
                # Hidden image component for processing
                image_output = gr.Image(type="numpy", visible=False)
                
                # Processing indicator
                processing_indicator = gr.HTML(
                    visible=False,
                    value="<div class='processing-indicator'>⏳ Processing... Please wait.</div>"
                )
                
                # Define helper functions
                def process_chat_message(message, history, metrics, image=None):
                    """Process a chat message and return updated history and metrics."""
                    start_time = time.time()
                    logger.info(f"Processing chat message: {message[:50]}{'...' if len(message) > 50 else ''}")
                    
                    # Check image size
                    size_valid, size_msg = ImageService.verify_image_size(image)
                    if not size_valid:
                        logger.warning(f"Image size validation failed: {size_msg}")
                        return history + [[message, size_msg]], "Error: Image too large"
                    
                    # Check API availability
                    api_available, error_msg = ReplicateService.verify_api_available()
                    if not api_available:
                        logger.error(f"API unavailable: {error_msg}")
                        return history + [[message, error_msg]], "Error: API unavailable"
                    
                    # Validate image requirement
                    valid_img, img_error = validate_image_input(image)
                    if not valid_img:
                        logger.warning(f"Image validation failed: {img_error}")
                        return history + [[message, img_error]], "Error: Image required"
                    
                    # Process the message
                    try:
                        # Convert image to base64
                        img_str = ImageService.image_to_base64(image)
                        
                        # Build system prompt
                        system_prompt = "You are a helpful AI assistant specializing in analyzing images and providing detailed information."
                        
                        # Convert history to context
                        context = ""
                        for h in history:
                            if h[0] is not None:
                                context += f"User: {h[0]}\nAssistant: {h[1]}\n\n"
                        
                        logger.debug("Running vision model")
                        # Run model
                        result = ReplicateService.run_vision_model(
                            f"{system_prompt}\n\nConversation History:\n{context}\nUser: {message}\nAssistant:",
                            image_base64=img_str
                        )
                        
                        # Calculate metrics
                        end_time = time.time()
                        latency = end_time - start_time
                        word_count = len(result.split())
                        updated_metrics = f"Latency: {latency:.2f}s | Words: {word_count}"
                        
                        logger.info(f"Chat message processed successfully in {latency:.2f}s")
                        # Return updated history and metrics
                        return history + [[message, result]], updated_metrics
                    except Exception as e:
                        logger.error(f"Error processing chat message: {str(e)}", exc_info=True)
                        error_msg = f"Sorry, I encountered an error: {str(e)}"
                        return history + [[message, error_msg]], "Error: System unavailable. Please try again."
                
                def regenerate_last_response(history, metrics, image=None):
                    """Regenerate the last bot message."""
                    if not history:
                        return history, metrics
                    
                    last_user_msg = history[-1][0]
                    if last_user_msg is None:
                        return history, metrics
                    
                    new_history = history[:-1]
                    
                    try:
                        response, updated_metrics = process_chat_message(last_user_msg, new_history, metrics, image)
                        return response, updated_metrics
                    except Exception as e:
                        return new_history + [[last_user_msg, f"Error regenerating response: {str(e)}"]], "Error: System unavailable. Please try again."
                
                def text_to_speech_conversion(history, voice_type, speed):
                    """Convert last bot message to speech."""
                    text = get_last_bot_message(history)
                    logger.info(f"Converting text to speech with voice: {voice_type}, speed: {speed}")
                    result = TTSService.process_audio(text, voice_type, speed)
                    if result[0] is None:
                        logger.warning(f"TTS conversion failed: {result[1]}")
                    else:
                        logger.info("TTS conversion successful")
                    return result
                
                # Helper function to update button states based on image presence
                def update_button_state(image):
                    """Update button states based on image presence."""
                    is_enabled = image is not None
                    return (
                        gr.update(interactive=is_enabled),  # send_btn
                        gr.update(interactive=is_enabled),  # extract_btn
                        gr.update(interactive=is_enabled),  # caption_btn
                        gr.update(interactive=is_enabled),  # summarize_btn
                        is_enabled,                         # image_uploaded_state
                        gr.update(visible=not is_enabled)   # image_instruction
                    )
                
                # Connect event handlers for image upload and processing
                # 1. For image upload
                upload_btn.upload(
                    lambda x: (x, [x] if x is not None else []),
                    upload_btn,
                    [image_output, gallery]
                ).then(
                    update_button_state,
                    inputs=[image_output],
                    outputs=[send_btn, extract_btn, caption_btn, summarize_btn, 
                             image_uploaded_state, image_instruction]
                )
                
                # Helper function for UI state transitions
                def start_processing():
                    """Set processing state to True and disable interactive elements."""
                    return (
                        gr.update(visible=True),       # processing_indicator
                        gr.update(interactive=False),  # msg
                        gr.update(interactive=False),  # send_btn
                        gr.update(interactive=False),  # upload_btn
                        gr.update(interactive=False),  # extract_btn
                        gr.update(interactive=False),  # caption_btn
                        gr.update(interactive=False),  # summarize_btn
                        gr.update(interactive=False),  # regenerate_btn
                        gr.update(interactive=False),  # tts_btn
                        True                           # processing_status
                    )
                
                def end_processing(chatbot_val, metrics_val, image_uploaded_state):
                    """Reset processing state and re-enable interactive elements."""
                    return (
                        chatbot_val,                                # chatbot
                        metrics_val,                                # performance_metrics
                        gr.update(visible=False),                   # processing_indicator
                        gr.update(interactive=True),                # msg
                        gr.update(interactive=image_uploaded_state),# send_btn
                        gr.update(interactive=True),                # upload_btn
                        gr.update(interactive=image_uploaded_state),# extract_btn
                        gr.update(interactive=image_uploaded_state),# caption_btn
                        gr.update(interactive=image_uploaded_state),# summarize_btn
                        gr.update(interactive=True),                # regenerate_btn
                        gr.update(interactive=True),                # tts_btn
                        False                                       # processing_status
                    )
                
                def end_processing_tts(audio_val, status_val, image_uploaded_state):
                    """End processing specifically for TTS operations."""
                    return (
                        audio_val,                                  # audio_output
                        status_val,                                 # tts_status
                        gr.update(visible=False),                   # processing_indicator
                        gr.update(interactive=True),                # msg
                        gr.update(interactive=image_uploaded_state),# send_btn
                        gr.update(interactive=True),                # upload_btn
                        gr.update(interactive=image_uploaded_state),# extract_btn
                        gr.update(interactive=image_uploaded_state),# caption_btn
                        gr.update(interactive=image_uploaded_state),# summarize_btn
                        gr.update(interactive=True),                # regenerate_btn
                        gr.update(interactive=True),                # tts_btn
                        False                                       # processing_status
                    )
                
                # 2. For sending messages
                def locked_chat_response(message, history, metrics, image=None):
                    updated_history, updated_metrics = process_chat_message(message, history, metrics, image)
                    return updated_history, updated_metrics, ""  # Clear the input field
                
                send_handler = msg.submit(
                    start_processing,
                    inputs=None,
                    outputs=[processing_indicator, msg, send_btn, upload_btn, extract_btn,
                             caption_btn, summarize_btn, regenerate_btn, tts_btn, processing_status]
                ).then(
                    locked_chat_response,
                    inputs=[msg, chatbot, performance_metrics, image_output],
                    outputs=[chatbot, performance_metrics, msg],
                    show_progress="full"
                ).then(
                    end_processing,
                    inputs=[chatbot, performance_metrics, image_uploaded_state],
                    outputs=[chatbot, performance_metrics, processing_indicator, msg, send_btn, 
                             upload_btn, extract_btn, caption_btn, summarize_btn, 
                             regenerate_btn, tts_btn, processing_status]
                )
                
                # Same for send button
                send_btn.click(
                    start_processing,
                    inputs=None,
                    outputs=[processing_indicator, msg, send_btn, upload_btn, extract_btn,
                             caption_btn, summarize_btn, regenerate_btn, tts_btn, processing_status]
                ).then(
                    locked_chat_response,
                    inputs=[msg, chatbot, performance_metrics, image_output],
                    outputs=[chatbot, performance_metrics, msg],
                    show_progress="full"
                ).then(
                    end_processing,
                    inputs=[chatbot, performance_metrics, image_uploaded_state],
                    outputs=[chatbot, performance_metrics, processing_indicator, msg, send_btn, 
                             upload_btn, extract_btn, caption_btn, summarize_btn, 
                             regenerate_btn, tts_btn, processing_status]
                )
                
                # Helper function for clearing the interface
                def clear_interface_state():
                    """Reset all interface elements to their initial state."""
                    return (
                        INIT_HISTORY,                    # chatbot
                        "Latency: N/A | Words: N/A",     # performance_metrics
                        gr.update(visible=False),        # processing_indicator
                        gr.update(interactive=True, value=""), # msg
                        gr.update(interactive=False),    # send_btn
                        gr.update(interactive=True),     # upload_btn
                        gr.update(interactive=False),    # extract_btn
                        gr.update(interactive=False),    # caption_btn
                        gr.update(interactive=False),    # summarize_btn
                        gr.update(interactive=True),     # regenerate_btn
                        gr.update(interactive=True),     # tts_btn
                        False,                           # processing_status
                        [],                              # gallery
                        None,                            # image_output
                        False,                           # image_uploaded_state
                        gr.update(visible=True)          # image_instruction
                    )
                
                # 3. For clear history button
                clear_btn.click(
                    clear_interface_state,
                    inputs=None,
                    outputs=[chatbot, performance_metrics, processing_indicator, msg, send_btn,
                             upload_btn, extract_btn, caption_btn, summarize_btn, regenerate_btn,
                             tts_btn, processing_status, gallery, image_output, 
                             image_uploaded_state, image_instruction]
                )
                
                # 4. For regenerate button
                regenerate_btn.click(
                    start_processing,
                    inputs=None,
                    outputs=[processing_indicator, msg, send_btn, upload_btn, extract_btn,
                             caption_btn, summarize_btn, regenerate_btn, tts_btn, processing_status]
                ).then(
                    regenerate_last_response,
                    inputs=[chatbot, performance_metrics, image_output],
                    outputs=[chatbot, performance_metrics],
                    show_progress="full"
                ).then(
                    end_processing,
                    inputs=[chatbot, performance_metrics, image_uploaded_state],
                    outputs=[chatbot, performance_metrics, processing_indicator, msg, send_btn, 
                             upload_btn, extract_btn, caption_btn, summarize_btn, 
                             regenerate_btn, tts_btn, processing_status]
                )
                
                # 5. For extract text button
                extract_btn.click(
                    start_processing,
                    inputs=None,
                    outputs=[processing_indicator, msg, send_btn, upload_btn, extract_btn,
                             caption_btn, summarize_btn, regenerate_btn, tts_btn, processing_status]
                ).then(
                    ImageUtils.extract_text,
                    inputs=[image_output, chatbot],
                    outputs=[chatbot, performance_metrics]
                ).then(
                    end_processing,
                    inputs=[chatbot, performance_metrics, image_uploaded_state],
                    outputs=[chatbot, performance_metrics, processing_indicator, msg, send_btn, 
                             upload_btn, extract_btn, caption_btn, summarize_btn, 
                             regenerate_btn, tts_btn, processing_status]
                )
                
                # 6. For caption image button
                caption_btn.click(
                    start_processing,
                    inputs=None,
                    outputs=[processing_indicator, msg, send_btn, upload_btn, extract_btn,
                             caption_btn, summarize_btn, regenerate_btn, tts_btn, processing_status]
                ).then(
                    ImageUtils.caption_image,
                    inputs=[image_output, chatbot],
                    outputs=[chatbot, performance_metrics]
                ).then(
                    end_processing,
                    inputs=[chatbot, performance_metrics, image_uploaded_state],
                    outputs=[chatbot, performance_metrics, processing_indicator, msg, send_btn, 
                             upload_btn, extract_btn, caption_btn, summarize_btn, 
                             regenerate_btn, tts_btn, processing_status]
                )
                
                # 7. For summarize image button
                summarize_btn.click(
                    start_processing,
                    inputs=None,
                    outputs=[processing_indicator, msg, send_btn, upload_btn, extract_btn,
                             caption_btn, summarize_btn, regenerate_btn, tts_btn, processing_status]
                ).then(
                    ImageUtils.summarize_image,
                    inputs=[image_output, chatbot],
                    outputs=[chatbot, performance_metrics]
                ).then(
                    end_processing,
                    inputs=[chatbot, performance_metrics, image_uploaded_state],
                    outputs=[chatbot, performance_metrics, processing_indicator, msg, send_btn, 
                             upload_btn, extract_btn, caption_btn, summarize_btn, 
                             regenerate_btn, tts_btn, processing_status]
                )
                
                # 8. For TTS button
                tts_btn.click(
                    start_processing,
                    inputs=None,
                    outputs=[processing_indicator, msg, send_btn, upload_btn, extract_btn,
                             caption_btn, summarize_btn, regenerate_btn, tts_btn, processing_status]
                ).then(
                    text_to_speech_conversion,
                    inputs=[chatbot, voice_type, speed],
                    outputs=[audio_output, tts_status]
                ).then(
                    end_processing_tts,
                    inputs=[audio_output, tts_status, image_uploaded_state],
                    outputs=[audio_output, tts_status, processing_indicator, msg, send_btn, 
                             upload_btn, extract_btn, caption_btn, summarize_btn, 
                             regenerate_btn, tts_btn, processing_status]
                )
                
            with gr.Tab("Guide"):
                GuideInterface.create_guide()
    
    return hearsee

# Run the application when directly executed
if __name__ == "__main__":
    logger.info("Starting HearSee application")
    app = create_app()
    logger.info("Launching Gradio interface")
    app.launch(share=False, inbrowser=True)
    logger.info("HearSee application stopped")