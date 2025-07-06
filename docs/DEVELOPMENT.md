# Development Guide

## Getting Started

### Prerequisites
- Python 3.11 or higher
- OpenAI API key

### Environment Setup

1. **Clone and navigate to the repository**
   ```bash
   git clone <repository-url>
   cd mcp-ai-poc
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   ./scripts/install_deps.sh
   ```

4. **Install package in editable mode**
   ```bash
   pip install -e .
   ```

5. **Set up environment variables**
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```

## Running the Application

### Interactive Chat Mode
```bash
python -m mcp_poc.app
```

### Using as a Module
```python
from mcp_poc.app import generate_completion

messages = [{"role": "user", "content": "Hello!"}]
response = generate_completion(messages)
print(response)
```

## Testing

### Run All Tests
```bash
pytest
```

### Run with Coverage
```bash
pytest --cov=mcp_poc
```

### Run Specific Test
```bash
pytest src/tests/test_app.py::test_generate_completion
```

## Code Quality

### Project Structure Guidelines
- Keep core logic in `src/mcp_poc/`
- Place tests in `src/tests/`
- Use descriptive function and variable names
- Follow PEP 8 style guidelines

### Testing Guidelines
- Mock external API calls in tests
- Test error conditions (missing API keys, network failures)
- Maintain good test coverage
- Use descriptive test names

## Common Development Tasks

### Adding New Features
1. Create feature branch
2. Implement functionality in `src/mcp_poc/`
3. Add corresponding tests in `src/tests/`
4. Run tests to ensure no regressions
5. Update documentation if needed

### Debugging
- Use environment variable `OPENAI_LOG=debug` for detailed API logs
- Check API key configuration if authentication fails
- Review OpenAI API documentation for model-specific requirements
