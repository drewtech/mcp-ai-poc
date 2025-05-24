import os
from openai import OpenAI


def get_client():
    """Get or create OpenAI client with API key from environment."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable must be set")
    return OpenAI(api_key=api_key)


def generate_completion(prompt: str, model: str = "gpt-3.5-turbo") -> str:
    """
    Generate a text completion using OpenAI's new Python SDK (>=1.0.0).
    """
    client = get_client()
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content.strip()


if __name__ == "__main__":
    print(generate_completion("Hello, world!"))
