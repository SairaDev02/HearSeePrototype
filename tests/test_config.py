"""
Test configuration settings for the HearSee application.

This module contains test-specific configuration settings and constants.
"""

# Test data paths
TEST_DATA_DIR = "tests/fixtures"

# Mock API responses
MOCK_VISION_RESPONSE = """
This is a sample response from the vision model.
It contains multiple lines of text that would typically
be returned from the Qwen VL model.
"""

MOCK_TTS_RESPONSE = "https://mock-audio-url.com/sample.wav"

# Test image settings
TEST_IMAGE_SIZE = (100, 100)
TEST_IMAGE_FORMAT = "PNG"

# Mock environment variables
TEST_ENV_VARS = {
    "REPLICATE_API_TOKEN": "mock-api-token"
}

# Test timeouts
TEST_TIMEOUT = 5  # seconds

# Mock API parameters
MOCK_API_PARAMS = {
    "vision": {
        "prompt": "Test prompt",
        "max_new_tokens": 512,
    },
    "tts": {
        "text": "Test text for speech conversion",
        "voice": "af_river",
        "speed": 1.0
    }
}

# Test chat history
TEST_CHAT_HISTORY = [
    ["Hello, can you analyze this image?", "I'd be happy to help analyze your image."],
    ["What can you see in it?", "I can see various elements in the image."]
]

# Test voice types
TEST_VOICE_TYPES = {
    "Female Test": "af_test",
    "Male Test": "am_test"
}

# Test TTS settings
TEST_TTS_SPEED_RANGE = (0.5, 2.0)
TEST_DEFAULT_VOICE = "Female Test"
TEST_DEFAULT_SPEED = 1.0