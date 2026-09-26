from functools import lru_cache
from pathlib import Path

from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

from app.rag.chunker import split_documents
from app.rag.embeddings import get_embeddings
from app.rag.loader import document_loader
from app.rag.retriever import create_retriever
from app.rag.vectorstore import create_vectorstore

DOCUMENTS_DIRECTORY = Path(__file__).resolve().parents[2] / "data" / "documents"


@lru_cache(maxsize=1)
def get_llm():
    return ChatGoogleGenerativeAI(
        model="gemini-3.8-flash",
        temperature=0,
    )


@lru_cache(maxsize=1)
def get_retriever():
    documents = document_loader(str(DOCUMENTS_DIRECTORY))
    if not documents:
        raise FileNotFoundError(
            f"No PDF documents found in {DOCUMENTS_DIRECTORY}"
        )

    chunks = split_documents(documents)
    vectorstore = create_vectorstore(chunks, get_embeddings())
    return create_retriever(vectorstore)


def answer_question(question: str):
    matching_documents = get_retriever().invoke(question)
    context_parts = []
    sources = []
    seen_sources = set()

    for document in matching_documents:
        metadata = document.metadata
        source_name = Path(str(metadata.get("source", "Unknown source"))).name
        page = metadata.get("page")
        display_page = page + 1 if isinstance(page, int) else page
        source_key = (source_name, display_page)

        context_parts.append(
            f"[Source: {source_name}, page {display_page}]\n{document.page_content}"
        )
        if source_key not in seen_sources:
            sources.append({"file": source_name, "page": display_page})
            seen_sources.add(source_key)

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are an AI financial advisor. Answer using the retrieved "
                "document excerpts, cite source names and page numbers when "
                "relevant, and do not invent facts attributed to the documents. "
                "If the excerpts do not contain the answer, say so. Keep advice "
                "educational rather than presenting it as personalized financial advice.",
            ),
            (
                "human",
                "Question: {question}\n\nRetrieved context:\n{context}",
            ),
        ]
    )
    response = get_llm().invoke(
        prompt.format_messages(
            question=question,
            context="\n\n".join(context_parts),
        )
    )
    answer = response.content
    if not isinstance(answer, str):
        answer = "\n".join(
            part.get("text", "") if isinstance(part, dict) else str(part)
            for part in answer
        )

    return {
        "candidates": [{"content": {"parts": [{"text": answer}]}}],
        "sources": sources,
    }