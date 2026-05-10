import argparse

from app.config import settings
from app.sources import HEALTHCARE_SOURCES
from app.web_scraper import save_documents_jsonl, scrape_sources, scrape_urls


def scrape_command(args: argparse.Namespace) -> None:
    if args.urls:
        documents = scrape_urls(args.urls)
    else:
        documents = scrape_sources(
            HEALTHCARE_SOURCES,
            include_child_pages=args.include_child_pages,
            max_child_pages_per_source=args.max_child_pages,
        )

    save_documents_jsonl(documents, args.out)
    print(f"Scraped {len(documents)} page(s) into {args.out}")


def ingest_command(args: argparse.Namespace) -> None:
    from app.vectorstore import build_vectorstore

    chunk_count = build_vectorstore(args.input, recreate=not args.append)
    print(
        f"Stored {chunk_count} chunk(s) in Qdrant collection "
        f"'{settings.qdrant_collection}'."
    )


def ask_command(args: argparse.Namespace) -> None:
    from app.rag import ask

    result = ask(args.question)
    print(result["answer"])
    print("\nSources:")
    for source in result["sources"]:
        print(f"- {source.get('title')}: {source.get('source')}")


def serve_command(args: argparse.Namespace) -> None:
    import uvicorn

    uvicorn.run("app.api:app", host=args.host, port=args.port, reload=args.reload)


def main() -> None:
    parser = argparse.ArgumentParser(description="Healthcare RAG chatbot tools.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    scrape_parser = subparsers.add_parser("scrape", help="Scrape healthcare pages.")
    scrape_parser.add_argument(
        "--urls",
        nargs="+",
        help="Optional explicit URLs. If omitted, the curated source list is used.",
    )
    scrape_parser.add_argument(
        "--include-child-pages",
        action="store_true",
        help="Also scrape a small number of same-site links from each index page.",
    )
    scrape_parser.add_argument(
        "--max-child-pages",
        type=int,
        default=5,
        help="Maximum child pages per curated source when child scraping is enabled.",
    )
    scrape_parser.add_argument(
        "--out",
        default=settings.scraped_data_path,
        help="Where to save scraped text as JSONL.",
    )
    scrape_parser.set_defaults(func=scrape_command)

    ingest_parser = subparsers.add_parser("ingest", help="Build the Qdrant index.")
    ingest_parser.add_argument(
        "--input",
        default=settings.scraped_data_path,
        help="JSONL file created by the scrape command.",
    )
    ingest_parser.add_argument(
        "--append",
        action="store_true",
        help="Append to the existing collection instead of recreating it.",
    )
    ingest_parser.set_defaults(func=ingest_command)

    ask_parser = subparsers.add_parser("ask", help="Ask the RAG chatbot a question.")
    ask_parser.add_argument("question", help="Question to ask.")
    ask_parser.set_defaults(func=ask_command)

    serve_parser = subparsers.add_parser("serve", help="Start the FastAPI app.")
    serve_parser.add_argument("--host", default="127.0.0.1")
    serve_parser.add_argument("--port", type=int, default=8000)
    serve_parser.add_argument("--reload", action="store_true")
    serve_parser.set_defaults(func=serve_command)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
