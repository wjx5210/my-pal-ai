import json
from pathlib import Path
from app.data_validator import validate_pal_data

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "pals.json"


def load_pals():

    with open(
        "data/pals.json",
        "r",
        encoding="utf-8"
    ) as f:

        pals = json.load(f)


    validate_pal_data(pals)


    return pals


def find_pals_by_name(name: str) -> list[dict[str, str]]:
    """根据帕鲁名称查询，返回所有匹配结果。"""

    normalized_name = name.strip()
    pals = load_pals()
    matched_pals = []

    for pal in pals:
        if normalized_name in pal["name"]:
            matched_pals.append(pal)

    return matched_pals
    return None


def find_pals_in_text(text: str) -> list[dict[str, str]]:
    """从一段自然语言文本中找出被提到的帕鲁。"""

    normalized_text = text.strip()
    pals = load_pals()
    mentioned_pals = []

    for pal in pals:
        if pal["name"] in normalized_text:
            mentioned_pals.append(pal)

    return mentioned_pals
