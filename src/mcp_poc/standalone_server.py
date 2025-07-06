"""
Standalone MCP server implementation with JSON-RPC protocol.
This provides a complete MCP server without requiring the mcp package.
"""

import asyncio
import json
import logging
import sys
from typing import Any, Dict
from .ai_tools import OpenAIClient

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global OpenAI client
openai_client = OpenAIClient()


class JSONRPCServer:
    """Simple JSON-RPC server for MCP protocol."""

    def __init__(self, server_name: str = "mcp-ai-poc"):
        self.server_name = server_name
        self.handlers = {}
        self.setup_handlers()

    def setup_handlers(self):
        """Set up MCP protocol handlers."""

        # Initialize handler
        self.handlers["initialize"] = self.handle_initialize

        # Capability handlers
        self.handlers["prompts/list"] = self.handle_list_prompts
        self.handlers["prompts/get"] = self.handle_get_prompt
        self.handlers["tools/list"] = self.handle_list_tools
        self.handlers["tools/call"] = self.handle_call_tool
        self.handlers["resources/list"] = self.handle_list_resources
        self.handlers["resources/read"] = self.handle_read_resource

    async def handle_initialize(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle initialization request."""
        return {
            "protocolVersion": "2024-11-05",
            "serverInfo": {"name": self.server_name, "version": "1.0.0"},
            "capabilities": {
                "prompts": {"listChanged": False},
                "tools": {"listChanged": False},
                "resources": {"listChanged": False, "subscribe": False},
            },
        }

    async def handle_list_prompts(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """List available prompts."""
        return {
            "prompts": [
                {
                    "name": "analyze_code",
                    "description": "Analyze code for quality, security, and best practices",
                    "arguments": [
                        {
                            "name": "code",
                            "description": "The code to analyze",
                            "required": True,
                        },
                        {
                            "name": "language",
                            "description": "Programming language of the code",
                            "required": False,
                        },
                    ],
                },
                {
                    "name": "generate_documentation",
                    "description": "Generate comprehensive documentation for code",
                    "arguments": [
                        {
                            "name": "code",
                            "description": "The code to document",
                            "required": True,
                        },
                        {
                            "name": "style",
                            "description": "Documentation style (e.g., 'sphinx', 'google', 'numpy')",
                            "required": False,
                        },
                    ],
                },
                {
                    "name": "code_review",
                    "description": "Perform a comprehensive code review",
                    "arguments": [
                        {
                            "name": "code",
                            "description": "The code to review",
                            "required": True,
                        },
                        {
                            "name": "focus",
                            "description": "Review focus (e.g., 'security', 'performance', 'maintainability')",
                            "required": False,
                        },
                    ],
                },
                {
                    "name": "explain_concept",
                    "description": "Explain programming concepts or technologies",
                    "arguments": [
                        {
                            "name": "concept",
                            "description": "The concept to explain",
                            "required": True,
                        },
                        {
                            "name": "level",
                            "description": "Explanation level (e.g., 'beginner', 'intermediate', 'advanced')",
                            "required": False,
                        },
                    ],
                },
            ]
        }

    async def handle_get_prompt(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Get a specific prompt."""
        name = params.get("name", "")
        arguments = params.get("arguments", {})

        prompt_templates = {
            "analyze_code": """Analyze the following {language} code for:
1. Code quality and best practices
2. Potential bugs or issues
3. Security vulnerabilities
4. Performance considerations
5. Maintainability and readability

Code to analyze:
```{language}
{code}
```

Provide a detailed analysis with specific recommendations for improvement.""",
            "generate_documentation": """Generate comprehensive documentation for the following code using {style} style:

Code:
```
{code}
```

Include:
1. Function/class descriptions
2. Parameter documentation
3. Return value documentation
4. Usage examples
5. Exception handling information

Use {style} documentation format.""",
            "code_review": """Perform a comprehensive code review with focus on {focus}:

Code to review:
```
{code}
```

Review criteria:
1. Code structure and organization
2. Error handling and edge cases
3. Performance implications
4. Security considerations
5. Adherence to best practices
6. Testing considerations

Focus area: {focus}

Provide constructive feedback with specific suggestions for improvement.""",
            "explain_concept": """Explain the programming concept "{concept}" at a {level} level.

Include:
1. Clear definition and explanation
2. Why it's important/useful
3. Common use cases and examples
4. Best practices
5. Common pitfalls to avoid
6. Related concepts

Tailor the explanation to a {level} audience.""",
        }

        if name not in prompt_templates:
            raise ValueError(f"Unknown prompt: {name}")

        # Fill in template with arguments
        template = prompt_templates[name]
        code = arguments.get("code", "")
        language = arguments.get("language", "unknown")
        style = arguments.get("style", "google")
        focus = arguments.get("focus", "general")
        concept = arguments.get("concept", "")
        level = arguments.get("level", "intermediate")

        prompt_text = template.format(
            code=code,
            language=language,
            style=style,
            focus=focus,
            concept=concept,
            level=level,
        )

        return {
            "description": f"Generated prompt for {name}",
            "messages": [
                {"role": "user", "content": {"type": "text", "text": prompt_text}}
            ],
        }

    async def handle_list_tools(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """List available tools."""
        return {
            "tools": [
                {
                    "name": "generate_code",
                    "description": "Generate code based on specifications",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "specification": {
                                "type": "string",
                                "description": "Description of what code to generate",
                            },
                            "language": {
                                "type": "string",
                                "description": "Programming language for the code",
                                "default": "python",
                            },
                            "style": {
                                "type": "string",
                                "description": "Coding style or framework to use",
                                "default": "clean",
                            },
                        },
                        "required": ["specification"],
                    },
                },
                {
                    "name": "refactor_code",
                    "description": "Refactor existing code for better quality",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "code": {
                                "type": "string",
                                "description": "The code to refactor",
                            },
                            "goal": {
                                "type": "string",
                                "description": "Refactoring goal (e.g., 'performance', 'readability', 'maintainability')",
                                "default": "maintainability",
                            },
                            "language": {
                                "type": "string",
                                "description": "Programming language of the code",
                                "default": "python",
                            },
                        },
                        "required": ["code"],
                    },
                },
                {
                    "name": "debug_code",
                    "description": "Help debug code issues and find solutions",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "code": {
                                "type": "string",
                                "description": "The code with issues",
                            },
                            "error": {
                                "type": "string",
                                "description": "Error message or description of the problem",
                            },
                            "context": {
                                "type": "string",
                                "description": "Additional context about when the error occurs",
                            },
                        },
                        "required": ["code", "error"],
                    },
                },
                {
                    "name": "optimize_performance",
                    "description": "Analyze and optimize code performance",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "code": {
                                "type": "string",
                                "description": "The code to optimize",
                            },
                            "bottleneck": {
                                "type": "string",
                                "description": "Known performance bottleneck or area of concern",
                            },
                            "constraints": {
                                "type": "string",
                                "description": "Performance constraints or requirements",
                            },
                        },
                        "required": ["code"],
                    },
                },
                {
                    "name": "generate_tests",
                    "description": "Generate unit tests for given code",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "code": {
                                "type": "string",
                                "description": "The code to generate tests for",
                            },
                            "framework": {
                                "type": "string",
                                "description": "Testing framework to use (e.g., 'pytest', 'unittest', 'jest')",
                                "default": "pytest",
                            },
                            "coverage": {
                                "type": "string",
                                "description": "Desired test coverage level",
                                "default": "comprehensive",
                            },
                        },
                        "required": ["code"],
                    },
                },
            ]
        }

    async def handle_call_tool(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle tool calls."""
        name = params.get("name", "")
        arguments = params.get("arguments", {})

        try:
            client = openai_client.get_client()

            # Tool implementations
            if name == "generate_code":
                specification = arguments.get("specification", "")
                language = arguments.get("language", "python")
                style = arguments.get("style", "clean")

                prompt = f"""Generate {language} code based on this specification:

{specification}

Requirements:
- Use {style} coding style
- Include appropriate comments
- Follow best practices for {language}
- Make the code production-ready
- Include error handling where appropriate

Generate only the code, no explanations."""

                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.3,
                )

                return {
                    "content": [
                        {"type": "text", "text": response.choices[0].message.content}
                    ]
                }

            elif name == "refactor_code":
                code = arguments.get("code", "")
                goal = arguments.get("goal", "maintainability")
                language = arguments.get("language", "python")

                prompt = f"""Refactor this {language} code with focus on {goal}:

Original code:
```{language}
{code}
```

Refactoring goals:
- Improve {goal}
- Maintain functionality
- Follow {language} best practices
- Add improvements where beneficial

Provide the refactored code with comments explaining the changes."""

                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.3,
                )

                return {
                    "content": [
                        {"type": "text", "text": response.choices[0].message.content}
                    ]
                }

            elif name == "debug_code":
                code = arguments.get("code", "")
                error = arguments.get("error", "")
                context = arguments.get("context", "")

                prompt = f"""Help debug this code issue:

Code:
```
{code}
```

Error: {error}

Context: {context}

Please:
1. Identify the root cause of the issue
2. Explain why the error is occurring
3. Provide a fixed version of the code
4. Suggest preventive measures for similar issues"""

                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.3,
                )

                return {
                    "content": [
                        {"type": "text", "text": response.choices[0].message.content}
                    ]
                }

            elif name == "optimize_performance":
                code = arguments.get("code", "")
                bottleneck = arguments.get("bottleneck", "")
                constraints = arguments.get("constraints", "")

                prompt = f"""Analyze and optimize this code for performance:

Code:
```
{code}
```

Known bottleneck: {bottleneck}
Constraints: {constraints}

Please:
1. Identify performance issues
2. Suggest optimization strategies
3. Provide optimized code
4. Explain the performance improvements
5. Mention any trade-offs"""

                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.3,
                )

                return {
                    "content": [
                        {"type": "text", "text": response.choices[0].message.content}
                    ]
                }

            elif name == "generate_tests":
                code = arguments.get("code", "")
                framework = arguments.get("framework", "pytest")
                coverage = arguments.get("coverage", "comprehensive")

                prompt = f"""Generate {coverage} unit tests for this code using {framework}:

Code to test:
```
{code}
```

Test requirements:
- Use {framework} framework
- {coverage} test coverage
- Test both positive and negative cases
- Include edge cases
- Add appropriate assertions
- Follow testing best practices

Generate complete test code that can be run immediately."""

                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.3,
                )

                return {
                    "content": [
                        {"type": "text", "text": response.choices[0].message.content}
                    ]
                }

            else:
                raise ValueError(f"Unknown tool: {name}")

        except Exception as e:
            logger.error(f"Error in tool {name}: {e}")
            return {
                "content": [{"type": "text", "text": f"Error: {str(e)}"}],
                "isError": True,
            }

    async def handle_list_resources(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """List available resources."""
        return {
            "resources": [
                {
                    "uri": "coding-guidelines://python",
                    "name": "Python Coding Guidelines",
                    "description": "Comprehensive Python coding best practices and guidelines",
                    "mimeType": "text/markdown",
                },
                {
                    "uri": "patterns://design-patterns",
                    "name": "Design Patterns Reference",
                    "description": "Common software design patterns with examples",
                    "mimeType": "text/markdown",
                },
                {
                    "uri": "security://best-practices",
                    "name": "Security Best Practices",
                    "description": "Security guidelines for safe coding practices",
                    "mimeType": "text/markdown",
                },
                {
                    "uri": "performance://optimization-guide",
                    "name": "Performance Optimization Guide",
                    "description": "Techniques and strategies for code optimization",
                    "mimeType": "text/markdown",
                },
            ]
        }

    async def handle_read_resource(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Read a specific resource."""
        uri = params.get("uri", "")

        resources = {
            "coding-guidelines://python": """# Python Coding Guidelines

## Code Style
- Follow PEP 8 for style guidelines
- Use meaningful variable and function names
- Keep functions small and focused (single responsibility)
- Use type hints for better code documentation

## Best Practices
- Use virtual environments for dependency management
- Write docstrings for all public functions and classes
- Handle exceptions appropriately
- Use logging instead of print statements
- Write unit tests for your code

## Performance Tips
- Use list comprehensions and generator expressions
- Prefer built-in functions over custom implementations
- Use appropriate data structures (dict, set, list)
- Profile your code to identify bottlenecks

## Security Considerations
- Validate all user inputs
- Use parameterized queries for database operations
- Don't store secrets in code
- Keep dependencies up to date""",
            "patterns://design-patterns": """# Design Patterns Reference

## Creational Patterns
- **Singleton**: Ensure only one instance exists
- **Factory**: Create objects without specifying exact classes
- **Builder**: Construct complex objects step by step

## Structural Patterns
- **Adapter**: Allow incompatible interfaces to work together
- **Decorator**: Add behavior to objects dynamically
- **Facade**: Provide simplified interface to complex subsystem

## Behavioral Patterns
- **Observer**: Define one-to-many dependency between objects
- **Strategy**: Define family of algorithms and make them interchangeable
- **Command**: Encapsulate requests as objects

## When to Use
Choose patterns based on the specific problem you're solving, not because they're popular.""",
            "security://best-practices": """# Security Best Practices

## Input Validation
- Validate all user inputs
- Use allowlists over blocklists
- Sanitize data before processing

## Authentication & Authorization
- Use strong authentication mechanisms
- Implement proper session management
- Follow principle of least privilege

## Data Protection
- Encrypt sensitive data at rest and in transit
- Use secure random number generators
- Implement proper key management

## Common Vulnerabilities
- SQL Injection: Use parameterized queries
- XSS: Escape output properly
- CSRF: Use anti-CSRF tokens
- Path Traversal: Validate file paths

## Dependencies
- Keep all dependencies updated
- Use vulnerability scanners
- Review third-party code""",
            "performance://optimization-guide": """# Performance Optimization Guide

## Profiling
- Measure before optimizing
- Use profiling tools to identify bottlenecks
- Focus on the 80/20 rule

## Algorithm Optimization
- Choose appropriate algorithms and data structures
- Consider time and space complexity
- Use caching for expensive operations

## Database Optimization
- Use proper indexing
- Optimize queries
- Consider connection pooling

## Memory Management
- Avoid memory leaks
- Use appropriate data structures
- Consider lazy loading for large datasets

## Concurrency
- Use async/await for I/O-bound operations
- Consider multiprocessing for CPU-bound tasks
- Be aware of GIL limitations in Python""",
        }

        if uri not in resources:
            raise ValueError(f"Unknown resource: {uri}")

        return {"contents": [{"type": "text", "text": resources[uri]}]}

    async def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle a JSON-RPC request."""
        try:
            method = request.get("method", "")
            params = request.get("params", {})
            request_id = request.get("id")

            if method not in self.handlers:
                raise ValueError(f"Unknown method: {method}")

            result = await self.handlers[method](params)

            return {"jsonrpc": "2.0", "id": request_id, "result": result}

        except Exception as e:
            logger.error(f"Error handling request: {e}")
            return {
                "jsonrpc": "2.0",
                "id": request.get("id"),
                "error": {"code": -1, "message": str(e)},
            }

    async def run(self):
        """Run the server using stdio."""
        try:
            while True:
                # Read line from stdin
                line = await asyncio.get_event_loop().run_in_executor(
                    None, sys.stdin.readline
                )

                if not line:
                    break

                try:
                    request = json.loads(line.strip())
                    response = await self.handle_request(request)

                    # Write response to stdout
                    print(json.dumps(response), flush=True)

                except json.JSONDecodeError as e:
                    logger.error(f"Invalid JSON: {e}")
                    error_response = {
                        "jsonrpc": "2.0",
                        "id": None,
                        "error": {"code": -32700, "message": "Parse error"},
                    }
                    print(json.dumps(error_response), flush=True)

        except KeyboardInterrupt:
            logger.info("Server stopped by user")
        except Exception as e:
            logger.error(f"Server error: {e}")


async def main():
    """Main entry point for the MCP server."""
    server = JSONRPCServer("mcp-ai-poc")
    await server.run()


if __name__ == "__main__":
    asyncio.run(main())
