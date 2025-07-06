#!/usr/bin/env python3
"""
Entry point for the MCP AI POC server.
Runs as an MCP server only.
"""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from mcp_poc.standalone_server import main
import asyncio

if __name__ == "__main__":
    asyncio.run(main())
