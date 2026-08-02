from app.pal_service import find_pals_by_name
from app.ai_service import (
    generate_pal_guide,
    answer_question
)

def format_pal_info(pal: dict[str, str]) -> str:
    """将帕鲁字典转换成适合终端显示的文本。"""

    return (
        f"名称：{pal['name']}\n"
        f"属性：{pal['element']}\n"
        f"简介：{pal['summary']}\n"
        f"攻略提示：{pal['tips']}"
    )

def is_pal_query(text: str) -> bool:
    """
    判断用户输入是否可能是在查询帕鲁。
    """

    matched_pals = find_pals_by_name(text)

    return len(matched_pals) > 0

def show_ai_guide(pal: dict[str, str]) -> None:
    """调用 AI 生成攻略并显示。"""

    print("\n--- AI 攻略 ---")

    guide = generate_pal_guide(pal)

    print(guide)


def main() -> None:
    """程序入口，支持连续查询和主动退出。"""

    print("=== 我的帕鲁攻略工具 ===")
    print("输入 exit 退出程序")

    while True:
        pal_name = input("\n请输入帕鲁名称或提问：").strip()

        if pal_name.lower() == "exit":
            print("程序已退出。")
            break

        matched_pals = find_pals_by_name(pal_name)

        if not matched_pals:
           answer = answer_question(pal_name)
           print(answer)
           continue

        # 只有一个结果，直接展示
        if len(matched_pals) == 1:
            selected_pal = matched_pals[0]

            print("\n查询成功")
            print(format_pal_info(selected_pal))

            show_ai_guide(selected_pal)

            continue

        # 多个结果，让用户选择
        print(f"\n找到 {len(matched_pals)} 个结果：")

        for index, pal in enumerate(matched_pals, start=1):
            print(f"{index}. {pal['name']}")

        choice = input("\n请输入要查看的编号：").strip()

        try:
            selected_index = int(choice) - 1
        except ValueError:
            print("输入无效，请输入数字编号。")
            continue

        if selected_index < 0 or selected_index >= len(matched_pals):
            print("编号超出范围。")
            continue

        selected_pal = matched_pals[selected_index]

        print("\n查询成功")
        print(format_pal_info(selected_pal))

        show_ai_guide(selected_pal)


if __name__ == "__main__":
    main()