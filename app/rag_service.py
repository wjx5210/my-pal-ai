from app.embedding_service import create_embedding
from app.vector_store import VectorStore



VECTOR_STORE_PATH = "data/vector_store.json"



def retrieve_context(
    question: str,
    top_k: int = 3
) -> list[str]:
    """
    根据问题检索相关知识。
    """


    query_vector = create_embedding(
        question
    )


    store = VectorStore.load(
        VECTOR_STORE_PATH
    )


    results = store.search(
        query_vector,
        top_k=top_k,
        threshold=0.7
    )


    return results