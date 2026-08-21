import json
from pathlib import Path

from app import ai_service


def test_pal_guide_prompt_contains_complete_wiki_data():
    pals = json.loads(Path("data/pals.json").read_text(encoding="utf-8"))
    prompt = ai_service.build_pal_guide_prompt(pals[0])

    assert "手工作业" in prompt
    assert "搬运" in prompt
    assert "工作速度" in prompt
    assert "茸茸盾牌" in prompt
    assert "滚滚毛球" in prompt
    assert "羊毛" in prompt
    assert "基础属性" in prompt


def test_generate_pal_guide_sends_complete_prompt(monkeypatch):
    pals = json.loads(Path("data/pals.json").read_text(encoding="utf-8"))
    captured = {}

    def fake_chat_completion(messages):
        captured["prompt"] = messages[-1]["content"]
        return "完整总结"

    monkeypatch.setattr(ai_service, "chat_completion", fake_chat_completion)

    assert ai_service.generate_pal_guide(pals[0]) == "完整总结"
    assert "工作速度" in captured["prompt"]
    assert "茸茸盾牌" in captured["prompt"]
    assert "帕鲁光束" in captured["prompt"]
