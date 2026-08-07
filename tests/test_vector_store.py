from app.vector_store import VectorStore


def test_vector_search():

    store = VectorStore()


    # 模拟三个知识向量
    store.add_document(
        "棉悠悠适合前期培养",
        [1.0, 0.0, 0.0]
    )


    store.add_document(
        "企丸丸拥有水冰属性能力",
        [0.0, 1.0, 0.0]
    )


    store.add_document(
        "火绒狐适合作为火属性战斗帕鲁",
        [0.9, 0.1, 0.0]
    )


    # 查询向量更接近棉悠悠和火绒狐
    results = store.search(
        [1.0, 0.1, 0.0],
        top_k=2
    )


    assert len(results) == 2


    assert (
    results[0]["text"]
    in [
        "棉悠悠适合前期培养",
        "火绒狐适合作为火属性战斗帕鲁"
    ]
    )