from openai import OpenAI
import os
from dotenv import load_dotenv


load_dotenv()


client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)


MODEL_NAME = "deepseek-v4-flash"



def classify_intent(question: str) -> str:
    """
    使用LLM判断用户问题类型。
    """

    prompt = f"""
你是一个问题分类助手。

请判断用户问题属于下面哪一种：

location:
查询帕鲁出现地点

combat:
查询战斗能力、培养价值

work:
查询基地工作能力

drop:
查询掉落材料

compare:
比较多个帕鲁

other:
其他问题


用户问题：
{question}


只返回一个英文类别名称。
不要解释。
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": "你负责准确分类用户问题。"
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )


    return response.choices[0].message.content.strip()