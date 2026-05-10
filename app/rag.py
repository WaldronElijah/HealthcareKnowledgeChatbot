from __future__ import annotations

from app.config import settings
from app.models import get_llm
from app.vectorstore import get_vectorstore


SYSTEM_PROMPT = """You are a healthcare information assistant.

Answer using only the provided context. If the context does not contain the
answer, say that you do not have enough information in the provided sources.

Do not diagnose, prescribe treatment, or invent medical advice. For personal
medical decisions, encourage the user to consult a qualified healthcare
professional.
"""


def format_context(documents) -> str:
    blocks = []
    for index, document in enumerate(documents, start=1):
        title = document.metadata.get("title") or "Untitled source"
        source = document.metadata.get("source") or "Unknown source"
        blocks.append(
            f"[{index}] {title}\nSource: {source}\n{document.page_content}"
        )
    return "\n\n".join(blocks)


def ask(question: str) -> dict:
    from langchain_core.messages import HumanMessage, SystemMessage

    vectorstore = get_vectorstore()
    retriever = vectorstore.as_retriever(search_kwargs={"k": settings.retrieval_k})
    documents = retriever.invoke(question)

    context = format_context(documents)
    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(
            content=(
                f"Context:\n{context}\n\n"
                f"Question:\n{question}\n\n"
                "Answer with a concise response and include source URLs when useful."
            )
        ),
    ]

    response = get_llm().invoke(messages)
    answer = getattr(response, "content", str(response))

    return {
        "answer": answer,
        "sources": [
            {
                "title": document.metadata.get("title"),
                "source": document.metadata.get("source"),
                "source_owner": document.metadata.get("source_owner"),
            }
            for document in documents
        ],
    }
