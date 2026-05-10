from __future__ import annotations

from app.config import settings


def get_llm():
    if settings.llm_provider == "openai":
        from langchain_openai import ChatOpenAI

        return ChatOpenAI(model=settings.openai_model, temperature=0)

    if settings.llm_provider == "ollama":
        from langchain_ollama import ChatOllama

        return ChatOllama(model=settings.ollama_model, temperature=0)

    raise ValueError(f"Unknown LLM_PROVIDER: {settings.llm_provider}")


def get_embeddings():
    if settings.embedding_provider == "openai":
        from langchain_openai import OpenAIEmbeddings

        return OpenAIEmbeddings(model=settings.openai_embedding_model)

    if settings.embedding_provider == "ollama":
        from langchain_ollama import OllamaEmbeddings

        return OllamaEmbeddings(model=settings.ollama_embedding_model)

    raise ValueError(f"Unknown EMBEDDING_PROVIDER: {settings.embedding_provider}")
