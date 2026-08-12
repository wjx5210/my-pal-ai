"""低速采集 PalDB 前 N 个帕鲁，并转换为 My Pal AI 数据。"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import time
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin, urlparse

import httpx
from bs4 import BeautifulSoup, Tag


BASE_URL = "https://paldb.cn"
INDEX_URL = f"{BASE_URL}/pals"
USER_AGENT = "MyPalAIKnowledgeBuilder/1.0 (educational; low-rate crawler)"
WORK_ALIASES = {"点火": "生火"}
ELEMENTS = ["无属性", "火属性", "水属性", "雷属性", "草属性", "暗属性", "龙属性", "地属性", "冰属性"]


@dataclass
class CrawlRecord:
    index: int
    url: str
    cache_file: str
    sha256: str
    collected_at: str
    status: str
    error: str | None = None


def clean_text(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip().strip('"“”')


def discover_detail_urls(html: str, limit: int) -> list[str]:
    return [url for url, _ in discover_detail_entries(html, limit)]


def discover_detail_entries(html: str, limit: int) -> list[tuple[str, str]]:
    soup = BeautifulSoup(html, "html.parser")
    entries: list[tuple[str, str]] = []
    for anchor in soup.select('a[href^="/pals/"]'):
        href = anchor.get("href")
        if not isinstance(href, str) or href.rstrip("/") == "/pals":
            continue
        url = urljoin(BASE_URL, href)
        if any(existing_url == url for existing_url, _ in entries):
            continue
        match = re.search(r"#\s*(\d{1,3}[A-Z]?)", clean_text(anchor.get_text(" ", strip=True)))
        dex_no = match.group(1) if match else ""
        entries.append((url, dex_no))
        if len(entries) == limit:
            break
    return entries


def heading_section(soup: BeautifulSoup, title: str) -> list[Tag]:
    heading = next((node for node in soup.find_all(["h2", "h3"]) if clean_text(node.get_text(" ", strip=True)) == title), None)
    if heading is None:
        return []
    parent = heading.parent
    if parent is None:
        return []
    # Small card headers contain only the heading; their parent owns the body.
    root = parent.parent if clean_text(parent.get_text(" ", strip=True)) == title else parent
    if not isinstance(root, Tag):
        return []
    return [node for node in root.find_all(recursive=True) if isinstance(node, Tag) and node is not heading]


def section_text(soup: BeautifulSoup, title: str) -> str:
    return clean_text(" ".join(node.get_text(" ", strip=True) for node in heading_section(soup, title)))


def parse_work_suitability(soup: BeautifulSoup) -> dict[str, int]:
    result: dict[str, int] = {}
    pattern = re.compile(r"(点火|生火|浇水|播种|发电|手工作业|采集|伐木|采矿|制药|冷却|搬运|牧场)\s*Lv\.?\s*(\d+)")
    for work, level in pattern.findall(section_text(soup, "工作适应性")):
        result[WORK_ALIASES.get(work, work)] = int(level)
    return result


def parse_drops(soup: BeautifulSoup) -> list[str]:
    drops: list[str] = []
    nodes = heading_section(soup, "掉落物品")
    for node in nodes:
        for image in node.find_all("img"):
            alt = clean_text(image.get("alt", ""))
            if alt and alt not in drops:
                drops.append(alt)
    return drops


def parse_locations(soup: BeautifulSoup) -> list[str]:
    locations: list[str] = []
    for title in ("栖息区域(刷新点)", "出现地点"):
        for node in heading_section(soup, title):
            if node.name == "span":
                classes = set(node.get("class", []))
                text = clean_text(node.get_text(" ", strip=True))
                if {"text-gray-300", "text-sm"}.issubset(classes) and text and text not in locations:
                    locations.append(text)
            for anchor in node.find_all("a"):
                text = clean_text(anchor.get_text(" ", strip=True))
                if text and not re.fullmatch(r"(白天|夜晚)\s*\d+\s*个刷新点", text) and text not in locations:
                    locations.append(text)
    return locations[:12]


def parse_partner_skill(soup: BeautifulSoup) -> tuple[str, str]:
    nodes = heading_section(soup, "伙伴技能")
    title = ""
    description = ""
    for node in nodes:
        subheading = node.find(["h3", "h4"])
        if subheading and not title:
            title = clean_text(subheading.get_text(" ", strip=True))
        paragraph = node.find("p")
        if paragraph and not description:
            description = clean_text(paragraph.get_text(" ", strip=True))
    return title, description


def parse_stats(soup: BeautifulSoup, title: str, labels: list[str]) -> dict[str, int]:
    text = section_text(soup, title)
    result: dict[str, int] = {}
    for label in labels:
        match = re.search(rf"{re.escape(label)}\s*(\d+)", text)
        if match:
            result[label] = int(match.group(1))
    return result


def parse_skills(soup: BeautifulSoup) -> list[dict]:
    skills: list[dict] = []
    pattern = re.compile(r"(.+?)(无属性|火属性|水属性|雷属性|草属性|暗属性|龙属性|地属性|冰属性)\s*(近战|远程)?\s*Lv\.?\s*(\d+)\s*威力:\s*(\d+)")
    for node in heading_section(soup, "主动技能"):
        for anchor in node.find_all("a"):
            text = clean_text(anchor.get_text(" ", strip=True))
            match = pattern.match(text)
            if match:
                skills.append({"name": clean_text(match.group(1)), "element": match.group(2), "range": match.group(3) or "", "unlock_level": int(match.group(4)), "power": int(match.group(5)), "description": text})
    return skills


def infer_stage(stats: dict[str, int], works: dict[str, int]) -> str:
    highest_work = max(works.values(), default=0)
    total = stats.get("HP", 0) + stats.get("攻击", 0) + stats.get("防御", 0)
    if highest_work >= 4 or total >= 330:
        return "后期"
    if highest_work >= 3 or total >= 270:
        return "中期至后期"
    if highest_work >= 2 or total >= 225:
        return "前期至中期"
    return "前期"


def derive_combat(elements: list[str], stats: dict[str, int], skills: list[dict]) -> dict:
    attack, defense, hp = stats.get("攻击", 0), stats.get("防御", 0), stats.get("HP", 0)
    positioning = "输出型帕鲁" if attack >= max(hp, defense) and attack >= 100 else "耐久型帕鲁" if defense >= 100 or hp >= 110 else "均衡型帕鲁"
    strengths = [f"拥有{'、'.join(elements)}技能覆盖"]
    if skills:
        strongest = max(skills, key=lambda item: item["power"])
        strengths.append(f"可学习威力 {strongest['power']} 的{strongest['name']}")
    weaknesses = ["实际表现还会受到等级、被动技能和培养程度影响"]
    if attack < 90:
        weaknesses.append("基础攻击偏低，不适合作为纯输出主力")
    return {"positioning": positioning, "strengths": strengths, "weaknesses": weaknesses}


def parse_pal_detail(html: str, url: str, collected_at: str, fallback_dex_no: str = "") -> dict:
    soup = BeautifulSoup(html, "html.parser")
    heading = soup.find("h1")
    if heading is None:
        raise ValueError(f"详情页缺少名称: {url}")
    name = clean_text(heading.get_text(" ", strip=True))
    page_text = clean_text(soup.get_text(" ", strip=True))
    og_title = soup.find("meta", attrs={"property": "og:title"})
    identity_text = " ".join(
        [
            page_text[:1200],
            str(og_title.get("content", "")) if og_title else "",
        ]
    )
    dex_match = re.search(r"(?:#|No\.?)\s*(\d{1,3}[A-Z]?)", identity_text, re.IGNORECASE)
    if not dex_match and not fallback_dex_no:
        raise ValueError(f"详情页缺少图鉴编号: {url}")
    dex_no = dex_match.group(1) if dex_match else fallback_dex_no
    title_metadata = str(og_title.get("content", "")) if og_title else ""
    elements = [value for value in ELEMENTS if value in title_metadata]
    if not elements:
        elements = [value for value in ELEMENTS if value in page_text[:500]]
    quote_node = soup.select_one("p.italic")
    quote = quote_node.get_text(" ", strip=True) if quote_node else None
    summary = clean_text(str(quote)) if quote else f"{name}是《幻兽帕鲁》中的{'、'.join(elements)}帕鲁。"
    partner_name, partner_description = parse_partner_skill(soup)
    works = parse_work_suitability(soup)
    stats = parse_stats(soup, "基础属性", ["HP", "攻击", "防御", "工作速度"])
    movement = parse_stats(soup, "移动能力", ["行走", "奔跑", "游泳", "耐力"])
    skills, drops, locations = parse_skills(soup), parse_drops(soup), parse_locations(soup)
    stage = infer_stage(stats, works)
    strongest_work = max(works, key=works.get) if works else "基地工作"
    recommendation = f"推荐在{stage}根据其{'、'.join(elements)}属性与{strongest_work}能力安排用途。"
    if partner_description:
        recommendation += f"伙伴技能“{partner_name}”：{partner_description}"
    return {
        "name": name, "element": elements, "summary": summary, "work_suitability": works,
        "combat": derive_combat(elements, stats, skills), "drops": drops, "locations": locations,
        "recommended_stage": stage, "recommendation": recommendation,
        "tips": f"比较{name}时应同时考虑属性、工作等级、基础数值和伙伴技能。",
        "wiki": {"dex_no": dex_no, "partner_skill": {"name": partner_name, "description": partner_description}, "base_stats": stats, "movement": movement, "active_skills": skills, "source_url": url, "source_site": "paldb.cn", "collected_at": collected_at},
    }


class PalDBClient:
    def __init__(self, cache_dir: Path, delay: float, retries: int, refresh: bool):
        self.cache_dir, self.delay, self.retries, self.refresh = cache_dir, delay, retries, refresh
        self.client = httpx.Client(headers={"User-Agent": USER_AGENT, "Accept-Language": "zh-CN,zh;q=0.9"}, timeout=30, follow_redirects=True)
        self.last_request = 0.0

    def close(self): self.client.close()

    def fetch(self, url: str) -> tuple[str, Path, str]:
        slug = urlparse(url).path.strip("/").replace("/", "__") or "index"
        cache_file = self.cache_dir / f"{slug}.html"
        if cache_file.exists() and not self.refresh:
            content = cache_file.read_text(encoding="utf-8")
            return content, cache_file, hashlib.sha256(content.encode()).hexdigest()
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        for attempt in range(self.retries + 1):
            time.sleep(max(0, self.delay - (time.monotonic() - self.last_request)))
            try:
                response = self.client.get(url); self.last_request = time.monotonic(); response.raise_for_status()
                cache_file.write_text(response.text, encoding="utf-8")
                return response.text, cache_file, hashlib.sha256(response.content).hexdigest()
            except (httpx.HTTPError, OSError):
                if attempt >= self.retries: raise
                time.sleep(2 ** attempt)
        raise RuntimeError("unreachable")


def validate_records(pals: list[dict], expected: int):
    if len(pals) != expected: raise ValueError(f"期望 {expected} 条，实际 {len(pals)} 条")
    if len({pal['name'] for pal in pals}) != expected: raise ValueError("名称重复")
    if len({pal['wiki']['dex_no'] for pal in pals}) != expected: raise ValueError("图鉴编号重复")
    for pal in pals:
        if not pal["element"] or set(pal["combat"]) != {"positioning", "strengths", "weaknesses"}:
            raise ValueError(f"{pal['name']} 结构无效")


def main():
    parser = argparse.ArgumentParser(description="采集 PalDB 前 N 个帕鲁")
    parser.add_argument("--limit", type=int, default=100)
    parser.add_argument("--delay", type=float, default=2.0)
    parser.add_argument("--retries", type=int, default=3)
    parser.add_argument("--refresh", action="store_true")
    parser.add_argument("--output", type=Path, default=Path("data/imported/paldb_first_100.json"))
    parser.add_argument("--cache-dir", type=Path, default=Path("data/raw/paldb"))
    parser.add_argument("--manifest", type=Path, default=Path("data/manifests/paldb_first_100.json"))
    args = parser.parse_args()
    if not 1 <= args.limit <= 100: parser.error("--limit 必须在 1 到 100 之间")
    collected_at, pals, records = datetime.now(timezone.utc).isoformat(), [], []
    client = PalDBClient(args.cache_dir, args.delay, args.retries, args.refresh)
    try:
        index_html, _, _ = client.fetch(INDEX_URL)
        entries = discover_detail_entries(index_html, args.limit)
        if len(entries) != args.limit: raise ValueError(f"只发现 {len(entries)} 个详情链接")
        for position, (url, fallback_dex_no) in enumerate(entries, 1):
            print(f"[{position:03d}/{args.limit:03d}] {url}")
            try:
                html, cache_file, digest = client.fetch(url)
                pals.append(parse_pal_detail(html, url, collected_at, fallback_dex_no))
                records.append(CrawlRecord(position, url, str(cache_file), digest, collected_at, "ok"))
            except Exception as exc:
                records.append(CrawlRecord(position, url, "", "", collected_at, "error", str(exc))); raise
    finally:
        client.close(); args.manifest.parent.mkdir(parents=True, exist_ok=True)
        args.manifest.write_text(json.dumps([asdict(item) for item in records], ensure_ascii=False, indent=2), encoding="utf-8")
    validate_records(pals, args.limit); args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(pals, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"完成：{len(pals)} 条 -> {args.output}")


if __name__ == "__main__": main()
