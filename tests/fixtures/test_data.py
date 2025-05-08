"""
Test data fixtures for HearSee application testing.

This module contains test data that can be used across test files.
"""

import json
import base64
from PIL import Image
import numpy as np
import io

# Sample chat history
SAMPLE_CHAT_HISTORY = [
    ["Hello! Can you help me analyze an image?", 
     "Of course! I'd be happy to help. You can upload an image using the Upload Image button below."],
    ["What kind of images can I upload?", 
     "You can upload most common image formats (JPG, PNG, etc.). Once uploaded, I can help you with:\n- Extracting text from the image\n- Generating image captions\n- Providing detailed image summaries\n I can also convert text to speech for you."],
    ["That sounds great!", 
     "Feel free to upload an image whenever you're ready. I'm here to help! 😊"]
]

# Sample API responses
SAMPLE_VISION_RESPONSE = """
This image shows a red square on a white background. The square appears to be a solid red color 
with no additional details or patterns. It's positioned in the center of the frame and takes up 
most of the visible area. The contrast between the vibrant red and the clean white background 
is quite striking.
"""

SAMPLE_TTS_RESPONSE = "https://replicate-api-mock.com/audio/sample.wav"

# Function to create a sample test image
def create_test_image(width=100, height=100, color='red'):
    """
    Create a sample test image.
    
    Args:
        width (int): Image width in pixels
        height (int): Image height in pixels
        color (str): Image color
        
    Returns:
        numpy.ndarray: Image as numpy array
    """
    img = Image.new('RGB', (width, height), color=color)
    return np.array(img)

# Function to create a sample base64 encoded image
def create_base64_image(width=100, height=100, color='blue'):
    """
    Create a sample base64 encoded image.
    
    Args:
        width (int): Image width in pixels
        height (int): Image height in pixels
        color (str): Image color
        
    Returns:
        str: Base64 encoded image
    """
    img = Image.new('RGB', (width, height), color=color)
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

# Sample environment variables
SAMPLE_ENV_VARS = {
    "REPLICATE_API_TOKEN": "mock-api-token-for-testing"
}

# Sample API parameters
SAMPLE_API_PARAMS = {
    "vision": {
        "prompt": "Describe this image in detail.",
        "max_new_tokens": 512,
    },
    "tts": {
        "text": "This is a sample text for speech conversion.",
        "voice": "af_river",
        "speed": 1.0
    }
}

# Sample error messages
SAMPLE_ERROR_MESSAGES = {
    "api_unavailable": "Error: Replicate API token not found. Set REPLICATE_API_TOKEN in your .env file.",
    "image_too_large": "Image size (15.0MB) exceeds maximum allowed size (10MB)",
    "no_image": "An image is required. Please upload an image before sending a message.",
    "empty_message": "Message cannot be empty",
    "api_error": "Error running vision model: API error",
    "download_error": "Error downloading audio: HTTP status 404"
}

# Sample test file paths
SAMPLE_FILE_PATHS = {
    "audio": "tests/fixtures/sample_audio.wav",
    "image": "tests/fixtures/sample_image.png",
    "log": "tests/fixtures/sample.log"
}

# Function to create a sample log file content
def create_log_content(num_entries=10):
    """
    Create sample log file content.
    
    Args:
        num_entries (int): Number of log entries to create
        
    Returns:
        str: Log file content
    """
    log_lines = []
    for i in range(num_entries):
        level = "INFO" if i % 3 != 0 else "ERROR" if i % 5 == 0 else "WARNING"
        log_lines.append(f"2023-05-08 10:{i:02d}:00 - app - {level} - Sample log message {i+1}")
    
    return "\n".join(log_lines)

# Sample performance metrics
SAMPLE_METRICS = {
    "latency": 1.25,  # seconds
    "word_count": 150
}

# Function to format metrics string
def format_metrics(metrics):
    """
    Format metrics dictionary as a string.
    
    Args:
        metrics (dict): Metrics dictionary
        
    Returns:
        str: Formatted metrics string
    """
    return f"Latency: {metrics['latency']:.2f}s | Words: {metrics['word_count']}"