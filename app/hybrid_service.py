from app.pal_service import find_pals_in_text
from app.rag_service import retrieve_context
from app.structured_retrieval import search_structured_pals


def hybrid_search(question):
    """
    混合检索：
    1. 实体检索
    2. RAG检索
    3. 合并结果
    """

    results = {
        "entities": [],
        "rag_contexts": []
    }


    # 1.实体检索
    pals = find_pals_in_text(question)

    if pals:
        results["entities"] = pals


    structured_results = search_structured_pals(question)
    if structured_results:
        results["rag_contexts"] = structured_results
        return results

    # 2.RAG检索
    rag_results = retrieve_context(question)

    if rag_results:
        results["rag_contexts"] = rag_results


    return results
