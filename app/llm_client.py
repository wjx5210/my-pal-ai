import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


MODEL_NAME = "deepseek-v4-flash"


client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)