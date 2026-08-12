from app.embedding_service import create_embedding
from app.vector_store import VectorStore


def build_pal_text(pal: dict) -> str:
    """
    将帕鲁数据转换成知识文本。
    """

    wiki = pal.get("wiki", {})
    partner_skill = wiki.get("partner_skill", {})
    active_skills = wiki.get("active_skills", [])

    return f"""
图鉴编号：
{wiki.get('dex_no', '暂无资料')}

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

伙伴技能：
{partner_skill.get('name', '暂无资料')}：{partner_skill.get('description', '暂无资料')}

基础属性：
{wiki.get('base_stats', {})}

移动能力：
{wiki.get('movement', {})}

主动技能：
{active_skills}

资料来源：
{wiki.get('source_url', '本地知识库')}
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
            vector,
            {
                "name": pal["name"],
                "element": pal["element"],
                "recommended_stage": pal["recommended_stage"],
                "dex_no": pal.get("wiki", {}).get("dex_no"),
                "source_url": pal.get("wiki", {}).get("source_url"),
            }
        )


    return store
