from unittest.mock import patch, MagicMock
from mcp_poc.app import generate_completion


@patch("mcp_poc.app.get_client")
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
