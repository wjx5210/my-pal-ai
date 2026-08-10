from datetime import datetime
from pathlib import Path


LOG_DIR = Path("logs")
LOG_FILE = LOG_DIR / "qa.log"


def save_qa_log(
    question: str,
    prompt: str,
    answer: str
):
    """
    保存一次问答日志。
    """

    LOG_DIR.mkdir(
        exist_ok=True
    )

    log_content = f"""
====================
时间:
{datetime.now()}

用户问题:
{question}


Prompt:
{prompt}


AI回答:
{answer}

"""

    with open(
        LOG_FILE,
        "a",
        encoding="utf-8"
    ) as f:

        f.write(log_content)