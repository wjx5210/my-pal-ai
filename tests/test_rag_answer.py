from unittest.mock import patch

from app.ai_service import answer_with_rag_context



def test_answer_with_rag_context():

    contexts = [
        {
            "text": "棉悠悠是一种无属性帕鲁，适合作为新手前期培养。",
            "score": 0.9,
            "metadata": {
                "name": "棉悠悠"
            }  
        },
        {
            "text": "企丸丸拥有水属性和冰属性能力，适合部分战斗场景。",
            "score": 0.85,
            "metadata": {
                "name": "企丸丸"
            }
        }
    ]


    with patch(
        "app.ai_service.chat_completion"
    ) as mock_chat:

        mock_chat.return_value = "测试回答"

        result = answer_with_rag_context(
            "新手前期推荐什么帕鲁？",
            contexts
        )


        assert "测试回答" in result
        assert "参考资料" in result
        assert "棉悠悠" in result


        mock_chat.assert_called_once()


        call_args = (
            mock_chat.call_args[0][0]
        )


        user_message = call_args[1]["content"]


        assert "棉悠悠" in user_message
        assert "企丸丸" in user_message
        assert "新手前期推荐什么帕鲁" in user_message