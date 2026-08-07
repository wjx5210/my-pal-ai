from unittest.mock import patch


def test_main_rag_flow():

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
        "app.main.find_pals_in_text",
        return_value=[]
    ), patch(
        "app.main.find_pals_by_name",
        return_value=[]
    ), patch(
        "app.main.retrieve_context",
        return_value=[
            "棉悠悠适合作为新手前期培养"
        ]
    ) as mock_retrieve, patch(
        "app.main.answer_with_rag_context",
        return_value="推荐培养棉悠悠"
    ) as mock_answer:


        from app.main import main


        main()


        mock_retrieve.assert_called_once_with(
            "新手前期推荐什么帕鲁？",
            top_k=3
        )


        mock_answer.assert_called_once()