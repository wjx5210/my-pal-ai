import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


MODEL_NAME = "deepseek-v4-flash"


client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)


def chat_completion(messages):
    """
    统一调用LLM接口。
    """

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            timeout=30
        )

        if not response.choices:
            print("LLM返回为空")

            return "AI没有生成有效回答。"


        return response.choices[0].message.content


    except TimeoutError:
        print("LLM请求超时")

        return "AI响应超时，请稍后重试。"


    except Exception as e:
        print(f"LLM调用异常：{type(e).__name__}: {e}")

        return "AI服务暂时不可用，请稍后重试。"