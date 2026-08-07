from app.vector_store import VectorStore



def test_similarity_threshold():

    store = VectorStore()


    store.add_document(
        "棉悠悠适合前期培养",
        [1.0, 0.0, 0.0]
    )


    store.add_document(
        "火绒狐是火属性帕鲁",
        [0.5, 0.5, 0.0]
    )


    results = store.search(
        [1.0, 0.0, 0.0],
        threshold=0.9
    )


    assert len(results) == 1

    assert (
        results[0]["text"]
        ==
        "棉悠悠适合前期培养"
    )