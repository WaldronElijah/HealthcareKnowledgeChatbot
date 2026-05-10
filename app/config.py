from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class Settings:
    scraped_data_path: str = os.getenv(
        "SCRAPED_DATA_PATH", "data/scraped/healthcare_pages.jsonl"
    )
    qdrant_path: str = os.getenv("QDRANT_PATH", "qdrant_db")
    qdrant_collection: str = os.getenv("QDRANT_COLLECTION", "healthcare_knowledge")
    llm_provider: str = os.getenv("LLM_PROVIDER", "openai")
    embedding_provider: str = os.getenv("EMBEDDING_PROVIDER", "openai")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    openai_embedding_model: str = os.getenv(
        "OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"
    )
    ollama_model: str = os.getenv("OLLAMA_MODEL", "llama3.1")
    ollama_embedding_model: str = os.getenv(
        "OLLAMA_EMBEDDING_MODEL", "nomic-embed-text"
    )
    chunk_size: int = int(os.getenv("CHUNK_SIZE", "1000"))
    chunk_overlap: int = int(os.getenv("CHUNK_OVERLAP", "150"))
    retrieval_k: int = int(os.getenv("RETRIEVAL_K", "4"))


settings = Settings()
