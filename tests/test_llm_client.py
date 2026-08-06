from app import llm_client


def test_chat_completion_api_error(monkeypatch):
    """
    测试LLM调用失败时的处理。
    """


    class FakeCompletions:

        def create(self, *args, **kwargs):
            raise Exception("API连接失败")


    class FakeChat:

        completions = FakeCompletions()


    class FakeClient:

        chat = FakeChat()


    monkeypatch.setattr(
        llm_client,
        "client",
        FakeClient()
    )


    result = llm_client.chat_completion(
        [
            {
                "role": "user",
                "content": "测试"
            }
        ]
    )


    assert result == "AI服务暂时不可用，请稍后重试。"