from unittest.mock import patch
import pytest
import os
from mcp_poc.ai_tools import OpenAIClient


def test_openai_client_missing_api_key():
    """Test that OpenAIClient raises ValueError when OPENAI_API_KEY is not set."""
    with patch.dict(os.environ, {}, clear=True):
        client = OpenAIClient()
        with pytest.raises(
            ValueError, match="OPENAI_API_KEY environment variable must be set"
        ):
            client.get_client()


def test_openai_client_empty_api_key():
    """Test that OpenAIClient raises ValueError when OPENAI_API_KEY is empty."""
    with patch.dict(os.environ, {"OPENAI_API_KEY": ""}):
        client = OpenAIClient()
        with pytest.raises(
            ValueError, match="OPENAI_API_KEY environment variable must be set"
        ):
            client.get_client()


@patch("mcp_poc.ai_tools.OpenAI")
def test_openai_client_with_valid_api_key(mock_openai):
    """Test that OpenAIClient creates client when OPENAI_API_KEY is set."""
    with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
        client = OpenAIClient()
        result = client.get_client()

        # Should have called OpenAI constructor with the API key
        mock_openai.assert_called_once_with(api_key="test-key")

        # Should return the mock client
        assert result == mock_openai.return_value


def test_openai_client_singleton_behavior():
    """Test that OpenAIClient reuses the same client instance."""
    with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
        with patch("mcp_poc.ai_tools.OpenAI") as mock_openai:
            client = OpenAIClient()

            # Get client twice
            result1 = client.get_client()
            result2 = client.get_client()

            # Should have called OpenAI constructor only once
            assert mock_openai.call_count == 1

            # Should return same instance both times
            assert result1 == result2
