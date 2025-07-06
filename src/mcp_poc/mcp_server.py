"""
MCP Server implementation for AI-powered tools and resources.
"""

import asyncio
import json
import logging
import sys
from typing import Any, Dict, List, Optional, Sequence

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    CallToolRequest,
    CallToolResult,
    GetPromptRequest,
    GetPromptResult,
    ListPromptsRequest,
    ListPromptsResult,
    ListResourcesRequest,
    ListResourcesResult,
    ListToolsRequest,
    ListToolsResult,
    Prompt,
    PromptArgument,
    PromptMessage,
    ReadResourceRequest,
    ReadResourceResult,
    Resource,
    TextContent,
    Tool,
    TextResourceContents,
    BlobResourceContents,
)

import os
from .ai_tools import OpenAIClient


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global OpenAI client
openai_client = OpenAIClient()


class MCPAIServer:
    """MCP Server that provides AI-powered tools and resources."""
    
    def __init__(self):
        self.server = Server("mcp-ai-poc")
        self.setup_handlers()
    
    def setup_handlers(self):
        """Set up all MCP protocol handlers."""
        
        @self.server.list_prompts()
        async def handle_list_prompts() -> List[Prompt]:
            """List available prompts."""
            return [
                Prompt(
                    name="analyze_code",
                    description="Analyze code for quality, security, and best practices",
                    arguments=[
                        PromptArgument(
                            name="code",
                            description="The code to analyze",
                            required=True
                        ),
                        PromptArgument(
                                name="language",
                                description="Programming language of the code",
                                required=False
                            )
                        ]
                    ),
                    Prompt(
                        name="generate_documentation",
                        description="Generate comprehensive documentation for code",
                        arguments=[
                            PromptArgument(
                                name="code",
                                description="The code to document",
                                required=True
                            ),
                            PromptArgument(
                                name="style",
                                description="Documentation style (e.g., 'sphinx', 'google', 'numpy')",
                                required=False
                            )
                        ]
                    ),
                    Prompt(
                        name="code_review",
                        description="Perform a comprehensive code review",
                        arguments=[
                            PromptArgument(
                                name="code",
                                description="The code to review",
                                required=True
                            ),
                            PromptArgument(
                                name="focus",
                                description="Review focus (e.g., 'security', 'performance', 'maintainability')",
                                required=False
                            )
                        ]
                    ),
                    Prompt(
                        name="explain_concept",
                        description="Explain programming concepts or technologies",
                        arguments=[
                            PromptArgument(
                                name="concept",
                                description="The concept to explain",
                                required=True
                            ),
                            PromptArgument(
                                name="level",
                                description="Explanation level (e.g., 'beginner', 'intermediate', 'advanced')",
                                required=False
                            )
                        ]
                    )
                ]
        
        @self.server.get_prompt()
        async def handle_get_prompt(
            name: str, arguments: Optional[Dict[str, str]] = None
        ) -> GetPromptResult:
            """Get a specific prompt."""
            if arguments is None:
                arguments = {}
            
            if name == "analyze_code":
                code = arguments.get("code", "")
                language = arguments.get("language", "unknown")
                
                prompt = f"""Analyze the following {language} code for:
1. Code quality and best practices
2. Potential bugs or issues
3. Security vulnerabilities
4. Performance considerations
5. Maintainability and readability

Code to analyze:
```{language}
{code}
```

Provide a detailed analysis with specific recommendations for improvement."""
                
                return GetPromptResult(
                    description=f"Code analysis for {language} code",
                    messages=[
                        PromptMessage(
                            role="user",
                            content=TextContent(type="text", text=prompt)
                        )
                    ]
                )
            
            elif name == "generate_documentation":
                code = arguments.get("code", "")
                style = arguments.get("style", "google")
                
                prompt = f"""Generate comprehensive documentation for the following code using {style} style:

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

Use {style} documentation format."""
                
                return GetPromptResult(
                    description=f"Documentation generation using {style} style",
                    messages=[
                        PromptMessage(
                            role="user",
                            content=TextContent(type="text", text=prompt)
                        )
                    ]
                )
            
            elif name == "code_review":
                code = arguments.get("code", "")
                focus = arguments.get("focus", "general")
                
                prompt = f"""Perform a comprehensive code review with focus on {focus}:

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

Provide constructive feedback with specific suggestions for improvement."""
                
                return GetPromptResult(
                    description=f"Code review with {focus} focus",
                    messages=[
                        PromptMessage(
                            role="user",
                            content=TextContent(type="text", text=prompt)
                        )
                    ]
                )
            
            elif name == "explain_concept":
                concept = arguments.get("concept", "")
                level = arguments.get("level", "intermediate")
                
                prompt = f"""Explain the programming concept "{concept}" at a {level} level.

Include:
1. Clear definition and explanation
2. Why it's important/useful
3. Common use cases and examples
4. Best practices
5. Common pitfalls to avoid
6. Related concepts

Tailor the explanation to a {level} audience."""
                
                return GetPromptResult(
                    description=f"Explanation of {concept} at {level} level",
                    messages=[
                        PromptMessage(
                            role="user",
                            content=TextContent(type="text", text=prompt)
                        )
                    ]
                )
            
            else:
                raise ValueError(f"Unknown prompt: {name}")
        
        @self.server.list_tools()
        async def handle_list_tools() -> List[Tool]:
            """List available tools."""
            return [
                Tool(
                    name="generate_code",
                    description="Generate code based on specifications",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "specification": {
                                "type": "string",
                                "description": "Description of what code to generate"
                            },
                            "language": {
                                "type": "string",
                                "description": "Programming language for the code",
                                "default": "python"
                            },
                            "style": {
                                "type": "string",
                                "description": "Coding style or framework to use",
                                "default": "clean"
                            }
                        },
                        "required": ["specification"]
                        }
                    ),
                    Tool(
                        name="refactor_code",
                        description="Refactor existing code for better quality",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "code": {
                                    "type": "string",
                                    "description": "The code to refactor"
                                },
                                "goal": {
                                    "type": "string",
                                    "description": "Refactoring goal (e.g., 'performance', 'readability', 'maintainability')",
                                    "default": "maintainability"
                                },
                                "language": {
                                    "type": "string",
                                    "description": "Programming language of the code",
                                    "default": "python"
                                }
                            },
                            "required": ["code"]
                        }
                    ),
                    Tool(
                        name="debug_code",
                        description="Help debug code issues and find solutions",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "code": {
                                    "type": "string",
                                    "description": "The code with issues"
                                },
                                "error": {
                                    "type": "string",
                                    "description": "Error message or description of the problem"
                                },
                                "context": {
                                    "type": "string",
                                    "description": "Additional context about when the error occurs"
                                }
                            },
                            "required": ["code", "error"]
                        }
                    ),
                    Tool(
                        name="optimize_performance",
                        description="Analyze and optimize code performance",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "code": {
                                    "type": "string",
                                    "description": "The code to optimize"
                                },
                                "bottleneck": {
                                    "type": "string",
                                    "description": "Known performance bottleneck or area of concern"
                                },
                                "constraints": {
                                    "type": "string",
                                    "description": "Performance constraints or requirements"
                                }
                            },
                            "required": ["code"]
                        }
                    ),
                    Tool(
                        name="generate_tests",
                        description="Generate unit tests for given code",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "code": {
                                    "type": "string",
                                    "description": "The code to generate tests for"
                                },
                                "framework": {
                                    "type": "string",
                                    "description": "Testing framework to use (e.g., 'pytest', 'unittest', 'jest')",
                                    "default": "pytest"
                                },
                                "coverage": {
                                    "type": "string",
                                    "description": "Desired test coverage level",
                                    "default": "comprehensive"
                                }                        },
                        "required": ["code"]
                    }
                )
            ]
        
        @self.server.call_tool()  # type: ignore
        async def handle_call_tool(
            name: str, arguments: Optional[Dict[str, Any]] = None
        ) -> CallToolResult:
            """Handle tool calls."""
            if arguments is None:
                arguments = {}
            
            try:
                client = openai_client.get_client()
                
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
                        temperature=0.3
                    )
                    
                    return CallToolResult(
                        content=[
                            TextContent(
                                type="text",
                                text=response.choices[0].message.content or "No response generated"
                            )
                        ]
                    )
                
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
                        temperature=0.3
                    )
                    
                    return CallToolResult(
                        content=[
                            TextContent(
                                type="text",
                                text=response.choices[0].message.content or "No response generated"
                            )
                        ]
                    )
                
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
                        temperature=0.3
                    )
                    
                    return CallToolResult(
                        content=[
                            TextContent(
                                type="text",
                                text=response.choices[0].message.content or "No response generated"
                            )
                        ]
                    )
                
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
                        temperature=0.3
                    )
                    
                    return CallToolResult(
                        content=[
                            TextContent(
                                type="text",
                                text=response.choices[0].message.content or "No response generated"
                            )
                        ]
                    )
                
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
                        temperature=0.3
                    )
                    
                    return CallToolResult(
                        content=[
                            TextContent(
                                type="text",
                                text=response.choices[0].message.content or "No response generated"
                            )
                        ]
                    )
                
                else:
                    raise ValueError(f"Unknown tool: {name}")
                    
            except Exception as e:
                logger.error(f"Error in tool {name}: {e}")
                return CallToolResult(
                    content=[
                        TextContent(
                            type="text",
                            text=f"Error: {str(e)}"
                        )
                    ],
                    isError=True
                )
        
        @self.server.list_resources()  # type: ignore
        async def handle_list_resources() -> List[Resource]:
            """List available resources."""
            return [
                Resource(
                    uri="coding-guidelines://python",  # type: ignore
                    name="Python Coding Guidelines",
                    description="Comprehensive Python coding best practices and guidelines",
                    mimeType="text/markdown"
                ),
                Resource(
                    uri="patterns://design-patterns",  # type: ignore
                    name="Design Patterns Reference",
                    description="Common software design patterns with examples",
                    mimeType="text/markdown"
                ),
                Resource(
                    uri="security://best-practices",  # type: ignore                    name="Security Best Practices",
                    description="Security guidelines for safe coding practices",
                    mimeType="text/markdown"
                ),
                Resource(
                    uri="performance://optimization-guide",  # type: ignore
                    name="Performance Optimization Guide",
                    description="Techniques and strategies for code optimization",
                    mimeType="text/markdown"
                )
            ]
        
        @self.server.read_resource()  # type: ignore
        async def handle_read_resource(uri: str) -> ReadResourceResult:
            """Read a specific resource."""
            
            if uri == "coding-guidelines://python":
                content = """# Python Coding Guidelines

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
- Keep dependencies up to date
"""
                
            elif uri == "patterns://design-patterns":
                content = """# Design Patterns Reference

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
Choose patterns based on the specific problem you're solving, not because they're popular.
"""
                
            elif uri == "security://best-practices":
                content = """# Security Best Practices

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
- Review third-party code
"""
                
            elif uri == "performance://optimization-guide":
                content = """# Performance Optimization Guide

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
- Be aware of GIL limitations in Python
"""
            else:
                raise ValueError(f"Unknown resource: {uri}")
            
            return ReadResourceResult(
                contents=[
                    TextResourceContents(  # type: ignore
                        text=content
                    )
                ]
            )


async def main():
    """Main entry point for the MCP server."""
    try:
        server_instance = MCPAIServer()
        
        # Run the server using stdio transport
        async with stdio_server() as (read_stream, write_stream):
            await server_instance.server.run(
                read_stream,
                write_stream,
                server_instance.server.create_initialization_options()
            )
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
