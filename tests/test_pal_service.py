from app.pal_service import find_pals_by_name


def test_find_pal_by_name():
    """
    测试根据名字查询帕鲁。
    """

    result = find_pals_by_name("棉悠悠")


    assert len(result) > 0

    assert result[0]["name"] == "棉悠悠"