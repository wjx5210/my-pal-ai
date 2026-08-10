from app.ai_service import answer_with_hybrid_context


def test_hybrid_ai(monkeypatch):

    def fake_chat(messages):
        return "测试回答"


    monkeypatch.setattr(
        "app.ai_service.chat_completion",
        fake_chat
    )


    context = {
        "entities":[
            {
                "name":"棉悠悠",
                "element":"无",
                "summary":"前期帕鲁",
                "tips":"适合牧场"
            }
        ],

        "knowledge":[
            "前期基地推荐多功能帕鲁"
        ]
    }


    result = answer_with_hybrid_context(
        "棉悠悠值得培养吗",
        context
    )


    assert result == "测试回答"