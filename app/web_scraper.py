from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Iterable
from urllib.parse import urldefrag, urljoin, urlparse

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


def same_site_links(html: str, base_url: str, limit: int) -> list[str]:
    soup = BeautifulSoup(html, "html.parser")
    base_host = urlparse(base_url).netloc
    links: list[str] = []
    seen = {base_url}

    for anchor in soup.select("a[href]"):
        href = anchor.get("href", "").strip()
        if not href or href.startswith(("mailto:", "tel:", "javascript:")):
            continue

        absolute_url = urldefrag(urljoin(base_url, href)).url
        parsed = urlparse(absolute_url)
        if parsed.scheme not in {"http", "https"}:
            continue
        if parsed.netloc != base_host:
            continue
        if absolute_url in seen:
            continue

        seen.add(absolute_url)
        links.append(absolute_url)
        if len(links) >= limit:
            break

    return links


def scrape_urls(urls: Iterable[str]) -> list[Document]:
    documents: list[Document] = []

    for url in urls:
        try:
            document = scrape_url(url)
        except requests.RequestException as error:
            print(f"Skipping {url}: {error}", file=sys.stderr)
            continue

        if document.page_content:
            documents.append(document)

    return documents


def scrape_sources(
    sources: Iterable[dict],
    include_child_pages: bool = False,
    max_child_pages_per_source: int = 5,
) -> list[Document]:
    documents: list[Document] = []
    scraped_urls: set[str] = set()

    for source in sources:
        url = source["url"]
        urls_to_scrape = [url]

        if include_child_pages and max_child_pages_per_source > 0:
            html = fetch_html(url)
            urls_to_scrape.extend(
                same_site_links(html, url, limit=max_child_pages_per_source)
            )

        for scrape_target in urls_to_scrape:
            if scrape_target in scraped_urls:
                continue

            try:
                document = scrape_url(scrape_target)
            except requests.RequestException as error:
                print(f"Skipping {scrape_target}: {error}", file=sys.stderr)
                continue

            if not document.page_content:
                continue

            document.metadata.update(
                {
                    "index_source": url,
                    "index_name": source["name"],
                    "type": source["type"],
                    "source_owner": source["source_owner"],
                    "priority": source["priority"],
                }
            )
            documents.append(document)
            scraped_urls.add(scrape_target)

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
