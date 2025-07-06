"""
MCP AI POC - Model Context Protocol Server

This package provides an AI-powered MCP server with tools for:
- Code generation and refactoring
- Debugging assistance
- Performance optimization
- Test generation
- Code analysis and documentation

Usage:
    # Start MCP server
    python run.py
    
    # Or via module
    python -m mcp_poc.standalone_server
"""

__version__ = "1.0.0"
__author__ = "Your Name"
__description__ = "MCP server with AI-powered development tools"

# Make key classes available at package level
from .ai_tools import OpenAIClient
from .standalone_server import JSONRPCServer

__all__ = [
    "OpenAIClient",
    "JSONRPCServer"
]
