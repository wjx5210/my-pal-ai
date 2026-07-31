import json
from pathlib import Path


DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "pals.json"


def load_pals() -> list[dict[str, str]]:
    """读取本地帕鲁数据。"""

    with DATA_FILE.open("r", encoding="utf-8") as file:
        pals = json.load(file)

    return pals


def find_pal_by_name(name: str) -> dict[str, str] | None:
    """根据帕鲁名称进行精确查询。"""

    normalized_name = name.strip()
    pals = load_pals()

    for pal in pals:
        if pal["name"] == normalized_name:
            return pal

    return None