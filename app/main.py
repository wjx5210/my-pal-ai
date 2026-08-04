from app.ai_service import (  # noqa: I001
    answer_question,
    answer_with_multiple_pal_context,
    answer_with_pal_context,
    generate_pal_guide,
)
from app.pal_service import (
    find_pals_by_name,
    find_pals_in_text,
)
from app.intent_service import classify_intent
from app.context_service import (
    select_context_by_intent,
    select_multiple_context_by_intent,
)

def format_pal_display(pal: dict[str, str]) -> str:
    """将帕鲁字典转换成适合终端显示的文本。"""

    return (
        f"名称：{pal['name']}\n"
        f"属性：{pal['element']}\n"
        f"简介：{pal['summary']}\n"
        f"攻略提示：{pal['tips']}"
    )


def show_ai_guide(pal: dict[str, str]) -> None:
    """调用 AI 生成攻略并显示。"""

    print("\n--- AI 攻略 ---")

    guide = generate_pal_guide(pal)

    print(guide)


def show_ai_answer(question: str, pal: dict[str, str]) -> None:
    """根据用户问题、意图和相关资料回答。"""

    print("\n--- AI回答 ---")


    # 第一步：让AI判断用户意图
    intent = classify_intent(question)

    print(f"识别问题类型：{intent}")


    # 第二步：根据意图筛选资料
    context = select_context_by_intent(
        intent,
        pal
    )


    # 第三步：使用筛选后的资料回答
    answer = answer_with_pal_context(
        question,
        context
    )


    print(answer)


def show_multiple_pal_answer(
    question: str,
    pals: list[dict[str, str]]
) -> None:
    """多个帕鲁情况下调用AI回答。"""

    print("\n--- AI回答 ---")


    # 第一步：判断用户意图
    intent = classify_intent(question)

    print(f"识别问题类型：{intent}")


    # 第二步：根据意图筛选多个帕鲁资料
    contexts = select_multiple_context_by_intent(
        intent,
        pals
    )


    # 第三步：生成比较回答
    answer = answer_with_multiple_pal_context(
        question,
        contexts
    )


    print(answer)


def main() -> None:
    """程序入口，支持连续查询和主动退出。"""

    print("=== 我的帕鲁攻略工具 ===")
    print("输入 exit 退出程序")

    while True:
        user_input = input("\n请输入帕鲁名称或提问：").strip()

        if user_input.lower() == "exit":
            print("程序已退出。")
            break

        # 第一优先级：
        # 判断用户问题中是否包含帕鲁名称
        mentioned_pals = find_pals_in_text(user_input)

        if mentioned_pals:
            if len(mentioned_pals) > 1:
                show_multiple_pal_answer(user_input, mentioned_pals)
                continue

            selected_pal = mentioned_pals[0]
            print("\n正在查询相关资料...")

            show_ai_answer(user_input, selected_pal)

            continue

        # 第二优先级：
        # 判断用户是否直接输入帕鲁名称
        matched_pals = find_pals_by_name(user_input)

        if not matched_pals:
            print("\n--- AI回答 ---")

            answer = answer_question(user_input)

            print(answer)

            continue

        # 一个匹配结果
        if len(matched_pals) == 1:
            selected_pal = matched_pals[0]

            print("\n查询成功")
            print(format_pal_display(selected_pal))

            show_ai_guide(selected_pal)

            continue

        # 多个匹配结果
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
        print(format_pal_display(selected_pal))

        show_ai_guide(selected_pal)


if __name__ == "__main__":
    main()
