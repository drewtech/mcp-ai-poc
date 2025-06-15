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


def generate_completion(messages: list, model: str = "gpt-4o") -> str:
    """
    Generate a text completion using OpenAI's new Python SDK (>=1.0.0).
    """
    client = _openai_client.get_client()
    response = client.chat.completions.create(
        model=model,
        messages=messages,
    )
    return response.choices[0].message.content.strip()  # type: ignore


def select_model():
    """List available models and let user choose."""
    try:
        client = _openai_client.get_client()
        models = client.models.list()

        # Filter for chat models only
        chat_models = [model.id for model in models.data if "gpt" in model.id.lower()]
        chat_models.sort()

        print("Available models:")
        for i, model in enumerate(chat_models, 1):
            print(f"{i}. {model}")

        print(
            f"\nEnter model number (1-{len(chat_models)}) or press Enter for default (gpt-4o):"
        )
        choice = input("Model choice: ").strip()

        if not choice:
            return "gpt-4o"

        try:
            model_index = int(choice) - 1
            if 0 <= model_index < len(chat_models):
                return chat_models[model_index]
            else:
                print("Invalid choice, using default: gpt-4o")
                return "gpt-4o"
        except ValueError:
            print("Invalid input, using default: gpt-4o")
            return "gpt-4o"

    except Exception as e:
        print(f"Error fetching models: {e}")
        print("Using default: gpt-4o")
        return "gpt-4o"


def chat_loop():
    """Interactive chat loop with conversation history."""
    # Select model at startup
    selected_model = select_model()
    print(f"\nUsing model: {selected_model}")

    messages = []
    print("Chat started! Type 'quit' or 'exit' to end the conversation.\n")

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() in ["quit", "exit"]:
            print("Goodbye!")
            break

        if not user_input:
            continue

        # Add user message to conversation history
        messages.append({"role": "user", "content": user_input})

        try:
            # Get AI response using selected model
            response = generate_completion(messages, model=selected_model)
            print(f"AI: {response}\n")

            # Add AI response to conversation history
            messages.append({"role": "assistant", "content": response})

        except Exception as e:
            print(f"Error: {e}\n")


if __name__ == "__main__":
    chat_loop()
