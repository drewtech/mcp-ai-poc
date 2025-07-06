# Architecture Overview

## Project Structure

This is a Python proof-of-concept application that demonstrates integration with OpenAI's API using their modern Python SDK (>=1.0.0).

### Core Components

```
src/mcp_poc/
├── app.py          # Main application logic
└── __init__.py     # Package initialization

src/tests/
└── test_app.py     # Unit tests for the application
```

## Key Classes and Functions

### `OpenAIClient`
- **Purpose**: Manages OpenAI API client instantiation and configuration
- **Pattern**: Singleton-like pattern with lazy initialization
- **Key Method**: `get_client()` - Returns configured OpenAI client instance

### `generate_completion(messages, model)`
- **Purpose**: Generate text completions using OpenAI's chat API
- **Parameters**:
  - `messages`: List of conversation messages
  - `model`: OpenAI model to use (default: "gpt-4o")
- **Returns**: Generated text response

### `select_model()`
- **Purpose**: Interactive model selection from available OpenAI models
- **Behavior**: Fetches and displays available GPT models, allows user selection
- **Fallback**: Defaults to "gpt-4o" if selection fails

### `chat_loop()`
- **Purpose**: Main interactive chat interface
- **Features**:
  - Model selection at startup
  - Conversation history management
  - Graceful error handling
  - Exit commands ("quit", "exit")

## Dependencies

- **openai**: Official OpenAI Python SDK for API interactions
- **pytest**: Testing framework (dev dependency)

## Configuration

- Requires `OPENAI_API_KEY` environment variable
- No additional configuration files needed
