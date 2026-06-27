from fastapi.testclient import TestClient

from apps.api.main import app

client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_chat_refusal_when_no_context() -> None:
    response = client.post("/v1/chat", json={"question": "测试问题"})
    assert response.status_code == 200
    body = response.json()
    assert "未找到足够依据" in body["answer"]
    assert body["citations"] == []
