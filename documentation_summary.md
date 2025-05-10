# HearSee Application Documentation Summary

## Application Overview

HearSee is a web application that combines vision AI and speech synthesis capabilities to provide an interactive experience for analyzing and discussing images with AI assistance. The application is built using Python with a Gradio-based web interface, leveraging Multimodal Large Language Models (MLLMs) and Text-to-Speech (TTS) models through the Replicate API.

## Core Functionality

### Vision AI Capabilities

1. **Image Chat**: Users can upload images and have natural conversations about their content using the Qwen 2 VL 7B multimodal large language model.
2. **Text Extraction**: The application can extract and transcribe text visible in images.
3. **Image Captioning**: Users can generate detailed descriptions of image content.
4. **Image Summarization**: The application provides comprehensive contextual summaries of images.

### Voice AI Capabilities

1. **Text-to-Speech**: AI responses can be converted to natural-sounding speech using the Kokoro TTS model.
2. **Voice Selection**: Users can choose from multiple voice types:
   - Female voices: River (American), Bella (American), Emma (British)
   - Male voices: Michael (American), Fenrir (American), George (British)
3. **Speed Control**: Speech playback speed can be adjusted from 0.5x to 2.0x.

### User Interface

1. **Chat Interface**: Intuitive chat interface with image upload capability.
2. **Performance Metrics**: Real-time metrics showing latency and word count.
3. **Response Regeneration**: Option to regenerate AI responses.
4. **Image Gallery**: Display area for uploaded content.
5. **User Guide**: Comprehensive in-app documentation.

## Technical Architecture

### Application Structure

The application follows a modular architecture with clear separation of concerns:

1. **Main Application (app.py)**: Entry point that initializes the Gradio interface, configures logging, and connects UI components to backend services.
2. **Services**: Core functionality modules:
   - `image_service.py`: Handles image processing, validation, and conversion.
   - `replicate_service.py`: Manages interactions with the Replicate API for AI models.
   - `tts_service.py`: Handles text-to-speech conversion and audio file management.
3. **UI Components**: Interface modules:
   - `chat_interface.py`: Defines the main chat interface layout and components.
   - `guide_interface.py`: Provides in-app documentation and help.
   - `components.py`: Reusable UI elements like chatbot, voice selector, etc.
4. **Utilities**: Helper functions:
   - `image_utils.py`: Functions for image operations like text extraction and captioning.
   - `validators.py`: Input validation for messages, images, and TTS parameters.
   - `logger.py`: Logging utilities.
5. **Configuration**: Settings and constants:
   - `settings.py`: Application constants, model identifiers, and default values.
   - `logging_config.py`: Logging system configuration.

### Technology Stack

1. **Frontend**: Gradio web interface
2. **Backend**: Python 3.7+
3. **AI Models**:
   - Qwen 2 VL 7B: Multimodal large language model for image understanding
   - Kokoro TTS: Text-to-speech synthesis model
4. **Dependencies**:
   - gradio: Web interface framework
   - replicate: API client for AI models
   - Pillow: Image processing
   - python-dotenv: Environment variable management
   - requests: HTTP client
   - pydantic: Data validation

## Main User Workflows

### Image Analysis Workflow

1. User uploads an image using the "Upload Image" button.
2. The image is validated for size and format.
3. The user can:
   - Type a message to chat about the image
   - Click "Extract Text" to identify text in the image
   - Click "Caption Image" to generate a description
   - Click "Summarize Image" for detailed analysis
4. The AI processes the request and displays the response in the chat interface.
5. Performance metrics (latency, word count) are shown.

### Text-to-Speech Workflow

1. After receiving an AI response, the user can click "Play Last Response".
2. The user can select a voice type from the dropdown menu.
3. The user can adjust the speech speed using the slider.
4. The application sends the text to the Kokoro TTS model via Replicate API.
5. The audio is downloaded and played through the browser.

## Installation and Setup

### Prerequisites

1. Python 3.7+
2. Replicate API key with billing enabled
3. Required Python packages (listed in requirements.txt)

### Installation Steps

1. Clone the repository
2. Install dependencies using `pip install -r requirements.txt`
3. Create a `.env` file with your Replicate API key: `REPLICATE_API_TOKEN=your_key_here`

### Running the Application

1. Execute `python app.py`
2. Open the URL displayed in the terminal (typically http://localhost:7860)

## Security, Privacy, and Accessibility Considerations

### Security

1. **API Key Protection**: The application uses environment variables to store the Replicate API key.
2. **Input Validation**: All user inputs are validated before processing.
3. **Error Handling**: Comprehensive error handling prevents exposing sensitive information.

### Privacy

1. **No Data Storage**: No user data or uploaded images are stored persistently.
2. **Session-Based**: All interactions are ephemeral and session-based.
3. **Regulatory Compliance**: The application complies with privacy regulations (GDPR, CCPA).

### Accessibility

1. **Text-to-Speech**: Audio output provides accessibility for visually impaired users.
2. **Clear UI**: The interface uses clear labels and instructions.
3. **Performance Feedback**: Users receive feedback on processing status and results.

## Technical Glossary

| Term | Definition |
|------|------------|
| **Multimodal LLM** | A language model that can process and understand multiple types of data (text and images). |
| **Qwen 2 VL 7B** | A vision-language model with 7 billion parameters that can understand images and generate text responses. |
| **Kokoro TTS** | A text-to-speech model that converts text to natural-sounding speech. |
| **Base64 Encoding** | A method of converting binary data (like images) to ASCII text for transmission. |
| **Gradio** | A Python library for creating customizable web interfaces for machine learning models. |
| **Replicate API** | A platform that hosts and serves machine learning models. |
| **API Token** | A secret key used to authenticate with the Replicate API. |
| **OCR** | Optical Character Recognition - technology to extract text from images. |
| **TTS** | Text-to-Speech - technology to convert text to spoken audio. |
| **Latency** | The time delay between sending a request and receiving a response. |

## Logging System

The application implements a comprehensive logging system that:

1. Captures events at different severity levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
2. Logs to both console and rotating log files
3. Maintains separate log files for all logs (`logs/app.log`) and errors only (`logs/error.log`)
4. Includes contextual information such as timestamps, module names, and exception tracebacks
5. Configures verbosity levels for different environments
6. Automatically rotates log files to prevent excessive disk usage (10MB max size with 5 backups)

## Testing Framework

HearSee implements a comprehensive testing framework to ensure code quality, reliability, and maintainability:

1. **Test Types**:
   - Unit tests for individual components
   - Integration tests for component interactions
   - Functional tests for end-user workflows

2. **Testing Tools**:
   - pytest: Primary testing framework
   - unittest.mock: For mocking external dependencies
   - pytest-cov: For test coverage reporting
   - coverage: For detailed coverage analysis

3. **Test Coverage Targets**:
   - Services: 95%+ coverage
   - Utilities: 90%+ coverage
   - Configuration: 85%+ coverage
   - UI Components: 80%+ coverage

## Limitations and Known Issues

1. Image upload is required for chat functionality
2. Processing large or complex images may take additional time
3. API rate limits may apply depending on your Replicate account
4. Maximum image size is limited to 10MB

## Development Guidelines

### Logging Guidelines

When developing new features or fixing bugs:

1. Import the logging module in each file that requires logging
2. Get a module-level logger using `logger = logging.getLogger(__name__)`
3. Use appropriate log levels:
   - DEBUG: Detailed information for debugging
   - INFO: Confirmation that things are working as expected
   - WARNING: Indication that something unexpected happened
   - ERROR: Error conditions that prevent functionality from working
   - CRITICAL: Critical errors that may lead to application failure
4. Include contextual information in log messages
5. Use exception logging with traceback for error conditions

### Testing Guidelines

When adding new tests:

1. Follow the existing directory structure
2. Use appropriate fixtures
3. Mock external dependencies
4. Follow naming conventions
5. Add docstrings
6. Test edge cases
7. Keep tests independent
8. Aim for high coverage