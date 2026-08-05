def select_context_by_intent(intent: str, pal: dict) -> dict:

    """
    根据意图选择需要提供给AI的资料。
    """

    context = {
        "name": pal["name"]
    }


    if intent == "location":
        context["element"] = pal.get("element", [])
        context["locations"] = pal.get("locations", [])


    elif intent == "combat":
        context["combat"] = pal.get("combat", {})
        context["recommended_stage"] = pal.get(
            "recommended_stage",
            "暂无资料"
        )
        context["recommendation"] = pal.get(
            "recommendation",
            "暂无资料"
        )


    elif intent == "work":
        context["work_suitability"] = pal.get(
            "work_suitability",
            {}
        )


    elif intent == "drop":
        context["drops"] = pal.get(
            "drops",
            []
        )


    else:
        return pal


    return context


def select_multiple_context_by_intent(
    intent: str,
    pals: list[dict]
) -> list[dict]:
    """
    根据意图筛选多个帕鲁资料。
    """

    contexts = []

    for pal in pals:

        context = {
            "name": pal["name"]
        }


        if intent == "compare":

            context["element"] = pal.get(
                "element",
                []
            )

            context["combat"] = pal.get(
                "combat",
                {}
            )

            context["work_suitability"] = pal.get(
                "work_suitability",
                {}
            )

            context["locations"] = pal.get(
                "locations",
                []
            )

            context["drops"] = pal.get(
                "drops",
                []
            )

            context["recommended_stage"] = pal.get(
                "recommended_stage",
                ""
            )

            context["recommendation"] = pal.get(
                "recommendation",
                ""
            )

            context["tips"] = pal.get(
                "tips",
                ""
            )

        else:
            context = pal


        contexts.append(context)


    return contexts