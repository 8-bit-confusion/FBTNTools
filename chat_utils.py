import os
import subprocess
import warnings

env = os.environ.copy()

try: from dotenv import load_dotenv
except(ImportError): warnings.warn("'dotenv' module not installed. Try running 'install_packages()'.")
try: from openai import OpenAI
except(ImportError): warnings.warn("'openai' module not installed. Try running 'install_packages()'.")

def install_packages():
    subprocess.call("pip install dotenv", shell=True, env=env)
    subprocess.call("pip install openai", shell=True, env=env)

class Prompts:
    @classmethod
    def text_prompt(cls, prompt: str):
        return {
            "role": "user",
            "content": prompt
        }

    @classmethod
    def image_prompt(cls, prompt: str, image: str):
        return {
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64, {image}"}}
            ]
        }

class ChatClient:
    def __init__(self):
        self._client: OpenAI = ChatClient.load_client()

    @classmethod
    def load_client(cls):
        load_dotenv()
        OpenAI.api_key = os.getenv("OPENAI_API_KEY")
        return OpenAI(api_key = os.getenv("OPENAI_API_KEY"))

    def response(self, *prompts: dict, system_message: str = None, temperature = 0.7):
        messages = []

        if system_message != None:
            messages.append({
                "role": "system",
                "content": system_message
            })
        
        for prompt in prompts:
            messages.append(prompt)

        return self._client.chat.completions.create(
            model = "gpt-4o",
            messages = messages,
            temperature = temperature
        )