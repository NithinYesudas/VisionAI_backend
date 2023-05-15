import os
import openai
openai.organization = "org-WCLXqOY552W4pCFBjqvvngoL"
openai.api_key = os.getenv("OPENAI_API_KEY")

def openai_prompt_runner(prompt: str):
    result = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=100,
        temperature=0,
    )
    return result["choices"][0]["text"]
