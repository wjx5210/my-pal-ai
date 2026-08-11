from fastapi import FastAPI
from pydantic import BaseModel

from app.qa_service import answer_with_debug
from app.pal_service import find_pals_by_name


app = FastAPI(
    title="我的帕鲁 AI 攻略助手"
)


class AskRequest(BaseModel):
    question: str


class Source(BaseModel):
    name: str
    type: str


class PalResponse(BaseModel):
    name: str
    element: list[str]
    summary: str
    tips: str


class AskResponse(BaseModel):
    answer: str
    sources: list[Source]


@app.get("/health")
def health_check():

    return {
        "status": "ok"
    }


@app.post(
    "/ask",
    response_model=AskResponse
)
def ask(request: AskRequest):

    result = answer_with_debug(
        request.question
    )

    sources = []


    for pal in result["retrieval"].get(
        "entities",
        []
    ):
        sources.append(
            {
                "name": pal["name"],
                "type": "pal"
            }
        )


    return {
        "answer": result["answer"],
        "sources": sources
    }


@app.get(
    "/pal/{name}",
    response_model=PalResponse
)
def get_pal(name: str):

    pals = find_pals_by_name(name)

    if not pals:
        return {
            "name": name,
            "element": "",
            "summary": "没有找到该帕鲁",
            "tips": ""
        }

    return pals[0]