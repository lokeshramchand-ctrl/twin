from fastapi import APIRouter

from schemas.chat_request import (
ChatRequest
)

from ai.agent import process

router = APIRouter()

@router.post(
"/chat"
)

def chat(
request:
ChatRequest
):

    answer = process(
        request
    )

    return {

        "answer":
        answer
    }