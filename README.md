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

## Testing Framework

HearSee implements a comprehensive testing framework to ensure code quality, reliability, and maintainability. This section provides detailed information about the testing setup, how to run tests, and guidelines for writing new tests. The framework leverages the following tools:

- [pytest](https://docs.pytest.org/en/stable/): A framework for writing and running test cases.
- [unittest.mock](https://docs.python.org/3/library/unittest.mock.html): A library for creating mock objects for testing.
- [pytest-cov](https://pytest-cov.readthedocs.io/en/latest/): A plugin for measuring code coverage in pytest.
### Test Directory Structure

```
tests/
├── conftest.py              # Global pytest fixtures
├── test_config.py           # Test configuration settings
├── README.md                # Test-specific documentation
├── fixtures/                # Test data and fixtures
│   ├── __init__.py
│   └── test_data.py         # Sample test data
├── unit/                    # Unit tests
│   ├── __init__.py
│   ├── config/              # Tests for configuration modules
│   ├── services/            # Tests for service modules
│   ├── utils/               # Tests for utility modules
│   └── ui/                  # Tests for UI modules
├── integration/             # Integration tests
│   └── __init__.py
└── functional/              # Functional tests
    └── __init__.py
```

### Testing Frameworks and Tools

HearSee uses the following testing frameworks and tools:

- **pytest**: Primary testing framework
- **unittest.mock**: For mocking external dependencies
- **pytest-cov**: For test coverage reporting
- **coverage**: For detailed coverage analysis

### Test Types

#### Unit Tests

Unit tests focus on testing individual components in isolation. These tests verify that each function, method, or class behaves as expected. Key unit test files include:

- `tests/unit/config/test_logging_config.py`: Tests for logging configuration
- `tests/unit/config/test_settings.py`: Tests for application settings
- `tests/unit/services/test_image_service.py`: Tests for image processing service
- `tests/unit/services/test_replicate_service.py`: Tests for Replicate API integration
- `tests/unit/services/test_tts_service.py`: Tests for text-to-speech service
- `tests/unit/utils/test_image_utils.py`: Tests for image utility functions
- `tests/unit/utils/test_logger.py`: Tests for logging utilities
- `tests/unit/utils/test_validators.py`: Tests for input validation functions

#### Integration Tests

Integration tests verify that different components work together correctly. These tests ensure that the interfaces between components function as expected. Key integration test files include:

- `tests/integration/test_image_processing_pipeline.py`: Tests for the complete image processing workflow
- `tests/integration/test_tts_pipeline.py`: Tests for the text-to-speech pipeline

#### Functional Tests

Functional tests check that the application functions correctly from an end-user perspective. These tests simulate user interactions and verify that the application behaves as expected.

### Test Fixtures and Configuration

#### Global Fixtures (conftest.py)

The `conftest.py` file defines global pytest fixtures that can be used across all test files:

- `mock_env_vars`: Mocks environment variables
- `mock_replicate`: Mocks the Replicate API client
- `mock_requests`: Mocks HTTP requests
- `mock_temp_file`: Mocks temporary file creation
- `sample_image`: Creates a sample test image
- `sample_base64_image`: Creates a sample base64 encoded image
- `sample_chat_history`: Creates a sample chat history
- `mock_logger`: Mocks the logger

#### Test Data (fixtures/test_data.py)

The `test_data.py` file provides sample test data:

- Sample chat history
- Sample API responses
- Functions to create test images
- Sample environment variables
- Sample API parameters
- Sample error messages
- Sample file paths
- Functions to create log content
- Sample performance metrics

#### Test Configuration

The testing framework is configured via:

- `pytest.ini`: Main pytest configuration
- `tests/test_config.py`: Test-specific configuration settings
- `.coveragerc`: Coverage reporting configuration

### Running Tests

#### Basic Test Commands

```bash
# Run all tests
pytest

# Run unit tests only
pytest tests/unit/

# Run integration tests only
pytest tests/integration/

# Run functional tests only
pytest tests/functional/

# Run tests for a specific module
pytest tests/unit/services/test_image_service.py

# Run a specific test function
pytest tests/unit/services/test_image_service.py::TestImageService::test_image_to_base64_with_numpy_array
```

#### Running Tests with Coverage

```bash
# Run tests with coverage report
pytest --cov=. --cov-report=html

# Run tests with terminal coverage report
pytest --cov=. --cov-report=term

# Run tests with XML coverage report (for CI/CD)
pytest --cov=. --cov-report=xml
```

#### Environment Variables for Testing

Tests can be configured with the following environment variables:

```bash
# Set to skip tests that require external services
export SKIP_EXTERNAL_TESTS=1

# Set to use a mock API token for testing
export REPLICATE_API_TOKEN=mock-api-token
```

### Test Coverage

The project aims for high test coverage across all modules. Coverage reports are generated using pytest-cov and can be viewed in HTML format after running tests with the `--cov-report=html` option.

Key coverage metrics:

- **Services**: 95%+ coverage
- **Utilities**: 90%+ coverage
- **Configuration**: 85%+ coverage
- **UI Components**: 80%+ coverage

The `.coveragerc` file configures coverage reporting and excludes certain files and code blocks from coverage analysis:

- External libraries in site-packages
- Setup scripts
- Code blocks marked with `# pragma: no cover`
- Special methods like `__repr__`
- Import error handling

### CI/CD Integration

The test suite is designed to be run as part of a CI/CD pipeline. When integrating with CI/CD systems:

1. Install dependencies: `pip install -r requirements.txt`
2. Run tests with coverage: `pytest --cov=. --cov-report=xml`
3. Upload coverage report to your coverage tracking service
4. Set up test failure notifications

Example GitHub Actions workflow:

```yaml
name: Tests

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    - name: Run tests
      run: |
        pytest --cov=. --cov-report=xml
      env:
        REPLICATE_API_TOKEN: ${{ secrets.REPLICATE_API_TOKEN }}
    - name: Upload coverage report
      uses: codecov/codecov-action@v1
```

### Troubleshooting Common Test Failures

#### API Token Issues

If tests fail with "API token not found" errors:
- Ensure the `REPLICATE_API_TOKEN` environment variable is set
- Check that the token is valid
- Use the mock fixtures for tests that don't need actual API access

#### Image Processing Failures

If image processing tests fail:
- Verify that PIL/Pillow is correctly installed
- Check that test images are being created with the correct dimensions
- Ensure that mock objects are properly configured

#### TTS Pipeline Failures

If text-to-speech tests fail:
- Check that the mock responses are properly configured
- Verify that temporary file handling is working correctly
- Ensure that HTTP request mocking is set up properly

#### Coverage Report Issues

If coverage reports show unexpectedly low coverage:
- Check the `.coveragerc` file for proper configuration
- Ensure that all test files are being discovered by pytest
- Verify that tests are actually running (not being skipped)

### Guidelines for Writing New Tests

When adding new tests to the HearSee project:

1. **Follow the existing directory structure**:
   - Place unit tests in the appropriate subdirectory of `tests/unit/`
   - Place integration tests in `tests/integration/`
   - Place functional tests in `tests/functional/`

2. **Use appropriate fixtures**:
   - Use fixtures from `conftest.py` for common test requirements
   - Create new fixtures in `conftest.py` if they'll be used across multiple test files
   - Create local fixtures in test files if they're only used in that file

3. **Mock external dependencies**:
   - Mock the Replicate API to avoid actual API calls
   - Mock file system operations for tests that create or modify files
   - Mock environment variables to provide a consistent test environment
   - Mock HTTP requests to avoid actual network requests

4. **Follow naming conventions**:
   - Name test files with the prefix `test_`
   - Name test functions with the prefix `test_`
   - Name test classes with the prefix `Test`

5. **Add docstrings**:
   - Add a docstring to each test class explaining what it tests
   - Add a docstring to each test function explaining the specific test case

6. **Test edge cases**:
   - Test with valid inputs
   - Test with invalid inputs
   - Test with edge cases (empty strings, None values, etc.)
   - Test error handling

7. **Keep tests independent**:
   - Each test should be able to run independently
   - Tests should not depend on the state left by other tests
   - Use setUp and tearDown methods (or fixtures) to create and clean up test state

8. **Aim for high coverage**:
   - Test all code paths
   - Test all error handling
   - Test all edge cases

For more detailed information about the testing framework, see the [tests/README.md](tests/README.md) file.