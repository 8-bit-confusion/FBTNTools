import requests
import os
from dotenv import load_dotenv
from openai import OpenAI
import base64

load_dotenv()

OpenAI.api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))

def encode_image(image_path):
  with open(image_path, 'rb') as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

def download_image(url, filename):
  response = requests.get(url)
  with open(filename, 'wb') as f:
    f.write(response.content)

def gen_image_urls(csv_filename):
    with open(csv_filename, 'r') as csv:
        return [line[:-1] for line in csv.readlines()[1:]]

def encode_from_url(url):
   response = requests.get(url)
   return base64.b64encode(response.content).decode('utf-8')

responses = []
for url in gen_image_urls("coquette_data_set.csv"):
    base64_image = encode_from_url(url)

    response = client.chat.completions.create(
        model = "gpt-4o",
        messages = [
            {
                "role": "system",
                "content": "Caption this photo. Do not describe the model's hair or make-up, \
                    just the garments and accessories. Stick to the facts, don't editorialize. \
                    Answer in a clause, like sleeveless, high-neck, sheer dress adorned with \
                    intricate beading and a voluminous train embellished with large, \
                    pastel-colored floral appliqués. Be descriptive of the material and fabric."
            },
            {
                'role': "user",
                "content": [
                    {
                        "type": "text",
                        "text": "What's in this image?"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64, {base64_image}"
                        }
                    }
                ]
            }
        ],
        temperature = 0.7,
        max_tokens = 150
    )

    print(response.choices[0].message.content)
    responses.append(response.choices[0].message.content)
