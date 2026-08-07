import json
from app.embedding_service import create_embedding
from app.vector_store import VectorStore


def build_pal_text(pal: dict) -> str:
    """
    将帕鲁数据转换成知识文本。
    """

    return f"""
名称：
{pal['name']}

属性：
{pal['element']}

简介：
{pal['summary']}

工作能力：
{pal['work_suitability']}

战斗定位：
{pal['combat']['positioning']}

优势：
{pal['combat']['strengths']}

弱点：
{pal['combat']['weaknesses']}

掉落：
{pal['drops']}

出现地点：
{pal['locations']}

推荐阶段：
{pal['recommended_stage']}

推荐理由：
{pal['recommendation']}

攻略提示：
{pal['tips']}
"""


def build_vector_store(
    pals: list[dict]
) -> VectorStore:

    store = VectorStore()


    for pal in pals:

        print(
            f"正在处理:{pal['name']}"
        )


        text = build_pal_text(
            pal
        )


        vector = create_embedding(
            text
        )


        store.add_document(
            text,
            vector
        )


    return store