from langchain_community.vectorstores import FAISS
from pathlib import Path


def create_vectorstore(documents,embeddings):
    return FAISS.from_documents(
        documents,
        embeddings,

    )

def save_vectorstore(vectorstore,directory:Path)->None:
    directory.mkdir(parents=True,exist_ok=True)
    vectorstore.save_local(str(directory))

def load_vectorstore(directory:Path,embeddings):
    index_file=directory/"index.faiss"
    metadata_file=directory/"index.pkl"
    if not index_file.is_file() or not metadata_file.is_file():
        raise FileNotFoundError(
            f"FAISS index not found in {directory}. "
            "Build it with: uv run python -m app.rag.index_documents"
        )
    return FAISS.load_local(
        str(directory),
        embeddings,
        allow_dangerous_deserialization=True
    )