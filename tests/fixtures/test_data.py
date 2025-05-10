"""
Test data fixtures for HearSee application testing.

This module contains test data fixtures that can be used across test files for unit,
integration, and functional testing of the HearSee application. It provides sample
data structures, mock API responses, utility functions for generating test images,
and other testing resources.
"""

import json
import base64
from PIL import Image
import numpy as np
import io

# Sample chat history for UI testing
SAMPLE_CHAT_HISTORY = [
    ["Hello! Can you help me analyze an image?",
     "Of course! I'd be happy to help. You can upload an image using the Upload Image button below."],
    ["What kind of images can I upload?",
     "You can upload most common image formats (JPG, PNG, etc.). Once uploaded, I can help you with:\n- Extracting text from the image\n- Generating image captions\n- Providing detailed image summaries\n I can also convert text to speech for you."],
    ["That sounds great!",
     "Feel free to upload an image whenever you're ready. I'm here to help! 😊"]
]
"""
Sample conversation history for testing chat interface.

This constant provides a realistic conversation flow between a user and the
HearSee assistant, demonstrating typical interaction patterns.
"""

# Sample API responses
SAMPLE_VISION_RESPONSE = """
This image shows a red square on a white background. The square appears to be a solid red color
with no additional details or patterns. It's positioned in the center of the frame and takes up
most of the visible area. The contrast between the vibrant red and the clean white background
is quite striking.
"""
"""
Sample response from the vision API.

This constant provides a realistic description that would be returned by the
vision model when analyzing a simple red square image.
"""

SAMPLE_TTS_RESPONSE = "https://replicate-api-mock.com/audio/sample.wav"
"""
Sample URL response from the text-to-speech API.

This constant represents a mock URL that would be returned by the TTS service
pointing to the generated audio file.
"""

# Function to create a sample test image
def create_test_image(width=100, height=100, color='red'):
    """
    Create a sample test image with specified dimensions and color.
    
    This function generates a simple solid-color test image that can be used
    for testing image processing functions without requiring external files.
    
    Args:
        width (int): Image width in pixels. Defaults to 100.
        height (int): Image height in pixels. Defaults to 100.
        color (str): Image color name (any color name supported by PIL). Defaults to 'red'.
        
    Returns:
        numpy.ndarray: Image as numpy array with shape (height, width, 3) and RGB values.
        
    Example:
        >>> img = create_test_image(200, 200, 'blue')
        >>> img.shape
        (200, 200, 3)
    """
    # Create a new RGB image with the specified color
    img = Image.new('RGB', (width, height), color=color)
    # Convert PIL Image to numpy array for compatibility with image processing functions
    return np.array(img)

# Function to create a sample base64 encoded image
def create_base64_image(width=100, height=100, color='blue'):
    """
    Create a sample base64 encoded image string.
    
    This function generates a base64 encoded PNG image string that can be used
    for testing functions that expect base64 encoded images, such as API requests
    or data URI content.
    
    Args:
        width (int): Image width in pixels. Defaults to 100.
        height (int): Image height in pixels. Defaults to 100.
        color (str): Image color name (any color name supported by PIL). Defaults to 'blue'.
        
    Returns:
        str: Base64 encoded image string (without the 'data:image/png;base64,' prefix)
        
    Example:
        >>> encoded = create_base64_image(50, 50, 'green')
        >>> encoded[:20]  # First 20 chars of the encoded string
        'iVBORw0KGgoAAAANSUhE'
    """
    # Create a new RGB image with the specified color
    img = Image.new('RGB', (width, height), color=color)
    # Use BytesIO as an in-memory binary stream
    buffered = io.BytesIO()
    # Save the image as PNG to the buffer
    img.save(buffered, format="PNG")
    # Encode the binary data as base64 and convert to string
    return base64.b64encode(buffered.getvalue()).decode()

# Sample environment variables
SAMPLE_ENV_VARS = {
    "REPLICATE_API_TOKEN": "mock-api-token-for-testing"
}
"""
Sample environment variables for testing.

This dictionary contains mock environment variables that would typically be
set in a .env file or system environment for the application to function.
"""

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
"""
Sample parameters for API requests.

This dictionary contains typical parameters that would be sent to the
vision and text-to-speech APIs, structured by service type.
"""

# Sample error messages
SAMPLE_ERROR_MESSAGES = {
    "api_unavailable": "Error: Replicate API token not found. Set REPLICATE_API_TOKEN in your .env file.",
    "image_too_large": "Image size (15.0MB) exceeds maximum allowed size (10MB)",
    "no_image": "An image is required. Please upload an image before sending a message.",
    "empty_message": "Message cannot be empty",
    "api_error": "Error running vision model: API error",
    "download_error": "Error downloading audio: HTTP status 404"
}
"""
Sample error messages for testing error handling.

This dictionary contains common error messages that might be displayed to users
or logged by the application under various error conditions.
"""

# Sample test file paths
SAMPLE_FILE_PATHS = {
    "audio": "tests/fixtures/sample_audio.wav",
    "image": "tests/fixtures/sample_image.png",
    "log": "tests/fixtures/sample.log"
}
"""
Sample file paths for test resources.

This dictionary contains paths to test fixture files that may be used
across different test modules.
"""

# Function to create a sample log file content
def create_log_content(num_entries=10):
    """
    Create sample log file content with varied log levels.
    
    This function generates realistic-looking log entries with timestamps,
    component names, log levels, and messages. The log levels are varied
    based on entry number to ensure a mix of INFO, WARNING, and ERROR entries.
    
    Args:
        num_entries (int): Number of log entries to create. Defaults to 10.
        
    Returns:
        str: Multi-line string containing formatted log entries.
        
    Example:
        >>> logs = create_log_content(3)
        >>> print(logs)
        2023-05-08 10:00:00 - app - INFO - Sample log message 1
        2023-05-08 10:01:00 - app - INFO - Sample log message 2
        2023-05-08 10:02:00 - app - ERROR - Sample log message 3
    """
    log_lines = []
    for i in range(num_entries):
        # Create varied log levels: mostly INFO, some WARNINGs, fewer ERRORs
        # Every 3rd entry is not INFO; every 5th entry that's not INFO is ERROR
        level = "INFO" if i % 3 != 0 else "ERROR" if i % 5 == 0 else "WARNING"
        # Format log line with timestamp, component, level and message
        log_lines.append(f"2023-05-08 10:{i:02d}:00 - app - {level} - Sample log message {i+1}")
    
    # Join all log lines with newlines to create a complete log file content
    return "\n".join(log_lines)

# Sample performance metrics
SAMPLE_METRICS = {
    "latency": 1.25,  # seconds
    "word_count": 150
}
"""
Sample performance metrics for testing.

This dictionary contains typical performance metrics that might be collected
during application operation, such as API response times and content statistics.
"""

# Function to format metrics string
def format_metrics(metrics):
    """
    Format metrics dictionary as a human-readable string.
    
    This function converts a metrics dictionary into a formatted string
    suitable for display in logs, UI, or reports.
    
    Args:
        metrics (dict): Metrics dictionary containing at least 'latency' and 'word_count' keys.
        
    Returns:
        str: Formatted metrics string with latency (to 2 decimal places) and word count.
        
    Example:
        >>> metrics = {'latency': 2.345, 'word_count': 42}
        >>> format_metrics(metrics)
        'Latency: 2.35s | Words: 42'
        
    Raises:
        KeyError: If required keys are missing from the metrics dictionary.
    """
    # Format latency to 2 decimal places and combine with word count
    return f"Latency: {metrics['latency']:.2f}s | Words: {metrics['word_count']}"