from app.qa_service import answer


def test_answer(monkeypatch):

    monkeypatch.setattr(
        "app.qa_service.hybrid_search",
        lambda q:{
            "entities":[],
            "rag_contexts":[
                {
                    "text":"前期推荐捣蛋猫"
                }
            ]
        }
    )


    monkeypatch.setattr(
        "app.qa_service.build_hybrid_context",
        lambda x:{
            "entities":[],
            "knowledge":[
                "前期推荐捣蛋猫"
            ]
        }
    )


    monkeypatch.setattr(
        "app.qa_service.answer_with_hybrid_context",
        lambda q,c:"测试回答"
    )


    result = answer(
        "前期基地抓什么"
    )


    assert result == "测试回答"