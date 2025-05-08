"""Utilities package for HearSee application."""

from .validators import (
    validate_message,
    validate_image_input,
    validate_history,
    get_last_bot_message,
    validate_tts_input,
    Validators
)

from .image_utils import ImageUtils

class ChatUtils:
    @staticmethod
    def regenerate_response(history, performance_metrics, image=None):
        """
        Regenerate the last bot message by re-running the model.
        
        Args:
            history: Current chat history
            performance_metrics: Current performance metrics
            image: Optional image for context
            
        Returns:
            tuple: Updated history and metrics
        """
        if not history:
            return history, performance_metrics

        # Get the last user message from history
        last_user_msg = history[-1][0]

        # If it's None (could be from image operations), return as is
        if last_user_msg is None:
            return history, performance_metrics

        # Remove the last exchange from history
        new_history = history[:-1]

        try:
            from services import ReplicateService
            # Build system prompt from chat history
            system_prompt = "You are a helpful AI assistant specializing in analyzing images and providing detailed information."
            context = "\\n\\n".join([f"User: {h[0]}\\nAssistant: {h[1]}" for h in new_history if h[0] is not None])
            
            # Prepare image if provided
            image_str = None
            if image is not None:
                from services import ImageService
                image_str = ImageService.image_to_base64(image)

            # Run the model
            result = ReplicateService.run_vision_model(
                f"{system_prompt}\\n\\nConversation History:\\n{context}\\nUser: {last_user_msg}\\nAssistant:",
                image_base64=image_str
            )

            updated_metrics = f"Regenerated response successfully"
            return new_history + [[last_user_msg, result]], updated_metrics

        except Exception as e:
            return new_history + [[last_user_msg, f"Error regenerating response: {str(e)}"]], "Error: Metrics unavailable"

    @staticmethod
    def locked_chat_response(message, history, performance_metrics, image=None):
        """
        Process a chat response with proper locking mechanism.
        
        Args:
            message: User message
            history: Chat history
            performance_metrics: Performance metrics
            image: Optional image
            
        Returns:
            tuple: Updated history, metrics, and empty string for input clearing
        """
        # Validate inputs
        valid_msg, msg_error = validate_message(message)
        if not valid_msg:
            return history + [[message, msg_error]], performance_metrics, ""

        try:
            from services import ReplicateService, ImageService
            
            # Prepare image if provided
            image_str = None
            if image is not None:
                image_str = ImageService.image_to_base64(image)

            # Build system prompt
            system_prompt = "You are a helpful AI assistant specializing in analyzing images and providing detailed information."
            context = "\\n\\n".join([f"User: {h[0]}\\nAssistant: {h[1]}" for h in history if h[0] is not None])
            
            # Run the model
            result = ReplicateService.run_vision_model(
                f"{system_prompt}\\n\\nConversation History:\\n{context}\\nUser: {message}\\nAssistant:",
                image_base64=image_str
            )

            updated_metrics = "Response generated successfully"
            return history + [[message, result]], updated_metrics, ""

        except Exception as e:
            error_msg = f"Error processing response: {str(e)}"
            return history + [[message, error_msg]], "Error: Metrics unavailable", ""

__all__ = [
    # Classes
    'Validators',
    'ImageUtils',
    'ChatUtils',
    
    # Validator functions
    'validate_message',
    'validate_image_input',
    'validate_history',
    'get_last_bot_message',
    'validate_tts_input',
]