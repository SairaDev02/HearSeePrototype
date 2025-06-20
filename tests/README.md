# HearSee Testing Framework

This directory contains the testing framework for the HearSee application. The testing structure follows Python best practices and is organized to support different types of tests.

## Directory Structure

```
tests/
├── conftest.py              # Global pytest fixtures
├── test_config.py           # Test configuration settings
├── README.md                # This file
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

## Test Types

### Unit Tests

Unit tests focus on testing individual components in isolation. These tests are located in the `unit/` directory and are organized by module type.

### Integration Tests

Integration tests verify that different components work together correctly. These tests are located in the `integration/` directory.

### Functional Tests

Functional tests check that the application functions correctly from an end-user perspective. These tests are located in the `functional/` directory.

## Test Configuration

The testing framework uses pytest and is configured via the `pytest.ini` file in the project root. Additional test configuration settings are defined in `tests/test_config.py`.

## Fixtures

Test fixtures are defined in the following locations:

- Global fixtures: `conftest.py`
- Test data: `fixtures/test_data.py`

## Mock Objects

The testing framework uses mock objects to isolate components from external dependencies:

- **Replicate API**: Mocked to avoid actual API calls during testing
- **File System**: Mocked for operations that create or modify files
- **Environment Variables**: Mocked to provide consistent test environments
- **HTTP Requests**: Mocked to avoid actual network requests

## Running Tests

To run the tests, use the following commands:

```bash
# Run all tests
pytest

# Run unit tests only
pytest tests/unit/

# Run integration tests only
pytest tests/integration/

# Run tests with coverage report
pytest --cov=. --cov-report=html

# Run tests for a specific module
pytest tests/unit/services/test_replicate_service.py
```

## Adding New Tests

When adding new tests:

1. Follow the existing directory structure
2. Use appropriate fixtures from `conftest.py`
3. Mock external dependencies
4. Follow the naming convention: `test_*.py` for files, `test_*` for functions
5. Add docstrings to test classes and functions

## Test Coverage

The testing framework is designed to provide comprehensive coverage of the application code. Key areas covered include:

- Configuration settings
- Service modules (image, replicate, TTS)
- Utility functions (validators, image processing)
- Error handling and edge cases