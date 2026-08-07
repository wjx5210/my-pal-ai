import pytest
from app.ai_service import answer_with_pal_context


@pytest.mark.ai
def test_pal_answer_contains_key_info():

    pal = {
        "name": "棉悠悠",
        "element": ["无属性"],
        "summary": "性格温顺，外形像一只覆盖着羊毛的小羊帕鲁。",
        "work_suitability": {
            "采集": 1,
            "牧场": 1
        },
        "combat": {
            "positioning": "前期辅助型帕鲁",
            "strengths": [
                "容易获得",
                "适合前期过渡"
            ],
            "weaknesses": [
                "战斗输出能力有限"
            ]
        },
        "drops": [
            "羊毛"
        ],
        "locations": [
            "初始区域附近"
        ],
        "recommended_stage": "前期",
        "recommendation": "适合作为新手阶段培养和资源获取的帕鲁。",
        "tips": "适合作为前期容易遇到的帕鲁。"
    }


    answer = answer_with_pal_context(
        "棉悠悠值得培养吗？",
        pal
    )


    assert "棉悠悠" in answer
    assert "前期" in answer