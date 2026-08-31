import os
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from app.ai_service import generate_pal_guide
from app.conversation_service import (
    append_exchange,
    clear_history,
    get_history,
)
from app.pal_service import find_pals_by_name, load_pals
from app.observability import observe_request
from app.qa_service import answer_with_debug


app = FastAPI(title="我的帕鲁 AI 攻略助手")
app.middleware("http")(observe_request)

allowed_origins = [
    origin.strip()
    for origin in os.getenv(
        "ALLOWED_ORIGINS",
        "http://localhost:5173,http://127.0.0.1:5173",
    ).split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Request-ID"],
)


class AskRequest(BaseModel):
    question: str = Field(min_length=1, max_length=1000)
    session_id: str | None = None


class Source(BaseModel):
    name: str
    type: str
    url: str
    score: float | None = None


class CombatInfo(BaseModel):
    positioning: str
    strengths: list[str]
    weaknesses: list[str]


class PalResponse(BaseModel):
    name: str
    element: list[str]
    summary: str
    work_suitability: dict[str, int]
    combat: CombatInfo
    drops: list[str]
    locations: list[str]
    recommended_stage: str
    recommendation: str
    tips: str


class AskResponse(BaseModel):
    session_id: str
    answer: str
    sources: list[Source]


class SummaryResponse(BaseModel):
    name: str
    summary: str


class HistoryResponse(BaseModel):
    session_id: str
    messages: list[dict[str, str]]


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/pals", response_model=list[PalResponse])
def list_pals():
    return load_pals()


@app.post("/ask", response_model=AskResponse)
def ask(request: AskRequest):
    question = request.question.strip()
    if not question:
        raise HTTPException(status_code=422, detail="问题不能为空")

    session_id = request.session_id or str(uuid4())
    history = get_history(session_id)
    result = answer_with_debug(question, history=history)

    sources_by_name: dict[str, dict] = {}
    for pal in result["retrieval"].get("entities", []):
        sources_by_name[pal["name"]] = {
            "name": pal["name"],
            "type": "entity",
            "url": f"/pal/{pal['name']}",
            "score": None,
        }

    for item in result["retrieval"].get("rag_contexts", []):
        name = item.get("metadata", {}).get("name")
        if not name:
            continue
        existing = sources_by_name.get(name)
        if existing is None or existing.get("score") is None:
            sources_by_name[name] = {
                "name": name,
                "type": "semantic",
                "url": f"/pal/{name}",
                "score": item.get("score"),
            }

    append_exchange(session_id, question, result["answer"])
    return {
        "session_id": session_id,
        "answer": result["answer"],
        "sources": list(sources_by_name.values()),
    }


@app.get("/sessions/{session_id}", response_model=HistoryResponse)
def session_history(session_id: str):
    return {"session_id": session_id, "messages": get_history(session_id)}


@app.delete("/sessions/{session_id}")
def delete_session(session_id: str):
    clear_history(session_id)
    return {"status": "cleared"}


@app.post("/pal/{name}/summary", response_model=SummaryResponse)
def summarize_pal(name: str):
    pals = find_pals_by_name(name)
    if not pals:
        raise HTTPException(status_code=404, detail="没有找到该帕鲁")
    pal = pals[0]
    return {"name": pal["name"], "summary": generate_pal_guide(pal)}


@app.get("/pal/{name}", response_model=PalResponse)
def get_pal(name: str):
    pals = find_pals_by_name(name)
    if not pals:
        raise HTTPException(status_code=404, detail="没有找到该帕鲁")
    return pals[0]
