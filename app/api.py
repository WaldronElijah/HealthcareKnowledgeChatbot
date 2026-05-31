from __future__ import annotations

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from app.rag import ask


app = FastAPI(title="Healthcare Knowledge Chatbot")
app.mount("/static", StaticFiles(directory="frontend"), name="static")


class AskRequest(BaseModel):
    question: str


@app.get("/")
def index() -> FileResponse:
    return FileResponse("frontend/index.html")


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/ask")
def ask_question(request: AskRequest) -> dict:
    return ask(request.question)
