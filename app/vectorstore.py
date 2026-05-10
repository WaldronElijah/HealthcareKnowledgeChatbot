from __future__ import annotations

import json
from pathlib import Path

from app.config import settings
from app.models import get_embeddings


def load_documents_jsonl(input_path: str | Path):
    from langchain_core.documents import Document

    documents = []
    with Path(input_path).open("r", encoding="utf-8") as file:
        for line in file:
            if not line.strip():
                continue

            row = json.loads(line)
            documents.append(
                Document(
                    page_content=row["page_content"],
                    metadata=row.get("metadata", {}),
                )
            )

    return documents


def split_documents(documents):
    from langchain_text_splitters import RecursiveCharacterTextSplitter

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
    )
    return splitter.split_documents(documents)


def build_vectorstore(input_path: str | Path | None = None, recreate: bool = True) -> int:
    from langchain_qdrant import QdrantVectorStore
    from qdrant_client import QdrantClient

    source_path = input_path or settings.scraped_data_path
    documents = load_documents_jsonl(source_path)
    chunks = split_documents(documents)

    client = QdrantClient(path=settings.qdrant_path)
    if recreate and client.collection_exists(settings.qdrant_collection):
        client.delete_collection(settings.qdrant_collection)
    client.close()

    QdrantVectorStore.from_documents(
        chunks,
        embedding=get_embeddings(),
        path=settings.qdrant_path,
        collection_name=settings.qdrant_collection,
    )

    return len(chunks)


def get_vectorstore():
    from langchain_qdrant import QdrantVectorStore

    return QdrantVectorStore.from_existing_collection(
        embedding=get_embeddings(),
        path=settings.qdrant_path,
        collection_name=settings.qdrant_collection,
    )
