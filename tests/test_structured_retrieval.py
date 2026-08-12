from app import hybrid_service
from app.structured_retrieval import search_structured_pals


def test_early_base_recommendation_returns_concrete_pals():
    results = search_structured_pals("前期基地最值得抓谁？", top_k=3)
    assert len(results) == 3
    assert all("前期" in item["metadata"]["recommended_stage"] for item in results)
    assert all("工作能力" in item["text"] for item in results)


def test_specific_work_recommendation_filters_by_work_type():
    results = search_structured_pals("前期基地采矿推荐抓谁？", top_k=5)
    assert results
    assert all("'采矿':" in item["text"] for item in results)


def test_hybrid_search_avoids_embedding_for_structured_query(monkeypatch):
    def fail_if_called(_question):
        raise AssertionError("structured recommendation should not call embedding")

    monkeypatch.setattr(hybrid_service, "retrieve_context", fail_if_called)
    result = hybrid_service.hybrid_search("前期基地最值得抓谁？")
    assert len(result["rag_contexts"]) == 3
    assert result["rag_contexts"][0]["metadata"]["retrieval_type"] == "structured"
