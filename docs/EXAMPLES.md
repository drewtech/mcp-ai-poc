# MCP AI POC Examples

This document provides comprehensive examples of using the enhanced MCP AI POC server.

## Using the Interactive Chat Mode

```bash
# Start interactive chat
python run.py

# Example conversation:
You: Explain how async/await works in Python
AI: [Detailed explanation of async/await concepts]

You: Generate a FastAPI endpoint for user authentication
AI: [Complete FastAPI code with authentication logic]
```

## Using as MCP Server

### 1. Start the Server

```bash
# Terminal 1: Start MCP server
python run.py --server
```

### 2. Test with Direct JSON-RPC

```bash
# Terminal 2: Send test requests
echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}' | python run.py --server

echo '{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}' | python run.py --server
```

### 3. Integration with Claude Desktop

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "mcp-ai-poc": {
      "command": "python",
      "args": ["/path/to/mcp-ai-poc/run.py", "--server"],
      "env": {
        "OPENAI_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

## Tool Usage Examples

### 1. Generate Code

**Input:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "generate_code",
    "arguments": {
      "specification": "Create a Python class for managing a todo list with add, remove, and list methods",
      "language": "python",
      "style": "clean"
    }
  }
}
```

**Output:**
```python
class TodoList:
    """A simple todo list manager."""
    
    def __init__(self):
        self.todos = []
    
    def add_todo(self, task: str) -> bool:
        """Add a new todo item."""
        if not task.strip():
            raise ValueError("Task cannot be empty")
        
        todo_item = {
            'id': len(self.todos) + 1,
            'task': task.strip(),
            'completed': False
        }
        self.todos.append(todo_item)
        return True
    
    def remove_todo(self, todo_id: int) -> bool:
        """Remove a todo item by ID."""
        for i, todo in enumerate(self.todos):
            if todo['id'] == todo_id:
                self.todos.pop(i)
                return True
        return False
    
    def list_todos(self) -> list:
        """Get all todo items."""
        return self.todos.copy()
```

### 2. Refactor Code

**Input:**
```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/call",
  "params": {
    "name": "refactor_code",
    "arguments": {
      "code": "def calc(a,b,op):\n    if op=='+':\n        return a+b\n    elif op=='-':\n        return a-b\n    elif op=='*':\n        return a*b\n    elif op=='/':\n        return a/b",
      "goal": "maintainability",
      "language": "python"
    }
  }
}
```

**Output includes improved version with type hints, error handling, enums, and documentation.**

### 3. Debug Code

**Input:**
```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "method": "tools/call",
  "params": {
    "name": "debug_code",
    "arguments": {
      "code": "def fibonacci(n):\n    if n <= 1:\n        return n\n    return fibonacci(n-1) + fibonacci(n-2)\n\nprint(fibonacci(50))",
      "error": "Code is extremely slow for large values",
      "context": "Calculating fibonacci(50) takes forever"
    }
  }
}
```

**Output provides root cause analysis and optimized solutions using memoization or iteration.**

## Prompt Usage Examples

### 1. Code Analysis Prompt

**Request:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "prompts/get",
  "params": {
    "name": "analyze_code",
    "arguments": {
      "code": "import requests\n\ndef get_user_data(user_id):\n    url = f'https://api.example.com/users/{user_id}'\n    response = requests.get(url)\n    return response.json()",
      "language": "python"
    }
  }
}
```

**Generated Prompt includes comprehensive analysis criteria for code quality, bugs, security, performance, and maintainability.**

### 2. Documentation Generation Prompt

**Request:**
```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "prompts/get",
  "params": {
    "name": "generate_documentation",
    "arguments": {
      "code": "class DataProcessor:\n    def __init__(self, config):\n        self.config = config\n    \n    def process(self, data):\n        # Process the data\n        return processed_data",
      "style": "google"
    }
  }
}
```

## Resource Usage Examples

### 1. Access Python Guidelines

**Request:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "resources/read",
  "params": {
    "uri": "coding-guidelines://python"
  }
}
```

**Response:** Returns comprehensive Python coding guidelines including PEP 8, best practices, performance tips, and security considerations.

### 2. Get Design Patterns Reference

**Request:**
```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "resources/read",
  "params": {
    "uri": "patterns://design-patterns"
  }
}
```

**Response:** Returns detailed information about creational, structural, and behavioral design patterns with use cases.

## Integration Examples

### With Custom Scripts

```python
#!/usr/bin/env python3
"""
Custom script to use MCP AI POC for code generation.
"""

import json
import subprocess
import sys

def generate_code(specification, language="python"):
    """Generate code using MCP server."""
    request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": "generate_code",
            "arguments": {
                "specification": specification,
                "language": language
            }
        }
    }
    
    # Start MCP server process
    process = subprocess.Popen(
        ["python", "run.py", "--server"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Send request
    stdout, stderr = process.communicate(json.dumps(request) + "\n")
    
    if stderr:
        print(f"Error: {stderr}", file=sys.stderr)
        return None
    
    response = json.loads(stdout)
    if "result" in response:
        return response["result"]["content"][0]["text"]
    else:
        print(f"Error in response: {response.get('error', 'Unknown error')}")
        return None

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python generate.py 'code specification'")
        sys.exit(1)
    
    code = generate_code(sys.argv[1])
    if code:
        print(code)
```

### With Jupyter Notebooks

```python
# In a Jupyter cell
import json
import subprocess

def mcp_tool_call(tool_name, arguments):
    """Call MCP tool from Jupyter notebook."""
    request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": tool_name,
            "arguments": arguments
        }
    }
    
    process = subprocess.run(
        ["python", "../run.py", "--server"],
        input=json.dumps(request),
        capture_output=True,
        text=True
    )
    
    response = json.loads(process.stdout)
    return response["result"]["content"][0]["text"]

# Generate unit tests for a function
test_code = mcp_tool_call("generate_tests", {
    "code": """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
    """,
    "framework": "pytest"
})

print(test_code)
```

## Original Chat Examples (Still Available)

### Simple Question-Answer
```python
from mcp_poc.app import generate_completion

# Single user question
messages = [
    {"role": "user", "content": "What is the capital of France?"}
]

response = generate_completion(messages)
print(response)  # "The capital of France is Paris."
```

### System-Prompted Assistant
```python
# Create a specialized assistant
messages = [
    {"role": "system", "content": "You are a Python programming tutor."},
    {"role": "user", "content": "How do I create a dictionary in Python?"}
]

response = generate_completion(messages, model="gpt-4o")
print(response)
```

These examples demonstrate the versatility and power of the enhanced MCP AI POC server for various development workflows and integration scenarios.
