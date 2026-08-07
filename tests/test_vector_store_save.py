from app.vector_store import VectorStore


def test_vector_store_save_and_load(tmp_path):

    store = VectorStore()


    store.add_document(
        "棉悠悠适合前期培养",
        [0.1, 0.2, 0.3]
    )


    file_path = tmp_path / "vector.json"


    store.save(
        str(file_path)
    )


    new_store = VectorStore.load(
        str(file_path)
    )


    assert len(
        new_store.documents
    ) == 1


    assert (
        new_store.documents[0]["text"]
        ==
        "棉悠悠适合前期培养"
    )