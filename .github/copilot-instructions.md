# Copilot Instructions

## Build, Test, Lint
- **Tests:** `python -m pytest`
- **Single test:** `python -m pytest tests/test_chat.py::test_chat_returns_answer`

## High-Level Architecture
- **FastAPI entrypoint** lives in `app/main.py`, which creates the app and mounts the API router under `/api`. It also prepends the repo root to `sys.path` to allow absolute imports.
- **API layer** is `api/chat.py` with `POST /chat`, which accepts `schemas.ChatRequest`, delegates to `ai.agent.process`, and returns `{ "answer": ... }` while mapping errors to HTTP 502.
- **AI pipeline** in `ai/agent.py` builds the user context via `services/context_builder.build_context`, injects `ai.prompts.SYSTEM_PROMPT`, and sends the request through `ai.ollama_client.ask_llm`.
- **LLM client/config** are split: `ai/ollama_client.py` performs the HTTP call and expects `message.content` in the response JSON; `config/settings.py` defines `OLLAMA_URL` and `MODEL`.
- **Schemas** in `schemas/` define the request and response Pydantic models; request fields drive context construction in `services/context_builder.py`.

## Key Conventions
- Keep prompt text in `ai/prompts.py` and context formatting in `services/context_builder.py` rather than embedding them in API handlers.
- Centralize model endpoint settings in `config/settings.py`; `ai/ollama_client.py` should remain the only module that performs the HTTP call.
- Preserve the response shape `{ "answer": "<string>" }` even if switching to `schemas.ChatResponse`.
- When adding or renaming request fields in `schemas/ChatRequest`, update `services/context_builder.build_context` to keep prompt context in sync.
- Tests should stub `ai.agent.ask_llm` to avoid network calls to Ollama.
