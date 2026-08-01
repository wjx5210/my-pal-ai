from app.pal_service import find_pals_by_name


def format_pal_info(pal: dict[str, str]) -> str:
    """将帕鲁字典转换成适合终端显示的文本。"""

    return (
        f"名称：{pal['name']}\n"
        f"属性：{pal['element']}\n"
        f"简介：{pal['summary']}\n"
        f"攻略提示：{pal['tips']}"
    )


def main() -> None:
    """程序入口。"""

    print("=== 我的帕鲁攻略工具 ===")

    pal_name = input("请输入帕鲁名称：")
    matched_pals = find_pals_by_name(pal_name)

    if not matched_pals:
        print(f'\n没有找到“{pal_name.strip()}”的信息。')
        return

    print(f"\n找到 {len(matched_pals)} 个结果：")

    for index, pal in enumerate(matched_pals, start=1):
        print(f"\n结果 {index}")
        print(format_pal_info(pal))


if __name__ == "__main__":
    main()