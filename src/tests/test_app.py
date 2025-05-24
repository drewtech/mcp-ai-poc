from unittest.mock import patch, MagicMock
import pytest
import os
from mcp_poc.app import generate_completion, OpenAIClient


@patch("mcp_poc.app._openai_client.get_client")
def test_generate_completion(mock_get_client):
    # Create mock response
    mock_message = MagicMock()
    mock_message.content = "Test response"

    mock_choice = MagicMock()
    mock_choice.message = mock_message

    mock_response = MagicMock()
    mock_response.choices = [mock_choice]

    # Create mock client
    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value = mock_response

    # Set up the mock to return our mock client
    mock_get_client.return_value = mock_client

    # Test the function
    result = generate_completion("Prompt")
    assert result == "Test response"

    # Verify the client was called correctly
    mock_client.chat.completions.create.assert_called_once_with(
        model="gpt-3.5-turbo", messages=[{"role": "user", "content": "Prompt"}]
    )


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
