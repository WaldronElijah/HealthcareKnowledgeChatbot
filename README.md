# Healthcare Knowledge Chatbot

A RAG project designed to collect healthcare data 
Expert project: scrape web pages, turn them into documents, embed them into a
vector database, retrieve relevant chunks, and answer questions with an LLM.

## 1. Configure models

Copy `.env.example` to `.env`, then choose OpenAI or Ollama.

OpenAI example:

```bash
LLM_PROVIDER=openai
EMBEDDING_PROVIDER=openai
OPENAI_MODEL=gpt-4o-mini
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
```

Ollama example:

```bash
LLM_PROVIDER=ollama
EMBEDDING_PROVIDER=ollama
OLLAMA_MODEL=llama3.1
OLLAMA_EMBEDDING_MODEL=nomic-embed-text
```

If you switch embedding providers or embedding models, rebuild the Qdrant
collection because the stored vectors come from that embedding model.

## 2. Scrape the starter healthcare sources

```bash
python main.py scrape
```

This writes scraped text to:

```text
data/scraped/healthcare_pages.jsonl
```

To do a slightly larger first test, scrape a few same-site links from each
source index page:

```bash
python main.py scrape --include-child-pages --max-child-pages 5
```

## 3. Build the vector database

```bash
python main.py ingest
```

This creates a local Qdrant database in:

```text
qdrant_db/
```

## 4. Ask a question from the CLI

```bash
python main.py ask "What are common symptoms of diabetes?"
```

## 5. Start the API

```bash
python main.py serve --reload
```

Then call:

```text
POST http://127.0.0.1:8000/ask
```

with JSON:

```json
{
  "question": "What are common symptoms of diabetes?"
}
```

## Current source list

The default sources live in `app/sources.py`:

- MedlinePlus Health Topics
- MedlinePlus All Health Topics
- CDC Health Topics
- CDC FastStats Diseases and Conditions
- Mayo Clinic Diseases and Conditions
- Cleveland Clinic Diseases and Conditions
- WebMD Health Topics
- WebMD Medical Reference
