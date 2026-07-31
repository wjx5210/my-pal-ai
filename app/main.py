from app.pal_service import find_pal_by_name


def format_pal_info(pal: dict[str, str]) -> str:
    """将帕鲁字典转换成适合终端显示的文本。"""

    return (
        "\n查询成功\n"
        f"名称：{pal['name']}\n"
        f"属性：{pal['element']}\n"
        f"简介：{pal['summary']}\n"
        f"攻略提示：{pal['tips']}"
    )


def main() -> None:
    """程序入口。"""

    print("=== 我的帕鲁攻略工具 ===")

    pal_name = input("请输入帕鲁名称：")
    pal = find_pal_by_name(pal_name)

    if pal is None:
        print(f'\n没有找到“{pal_name.strip()}”的信息。')
        return

    result = format_pal_info(pal)
    print(result)


if __name__ == "__main__":
    main()