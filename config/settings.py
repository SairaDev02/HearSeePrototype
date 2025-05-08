"""
Configuration settings for the HearSee application.
This module contains all constant values and configuration parameters.
"""

# Replicate Model Constants
QWEN_VL_MODEL = "lucataco/qwen2-vl-7b-instruct:bf57361c75677fc33d480d0c5f02926e621b2caa2000347cb74aeae9d2ca07ee"
KOKORO_TTS_MODEL = "jaaari/kokoro-82m:f559560eb822dc509045f3921a1921234918b91739db4bf3daab2169b71c7a13"

# API Configuration
DEFAULT_MAX_TOKENS = 512

# Image Processing Settings
MAX_IMAGE_SIZE = 10 * 1024 * 1024  # 10MB in bytes

# Initial Chat History
INIT_HISTORY = [
    ["Hello! Can you help me analyze an image?", 
     "Of course! I'd be happy to help. You can upload an image using the Upload Image button below."],
    ["What kind of images can I upload?", 
     "You can upload most common image formats (JPG, PNG, etc.). Once uploaded, I can help you with:\n- Extracting text from the image\n- Generating image captions\n- Providing detailed image summaries\n I can also convert text to speech for you."],
    ["That sounds great!", 
     "Feel free to upload an image whenever you're ready. I'm here to help! 😊"]
]

# TTS Configuration
VOICE_TYPES = {
    "Female River (American)": "af_river",
    "Female Bella (American)": "af_bella",
    "Female Emma (British)": "bf_emma",
    "Male Michael (American)": "am_michael",
    "Male Fenrir (American)": "am_fenrir",
    "Male George (British)": "bm_george"
}

TTS_SPEED_RANGE = (0.5, 2.0)  # (min_speed, max_speed)

# Default TTS Settings
DEFAULT_VOICE = "Female River (American)"
DEFAULT_SPEED = 1.0