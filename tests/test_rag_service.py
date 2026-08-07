from app.rag_service import retrieve_context


def test_retrieve_context():

    results = retrieve_context(
        "新手前期推荐什么帕鲁？",
        top_k=3
    )


    assert len(results) > 0

    print("\n检索结果：")

    for item in results:
        print(item)