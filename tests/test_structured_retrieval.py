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


def test_early_ground_mount_recommendation_enforces_mount_constraint():
    results = search_structured_pals("前期陆地坐骑有哪些？", top_k=10)

    assert results
    assert {item["metadata"]["name"] for item in results} == {
        "美露帕", "草莽猪", "紫霞鹿", "祇岳鹿", "猎狼",
    }
    assert all(item["metadata"]["mount_type"] == "ground" for item in results)
    assert all("可骑在它的背上移动" in item["text"] for item in results)


def test_hybrid_search_avoids_embedding_for_structured_query(monkeypatch):
    def fail_if_called(_question):
        raise AssertionError("structured recommendation should not call embedding")

    monkeypatch.setattr(hybrid_service, "retrieve_context", fail_if_called)
    result = hybrid_service.hybrid_search("前期基地最值得抓谁？")
    assert len(result["rag_contexts"]) == 3
    assert result["rag_contexts"][0]["metadata"]["retrieval_type"] == "structured"


def test_hybrid_search_keeps_ground_mounts_as_the_only_references(monkeypatch):
    def fail_if_called(_question):
        raise AssertionError("ground mount recommendation should stay structured")

    monkeypatch.setattr(hybrid_service, "retrieve_context", fail_if_called)
    result = hybrid_service.hybrid_search("前期陆地坐骑有哪些？")

    assert result["rag_contexts"]
    assert all(
        item["metadata"].get("mount_type") == "ground"
        for item in result["rag_contexts"]
    )
