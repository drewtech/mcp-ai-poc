"""
AI tools and utilities for the MCP server.
"""

import os
from openai import OpenAI


class OpenAIClient:
    """Manages OpenAI API client with singleton-like behavior."""

    def __init__(self):
        self._client = None

    def get_client(self):
        """Get or create OpenAI client with API key from environment."""
        if self._client is None:
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY environment variable must be set")
            self._client = OpenAI(api_key=api_key)
        return self._client
