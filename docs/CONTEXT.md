# Project Context for AI

## What is this project?

**MCP AI POC** is a Python proof-of-concept application that demonstrates modern integration with OpenAI's API using their latest Python SDK (>=1.0.0). The project serves as a foundation for building AI-powered applications with conversational interfaces.

## Key Characteristics

### **Technology Stack**
- **Language**: Python 3.11+
- **Primary Dependency**: OpenAI Python SDK
- **Testing**: pytest
- **Package Management**: pip with requirements.txt
- **Build System**: setuptools via pyproject.toml

### **Application Type**
- Command-line interactive chat application
- Library/module for AI integration
- Educational/demonstration project

### **Architecture Pattern**
- Simple, clean modular design
- Singleton-like client management
- Functional programming approach
- Clear separation of concerns

## Core Functionality

1. **Interactive Chat Interface**: Terminal-based conversation with OpenAI models
2. **Model Selection**: Dynamic discovery and selection of available GPT models  
3. **Conversation History**: Maintains context across chat turns
4. **API Client Management**: Efficient OpenAI client instantiation and reuse
5. **Error Handling**: Graceful handling of API failures and configuration issues

## When to use this project

### **Good for:**
- Learning OpenAI API integration patterns
- Building chatbots or conversational AI apps
- Prototyping AI-powered features
- Educational purposes for AI/ML developers
- Base template for larger AI applications

### **Not designed for:**
- Production-scale applications (needs scaling considerations)
- Web interfaces (CLI-focused)
- Complex multi-agent systems
- Enterprise authentication/authorization

## Development Context

### **File Organization Logic**
```
src/mcp_poc/     # Core application code
src/tests/       # Unit tests
docs/            # Documentation for AI context
scripts/         # Development utilities
```

### **Key Design Decisions**
- Environment-based API key configuration (secure, flexible)
- Lazy client initialization (efficient resource usage)
- Module-level client instance (simplified usage)
- Default to GPT-4o model (balance of capability and cost)

### **Testing Strategy**
- Mock external API calls for reliable testing
- Test error conditions and edge cases
- Focus on core functionality verification

## AI Assistant Guidelines

When working with this codebase:

1. **Maintain simplicity** - This is a POC, not a complex framework
2. **Follow existing patterns** - Consistent with current architecture
3. **Test changes** - Add tests for new functionality
4. **Consider API costs** - Be mindful of OpenAI usage in examples
5. **Keep it educational** - Code should be easy to understand and learn from

### **Common Tasks**
- Adding new chat features or commands
- Implementing different conversation patterns
- Extending model selection capabilities
- Adding configuration options
- Improving error handling and user experience

### **Integration Points**
- Environment variables (API keys, configuration)
- OpenAI API (models, chat completions)
- Terminal I/O (user interaction)
- Python package system (imports, distribution)

This project represents a clean, minimal starting point for OpenAI integration that can be extended based on specific use cases while maintaining clarity and educational value.
