"""UI package for HearSee application."""

# Import components directly
from .components import (
    create_chatbot_component,
    create_image_instruction,
    create_voice_type_dropdown,
    create_speed_slider,
    create_mllm_status
)

# Import interfaces
from .chat_interface import ChatInterface, create_interface
from .guide_interface import GuideInterface, create_guide_interface

__all__ = [
    # Components
    'create_chatbot_component',
    'create_image_instruction',
    'create_voice_type_dropdown',
    'create_speed_slider',
    'create_mllm_status',
    
    # Interfaces
    'ChatInterface',
    'GuideInterface',
    'create_interface',
    'create_guide_interface'
]

# Utility class for managing UI state and updates
class UIStateManager:
    @staticmethod
    def start_processing():
        """
        Set processing state to True and disable interactive elements.
        
        Returns:
            dict: Gradio component updates
        """
        import gradio as gr
        return {
            'processing_indicator': gr.update(visible=True),
            'msg': gr.update(interactive=False),
            'send_btn': gr.update(interactive=False),
            'upload_btn': gr.update(interactive=False),
            'extract_btn': gr.update(interactive=False),
            'caption_btn': gr.update(interactive=False),
            'summarize_btn': gr.update(interactive=False),
            'regenerate_btn': gr.update(interactive=False),
            'tts_btn': gr.update(interactive=False),
            'processing_status': True
        }

    @staticmethod
    def end_processing(chatbot_val=None, metrics_val=None, image_uploaded_state=False):
        """
        Reset processing state and re-enable interactive elements.
        
        Args:
            chatbot_val: Current chatbot state
            metrics_val: Current metrics state
            image_uploaded_state: Whether an image is currently uploaded
        
        Returns:
            dict: Gradio component updates
        """
        import gradio as gr
        updates = {
            'processing_indicator': gr.update(visible=False),
            'msg': gr.update(interactive=True),
            'upload_btn': gr.update(interactive=True),
            'regenerate_btn': gr.update(interactive=True),
            'tts_btn': gr.update(interactive=True),
            'processing_status': False
        }
        
        # Update components that depend on image state
        for btn in ['send_btn', 'extract_btn', 'caption_btn', 'summarize_btn']:
            updates[btn] = gr.update(interactive=image_uploaded_state)
            
        # Add optional updates if provided
        if chatbot_val is not None:
            updates['chatbot'] = chatbot_val
        if metrics_val is not None:
            updates['performance_metrics'] = metrics_val
            
        return updates

    @staticmethod
    def end_processing_tts(audio_val, status_val, image_uploaded_state=False):
        """
        End processing specifically for TTS operations.
        
        Args:
            audio_val: Audio output value
            status_val: TTS status message
            image_uploaded_state: Whether an image is currently uploaded
        
        Returns:
            dict: Gradio component updates
        """
        import gradio as gr
        updates = {
            'audio_output': audio_val,
            'tts_status': status_val,
            **UIStateManager.end_processing(image_uploaded_state=image_uploaded_state)
        }
        return updates

    @staticmethod
    def update_button_state(image):
        """
        Update button states based on image presence.
        
        Args:
            image: The uploaded image
        
        Returns:
            dict: Gradio component updates
        """
        import gradio as gr
        is_enabled = image is not None
        return {
            'send_btn': gr.update(interactive=is_enabled),
            'extract_btn': gr.update(interactive=is_enabled),
            'caption_btn': gr.update(interactive=is_enabled),
            'summarize_btn': gr.update(interactive=is_enabled),
            'image_uploaded_state': is_enabled,
            'image_instruction': gr.update(visible=not is_enabled)
        }

    @staticmethod
    def clear_interface_state():
        """
        Reset all interface elements to their initial state.
        
        Returns:
            dict: Gradio component updates
        """
        import gradio as gr
        from config.settings import INIT_HISTORY
        
        return {
            'chatbot': INIT_HISTORY,
            'performance_metrics': "Latency: N/A | Words: N/A",
            'processing_indicator': gr.update(visible=False),
            'msg': gr.update(interactive=True, value=""),
            'send_btn': gr.update(interactive=False),
            'upload_btn': gr.update(interactive=True),
            'extract_btn': gr.update(interactive=False),
            'caption_btn': gr.update(interactive=False),
            'summarize_btn': gr.update(interactive=False),
            'regenerate_btn': gr.update(interactive=True),
            'tts_btn': gr.update(interactive=True),
            'processing_status': False,
            'gallery': [],
            'image_output': None,
            'image_uploaded_state': False,
            'image_instruction': gr.update(visible=True)
        }