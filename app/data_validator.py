# app/data_validator.py


REQUIRED_FIELDS = [
    "name",
    "element",
    "summary",
    "work_suitability",
    "combat",
    "drops",
    "locations",
    "recommended_stage",
    "recommendation",
    "tips"
]


def validate_pal_data(pals: list[dict]) -> bool:
    """
    校验帕鲁数据结构。
    """

    for pal in pals:

        for field in REQUIRED_FIELDS:

            if field not in pal:
                raise ValueError(
                    f"{pal.get('name', '未知帕鲁')} 缺少字段: {field}"
                )


    return True