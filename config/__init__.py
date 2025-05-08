"""Configuration package for HearSee application."""

from .settings import (
    QWEN_VL_MODEL,
    KOKORO_TTS_MODEL,
    DEFAULT_MAX_TOKENS,
    MAX_IMAGE_SIZE,
    INIT_HISTORY,
    VOICE_TYPES,
    TTS_SPEED_RANGE,
    DEFAULT_VOICE,
    DEFAULT_SPEED
)

__all__ = [
    'QWEN_VL_MODEL',
    'KOKORO_TTS_MODEL',
    'DEFAULT_MAX_TOKENS',
    'MAX_IMAGE_SIZE',
    'INIT_HISTORY',
    'VOICE_TYPES',
    'TTS_SPEED_RANGE',
    'DEFAULT_VOICE',
    'DEFAULT_SPEED'
]