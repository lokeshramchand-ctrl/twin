from fastapi.testclient import TestClient

import ai.agent as agent
from app.main import app


def test_chat_returns_answer(monkeypatch):
    def fake_ask_llm(messages):
        assert messages[0]["role"] == "system"
        assert messages[1]["role"] == "user"
        return "Parcel summary with hazards and transportation details."

    monkeypatch.setattr(agent, "ask_llm", fake_ask_llm)

    client = TestClient(app)
    payload = {
        "question": "Explain this property.",
        "address": "123 Main St",
        "parcel": {"apn": "000-000-000"},
        "zoning": {"code": "R1"},
        "flood": {"risk": "low"},
        "fire": {"risk": "moderate"},
        "schools": {"district": "Example USD"},
        "highways": {"nearby": ["I-5"]},
    }

    response = client.post("/api/chat", json=payload)

    assert response.status_code == 200
    assert response.json() == {
        "answer": "Parcel summary with hazards and transportation details."
    }
