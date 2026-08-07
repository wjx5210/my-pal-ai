from app.embedding_service import create_embedding


def test_create_embedding():

    vector = create_embedding(
        "棉悠悠适合前期培养"
    )


    assert len(vector) > 0

    assert isinstance(vector[0], float)