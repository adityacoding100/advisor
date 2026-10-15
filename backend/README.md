# Backend setup

Set `OPENAI_API_KEY` in the backend environment. It is used for both chat
generation and retrieval embeddings.

Optional model overrides:
- `OPENAI_CHAT_MODEL` (default: `gpt-6-luna`)
- `OPENAI_EMBEDDING_MODEL` (default: `text-embedding-3-small`)

After changing embedding providers or embedding models, rebuild FAISS once:

```bash
uv run python -m app.rag.index_documents
```

Install dependencies with `uv sync`.
