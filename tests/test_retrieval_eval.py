import json
from pathlib import Path

import pytest

from app.hybrid_service import hybrid_search


def load_questions():

    path = Path(
        "evaluation/retrieval_questions.json"
    )

    with open(
        path,
        encoding="utf-8"
    ) as f:
        return json.load(f)



@pytest.mark.ai
def test_retrieval_quality():

    questions = load_questions()

    for item in questions:

        result = hybrid_search(
            item["question"]
        )

        entities = [
            pal["name"]
            for pal in result["entities"]
        ]


        if "expected_entities" in item:

            entities = [
                pal["name"]
                for pal in result["entities"]
            ]

            for expected in item["expected_entities"]:

                assert expected in entities, (
                    f"问题:{item['question']}\n"
                    f"缺少实体:{expected}\n"
                    f"实际召回:{entities}"
                )


        if "expected_keywords" in item:

            texts = [
                item["text"]
                for item in result["rag_contexts"]
            ]

            context_text = "\n".join(texts)

            for keyword in item["expected_keywords"]:
                assert keyword in context_text, (
                    f"问题:{item['question']}\n"
                    f"缺少关键词:{keyword}\n"
                    f"检索内容:{context_text}"
                )
