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
        return [str(line[:-1]).replace("\x00", "") for line in csv.readlines()]

def encode_from_url(url):
   response = requests.get(url)
   return base64.b64encode(response.content).decode('utf-8')

REM_CHARS = "\x00\xfe\xff"
def clean_url(url):
    for c in REM_CHARS:
        url = url.replace(c, "")
    return url

responses = []
for url in gen_image_urls("iunsct.csv"):
    if url == "": continue
    base64_image = encode_from_url(clean_url(url))

    response = client.chat.completions.create(
        model = "gpt-4o",
        messages = [
            {
                'role': "user",
                "content": [
                    {
                        "type": "text",
                        "text": "please list the clothing items in this image. \
                            be detailed in your description of garment styles, fabrics, textures, accessories, etc."
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
    )

    print(response.choices[0].message.content)
    responses.append(response.choices[0].message.content)
