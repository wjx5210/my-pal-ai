from app.intent_service import classify_intent

questions = [
    "棉悠悠在哪里抓",
    "棉悠悠值得培养吗",
    "企丸丸有什么工作能力",
    "棉悠悠掉什么材料",
    "棉悠悠和企丸丸哪个好"
]


for q in questions:
    result = classify_intent(q)

    print(q)
    print("意图:", result)
    print("----------------")