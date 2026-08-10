import json
import pytest
from pathlib import Path

from app.qa_service import answer


def load_questions():

    path = Path(
        "evaluation/questions.json"
    )

    with open(
        path,
        encoding="utf-8"
    ) as f:
        return json.load(f)


@pytest.mark.ai
def test_rag_answers():

    questions = load_questions()

    for item in questions:

        response = answer(
            item["question"]
        )

        for keyword in item["expected_keywords"]:

            assert keyword in response, (
                f"问题:{item['question']}\n"
                f"缺少关键词:{keyword}\n"
                f"回答:{response}"
            )