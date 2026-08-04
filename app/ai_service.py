import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

API_KEY = os.getenv("DEEPSEEK_API_KEY")
BASE_URL = "https://api.deepseek.com"
MODEL_NAME = "deepseek-v4-flash"

if not API_KEY:
    raise RuntimeError("没有读取到 DEEPSEEK_API_KEY，请检查项目根目录中的 .env 文件。")

client = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL,
)


def generate_pal_guide(pal_info: dict[str, str]) -> str:
    """根据帕鲁数据生成 AI 攻略。"""

    prompt = f"""
你是一名《幻兽帕鲁》攻略助手。

请严格根据下面提供的帕鲁资料回答用户。

帕鲁资料：
名称：{pal_info['name']}
属性：{pal_info['element']}
简介：{pal_info['summary']}
攻略提示：{pal_info['tips']}

要求：
1. 使用中文回答。
2. 不要编造资料中没有的信息。
3. 用简洁的攻略风格介绍这只帕鲁。
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": "你是一个专业的游戏攻略助手。"},
            {"role": "user", "content": prompt},
        ],
    )

    return response.choices[0].message.content


def answer_question(question: str) -> str:
    """回答用户提出的自然语言问题。"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": """
你是一名《幻兽帕鲁》攻略助手。

请使用中文回答。
如果不知道答案，请明确说明不知道。
不要编造不存在的信息。
""",
            },
            {"role": "user", "content": question},
        ],
    )

    return response.choices[0].message.content


def format_pal_info(pal: dict) -> str:
    """
    将帕鲁字典格式化成AI容易理解的文本。
    """

    text = f"""
名称：{pal['name']}
属性：{', '.join(pal['element'])}

简介：
{pal['summary']}

工作能力：
{pal['work_suitability']}

战斗能力：
{pal['combat']}

掉落物：
{', '.join(pal['drops'])}

出现地点：
{', '.join(pal['locations'])}

推荐阶段：
{pal['recommended_stage']}

推荐理由：
{pal['recommendation']}

攻略提示：
{pal['tips']}
"""

    return text


def answer_with_pal_context(question: str, pal_info: dict[str, str]) -> str:
    """根据用户问题和帕鲁资料生成回答。"""

    prompt = f"""
你是一名《幻兽帕鲁》攻略助手。

用户问题：
{question}

参考帕鲁资料：

{format_pal_info(pal_info)}

要求：
1. 使用中文回答。
2. 优先根据提供资料分析。
3. 不要编造资料中不存在的信息。
4. 针对用户的问题回答，不要只介绍帕鲁。
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": "你是一个专业的游戏攻略助手。"},
            {"role": "user", "content": prompt},
        ],
    )

    return response.choices[0].message.content


def answer_with_multiple_pal_context(question: str, pals: list[dict[str, str]]) -> str:
    """根据多个帕鲁资料回答问题。"""

    pal_text = ""

    for index, pal in enumerate(pals, start=1):
        pal_text += f"""
帕鲁{index}：

{format_pal_info(pal)}

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

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": "你是专业游戏攻略助手。"},
            {"role": "user", "content": prompt},
        ],
    )

    return response.choices[0].message.content
