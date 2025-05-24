import os
from openai import OpenAI


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_completion(prompt: str, model: str = "gpt-3.5-turbo") -> str:
    """
    Generate a text completion using OpenAI's new Python SDK (>=1.0.0).
    """
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content.strip()


if __name__ == "__main__":
    print(generate_completion("Hello, world!"))
