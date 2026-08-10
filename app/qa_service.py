from app.hybrid_service import hybrid_search
from app.context_builder import build_hybrid_context
from app.ai_service import answer_with_hybrid_context


def answer(question: str) -> str:
    """
    统一问答入口。
    """

    result = hybrid_search(question)

    context = build_hybrid_context(result)

    response = answer_with_hybrid_context(
        question,
        context
    )

    return response