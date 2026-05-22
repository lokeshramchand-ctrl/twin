import requests

from config.settings import (
OLLAMA_URL,
MODEL
)

def ask_llm(
messages
):

    payload = {

        "model":
        MODEL,

        "messages":
        messages,

        "stream":
        False
    }

    r = requests.post(
        OLLAMA_URL,
        json=payload
    )

    data = r.json()

    return data[
        "message"
    ][
        "content"
    ]