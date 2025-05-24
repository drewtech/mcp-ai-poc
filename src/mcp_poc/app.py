import os
from openai import OpenAI


class OpenAIClient:
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


# Module-level instance
_openai_client = OpenAIClient()


def generate_completion(prompt: str, model: str = "gpt-3.5-turbo") -> str:
    """
    Generate a text completion using OpenAI's new Python SDK (>=1.0.0).
    """
    client = _openai_client.get_client()
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content.strip()


if __name__ == "__main__":
    print(generate_completion("Hello, world!"))
