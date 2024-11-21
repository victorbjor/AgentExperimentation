import base64
from pprint import pprint

import ollama


def image_to_base64(image_path) -> str:
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
    return encoded_string


message = {
    "role": "user",
    "content": "What is this?",
    "images": [image_to_base64('/path/to/image.png')]
}

pprint(message)

response = ollama.chat(
    model='llama3.2-vision:90b',  # This uses ~90Gb RAM, so make sure you have that. Oh, and do `ollama pull llama3.2-vision:90b`
    stream=False,
    messages=[message]
)

pprint(response['message'])
