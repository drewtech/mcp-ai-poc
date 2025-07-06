# Troubleshooting Guide

## Common Issues and Solutions

### Authentication Issues

#### Problem: "OPENAI_API_KEY environment variable must be set"
**Cause**: Missing or empty API key configuration

**Solutions:**
```bash
# Set for current session
export OPENAI_API_KEY="your-api-key-here"

# Set permanently in ~/.bashrc or ~/.zshrc
echo 'export OPENAI_API_KEY="your-api-key-here"' >> ~/.bashrc
source ~/.bashrc

# Verify it's set
echo $OPENAI_API_KEY
```

#### Problem: "Incorrect API key provided"
**Cause**: Invalid or expired API key

**Solutions:**
1. Verify API key in OpenAI dashboard
2. Check for extra spaces or characters
3. Regenerate API key if needed

### Installation Issues

#### Problem: "No module named 'mcp_poc'"
**Cause**: Package not installed in editable mode

**Solution:**
```bash
# From project root
pip install -e .

# Or install dependencies first
./scripts/install_deps.sh
pip install -e .
```

#### Problem: "Python version not supported"
**Cause**: Using Python < 3.11

**Solution:**
```bash
# Check Python version
python --version

# Install Python 3.11+ or use pyenv
pyenv install 3.11.0
pyenv local 3.11.0
```

### Runtime Issues

#### Problem: "Rate limit exceeded"
**Cause**: Too many API requests in short timeframe

**Solutions:**
1. Wait before retrying (rate limits reset over time)
2. Implement retry logic with exponential backoff
3. Reduce request frequency
4. Check OpenAI account tier and limits

#### Problem: "Model not found" or invalid model
**Cause**: Using unavailable or deprecated model name

**Solutions:**
1. Use `select_model()` to see available models
2. Update to current model names (e.g., "gpt-4o" instead of "gpt-4")
3. Check OpenAI documentation for model availability

#### Problem: Chat responses are empty or truncated
**Cause**: Model response limits or API issues

**Solutions:**
1. Check message history length (trim if too long)
2. Verify model supports your request type
3. Add error checking for response content

### Development Issues

#### Problem: Tests failing with API errors
**Cause**: Tests trying to make real API calls

**Solution:**
```python
# Ensure tests use mocks, not real API calls
@patch("mcp_poc.app._openai_client.get_client")
def test_function(mock_get_client):
    # Test with mocked client
```

#### Problem: Import errors in tests
**Cause**: Package structure or path issues

**Solutions:**
```bash
# Install in editable mode
pip install -e .

# Or run tests from correct directory
cd /path/to/mcp-ai-poc
python -m pytest
```

## Debugging Techniques

### Enable Debug Logging
```bash
# Set OpenAI debug logging
export OPENAI_LOG=debug
python -m mcp_poc.app
```

### Test API Connection
```python
# Quick API test
from mcp_poc.app import OpenAIClient

try:
    client = OpenAIClient()
    openai_client = client.get_client()
    models = openai_client.models.list()
    print("API connection successful!")
    print(f"Available models: {len(models.data)}")
except Exception as e:
    print(f"API connection failed: {e}")
```

### Verify Environment
```python
import os
print(f"API Key set: {'OPENAI_API_KEY' in os.environ}")
print(f"Python version: {sys.version}")
print(f"OpenAI version: {openai.__version__}")
```

## Performance Issues

### Slow Response Times
**Causes & Solutions:**
1. **Large message history**: Trim conversation history periodically
2. **Complex model**: Use lighter models for simple tasks (gpt-3.5-turbo vs gpt-4o)
3. **Network issues**: Check internet connection and OpenAI service status

### Memory Usage
**Causes & Solutions:**
1. **Growing message history**: Implement history limits
2. **Large responses**: Set max_tokens parameter in API calls

## Getting Help

### Check Logs
```bash
# Run with verbose output
python -c "
import logging
logging.basicConfig(level=logging.DEBUG)
from mcp_poc.app import chat_loop
chat_loop()
"
```

### Verify Dependencies
```bash
pip list | grep openai
pip check
```

### Test Minimal Example
```python
# Minimal test to isolate issues
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Hello"}]
)
print(response.choices[0].message.content)
```

### Resources
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [OpenAI Python SDK](https://github.com/openai/openai-python)
- [OpenAI Status Page](https://status.openai.com/)
- Project Issues: Check repository issue tracker
