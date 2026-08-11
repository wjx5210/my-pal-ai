from fastapi.testclient import TestClient
from app.api.server import app
from unittest.mock import patch


client = TestClient(app)


def test_health():

    response = client.get("/health")

    assert response.status_code == 200

    assert response.json() == {
        "status": "ok"
    }


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

    assert data["work_suitability"]["采集"] == 1


    # 战斗信息

    assert "combat" in data

    assert "positioning" in data["combat"]


    # 掉落

    assert "drops" in data

    assert "羊毛" in data["drops"]


    # 推荐阶段

    assert data["recommended_stage"] == "前期"


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