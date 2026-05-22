from ai.prompts import (
SYSTEM_PROMPT
)

from ai.ollama_client import (
ask_llm
)

from services.context_builder import (
build_context
)

def process(
request
):

    context = build_context(
        request
    )

    messages = [

    {
        "role":
        "system",

        "content":
        SYSTEM_PROMPT
    },

    {
        "role":
        "user",

        "content":
        context
    }

    ]

    answer = ask_llm(
        messages
    )

    return answer