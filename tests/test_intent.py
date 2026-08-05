from app import intent_service


def test_classify_intent_compare(monkeypatch):
    """
    测试比较类问题的意图识别。
    """

    def fake_chat_completion(messages):
        return "compare"


    monkeypatch.setattr(
        intent_service,
        "chat_completion",
        fake_chat_completion
    )


    result = intent_service.classify_intent(
        "棉悠悠和企丸丸哪个好"
    )


    assert result == "compare"


def fake_chat_completion(messages):
    return "compare"