from mcp_poc.app import generate_completion, client


def test_generate_completion(monkeypatch):
    # Set a dummy environment variable so that
    # client = OpenAI(api_key=os.getenv("OPENAI_API_KEY")) doesn’t fail
    monkeypatch.setenv("OPENAI_API_KEY", "dummy_key")

    # Mock the OpenAI client response
    class DummyChoice:
        def __init__(self, content):
            self.message = type("M", (), {"content": content})

    class DummyResponse:
        choices = [DummyChoice("Test response")]

    # Patch the client.chat.completions.create method
    monkeypatch.setattr(
        client.chat.completions,
        "create",
        lambda model, messages: DummyResponse()
    )

    assert generate_completion("Prompt") == "Test response"
