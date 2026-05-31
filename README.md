# Healthcare Knowledge Chatbot

A small Retrieval-Augmented Generation (RAG) chatbot focused on diabetes
questions. The app scrapes trusted healthcare webpages, embeds the extracted
text into Qdrant, retrieves relevant chunks for a user question, and generates a
grounded answer with source links.

The current first version is intentionally simple: one disease focus, one
FastAPI backend, one static HTML/CSS/JavaScript frontend, and switchable model
providers.

## Project Flow

```text
diabetes webpages
  -> requests + BeautifulSoup scraper
  -> JSONL scraped text
  -> text chunks
  -> embeddings
  -> Qdrant vector database
  -> retrieval
  -> OpenAI or Ollama chat model
  -> CLI, API, or browser UI answer
```

## Project Structure

```text
app/
  api.py            FastAPI routes and static frontend serving
  config.py         environment-based settings
  models.py         OpenAI/Ollama model factories
  rag.py            retrieval and answer generation
  sources.py        diabetes-specific source list
  vectorstore.py    Qdrant ingestion and retrieval helpers
  web_scraper.py    requests/BeautifulSoup scraper

frontend/
  index.html
  styles.css
  app.js

main.py             CLI entrypoint
requirements.txt
.env.example
```

## Setup

Create and activate a virtual environment, then install dependencies.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Copy the example environment file:

```bash
cp .env.example .env
```

## Environment

OpenAI example:

```env
SCRAPED_DATA_PATH=data/scraped/healthcare_pages.jsonl
QDRANT_PATH=qdrant_db
QDRANT_COLLECTION=healthcare_knowledge

LLM_PROVIDER=openai
EMBEDDING_PROVIDER=openai

OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o-mini
OPENAI_EMBEDDING_MODEL=text-embedding-3-small

CHUNK_SIZE=1000
CHUNK_OVERLAP=150
RETRIEVAL_K=4
```

Ollama example:

```env
SCRAPED_DATA_PATH=data/scraped/healthcare_pages.jsonl
QDRANT_PATH=qdrant_db
QDRANT_COLLECTION=healthcare_knowledge

LLM_PROVIDER=ollama
EMBEDDING_PROVIDER=ollama

OLLAMA_MODEL=llama3.1
OLLAMA_EMBEDDING_MODEL=nomic-embed-text

CHUNK_SIZE=1000
CHUNK_OVERLAP=150
RETRIEVAL_K=4
```

If you use Ollama, pull the local models first:

```bash
ollama pull llama3.1
ollama pull nomic-embed-text
```

If you switch embedding providers or embedding models, rebuild the Qdrant
collection because the stored vectors are tied to that embedding model.

## Scrape Sources

The default sources are diabetes-specific and live in `app/sources.py`.

```bash
python main.py scrape
```

This writes generated scraped text to:

```text
data/scraped/healthcare_pages.jsonl
```

To scrape a small number of same-site links from each source:

```bash
python main.py scrape --include-child-pages --max-child-pages 5
```

To scrape a custom URL list:

```bash
python main.py scrape --urls https://example.com/page-1 https://example.com/page-2
```

## Build Qdrant Index

```bash
python main.py ingest
```

This splits the scraped text, creates embeddings, and stores the vectors in the
configured Qdrant collection.

For local Qdrant storage, the generated database lives in:

```text
qdrant_db/
```

## Ask From The CLI

```bash
python main.py ask "What are common symptoms of diabetes?"
```

## Run The Web App

Start FastAPI:

```bash
python main.py serve
```

Then open:

```text
http://127.0.0.1:8000/
```

The browser UI lets users enter a question, view the generated answer, see
sources, and ask another question.

FastAPI docs are available at:

```text
http://127.0.0.1:8000/docs
```

## API

Health check:

```text
GET /health
```

Ask endpoint:

```text
POST /ask
```

Request body:

```json
{
  "question": "What are common symptoms of diabetes?"
}
```

Response shape:

```json
{
  "answer": "Common symptoms of diabetes include...",
  "sources": [
    {
      "title": "Symptoms of Diabetes | Diabetes | CDC",
      "source": "https://www.cdc.gov/diabetes/signs-symptoms/index.html",
      "source_owner": "CDC"
    }
  ]
}
```

## Changing The Disease Focus

To focus on a different disease, update `HEALTHCARE_SOURCES` in
`app/sources.py` with disease-specific pages. Prefer trusted, focused pages
over broad index pages.

After changing sources, rerun:

```bash
python main.py scrape
python main.py ingest
```

## Notes

- `.env` should not be committed because it contains secrets.
- `data/scraped/` is generated scrape output.
- `qdrant_db/` is local vector database storage.
- The assistant is for educational healthcare information only and should not
  diagnose, prescribe treatment, or replace professional medical advice.
