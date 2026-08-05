from app.context_service import select_multiple_context_by_intent


def test_compare_context():

    pals = [
        {
            "name": "棉悠悠",
            "element": ["无属性"],
            "combat": {
                "strengths": "容易获得"
            },
            "work_suitability": {
                "牧场": 1
            }
        },
        {
            "name": "企丸丸",
            "element": [
                "水属性",
                "冰属性"
            ],
            "combat": {
                "strengths": "拥有属性技能"
            },
            "work_suitability": {
                "浇水": 1
            }
        }
    ]


    result = select_multiple_context_by_intent(
        "compare",
        pals
    )


    assert len(result) == 2

    assert result[0]["name"] == "棉悠悠"

    assert result[1]["name"] == "企丸丸"