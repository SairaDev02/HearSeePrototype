# HearSee - Interactive AI Vision & Voice Web Application

HearSee is a powerful and user-friendly web application that combines vision AI and speech synthesis capabilities to provide an interactive experience for analyzing and discussing images with AI assistance.

## Features

### 🖼️ Vision AI Capabilities
- **Image Chat**: Upload images and have natural conversations about their content
- **Text Extraction**: Extract and transcribe text visible in images 
- **Image Captioning**: Generate detailed descriptions of image content
- **Image Summarization**: Obtain comprehensive contextual summaries of images

### 🔊 Voice AI Capabilities
- **Text-to-Speech**: Convert AI responses to natural-sounding speech
- **Voice Selection**: Choose from multiple voice types:
  - Female voices: River (American), Bella (American), Emma (British)
  - Male voices: Michael (American), Fenrir (American), George (British)
- **Speed Control**: Adjust speech playback speed (0.5x - 2.0x)

### 💻 User Interface
- Intuitive chat interface with image upload capability
- Real-time performance metrics (latency, word count)
- Response regeneration option
- Image gallery for uploaded content
- Comprehensive user guide

## Technology Stack

HearSee leverages state-of-the-art AI models through the Replicate API:

- **Qwen 2 VL 7B**: Multimodal large language model for image understanding and text generation
- **Kokoro TTS**: High-quality text-to-speech synthesis model
- **Python Logging**: Structured logging framework for application monitoring and debugging

## Prerequisites

- Python 3.7+
- Replicate API key
- Required Python packages (see Installation)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/HearSeePrototype.git
   cd HearSeePrototype
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root with your Replicate API key:
   ```
   REPLICATE_API_TOKEN=your_replicate_api_key_here
   ```

## Usage

1. Run the application:
   ```bash
   python app.py
   ```

2. Open your web browser and navigate to the URL displayed in the terminal (typically http://localhost:7860)

3. Follow these steps to use the application:
   - Upload an image using the "Upload Image" button
   - Type a message or use one of the special functions (Extract Text, Caption Image, Summarize Image)
   - View the AI's response
   - Optionally convert the response to speech with the "Play Last Response" button

## Required Python Packages

```
gradio
replicate
Pillow
python-dotenv
requests
pydantic
pydantic_core
```

## Logging System

HearSee implements a comprehensive logging system that:

- Captures application events at different severity levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- Logs to both console and rotating log files
- Maintains separate log files for all logs (`logs/app.log`) and errors only (`logs/error.log`)
- Includes contextual information such as timestamps, module names, and exception tracebacks
- Configurable verbosity levels for different environments
- Automatically rotates log files to prevent excessive disk usage (10MB max size with 5 backups)

Log files are stored in the `logs` directory and are automatically created on application startup.

## API Usage Notes

HearSee uses the following Replicate models:
- [Qwen 2 VL 7B](https://replicate.com/lucataco/qwen2-vl-7b-instruct) for image understanding and text generation
- [Kokoro TTS](https://replicate.com/jaaari/kokoro-82m) for text-to-speech synthesis

Make sure your Replicate API account has billing enabled to use these models.

## Privacy Statement

HearSee prioritizes user privacy:
- No user data or uploaded images are stored
- All interactions are ephemeral and session-based
- The application complies with privacy regulations (GDPR, CCPA)

## Limitations

- Image upload is required for chat functionality
- Processing large or complex images may take additional time
- API rate limits may apply depending on your Replicate account

## License

[MIT License](LICENSE)

## Development

### Logging Guidelines

When developing new features or fixing bugs, follow these logging guidelines:

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

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Contact

Email: sairadev02@gmail.com