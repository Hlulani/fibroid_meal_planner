from ollama import Client

client = Client(host="http://127.0.0.1:11434")

def generate_recipe_with_ai(prompt: str) -> str:
    """
    Sends the recipe prompt to your running local Llama model.
    """
    try:
        response = client.generate(
            model="llama3:latest",  # match your installed tag
            prompt=prompt,
        )
        return response["response"]
    except Exception as e:
        return f"⚠️ AI generation failed — {e}"
