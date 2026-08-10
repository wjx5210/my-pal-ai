from app.hybrid_service import hybrid_search


def test_hybrid_import():
    result = hybrid_search("棉悠悠和企丸丸哪个好")

    print(result)

    assert "entities" in result
    assert "rag_contexts" in result