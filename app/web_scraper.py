from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Iterable

import requests
from bs4 import BeautifulSoup

try:
    from langchain_core.documents import Document
except ModuleNotFoundError:
    from dataclasses import dataclass

    @dataclass
    class Document:
        page_content: str
        metadata: dict


DEFAULT_HEADERS = {
    "User-Agent": (
        "HealthcareKnowledgeChatbot/0.1 "
        "(educational RAG project; contact: local-dev)"
    )
}

REMOVE_SELECTORS = [
    "script",
    "style",
    "noscript",
    "svg",
    "iframe",
    "header",
    "footer",
    "nav",
    "form",
    "aside",
]


def fetch_html(url: str, timeout: int = 20) -> str:
    response = requests.get(url, headers=DEFAULT_HEADERS, timeout=timeout)
    response.raise_for_status()
    return response.text


def html_to_text(html: str) -> tuple[str, str]:
    soup = BeautifulSoup(html, "html.parser")

    for selector in REMOVE_SELECTORS:
        for tag in soup.select(selector):
            tag.decompose()

    title = soup.title.get_text(" ", strip=True) if soup.title else ""

    # Prefer article/main content when present, otherwise fall back to body.
    content = soup.find("article") or soup.find("main") or soup.body or soup
    text = content.get_text("\n", strip=True)
    text = normalize_text(text)

    return title, text


def normalize_text(text: str) -> str:
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]{2,}", " ", text)
    return text.strip()


def scrape_url(url: str) -> Document:
    html = fetch_html(url)
    title, text = html_to_text(html)

    return Document(
        page_content=text,
        metadata={
            "source": url,
            "title": title,
        },
    )


def scrape_urls(urls: Iterable[str]) -> list[Document]:
    documents: list[Document] = []

    for url in urls:
        document = scrape_url(url)
        if document.page_content:
            documents.append(document)

    return documents


def save_documents_jsonl(documents: Iterable[Document], output_path: str | Path) -> None:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as file:
        for document in documents:
            row = {
                "page_content": document.page_content,
                "metadata": document.metadata,
            }
            file.write(json.dumps(row, ensure_ascii=False) + "\n")
