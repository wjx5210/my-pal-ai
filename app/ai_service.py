from app.llm_client import chat_completion, MODEL_NAME
from app.logger_service import save_qa_log
from app.config import ENABLE_PROMPT_LOG
from app.knowledge_builder import build_pal_text


def build_pal_guide_prompt(pal_info: dict) -> str:
    """Build a detail-page prompt from every available knowledge field."""

    pal_text = build_pal_text(pal_info)
    return f"""
你是一名《幻兽帕鲁》攻略助手。

请严格根据下面提供的完整帕鲁资料生成详情页总结，不要声称资料中已经提供的字段缺失。

完整帕鲁资料：
{pal_text}

要求：
1. 使用中文回答，不要编造资料中没有的信息。
2. 先概括定位和推荐阶段。
3. 结合工作适性名称与等级说明基地用途。
4. 结合基础属性、战斗优势、弱点和主动技能说明战斗表现。
5. 说明伙伴技能、掉落物和捕获地点；地点代码无法自然解释时，只说明资料记录的区域。
6. 最后给出明确的培养建议和使用注意事项。
7. 内容控制在 300 至 500 字，使用简洁的小标题或项目符号。
"""


def generate_pal_guide(pal_info: dict) -> str:
    """根据帕鲁数据生成 AI 攻略。"""

    prompt = build_pal_guide_prompt(pal_info)
    return chat_completion(
    [
        {
            "role": "system",
            "content": "你是一个专业的游戏攻略助手。"
        },
        {
            "role": "user",
            "content": prompt
        }
    ]
)


def answer_question(question: str) -> str:
    """
    回答用户提出的自然语言问题。
    """

    prompt = f"""
你是一名《幻兽帕鲁》攻略助手。

用户问题：
{question}

要求：
1. 使用中文回答。
2. 如果不知道，请明确说明。
3. 不要编造不存在的信息。
"""


    return chat_completion(
        [
            {
                "role": "system",
                "content": "你是一个专业的游戏攻略助手。"
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )


def answer_with_rag_context(question: str,contexts: list[str]) -> str:
    """
    根据RAG检索出的知识生成回答。
    """
    if not contexts:
        return (
            "抱歉，当前知识库中没有找到"
            "与该问题相关的资料。"
            "请尝试询问《幻兽帕鲁》相关攻略问题。"
        )

    knowledge = "\n\n".join(
        [
            item["text"]
            for item in contexts
        ]
    )

    sources = []

    for item in contexts:

        name = item.get(
            "metadata",
            {}
        ).get(
            "name"
        )

        if name:
            sources.append(name)

    prompt = f"""
你是一名《幻兽帕鲁》攻略助手。

用户问题：

{question}


以下是从知识库检索出的相关资料：

{knowledge}


要求：

1. 使用中文回答。
2. 优先根据知识库资料回答。
3. 不要编造资料中不存在的信息。
4. 如果资料不足，请明确说明。
5. 针对用户问题回答，不要简单重复资料。
"""


    answer = chat_completion(
        [
            {
                "role": "system",
                "content": "你是一个专业的游戏攻略助手。"
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    if sources:

        answer += "\n\n参考资料：\n"

        for source in sources:

            answer += f"- {source}\n"

    return answer


def format_pal_prompt(pal: dict) -> str:
    """
    将帕鲁字典格式化成AI容易理解的文本。
    """

    text = f"""
名称：{pal.get('name', '暂无资料')}

属性：{', '.join(pal.get('element', [ '暂无资料']))}

简介：
{pal.get('summary', '暂无资料')}

工作能力：
{pal.get('work_suitability', '暂无资料')}

战斗能力：
{pal.get('combat', '暂无资料')}

掉落物：
{', '.join(pal.get('drops', ['暂无资料']))}

出现地点：
{', '.join(pal.get('locations', ['暂无资料']))}

推荐阶段：
{pal.get('recommended_stage', '暂无资料')}

推荐理由：
{pal.get('recommendation', '暂无资料')}

攻略提示：
{pal.get('tips', '暂无资料')}
"""

    return text


def answer_with_pal_context(question: str, pal_info: dict[str, str]) -> str:
    """根据用户问题和帕鲁资料生成回答。"""

    prompt = f"""
你是一名《幻兽帕鲁》攻略助手。

用户问题：
{question}

参考帕鲁资料：

{format_pal_prompt(pal_info)}

要求：
1. 使用中文回答。
2. 优先根据提供资料分析。
3. 不要编造资料中不存在的信息。
4. 针对用户的问题回答，不要只介绍帕鲁。
"""

    return chat_completion(
    [
        {
            "role": "system",
            "content": "你是一个专业的游戏攻略助手。"
        },
        {
            "role": "user",
            "content": prompt
        }
    ]
)


def answer_with_multiple_pal_context(question: str, pals: list[dict[str, str]]) -> str:
    """根据多个帕鲁资料回答问题。"""

    pal_text = ""

    for index, pal in enumerate(pals, start=1):
        pal_text += f"""
帕鲁{index}：

{format_pal_prompt(pal)}

"""

    prompt = f"""
你是一名《幻兽帕鲁》攻略助手。

用户问题：
{question}

参考资料：

{pal_text}

要求：
1. 使用中文回答。
2. 根据提供资料分析。
3. 如果资料不足，请明确说明。
4. 用户如果是在比较帕鲁，请给出明确建议。
"""

    return chat_completion(
    [
        {
            "role": "system",
            "content": "你是一个专业的游戏攻略助手。"
        },
        {
            "role": "user",
            "content": prompt
        }
    ]
)


def answer_with_hybrid_context(
    question: str,
    context: dict,
    history: list[dict[str, str]] | None = None,
) -> str:
    """
    根据Hybrid检索结果生成回答。
    """

    entity_text = ""


    for pal in context["entities"]:
        entity_text += f"""
{format_pal_prompt(pal)}

"""


    knowledge_text = "\n\n".join(
        context["knowledge"]
    )

    history_text = "暂无历史对话"

    if history:
        history_text = "\n".join(
            f"{'用户' if item['role'] == 'user' else '助手'}：{item['content']}"
            for item in history[-12:]
        )


    prompt = f"""
你是一名《幻兽帕鲁》攻略助手。

用户问题：

{question}


最近的会话历史：

{history_text}


以下是相关帕鲁资料：

{entity_text}


以下是知识库资料：

{knowledge_text}


回答要求：

1. 使用中文回答。
2. 优先根据提供资料分析。
3. 不要编造资料中不存在的信息。
4. 如果资料不足，请明确说明。
5. 如果用户是在比较帕鲁，请给出明确建议。
6. 如果用户要求比较多个帕鲁，请从多个角度分析差异。
7. 即使资料不完整，也可以基于已有资料给出有限条件下的推荐，不要简单拒绝判断。
8. 如果问题是追问，请结合会话历史理解省略的帕鲁名称或比较对象。
9. 历史对话只用于理解上下文，事实仍以本次提供的知识库资料为准。
"""


    answer = chat_completion(
        [
            {
                "role": "system",
                "content": "你是一个专业的游戏攻略助手。"
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    if ENABLE_PROMPT_LOG:

        save_qa_log(
            question,
            prompt,
            answer
        )


    return answer
