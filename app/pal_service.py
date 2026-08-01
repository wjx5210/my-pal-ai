import json
from pathlib import Path


DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "pals.json"


def load_pals() -> list[dict[str, str]]:
    """读取本地帕鲁数据。"""

    with DATA_FILE.open("r", encoding="utf-8") as file:
        pals = json.load(file)

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