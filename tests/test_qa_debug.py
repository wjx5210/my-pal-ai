from app.qa_service import answer_with_debug


def test_answer_debug(monkeypatch):

    monkeypatch.setattr(
        "app.qa_service.hybrid_search",
        lambda q: {
            "entities": [],
            "rag_contexts": [
                {
                    "text": "前期推荐捣蛋猫"
                }
            ]
        }
    )


    monkeypatch.setattr(
        "app.qa_service.build_hybrid_context",
        lambda x: {
            "entities": [],
            "knowledge": [
                "前期推荐捣蛋猫"
            ]
        }
    )


    monkeypatch.setattr(
        "app.qa_service.answer_with_hybrid_context",
        lambda q,c: "测试回答"
    )


    result = answer_with_debug(
        "前期抓什么帕鲁"
    )


    assert result["answer"] == "测试回答"
    assert "retrieval" in result
    assert "context" in result