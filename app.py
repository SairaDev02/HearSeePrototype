"""
HearSee - Multimodal Chat Application with Vision and Voice Capabilities

This is the main entry point for the HearSee application, which integrates
image understanding and text-to-speech capabilities. The application provides
a user-friendly interface for uploading images, analyzing them with AI vision models,
and converting text responses to speech.

The application is built using Gradio for the web interface, with modular services
for image processing, AI model integration via Replicate, and text-to-speech conversion.
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
    
    This function initializes the Gradio interface with custom theming,
    sets up the chat and guide tabs, and connects all event handlers
    for the interactive elements.
    
    Returns:
        gr.Blocks: Configured Gradio application ready to be launched
    
    Example:
        app = create_app()
        app.launch()
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
        
        # Shared state variables to track application status across components
        image_uploaded_state = gr.State(value=False)  # Tracks whether an image is currently uploaded
        processing_status = gr.State(value=False)     # Tracks whether processing is currently happening
        
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
                
                # Hidden image component for processing - stores the actual image data
                # but isn't visible to the user (gallery is used for display)
                image_output = gr.Image(type="numpy", visible=False)
                
                # Processing indicator - shown when the system is processing a request
                # Hidden by default, only shown during active processing
                processing_indicator = gr.HTML(
                    visible=False,
                    value="<div class='processing-indicator'>⏳ Processing... Please wait.</div>"
                )
                
                # Define helper functions
                def process_chat_message(message, history, metrics, image=None):
                    """Process a chat message and return updated history and metrics.
                    
                    This function handles the core functionality of processing user messages
                    with the uploaded image. It validates inputs, calls the vision model,
                    and formats the response.
                    
                    Args:
                        message (str): The user's text message
                        history (list): The conversation history as a list of [user, bot] message pairs
                        metrics (str): Current performance metrics string
                        image (numpy.ndarray, optional): The uploaded image data. Defaults to None.
                    
                    Returns:
                        tuple: (updated_history, updated_metrics)
                            - updated_history (list): Conversation history with new message pair
                            - updated_metrics (str): Updated performance metrics string
                    
                    Raises:
                        Exception: If any error occurs during processing
                    
                    Example:
                        history, metrics = process_chat_message("Describe this image",
                                                               previous_history,
                                                               "Latency: N/A | Words: N/A",
                                                               image_data)
                    """
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
                        # Convert image to base64 for API transmission
                        img_str = ImageService.image_to_base64(image)
                        
                        # Build system prompt that defines the AI assistant's role and capabilities
                        system_prompt = "You are a helpful AI assistant specializing in analyzing images and providing detailed information."
                        
                        # Convert conversation history to a formatted context string
                        # This preserves the conversation flow for the model
                        context = ""
                        for h in history:
                            if h[0] is not None:  # Skip entries with no user message
                                context += f"User: {h[0]}\nAssistant: {h[1]}\n\n"
                        
                        logger.debug("Running vision model")
                        # Run the vision model with the complete prompt context and image
                        result = ReplicateService.run_vision_model(
                            f"{system_prompt}\n\nConversation History:\n{context}\nUser: {message}\nAssistant:",
                            image_base64=img_str
                        )
                        
                        # Calculate performance metrics for user feedback
                        end_time = time.time()
                        latency = end_time - start_time  # Total processing time in seconds
                        word_count = len(result.split())  # Approximate word count of response
                        updated_metrics = f"Latency: {latency:.2f}s | Words: {word_count}"
                        
                        logger.info(f"Chat message processed successfully in {latency:.2f}s")
                        # Return updated history and metrics
                        return history + [[message, result]], updated_metrics
                    except Exception as e:
                        logger.error(f"Error processing chat message: {str(e)}", exc_info=True)
                        error_msg = f"Sorry, I encountered an error: {str(e)}"
                        return history + [[message, error_msg]], "Error: System unavailable. Please try again."
                
                def regenerate_last_response(history, metrics, image=None):
                    """Regenerate the last bot message.
                    
                    This function extracts the last user message from history,
                    removes the last response pair, and generates a new response.
                    
                    Args:
                        history (list): The conversation history as a list of [user, bot] message pairs
                        metrics (str): Current performance metrics string
                        image (numpy.ndarray, optional): The uploaded image data. Defaults to None.
                    
                    Returns:
                        tuple: (updated_history, updated_metrics)
                            - updated_history (list): Conversation history with regenerated response
                            - updated_metrics (str): Updated performance metrics string
                    
                    Example:
                        new_history, new_metrics = regenerate_last_response(history, metrics, image)
                    """
                    if not history:
                        return history, metrics
                    
                    # Extract the last user message from history
                    last_user_msg = history[-1][0]
                    if last_user_msg is None:  # Skip if there's no valid user message
                        return history, metrics
                    
                    # Remove the last conversation pair to regenerate response
                    new_history = history[:-1]
                    
                    try:
                        response, updated_metrics = process_chat_message(last_user_msg, new_history, metrics, image)
                        return response, updated_metrics
                    except Exception as e:
                        return new_history + [[last_user_msg, f"Error regenerating response: {str(e)}"]], "Error: System unavailable. Please try again."
                
                def text_to_speech_conversion(history, voice_type, speed):
                    """Convert last bot message to speech.
                    
                    This function extracts the last bot message from the conversation history
                    and converts it to speech using the specified voice type and speed.
                    
                    Args:
                        history (list): The conversation history as a list of [user, bot] message pairs
                        voice_type (str): The type of voice to use for TTS
                        speed (float): The speed factor for speech playback
                    
                    Returns:
                        tuple: (audio_file, status_message)
                            - audio_file (str or None): Path to the generated audio file or None if failed
                            - status_message (str): Status message indicating success or failure
                    
                    Example:
                        audio, status = text_to_speech_conversion(history, "female", 1.0)
                    """
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
                    """Update button states based on image presence.
                    
                    This function enables or disables UI buttons depending on whether
                    an image has been uploaded.
                    
                    Args:
                        image (numpy.ndarray or None): The uploaded image data or None
                    
                    Returns:
                        tuple: (send_btn_update, extract_btn_update, caption_btn_update,
                               summarize_btn_update, image_uploaded_state, image_instruction_update)
                            - Various gr.update objects to update UI components
                            - Boolean state indicating if image is uploaded
                    
                    Example:
                        updates = update_button_state(image_data)
                    """
                    # Determine if buttons should be enabled based on image presence
                    is_enabled = image is not None
                    return (
                        gr.update(interactive=is_enabled),  # send_btn - only active with image
                        gr.update(interactive=is_enabled),  # extract_btn - only active with image
                        gr.update(interactive=is_enabled),  # caption_btn - only active with image
                        gr.update(interactive=is_enabled),  # summarize_btn - only active with image
                        is_enabled,                         # image_uploaded_state - tracks if image exists
                        gr.update(visible=not is_enabled)   # image_instruction - hide when image uploaded
                    )
                
                # Connect event handlers for image upload and processing
                # 1. For image upload - this is the entry point for most interactions
                upload_btn.upload(
                    # Lambda function to store image in both hidden component and visible gallery
                    # If image is None, gallery gets empty list, otherwise a list with the image
                    lambda x: (x, [x] if x is not None else []),
                    upload_btn,  # Input is the upload button itself
                    [image_output, gallery]  # Outputs are the hidden image storage and visible gallery
                ).then(
                    # After image upload, update UI state based on image presence
                    update_button_state,
                    inputs=[image_output],  # Input is the uploaded image
                    outputs=[send_btn, extract_btn, caption_btn, summarize_btn,
                             image_uploaded_state, image_instruction]  # Update multiple UI elements
                )
                
                # Helper function for UI state transitions
                def start_processing():
                    """Set processing state to True and disable interactive elements.
                    
                    This function updates the UI to show a processing indicator and
                    disables all interactive elements to prevent multiple submissions
                    while processing is in progress.
                    
                    Returns:
                        tuple: Updates for multiple UI components to show processing state
                    
                    Example:
                        ui_updates = start_processing()
                    """
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
                    """Reset processing state and re-enable interactive elements.
                    
                    This function updates the UI to hide the processing indicator and
                    re-enables interactive elements after processing is complete.
                    
                    Args:
                        chatbot_val (list): The current chatbot conversation history
                        metrics_val (str): The current performance metrics
                        image_uploaded_state (bool): Whether an image is currently uploaded
                    
                    Returns:
                        tuple: Updates for multiple UI components to restore interactive state
                    
                    Example:
                        ui_updates = end_processing(chatbot, metrics, True)
                    """
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
                    """End processing specifically for TTS operations.
                    
                    Similar to end_processing but specifically for text-to-speech operations,
                    updating the audio output and TTS status components.
                    
                    Args:
                        audio_val (str): Path to the generated audio file
                        status_val (str): Status message for TTS operation
                        image_uploaded_state (bool): Whether an image is currently uploaded
                    
                    Returns:
                        tuple: Updates for multiple UI components to restore interactive state
                              after TTS processing
                    
                    Example:
                        ui_updates = end_processing_tts(audio_path, "Success", True)
                    """
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
                    """Process chat message and clear input field.
                    
                    This function processes the chat message and returns the updated history,
                    metrics, and an empty string to clear the input field.
                    
                    Args:
                        message (str): The user's text message
                        history (list): The conversation history
                        metrics (str): Current performance metrics
                        image (numpy.ndarray, optional): The uploaded image. Defaults to None.
                    
                    Returns:
                        tuple: (updated_history, updated_metrics, empty_string)
                    
                    Example:
                        history, metrics, _ = locked_chat_response("Hello", [], "Latency: N/A", None)
                    """
                    updated_history, updated_metrics = process_chat_message(message, history, metrics, image)
                    return updated_history, updated_metrics, ""  # Clear the input field
                
                # Event chain for message submission via Enter key
                # This creates a three-step process: 1) Show processing state, 2) Process message, 3) Restore UI
                send_handler = msg.submit(
                    # Step 1: Show processing state and disable all interactive elements
                    start_processing,
                    inputs=None,  # No inputs needed
                    outputs=[processing_indicator, msg, send_btn, upload_btn, extract_btn,
                             caption_btn, summarize_btn, regenerate_btn, tts_btn, processing_status]
                ).then(
                    # Step 2: Process the message with the AI model
                    locked_chat_response,
                    inputs=[msg, chatbot, performance_metrics, image_output],  # Message and context
                    outputs=[chatbot, performance_metrics, msg],  # Updated conversation and metrics
                    show_progress="full"  # Show progress bar during processing
                ).then(
                    # Step 3: Restore UI state after processing completes
                    end_processing,
                    inputs=[chatbot, performance_metrics, image_uploaded_state],  # Current state
                    outputs=[chatbot, performance_metrics, processing_indicator, msg, send_btn,
                             upload_btn, extract_btn, caption_btn, summarize_btn,
                             regenerate_btn, tts_btn, processing_status]  # UI elements to update
                )
                
                # Same event chain for send button click (identical to Enter key submission)
                # This provides an alternative way to submit messages for users who prefer clicking
                send_btn.click(
                    # Step 1: Show processing state
                    start_processing,
                    inputs=None,
                    outputs=[processing_indicator, msg, send_btn, upload_btn, extract_btn,
                             caption_btn, summarize_btn, regenerate_btn, tts_btn, processing_status]
                ).then(
                    # Step 2: Process the message
                    locked_chat_response,
                    inputs=[msg, chatbot, performance_metrics, image_output],
                    outputs=[chatbot, performance_metrics, msg],
                    show_progress="full"
                ).then(
                    # Step 3: Restore UI state
                    end_processing,
                    inputs=[chatbot, performance_metrics, image_uploaded_state],
                    outputs=[chatbot, performance_metrics, processing_indicator, msg, send_btn,
                             upload_btn, extract_btn, caption_btn, summarize_btn,
                             regenerate_btn, tts_btn, processing_status]
                )
                
                # Helper function for clearing the interface
                def clear_interface_state():
                    """Reset all interface elements to their initial state.
                    
                    This function resets the entire UI to its initial state, clearing
                    the conversation history, uploaded images, and resetting all controls.
                    
                    Returns:
                        tuple: Updates for all UI components to reset to initial state
                    
                    Example:
                        ui_updates = clear_interface_state()
                    """
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
                
                # 4. For regenerate button - allows user to get a new response to the last question
                # Follows the same three-step pattern as other interactions
                regenerate_btn.click(
                    # Step 1: Show processing state
                    start_processing,
                    inputs=None,
                    outputs=[processing_indicator, msg, send_btn, upload_btn, extract_btn,
                             caption_btn, summarize_btn, regenerate_btn, tts_btn, processing_status]
                ).then(
                    # Step 2: Regenerate the last response using the same image and last user message
                    regenerate_last_response,
                    inputs=[chatbot, performance_metrics, image_output],
                    outputs=[chatbot, performance_metrics],
                    show_progress="full"
                ).then(
                    # Step 3: Restore UI state
                    end_processing,
                    inputs=[chatbot, performance_metrics, image_uploaded_state],
                    outputs=[chatbot, performance_metrics, processing_indicator, msg, send_btn,
                             upload_btn, extract_btn, caption_btn, summarize_btn,
                             regenerate_btn, tts_btn, processing_status]
                )
                
                # 5. For extract text button - specialized function to extract text from images
                # Uses OCR (Optical Character Recognition) via the ImageUtils service
                extract_btn.click(
                    # Step 1: Show processing state
                    start_processing,
                    inputs=None,
                    outputs=[processing_indicator, msg, send_btn, upload_btn, extract_btn,
                             caption_btn, summarize_btn, regenerate_btn, tts_btn, processing_status]
                ).then(
                    # Step 2: Extract text from the image using OCR
                    ImageUtils.extract_text,  # External utility function for OCR
                    inputs=[image_output, chatbot],  # Image data and current conversation
                    outputs=[chatbot, performance_metrics]  # Updated with extraction results
                ).then(
                    # Step 3: Restore UI state
                    end_processing,
                    inputs=[chatbot, performance_metrics, image_uploaded_state],
                    outputs=[chatbot, performance_metrics, processing_indicator, msg, send_btn,
                             upload_btn, extract_btn, caption_btn, summarize_btn,
                             regenerate_btn, tts_btn, processing_status]
                )
                
                # 6. For caption image button - generates a descriptive caption for the image
                # Uses AI vision models to create a concise description
                caption_btn.click(
                    # Step 1: Show processing state
                    start_processing,
                    inputs=None,
                    outputs=[processing_indicator, msg, send_btn, upload_btn, extract_btn,
                             caption_btn, summarize_btn, regenerate_btn, tts_btn, processing_status]
                ).then(
                    # Step 2: Generate caption for the image
                    ImageUtils.caption_image,  # External utility for image captioning
                    inputs=[image_output, chatbot],  # Image data and current conversation
                    outputs=[chatbot, performance_metrics]  # Updated with caption results
                ).then(
                    # Step 3: Restore UI state
                    end_processing,
                    inputs=[chatbot, performance_metrics, image_uploaded_state],
                    outputs=[chatbot, performance_metrics, processing_indicator, msg, send_btn,
                             upload_btn, extract_btn, caption_btn, summarize_btn,
                             regenerate_btn, tts_btn, processing_status]
                )
                
                # 7. For summarize image button - provides a detailed analysis of the image
                # More comprehensive than caption, includes content, context, and details
                summarize_btn.click(
                    # Step 1: Show processing state
                    start_processing,
                    inputs=None,
                    outputs=[processing_indicator, msg, send_btn, upload_btn, extract_btn,
                             caption_btn, summarize_btn, regenerate_btn, tts_btn, processing_status]
                ).then(
                    # Step 2: Generate detailed summary of the image
                    ImageUtils.summarize_image,  # External utility for image summarization
                    inputs=[image_output, chatbot],  # Image data and current conversation
                    outputs=[chatbot, performance_metrics]  # Updated with summary results
                ).then(
                    # Step 3: Restore UI state
                    end_processing,
                    inputs=[chatbot, performance_metrics, image_uploaded_state],
                    outputs=[chatbot, performance_metrics, processing_indicator, msg, send_btn,
                             upload_btn, extract_btn, caption_btn, summarize_btn,
                             regenerate_btn, tts_btn, processing_status]
                )
                
                # 8. For TTS button - converts the last bot response to speech
                # Uses a different end processing function specific to TTS operations
                tts_btn.click(
                    # Step 1: Show processing state
                    start_processing,
                    inputs=None,
                    outputs=[processing_indicator, msg, send_btn, upload_btn, extract_btn,
                             caption_btn, summarize_btn, regenerate_btn, tts_btn, processing_status]
                ).then(
                    # Step 2: Convert text to speech with selected voice and speed
                    text_to_speech_conversion,
                    inputs=[chatbot, voice_type, speed],  # Conversation history and TTS parameters
                    outputs=[audio_output, tts_status]  # Audio file path and status message
                ).then(
                    # Step 3: Restore UI state with TTS-specific handler
                    # This handler updates audio components in addition to standard UI elements
                    end_processing_tts,
                    inputs=[audio_output, tts_status, image_uploaded_state],
                    outputs=[audio_output, tts_status, processing_indicator, msg, send_btn,
                             upload_btn, extract_btn, caption_btn, summarize_btn,
                             regenerate_btn, tts_btn, processing_status]
                )
                
            # Create the Guide tab with usage instructions
            with gr.Tab("Guide"):
                # Use the modular GuideInterface to create the guide content
                GuideInterface.create_guide()  # Loads guide content from the UI module
    
    return hearsee

# Run the application when directly executed
if __name__ == "__main__":
    logger.info("Starting HearSee application")
    app = create_app()
    logger.info("Launching Gradio interface")
    app.launch(share=False, inbrowser=True)  # Launch locally and open in browser
    logger.info("HearSee application stopped")