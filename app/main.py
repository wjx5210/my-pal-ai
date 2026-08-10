from app.ai_service import generate_pal_guide
from app.pal_service import (
    find_pals_by_name,
    find_pals_in_text,
)
from app.qa_service import (
    answer, 
    answer_with_debug,
)
from app.config import DEBUG_RETRIEVAL


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


def is_only_pal_name(user_input: str) -> bool:
    """
    判断用户输入是否只是查询帕鲁名称。
    """

    pals = find_pals_by_name(user_input)

    return len(pals) == 1


def main() -> None:
    """程序入口，支持连续查询和主动退出。"""

    print("=== 我的帕鲁攻略工具 ===")
    print("输入 exit 退出程序")

    while True:
        user_input = input("\n请输入帕鲁名称或提问：").strip()

        if user_input.lower() == "exit":
            print("程序已退出。")
            break


        if not is_only_pal_name(user_input):

            if DEBUG_RETRIEVAL:

                debug_result = answer_with_debug(user_input)

                print("\n--- 检索结果 ---")

                for item in debug_result["retrieval"].get(
                    "rag_contexts",
                    []
                ):
                    print(
                        f"score: {item['score']:.3f}"
                    )

                    print(
                        item["text"]
                    )

                    print("---")

                result = debug_result["answer"]

            else:

                result = answer(user_input)

            print("\n--- AI回答 ---")

            print(result)

            continue

        matched_pals = find_pals_by_name(user_input)

        if not matched_pals:
            print("没有找到相关帕鲁")
            continue


        selected_pal = matched_pals[0]

        print("\n查询成功")

        print(format_pal_display(selected_pal))

        show_ai_guide(selected_pal)


if __name__ == "__main__":
    main()
