# MCP AI POC

[![CI](https://github.com/drewtech/mcp-ai-poc/actions/workflows/ci.yml/badge.svg)](https://github.com/drewtech/mcp-ai-poc/actions)

**MCP (Model Context Protocol) Server** with AI-powered development tools and resources.

## What This Project Provides

This project provides a comprehensive **MCP server** that offers:

### 🛠️ **AI-Powered Tools**
- **Code Generation**: Generate production-ready code from specifications
- **Code Refactoring**: Improve existing code for better maintainability, performance, or readability
- **Debugging Assistant**: Analyze and fix code issues with detailed explanations
- **Performance Optimization**: Identify bottlenecks and optimize code performance
- **Test Generation**: Create comprehensive unit tests for any codebase

### 📋 **Smart Prompts**
- **Code Analysis**: Deep analysis for quality, security, and best practices
- **Documentation Generation**: Auto-generate docs in multiple styles (Google, Sphinx, NumPy)
- **Code Review**: Comprehensive reviews with focus on specific areas
- **Concept Explanation**: Explain programming concepts at different skill levels

### 📚 **Knowledge Resources**
- **Python Coding Guidelines**: Best practices and style guides
- **Design Patterns Reference**: Common patterns with examples
- **Security Best Practices**: Security guidelines and vulnerability prevention
- **Performance Optimization Guide**: Strategies for faster, more efficient code

## Quick Start

### 1. Installation

```bash
# Clone and set up the project
git clone <your-repo-url>
cd mcp-ai-poc

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r dev-requirements.txt  # For development and testing

# Install in editable mode
pip install -e .
```

### 2. Set Up Environment

```bash
# Set your OpenAI API key
export OPENAI_API_KEY="your-api-key-here"
```

### 3. Run as MCP Server

```bash
# Start MCP server
python src/run.py
# or
python -m mcp_poc.standalone_server
```

### 4. Run Tests (Optional)

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest src/tests/test_server.py
```

## MCP Integration

### Using with MCP-Compatible Clients

This server implements the Model Context Protocol and can be used with any MCP-compatible client like Claude Desktop, etc.

#### Configuration Example

Add to your MCP client configuration:

```json
{
  "mcpServers": {
    "mcp-ai-poc": {
      "command": "python",
      "args": ["/path/to/mcp-ai-poc/src/run.py"],
      "env": {
        "OPENAI_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

#### Available MCP Capabilities

**Tools:**
- `generate_code` - Generate code from specifications
- `refactor_code` - Refactor existing code
- `debug_code` - Debug and fix code issues
- `optimize_performance` - Optimize code performance
- `generate_tests` - Generate unit tests

**Prompts:**
- `analyze_code` - Comprehensive code analysis
- `generate_documentation` - Create documentation
- `code_review` - Perform code reviews
- `explain_concept` - Explain programming concepts

**Resources:**
- `coding-guidelines://python` - Python best practices
- `patterns://design-patterns` - Design patterns reference
- `security://best-practices` - Security guidelines
- `performance://optimization-guide` - Performance tips

## Key Features

### 🚀 **Comprehensive MCP Server**

This project provides a full-featured MCP server with production-ready capabilities:

### 🔧 **Architecture**

- **Standalone Server**: No external MCP dependencies required
- **JSON-RPC Protocol**: Implements MCP's communication protocol
- **Modular Design**: Separate modules for AI tools, server logic, and utilities
- **Error Handling**: Robust error handling for production use
- **Comprehensive Testing**: Full test suite with pytest for reliability

### 💡 **Practical AI Tools**

Each tool is designed to solve real development problems:

- **Code Generation**: Handles specifications with context awareness
- **Refactoring**: Focuses on specific goals (performance, readability, etc.)
- **Debugging**: Provides root cause analysis and fixes
- **Optimization**: Identifies bottlenecks with trade-off analysis
- **Testing**: Generates comprehensive test suites

### 📖 **Rich Knowledge Base**

Built-in resources provide instant access to:
- Coding standards and best practices
- Security guidelines
- Performance optimization strategies
- Design pattern references

## Use Cases

### For Individual Developers
- **Code Review**: Get instant feedback on your code
- **Learning**: Understand concepts and best practices
- **Debugging**: Get help with tricky bugs
- **Documentation**: Generate docs automatically

### For Teams
- **Consistency**: Enforce coding standards across the team
- **Knowledge Sharing**: Built-in best practices and patterns
- **Code Quality**: Automated analysis and suggestions
- **Onboarding**: Help new team members learn patterns

### For AI Assistants
- **Enhanced Capabilities**: Provide AI assistants with powerful development tools
- **Context-Aware Help**: Tools understand programming context
- **Structured Responses**: Well-formatted, actionable output
- **Resource Access**: Built-in knowledge base for common questions

## Project Structure

```
src/
├── mcp_poc/                    # Main package
│   ├── __init__.py            # Package initialization
│   ├── app.py                 # Main application (chat + server entry)
│   ├── ai_tools.py            # OpenAI client and utilities
│   ├── standalone_server.py   # MCP server implementation
│   └── mcp_server.py          # Alternative MCP server (requires mcp package)
├── tests/                     # Test suite
│   ├── test_app.py           # Application tests
│   └── test_server.py        # MCP server tests
└── run.py                     # Main entry point

Configuration & Dependencies:
├── requirements.txt           # Runtime dependencies
├── dev-requirements.txt       # Development and testing dependencies
├── pyproject.toml            # Project configuration and build settings
└── mcp_config.json           # MCP client configuration example

Documentation:                # Comprehensive docs
├── docs/
│   ├── CONTEXT.md            # Project overview
│   ├── ARCHITECTURE.md       # Technical details
│   ├── API.md                # API reference
│   ├── DEVELOPMENT.md        # Development guide
│   ├── EXAMPLES.md           # Usage examples
│   └── TROUBLESHOOTING.md    # Common issues
└── README.md                 # This file
```

## Documentation

### For AI Assistants
- **[📋 Project Context](docs/CONTEXT.md)** - High-level overview and AI guidelines
- **[🏗️ Architecture](docs/ARCHITECTURE.md)** - Code structure and design patterns
- **[📚 API Reference](docs/API.md)** - Detailed function and class documentation

### For Developers
- **[🛠️ Development Guide](docs/DEVELOPMENT.md)** - Setup, testing, and contribution guidelines
- **[💡 Examples](docs/EXAMPLES.md)** - Usage examples and integration patterns
- **[🐛 Troubleshooting](docs/TROUBLESHOOTING.md)** - Common issues and solutions

## Enhanced Features

### 🎯 **Intelligent Code Analysis**
- Multi-dimensional code quality assessment
- Security vulnerability detection
- Performance bottleneck identification
- Best practice recommendations

### 🔄 **Context-Aware Refactoring**
- Goal-specific refactoring (performance, readability, maintainability)
- Language-specific optimizations
- Preservation of functionality
- Clear change explanations

### 🐛 **Advanced Debugging**
- Root cause analysis
- Step-by-step problem breakdown
- Fixed code with explanations
- Prevention strategies

### ⚡ **Performance Optimization**
- Algorithmic improvements
- Memory usage optimization
- Concurrency recommendations
- Trade-off analysis

### 🧪 **Comprehensive Testing**
- Framework-specific test generation
- Edge case coverage
- Multiple testing strategies
- Production-ready test code

## Next Steps for Further Enhancement

### 1. **Add More Tools**
- **API Documentation Generator**: Auto-generate API docs
- **Database Query Optimizer**: Optimize SQL queries
- **Dependency Analyzer**: Analyze and update dependencies
- **Code Complexity Analyzer**: Measure and reduce complexity

### 2. **Enhanced Resources**
- **Framework-Specific Guides**: React, Django, FastAPI guides
- **Language References**: Support for more programming languages
- **Architecture Patterns**: Microservices, event-driven, etc.
- **DevOps Best Practices**: CI/CD, deployment, monitoring

### 3. **Integration Features**
- **Git Integration**: Analyze commits, generate changelogs
- **IDE Plugins**: VS Code, IntelliJ extensions
- **CI/CD Integration**: Automated code analysis in pipelines
- **Slack/Teams Bots**: Team collaboration features

### 4. **Advanced AI Features**
- **Multi-Model Support**: Support for different AI models
- **Custom Training**: Fine-tune models for specific codebases
- **Code Similarity Detection**: Find similar code patterns
- **Automated Testing**: AI-generated integration tests

This enhanced MCP server transforms your simple chat client into a powerful development assistant that can be integrated into any MCP-compatible environment, providing immediate value to developers and AI assistants alike.