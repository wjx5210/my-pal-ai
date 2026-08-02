import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

API_KEY = os.getenv("DEEPSEEK_API_KEY")
BASE_URL = "https://api.deepseek.com"
MODEL_NAME = "deepseek-v4-flash"

if not API_KEY:
    raise RuntimeError(
        "没有读取到 DEEPSEEK_API_KEY，请检查项目根目录中的 .env 文件。"
    )

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
            {
                "role": "system",
                "content": "你是一个专业的游戏攻略助手。"
            },
            {
                "role": "user",
                "content": prompt
            }
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
"""
            },
            {
                "role": "user",
                "content": question
            }
        ],
    )

    return response.choices[0].message.content

def answer_with_pal_context(
    question: str,
    pal_info: dict[str, str]
) -> str:
    """根据用户问题和帕鲁资料生成回答。"""

    prompt = f"""
你是一名《幻兽帕鲁》攻略助手。

用户问题：
{question}

参考帕鲁资料：

名称：{pal_info['name']}
属性：{pal_info['element']}
简介：{pal_info['summary']}
攻略提示：{pal_info['tips']}

要求：
1. 使用中文回答。
2. 优先根据提供资料分析。
3. 不要编造资料中不存在的信息。
4. 针对用户的问题回答，不要只介绍帕鲁。
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": "你是一个专业的游戏攻略助手。"
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
    )

    return response.choices[0].message.content