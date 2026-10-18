import os
from langchain_openai import OpenAIEmbeddings
def get_embeddings():
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY is required for retrieval embeddings")
    return OpenAIEmbeddings(
        model=os.getenv("OPENAI_EMBEDDING_MODEL"),
    )