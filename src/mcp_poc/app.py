"""
MCP AI POC Application - MCP Server Mode Only
"""

import asyncio
from .standalone_server import main as server_main


def main():
    """Main entry point - runs MCP server only."""
    asyncio.run(server_main())


if __name__ == "__main__":
    main()
