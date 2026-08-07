import os

from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()


client = OpenAI(
    api_key=os.getenv("BAILIAN_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)


EMBEDDING_MODEL = "text-embedding-v3"



def create_embedding(text: str) -> list[float]:
    """
    使用Embedding API生成文本向量。
    """

    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=text
    )


    return response.data[0].embedding