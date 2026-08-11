from app.hybrid_service import hybrid_search
from app.context_builder import build_hybrid_context
from app.ai_service import answer_with_hybrid_context


def _build_retrieval_query(
    question: str,
    history: list[dict[str, str]] | None,
) -> str:
    """Add recent user turns so short follow-ups retain retrieval context."""

    if not history:
        return question

    recent_questions = [
        item["content"]
        for item in history[-6:]
        if item.get("role") == "user"
    ]
    return "\n".join([*recent_questions, question])


def answer(
    question: str,
    history: list[dict[str, str]] | None = None,
) -> str:
    """
    统一问答入口。
    """

    result = hybrid_search(_build_retrieval_query(question, history))

    context = build_hybrid_context(result)

    if history is None:
        response = answer_with_hybrid_context(question, context)
    else:
        response = answer_with_hybrid_context(
            question,
            context,
            history=history,
        )

    return response


def answer_with_debug(
    question: str,
    history: list[dict[str, str]] | None = None,
) -> dict:
    """
    调试模式问答入口。
    返回AI回答以及检索上下文。
    """

    result = hybrid_search(_build_retrieval_query(question, history))

    context = build_hybrid_context(result)

    if history is None:
        response = answer_with_hybrid_context(question, context)
    else:
        response = answer_with_hybrid_context(
            question,
            context,
            history=history,
        )

    return {
        "answer": response,
        "retrieval": result,
        "context": context
    }
