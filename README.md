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

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Contact

Email: sairadev02@gmail.com