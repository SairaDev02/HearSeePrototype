import gradio as gr
import time
import replicate
import os
import tempfile
import base64
from PIL import Image
import io
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Constants for model IDs for easy updates
QWEN_VL_MODEL = "lucataco/qwen2-vl-7b-instruct:bf57361c75677fc33d480d0c5f02926e621b2caa2000347cb74aeae9d2ca07ee"
KOKORO_TTS_MODEL = "jaaari/kokoro-82m:f559560eb822dc509045f3921a1921234918b91739db4bf3daab2169b71c7a13"

# Check if the Replicate API token is set
if "REPLICATE_API_TOKEN" not in os.environ:
    print("Warning: REPLICATE_API_TOKEN not found in environment variables or .env file")
    print("Set API token in the .env file or environment variables")
    REPLICATE_API_AVAILABLE = False
else:
    REPLICATE_API_AVAILABLE = True

def verify_api_available():
    """Check if the API is available before attempting to use it"""
    if not REPLICATE_API_AVAILABLE:
        return False, "Error: Replicate API token not found. Set REPLICATE_API_TOKEN in your .env file."
    return True, ""

def image_to_base64(image):
    """Convert image to base64 for API processing"""
    if image is None:
        return None
    try:
        buffered = io.BytesIO()
        img = Image.fromarray(image)
        img.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode()
    except Exception as e:
        print(f"Error converting image to base64: {e}")
        return None

def chat_response(message, history, performance_metrics):
    """Process user message using Replicate LLM"""
    # Check if API is available first
    api_available, error_msg = verify_api_available()
    if not api_available:
        return error_msg if not history else history + [[message, error_msg]], performance_metrics

    if not message or message.strip() == "":
        return "Please enter a message." if not history else history, performance_metrics

    try:
        # Start measuring time
        start_time = time.time()
        first_token_time = None

        # Build system prompt from chat history
        system_prompt = "You are a helpful AI assistant specializing in analyzing images and providing detailed information."
        # Convert history to context for the LLM
        context = ""
        for h in history:
            if h[0] is not None:  # Check if user message exists
                context += f"User: {h[0]}\nAssistant: {h[1]}\n\n"

        # Call Qwen model for text chat
        output_iterator = replicate.run(
            QWEN_VL_MODEL,
            input={
                "prompt": f"{system_prompt}\n\nConversation History:\n{context}\nUser: {message}\nAssistant:",
                "max_new_tokens": 1024,
                "temperature": 0.7
            },
            stream=True  # Enable streaming to measure time to first token
        )

        # Process the streamed output
        result = ""
        token_count = 0

        for token in output_iterator:
            if first_token_time is None and token:
                first_token_time = time.time()  # Record time of first token

            if token:
                result += token
                token_count += 1

        # Calculate end time and metrics
        end_time = time.time()
        total_time = end_time - start_time
        latency = total_time  # Overall latency

        # Calculate time to first token if we received tokens
        ttft = "N/A"
        if first_token_time is not None:
            ttft = f"{(first_token_time - start_time):.2f}s"

        # Calculate tokens per second
        tps = "N/A"
        if token_count > 0 and total_time > 0:
            tps = f"{token_count / total_time:.2f}"

        # Update performance metrics
        updated_metrics = f"Tokens/sec: {tps} | Time to first token: {ttft} | Latency: {latency:.2f}s"

        return result, updated_metrics
    except Exception as e:
        return f"Sorry, I encountered an error: {str(e)}", "Error: Metrics unavailable"

def extract_text(image, history=None):
    """Extract text from image using Qwen 2 VL model"""
    # Check if API is available first
    api_available, error_msg = verify_api_available()
    if not api_available:
        return [[None, error_msg]] if history is None else history + [[None, error_msg]]

    if image is None:
        return [[None, "Please upload an image first."]] if history is None else history + [[None, "Please upload an image first."]]
    try:
        # Convert the image to base64 for processing
        img_str = image_to_base64(image)
        if img_str is None:
            error_message = "Error processing the image. Please try another image."
            return [[None, error_message]] if history is None else history + [[None, error_message]]

        # Build system prompt
        system_prompt = "You are a helpful AI assistant specializing in extracting text from images."
        user_prompt = "Extract and transcribe all text visible in this image. Be thorough and precise."

        # Call Qwen 2 VL model from Replicate
        output = replicate.run(
            QWEN_VL_MODEL,
            input={
                "prompt": f"{system_prompt}\n\n{user_prompt}",
                "media": f"data:image/png;base64,{img_str}",
                "max_new_tokens": 1024,
                "temperature": 0.5
            }
        )

        # Qwen returns a stream of text, so combine it
        result = "".join(output) if isinstance(output, list) else output

        # Update history with the extracted text result
        user_message = "Please extract the text from this image."
        if history is None:
            return [[user_message, result]]
        else:
            return history + [[user_message, result]]
    except Exception as e:
        error_message = f"Error extracting text: {str(e)}"
        if history is None:
            return [[None, error_message]]
        else:
            return history + [[None, error_message]]

def caption_image(image, history=None):
    """Generate caption for image using Qwen 2 VL model"""
    # Check if API is available first
    api_available, error_msg = verify_api_available()
    if not api_available:
        return [[None, error_msg]] if history is None else history + [[None, error_msg]]

    if image is None:
        return [[None, "Please upload an image first."]] if history is None else history + [[None, "Please upload an image first."]]

    try:
        # Convert the image to base64 for processing
        img_str = image_to_base64(image)
        if img_str is None:
            error_message = "Error processing the image. Please try another image."
            return [[None, error_message]] if history is None else history + [[None, error_message]]

        # Build system prompt
        system_prompt = "You are a helpful AI assistant specializing in describing images in detail."
        user_prompt = "Describe this image in detail, including objects, people, scenery, colors, and composition."

        # Call Qwen 2 VL model from Replicate
        output = replicate.run(
            QWEN_VL_MODEL,
            input={
                "prompt": f"{system_prompt}\n\n{user_prompt}",
                "media": f"data:image/png;base64,{img_str}",
                "max_new_tokens": 1024,
                "temperature": 0.7
            }
        )

        # Qwen returns a stream of text, so combine it
        result = "".join(output) if isinstance(output, list) else output

        # Update history with the caption result
        user_message = "Please describe this image in detail."
        if history is None:
            return [[user_message, result]]
        else:
            return history + [[user_message, result]]
    except Exception as e:
        error_message = f"Error generating caption: {str(e)}"
        if history is None:
            return [[None, error_message]]
        else:
            return history + [[None, error_message]]

def summarize_image(image, history=None):
    """Generate summary for image using Qwen 2 VL model"""
    # Check if API is available first
    api_available, error_msg = verify_api_available()
    if not api_available:
        return [[None, error_msg]] if history is None else history + [[None, error_msg]]

    if image is None:
        return [[None, "Please upload an image first."]] if history is None else history + [[None, "Please upload an image first."]]

    try:
        # Convert the image to base64 for processing
        img_str = image_to_base64(image)
        if img_str is None:
            error_message = "Error processing the image. Please try another image."
            return [[None, error_message]] if history is None else history + [[None, error_message]]

        # Call Qwen 2 VL model from Replicate
        output = replicate.run(
            QWEN_VL_MODEL,
            input={
                "prompt": "Analyze this image and provide a comprehensive summary including objects, people, activities, environment, colors, and mood.",
                "media": f"data:image/png;base64,{img_str}",
                "max_new_tokens": 512,
                "temperature": 0.5
            }
        )

        # Qwen returns a stream of text, so combine it
        result = "".join(output) if isinstance(output, list) else output

        # Update history with the summary result
        user_message = "Please provide a comprehensive summary of this image."
        if history is None:
            return [[user_message, result]]
        else:
            return history + [[user_message, result]]
    except Exception as e:
        error_message = f"Error summarizing image: {str(e)}"
        if history is None:
            return [[None, error_message]]
        else:
            return history + [[None, error_message]]

def regenerate_response(history, performance_metrics):
    """Actually regenerate the last bot message by re-running the model"""
    if not history:
        return history, performance_metrics

    # Get the last user message
    last_user_msg = history[-1][0]

    # If it's None (could be from image operations), return as is
    if last_user_msg is None:
        return history, performance_metrics

    # Remove the last exchange
    new_history = history[:-1]

    # Call the model again with the last user message
    try:
        response, updated_metrics = chat_response(last_user_msg, new_history, performance_metrics)
        return new_history + [[last_user_msg, response]], updated_metrics
    except Exception as e:
        return new_history + [[last_user_msg, f"Error regenerating response: {str(e)}"]], "Error: Metrics unavailable"

def text_to_speech(text, voice_type, speed):
    """Generate audio using Kokoro-82M model via Replicate"""
    # Check if API is available first
    api_available, error_msg = verify_api_available()
    if not api_available:
        return None, error_msg

    if not text:
        return None, "No text to convert to speech."

    try:
        voice_map = {
            "Female Heart (American)": "af_heart",
            "Female Bella (American)": "af_bella",
            "Female Emma (British)": "bf_emma",
            "Male Michael (American)": "am_michael",
            "Male Fenrir (American)": "am_fenrir",
            "Male George (British)": "bm_george"
        }

        voice_id = voice_map.get(voice_type, "af_heart")  # Default to female American voice

        # Validate speed is within acceptable range
        safe_speed = max(0.5, min(2.0, float(speed)))

        # Call Kokoro TTS model
        output = replicate.run(
            KOKORO_TTS_MODEL,
            input={
                "text": text,
                "voice": voice_id,
                "speed": safe_speed
            }
        )

        # Kokoro returns a URL to the audio file
        audio_url = output

        # For Gradio, we should return the URL
        return audio_url, f"Generated audio using {voice_type} voice at {safe_speed}x speed"
    except Exception as e:
        return None, f"Error generating speech: {str(e)}"

def get_last_bot_message(history):
    """Extract the last bot message from chat history."""
    if not history:
        return "No messages to convert to speech."
    return history[-1][1]

def create_chat_interface():
    # Initial system prompt as chat history
    initial_history = [
        ["Hello! Can you help me analyze an image?", "Of course! I'd be happy to help. You can upload an image using the Upload Image button below."],
        ["What kind of images can I upload?", "You can upload most common image formats (JPG, PNG, etc.). Once uploaded, I can help you with:\n- Extracting text from the image\n- Generating image captions\n- Providing detailed image summaries\n I can also convert text to speech for you."],
        ["That sounds great!", "Feel free to upload an image whenever you're ready. I'm here to help! 😊"]
    ]
    with gr.Column():
        # Add styles using elem_classes
        chatbot = gr.Chatbot(
            value=initial_history,
            height=400,
            elem_classes="chatbox-style"
        )

        # Add custom styles to the page
        gr.HTML("""
            <style>
            .chatbox-style {
                border: 1px solid #ccc !important;
                border-radius: 8px !important;
                padding: 10px !important;
                background-color: #f9f9f9 !important;
            }
            </style>
        """)

        with gr.Row():
            msg = gr.Textbox(
                label="Type your message here...",
                placeholder="Enter text and press enter",
                scale=9,
                container=False
            )
            send_btn = gr.Button("Send", scale=1)

        with gr.Row():
            upload_btn = gr.UploadButton("📁 Upload Image", file_types=["image"])
            regenerate_btn = gr.Button("🔄 Regenerate")
            clear_btn = gr.Button("🗑️ Clear History")

        with gr.Row():
            extract_btn = gr.Button("📝 Extract Text")
            caption_btn = gr.Button("💭 Caption Image")
            summarize_btn = gr.Button("📋 Summarize Image")

        # Store uploaded image
        image_output = gr.Image(type="numpy", visible=False)

        # Add Text-to-Speech section
        gr.Markdown("### Text-to-Speech Options")

        with gr.Row():
            with gr.Column(scale=3):
                voice_type = gr.Dropdown(
                    choices=[
                        "Female Heart (American)",
                        "Female Bella (American)",
                        "Female Emma (British)",
                        "Male Michael (American)",
                        "Male Fenrir (American)",
                        "Male George (British)"
                    ],
                    value="Female Heart (American)",
                    label="Voice Type"
                )
            with gr.Column(scale=3):
                speed = gr.Slider(
                    minimum=0.5,
                    maximum=2.0,
                    value=1.0,
                    step=0.1,
                    label="Playback Speed"
                )
            with gr.Column(scale=1):
                tts_btn = gr.Button("🔊 Play Last Response")

        # Audio output component
        audio_output = gr.Audio(label="Generated Speech")

        # Put TTS Status and Performance Metrics in the same row
        with gr.Row():
            # TTS Status on the left
            tts_status = gr.Textbox(
                label="TTS Status",
                scale=2
            )

            # Performance metrics on the right
            performance_metrics = gr.Textbox(
                label="Performance Metrics",
                value="Tokens/sec: N/A | Time to first token: N/A | Latency: N/A",
                interactive=False,
                scale=3
            )

        # Event handlers for chat
        msg.submit(chat_response, [msg, chatbot, performance_metrics], [chatbot, performance_metrics], api_name="chat")
        send_btn.click(chat_response, [msg, chatbot, performance_metrics], [chatbot, performance_metrics])
        upload_btn.upload(lambda x: x, upload_btn, image_output)

        # Reset performance metrics when clearing history
        clear_btn.click(lambda: ([], "Tokens/sec: N/A | Time to first token: N/A | Latency: N/A"),
                         None,
                         [chatbot, performance_metrics],
                         queue=False)

        # Use the improved regenerate function with performance metrics
        regenerate_btn.click(regenerate_response, [chatbot, performance_metrics], [chatbot, performance_metrics])

        # Event handlers for image processing
        extract_btn.click(extract_text, inputs=[image_output, chatbot], outputs=[chatbot])
        caption_btn.click(caption_image, inputs=[image_output, chatbot], outputs=[chatbot])
        summarize_btn.click(summarize_image, inputs=[image_output, chatbot], outputs=[chatbot])

        # Event handler for TTS
        tts_btn.click(
            fn=lambda history, voice, speed: text_to_speech(get_last_bot_message(history), voice, speed),
            inputs=[chatbot, voice_type, speed],
            outputs=[audio_output, tts_status]
        )

def create_guide_interface():
    return gr.Markdown("""
    # Chat Application Guide

    Welcome to the Chat Application! Here's how to use the various features:

    ### Basic Chat
    - Type your message in the text box and press Enter or click Send
    - The chatbot will respond to your messages

    ### Image Features (Powered by Qwen 2 VL 7B)
    1. **Upload Image**: Click to upload an image file
    2. **Extract Text**: Extracts any text present in the uploaded image
    3. **Caption Image**: Generates a detailed description of the uploaded image
    4. **Summarize Image**: Provides a comprehensive analysis of the image content

    ### Text-to-Speech Features (Powered by Kokoro TTS)
    1. **Voice Type**: Select from different voice options including:
       - Female and Male voices
       - Multiple accents: American & British
    2. **Playback Speed**: Adjust how fast the text is spoken (0.5x to 2.0x)
    3. **Play Last Response**: Convert the last bot message to speech

    ### Other Controls
    - **Regenerate**: Regenerates the last response with a new AI call
    - **Clear History**: Clears the chat history

    ### Performance Metrics
    - **Tokens per second**: How fast the model generates tokens
    - **Time to first token**: How long it takes to get the first response
    - **Latency**: Total time from request to complete response

    Disclaimer: This web application **does not store any data** to comply with privacy regulations (GDPR, CCPA). All interactions are ephemeral. The chat history will be cleared when you close the browser tab.
    """)

# Create the main application
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# Interactive Chat Application with AI Vision and Voice")

    with gr.Tabs():
        with gr.Tab("Chat"):
            create_chat_interface()
        with gr.Tab("Guide"):
            create_guide_interface()

if __name__ == "__main__":
    demo.launch()
    with gr.Tabs():
        with gr.Tab("Chat"):
            create_chat_interface()
        with gr.Tab("Guide"):
            create_guide_interface()

if __name__ == "__main__":
    demo.launch()