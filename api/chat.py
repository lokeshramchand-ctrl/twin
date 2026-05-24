from fastapi import APIRouter, HTTPException

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

    try:
        answer = process(
            request
        )

    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=str(exc)
        ) from exc

    return {

        "answer":
        answer
    }