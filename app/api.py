from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel

from app.rag import ask


app = FastAPI(title="Healthcare Knowledge Chatbot")


class AskRequest(BaseModel):
    question: str


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/ask")
def ask_question(request: AskRequest) -> dict:
    return ask(request.question)
