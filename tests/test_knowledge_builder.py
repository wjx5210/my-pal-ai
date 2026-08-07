from app.knowledge_builder import (
    build_pal_text,
    build_vector_store
)


def test_build_pal_text():

    pal = {
        "name": "棉悠悠",
        "element": ["无属性"],
        "summary": "适合作为新手前期过渡。",
        "work_suitability": {
            "牧场": 1
        },
        "combat": {
            "positioning": "前期辅助型",
            "strengths": [
                "容易获得"
            ],
            "weaknesses": [
                "输出有限"
            ]
        },
        "drops": [
            "羊毛"
        ],
        "locations": [
            "初始区域"
        ],
        "recommended_stage": "前期",
        "recommendation": "适合新手培养。",
        "tips": "容易遇到。"
    }


    text = build_pal_text(pal)


    assert "棉悠悠" in text
    assert "前期" in text


def test_build_vector_store():

    pals = [
        {
            "name": "棉悠悠",
            "element": ["无属性"],
            "summary": "适合作为新手前期过渡。",
            "work_suitability": {
                "牧场": 1
            },
            "combat": {
                "positioning": "前期辅助型",
                "strengths": [
                    "容易获得"
                ],
                "weaknesses": [
                    "输出有限"
                ]
            },
            "drops": [
                "羊毛"
            ],
            "locations": [
                "初始区域"
            ],
            "recommended_stage": "前期",
            "recommendation": "适合新手培养。",
            "tips": "容易遇到。"
        }
    ]


    store = build_vector_store(
        pals
    )


    assert len(store.documents) == 1

    assert (
        "棉悠悠"
        in store.documents[0]["text"]
    )

    assert (
        len(store.documents[0]["vector"])
        > 0
    )