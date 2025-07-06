# API Reference

## Module: `mcp_poc.app`

### Classes

#### `OpenAIClient`

Manages OpenAI API client lifecycle with lazy initialization.

**Methods:**

##### `get_client() -> OpenAI`
Returns a configured OpenAI client instance.

**Returns:**
- `OpenAI`: Configured client instance

**Raises:**
- `ValueError`: If `OPENAI_API_KEY` environment variable is not set

**Example:**
```python
client_manager = OpenAIClient()
client = client_manager.get_client()
```

### Functions

#### `generate_completion(messages: list, model: str = "gpt-4o") -> str`

Generate text completion using OpenAI's chat API.

**Parameters:**
- `messages` (list): List of message dictionaries with 'role' and 'content' keys
- `model` (str, optional): OpenAI model identifier. Defaults to "gpt-4o"

**Returns:**
- `str`: Generated text response

**Raises:**
- `ValueError`: If API key is not configured
- `openai.APIError`: If API request fails

**Example:**
```python
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What is Python?"}
]
response = generate_completion(messages, model="gpt-4o")
print(response)
```

#### `select_model() -> str`

Interactive model selection from available OpenAI models.

**Returns:**
- `str`: Selected model identifier

**Behavior:**
- Fetches available GPT models from OpenAI API
- Displays numbered list for user selection
- Returns "gpt-4o" as default if selection fails or is empty

**Example:**
```python
chosen_model = select_model()
# User sees:
# Available models:
# 1. gpt-3.5-turbo
# 2. gpt-4
# 3. gpt-4o
# Enter model number (1-3) or press Enter for default (gpt-4o):
```

#### `chat_loop() -> None`

Main interactive chat interface with conversation history.

**Features:**
- Model selection at startup
- Persistent conversation history
- Exit commands: "quit", "exit"
- Error handling for API failures

**Example:**
```python
chat_loop()
# Starts interactive session:
# Using model: gpt-4o
# Chat started! Type 'quit' or 'exit' to end the conversation.
# You: Hello!
# AI: Hello! How can I help you today?
```

## Message Format

### Chat Messages
Messages should follow OpenAI's chat format:

```python
{
    "role": "system" | "user" | "assistant",
    "content": "string"
}
```

**Roles:**
- `system`: Sets behavior/context for the assistant
- `user`: Messages from the human user
- `assistant`: Previous responses from the AI

### Example Conversation
```python
messages = [
    {"role": "system", "content": "You are a Python expert."},
    {"role": "user", "content": "Explain list comprehensions"},
    {"role": "assistant", "content": "List comprehensions are..."},
    {"role": "user", "content": "Can you show an example?"}
]
```

## Error Handling

### Common Exceptions

- `ValueError`: Missing or invalid API key
- `openai.APIError`: General API errors
- `openai.RateLimitError`: API rate limit exceeded
- `openai.AuthenticationError`: Invalid API key

### Recommended Error Handling
```python
try:
    response = generate_completion(messages)
except ValueError as e:
    print(f"Configuration error: {e}")
except Exception as e:
    print(f"API error: {e}")
```
