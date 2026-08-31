from fastapi.testclient import TestClient
from app.api.server import app
from unittest.mock import patch
from uuid import UUID


client = TestClient(app)


def test_health():

    response = client.get("/health")

    assert response.status_code == 200

    assert response.json() == {
        "status": "ok"
    }

    UUID(response.headers["X-Request-ID"])


def test_request_id_is_preserved_and_logged(caplog):
    request_id = "deploy-check-20260831"

    with caplog.at_level("INFO", logger="uvicorn.error.app_access"):
        response = client.get(
            "/health",
            headers={"X-Request-ID": request_id},
        )

    assert response.headers["X-Request-ID"] == request_id
    assert any(
        request_id in record.message
        and "path=/health" in record.message
        and "status_code=200" in record.message
        and "duration_ms=" in record.message
        for record in caplog.records
    )


def test_invalid_request_id_is_replaced():
    response = client.get(
        "/health",
        headers={"X-Request-ID": "not valid because it has spaces"},
    )

    generated_id = response.headers["X-Request-ID"]
    assert generated_id != "not valid because it has spaces"
    UUID(generated_id)


def test_get_pal():

    response = client.get(
        "/pal/棉悠悠"
    )

    assert response.status_code == 200

    data = response.json()


    # 基础信息

    assert data["name"] == "棉悠悠"

    assert "element" in data

    assert "summary" in data


    # 工作能力

    assert "work_suitability" in data

    assert data["work_suitability"]["手工作业"] == 1


    # 战斗信息

    assert "combat" in data

    assert "positioning" in data["combat"]


    # 掉落

    assert "drops" in data

    assert "羊毛" in data["drops"]


    # 推荐阶段

    assert data["recommended_stage"] == "前期"


def test_list_pals():
    response = client.get("/pals")

    assert response.status_code == 200
    assert len(response.json()) >= 18
    assert response.json()[0]["name"] == "棉悠悠"


def test_get_unknown_pal_returns_404():
    response = client.get("/pal/不存在的帕鲁")

    assert response.status_code == 404


def test_ask():

    mock_result = {
        "answer": "推荐企丸丸",
        "retrieval": {
            "entities": [
                {
                    "name": "企丸丸"
                }
            ]
        },
        "context": []
    }


    with patch(
        "app.api.server.answer_with_debug",
        return_value=mock_result
    ):

        response = client.post(
            "/ask",
            json={
                "question":"棉悠悠和企丸丸哪个好"
            }
        )


    assert response.status_code == 200


    data = response.json()


    assert data["answer"] == "推荐企丸丸"


    assert data["sources"][0]["name"] == "企丸丸"
    assert data["session_id"]


def test_ask_reuses_session_history():
    mock_result = {
        "answer": "它更适合基地工作",
        "retrieval": {"entities": [], "rag_contexts": []},
        "context": [],
    }

    with patch(
        "app.api.server.answer_with_debug",
        return_value=mock_result,
    ) as mocked_answer:
        response = client.post(
            "/ask",
            json={"question": "那它适合基地吗", "session_id": "test-session"},
        )

    assert response.status_code == 200
    assert response.json()["session_id"] == "test-session"
    mocked_answer.assert_called_once()


def test_pal_ai_summary():
    with patch(
        "app.api.server.generate_pal_guide",
        return_value="适合前期提供羊毛。",
    ):
        response = client.post("/pal/棉悠悠/summary")

    assert response.status_code == 200
    assert response.json()["name"] == "棉悠悠"
    assert "羊毛" in response.json()["summary"]
