from app.knowledge_builder import build_pal_text
from app.pal_service import load_pals


STAGE_KEYWORDS = {"前期": "前期", "中期": "中期", "后期": "后期"}
WORK_KEYWORDS = {
    "生火": "生火", "浇水": "浇水", "播种": "播种", "发电": "发电",
    "手工": "手工作业", "采集": "采集", "伐木": "伐木", "采矿": "采矿",
    "制药": "制药", "冷却": "冷却", "搬运": "搬运", "牧场": "牧场",
}
BASE_KEYWORDS = ("基地", "工作", "生产", "打工")
RECOMMENDATION_KEYWORDS = ("推荐", "值得", "抓谁", "选谁", "培养谁", "哪个好")
MOUNT_KEYWORDS = {
    "陆地坐骑": "ground",
    "地面坐骑": "ground",
    "陆地骑乘": "ground",
}


def _mount_type(pal: dict) -> str | None:
    """Classify mounts from the normalized partner-skill description."""
    description = (
        pal.get("wiki", {})
        .get("partner_skill", {})
        .get("description", "")
    )
    if "可骑在它的背上在空中飞行" in description:
        return "flying"
    if "可骑在它的背上在水上移动" in description:
        return "water"
    if "可骑在它的背上移动" in description:
        return "ground"
    return None


def search_structured_pals(question: str, top_k: int = 3) -> list[dict]:
    """Retrieve broad recommendations from explicit JSON fields."""
    stages = [value for key, value in STAGE_KEYWORDS.items() if key in question]
    work_types = [value for key, value in WORK_KEYWORDS.items() if key in question]
    mount_types = [value for key, value in MOUNT_KEYWORDS.items() if key in question]
    is_base = any(key in question for key in BASE_KEYWORDS)
    is_recommendation = any(key in question for key in RECOMMENDATION_KEYWORDS)
    has_filters = stages or work_types or mount_types or is_base
    if not has_filters or (not is_recommendation and not mount_types):
        return []

    ranked = []
    for pal in load_pals():
        stage = pal["recommended_stage"]
        work = pal["work_suitability"]
        mount_type = _mount_type(pal)
        if stages and not any(expected in stage for expected in stages):
            continue
        if work_types and not all(item in work for item in work_types):
            continue
        if mount_types and mount_type not in mount_types:
            continue

        score = 4.0 if stages else 0.0
        if stages and stage == stages[0]:
            score += 1.0
        if is_base:
            score += len(work) * 0.8 + sum(work.values()) * 0.25
            score += max(work.values(), default=0) * 0.35
        score += sum(work.get(item, 0) * 2.0 for item in work_types)
        if mount_types:
            movement = pal.get("wiki", {}).get("movement", {})
            score += movement.get("奔跑", 0) / 1000
        ranked.append((score, pal))

    ranked.sort(key=lambda item: (-item[0], item[1]["name"]))
    results = []
    for score, pal in ranked[:top_k]:
        wiki = pal.get("wiki", {})
        results.append({
            "text": build_pal_text(pal),
            "score": score,
            "metadata": {
                "name": pal["name"],
                "element": pal["element"],
                "recommended_stage": pal["recommended_stage"],
                "dex_no": wiki.get("dex_no"),
                "source_url": wiki.get("source_url"),
                "retrieval_type": "structured",
                "mount_type": _mount_type(pal),
            },
        })
    return results
