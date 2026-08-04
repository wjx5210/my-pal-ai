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