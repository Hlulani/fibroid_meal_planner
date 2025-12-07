# ai_engine.py

from ollama import Client

# Connect to local Ollama
client = Client(host="http://localhost:11434")

def generate_recipe(prompt: str) -> str:
    """
    Sends a prompt to the local Llama model and returns the generated text.
    """
    try:
        response = client.generate(
            model="llama3",
            prompt=prompt,
        )
        return response["response"]
    except Exception as e:
        return f"⚠️ AI generation failed: {e}"
