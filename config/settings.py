"""
Configuration settings for the HearSee application.

This module centralizes all constant values and configuration parameters used throughout
the application. It includes model identifiers, API settings, image processing limits,
initial chat history, and text-to-speech configuration.

Constants:
    QWEN_VL_MODEL (str): Replicate model identifier for the Qwen VL vision-language model
    KOKORO_TTS_MODEL (str): Replicate model identifier for the Kokoro text-to-speech model
    DEFAULT_MAX_TOKENS (int): Default maximum token limit for API responses
    MAX_IMAGE_SIZE (int): Maximum allowed image size in bytes
    INIT_HISTORY (list): Initial conversation history for the chat interface
    VOICE_TYPES (dict): Mapping of human-readable voice names to voice IDs
    TTS_SPEED_RANGE (tuple): Minimum and maximum allowed speech speed values
    DEFAULT_VOICE (str): Default voice type for text-to-speech conversion
    DEFAULT_SPEED (float): Default speech speed for text-to-speech conversion
"""

# Replicate Model Constants - specific model versions for reproducibility
# Format: "username/model-name:model-version-hash"
QWEN_VL_MODEL = "lucataco/qwen2-vl-7b-instruct:bf57361c75677fc33d480d0c5f02926e621b2caa2000347cb74aeae9d2ca07ee"
KOKORO_TTS_MODEL = "jaaari/kokoro-82m:f559560eb822dc509045f3921a1921234918b91739db4bf3daab2169b71c7a13"

# API Configuration - controls response length
DEFAULT_MAX_TOKENS = 512  # Balances between detailed responses and API costs

# Image Processing Settings - prevents uploading excessively large images
MAX_IMAGE_SIZE = 10 * 1024 * 1024  # 10MB in bytes (10 * 1024KB * 1024B)

# Initial Chat History - provides a welcoming experience and guides new users
# Format: List of [user_message, assistant_response] pairs
INIT_HISTORY = [
    ["Hello! Can you help me analyze an image?",
     "Of course! I'd be happy to help. You can upload an image using the Upload Image button below."],
    ["What kind of images can I upload?",
     "You can upload most common image formats (JPG, PNG, etc.). Once uploaded, I can help you with:\n- Extracting text from the image\n- Generating image captions\n- Providing detailed image summaries\n I can also convert text to speech for you."],
    ["That sounds great!",
     "Feel free to upload an image whenever you're ready. I'm here to help! 😊"]
]

# TTS Configuration - voice options for text-to-speech conversion
# Format: "Human-readable name": "voice_id"
# Naming convention: [gender_initial][accent_initial]_[name]
# Example: "af_river" = American Female voice named River
VOICE_TYPES = {
    "Female River (American)": "af_river",
    "Female Bella (American)": "af_bella",
    "Female Emma (British)": "bf_emma",
    "Male Michael (American)": "am_michael",
    "Male Fenrir (American)": "am_fenrir",
    "Male George (British)": "bm_george"
}

# Valid range for speech speed adjustment - prevents unintelligible output
TTS_SPEED_RANGE = (0.5, 2.0)  # (min_speed, max_speed)

# Default TTS Settings - used when user doesn't specify preferences
DEFAULT_VOICE = "Female River (American)"  # Must match a key in VOICE_TYPES
DEFAULT_SPEED = 1.0  # Normal speaking rate (1.0x)