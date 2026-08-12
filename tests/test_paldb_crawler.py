from pathlib import Path

from scripts.crawl_paldb import parse_pal_detail


def test_parse_paldb_detail_page():
    html = Path("tests/fixtures/paldb_sample.html").read_text(encoding="utf-8")
    pal = parse_pal_detail(html, "https://paldb.cn/pals/Sample", "2026-08-12T00:00:00+00:00")
    assert pal["name"] == "示例帕鲁"
    assert pal["element"] == ["火属性"]
    assert pal["work_suitability"] == {"生火": 2, "搬运": 1}
    assert pal["drops"] == ["喷火器官"]
    assert pal["locations"] == ["示例区域"]
    assert pal["wiki"]["dex_no"] == "099"
    assert pal["wiki"]["base_stats"]["攻击"] == 110
    assert pal["wiki"]["active_skills"][0]["name"] == "火焰弹"
