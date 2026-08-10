from unittest.mock import patch


def test_main_qa_flow():

    inputs = iter(
        [
            "新手前期推荐什么帕鲁？",
            "exit"
        ]
    )


    with patch(
        "builtins.input",
        side_effect=lambda _: next(inputs)
    ), patch(
        "app.main.answer_with_debug",
        return_value={
            "answer": "推荐培养棉悠悠",
            "context": {},
            "retrieval": {}
        }
    ) as mock_answer:


        from app.main import main

        main()


        mock_answer.assert_called_once_with(
            "新手前期推荐什么帕鲁？"
        )