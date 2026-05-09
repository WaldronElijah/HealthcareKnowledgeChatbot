import argparse

from app.web_scraper import save_documents_jsonl, scrape_urls


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Scrape healthcare webpages into plain-text documents."
    )
    parser.add_argument(
        "--urls",
        nargs="+",
        required=True,
        help="One or more webpage URLs to scrape.",
    )
    parser.add_argument(
        "--out",
        default="data/scraped/healthcare_pages.jsonl",
        help="Where to save scraped text as JSONL.",
    )
    args = parser.parse_args()

    documents = scrape_urls(args.urls)
    save_documents_jsonl(documents, args.out)

    print(f"Scraped {len(documents)} page(s) into {args.out}")


if __name__ == "__main__":
    main()
