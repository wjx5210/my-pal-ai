from app.ai_service import answer_with_rag_context


def test_rag_empty_context():

    result = answer_with_rag_context(
        "今天适合去哪里旅游？",
        []
    )


    assert (
        "知识库"
        in result
    )


    assert (
        "没有找到"
        in result
    )