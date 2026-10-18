import logging
import os
import time
from contextlib import contextmanager
from functools import lru_cache
from pathlib import Path
from uuid import uuid4

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from app.rag.embeddings import get_embeddings
from app.rag.retriever import create_retriever
from app.rag.vectorstore import load_vectorstore



logger = logging.getLogger("uvicorn.error")
logger.setLevel(logging.INFO)
BACKEND_ROOT = Path(__file__).resolve().parents[2]
INDEX_DIRECTORY = BACKEND_ROOT / "data" / "faiss_index"


@contextmanager
def _log_step(request_id: str, step: str):
    started = time.perf_counter()
    logger.info("request_id=%s step=%s status=started", request_id, step)
    try:
        yield
    except Exception:
        elapsed_ms = (time.perf_counter() - started) * 1000
        logger.exception(
            "request_id=%s step=%s status=failed duration_ms=%.1f",
            request_id,
            step,
            elapsed_ms,
        )
        raise
    else:
        elapsed_ms = (time.perf_counter() - started) * 1000
        logger.info(
            "request_id=%s step=%s status=complete duration_ms=%.1f",
            request_id,
            step,
            elapsed_ms,
        )


@lru_cache(maxsize=1)
def get_llm():
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY is required for chat generation")

    return ChatOpenAI(
        model=os.getenv("OPENAI_CHAT_MODEL", "gpt-6-luna"),
        reasoning_effort="low",
    )


@lru_cache(maxsize=1)
def get_retriever():
    vectorstore=load_vectorstore(INDEX_DIRECTORY,get_embeddings())
    return create_retriever(vectorstore)


def answer_question(question: str):
    request_id = uuid4().hex[:8]
    request_started = time.perf_counter()
    logger.info(
        "request_id=%s step=request status=started question_chars=%d",
        request_id,
        len(question),
    )

    try:
        with _log_step(request_id, "faiss_index_load_or_cache_lookup"):
            retriever = get_retriever()

        with _log_step(request_id, "query_embedding_and_similarity_search"):
            try:
                matching_documents = retriever.invoke(question)
            except AssertionError as error:
                raise RuntimeError(
                    "FAISS index embedding dimensions do not match the active embedding model. "
                    "Rebuild the index with: uv run python -m app.rag.index_documents"
                ) from error

        with _log_step(request_id, "context_and_prompt_formatting"):
            context_parts = []
            sources = []
            seen_sources = set()

            for document in matching_documents:
                metadata = document.metadata
                source_name = Path(
                    str(metadata.get("source", "Unknown source"))
                ).name
                page = metadata.get("page")
                display_page = page + 1 if isinstance(page, int) else page
                source_key = (source_name, display_page)

                context_parts.append(
                    f"[Source: {source_name}, page {display_page}]\n"
                    f"{document.page_content}"
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
            messages = prompt.format_messages(
                question=question,
                context="\n\n".join(context_parts),
            )

        with _log_step(request_id, "openai_model_initialization"):
            llm = get_llm()

        with _log_step(request_id, "openai_response_generation"):
            response = llm.invoke(messages)

        with _log_step(request_id, "response_formatting"):
            answer = response.content
            if not isinstance(answer, str):
                answer = "\n".join(
                    part.get("text", "") if isinstance(part, dict) else str(part)
                    for part in answer
                )

            result = {
                "candidates": [{"content": {"parts": [{"text": answer}]}}],
                "sources": sources,
            }

        return result
    finally:
        elapsed_ms = (time.perf_counter() - request_started) * 1000
        logger.info(
            "request_id=%s step=request status=finished duration_ms=%.1f",
            request_id,
            elapsed_ms,
        )