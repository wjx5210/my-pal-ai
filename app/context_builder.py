def build_hybrid_context(result):
    """
    将Hybrid检索结果转换成统一上下文
    """

    context = {
        "entities": [],
        "knowledge": []
    }


    for pal in result["entities"]:
        context["entities"].append(
            pal
        )


    for item in result["rag_contexts"]:
        context["knowledge"].append(
            item["text"]
        )


    return context