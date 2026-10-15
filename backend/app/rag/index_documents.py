import logging
import time
from pathlib import Path
from dotenv import load_dotenv
from app.rag.chunker import split_documents
from app.rag.embeddings import get_embeddings
from app.rag.loader import document_loader
from app.rag.vectorstore import create_vectorstore,save_vectorstore

BACKEND_ROOT=Path(__file__).resolve().parents[2]
DOCUMENTS_DIRECTORY=BACKEND_ROOT/"data"/"documents"
INDEX_DIRECTORY=BACKEND_ROOT/"data"/"faiss_index"
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")
logger = logging.getLogger(__name__)

def main()->None:
    total_started = time.perf_counter()
    load_dotenv(BACKEND_ROOT/'.env')
    logger.info("index_step=document_loading status=started path=%s", DOCUMENTS_DIRECTORY)
    step_started = time.perf_counter()
    documents=document_loader(str(DOCUMENTS_DIRECTORY))
    logger.info(
        "index_step=document_loading status=complete duration_ms=%.1f pages=%d",
        (time.perf_counter() - step_started) * 1000,
        len(documents),
    )
    if not documents:
        raise FileNotFoundError(
              f"No PDF documents found in {DOCUMENTS_DIRECTORY}"
        )

    logger.info("index_step=document_chunking status=started")
    step_started = time.perf_counter()
    chunks=split_documents(documents)
    logger.info(
        "index_step=document_chunking status=complete duration_ms=%.1f chunks=%d",
        (time.perf_counter() - step_started) * 1000,
        len(chunks),
    )

    logger.info("index_step=embedding_and_faiss_build status=started")
    step_started = time.perf_counter()
    vectorstore=create_vectorstore(chunks,get_embeddings())
    logger.info(
        "index_step=embedding_and_faiss_build status=complete duration_ms=%.1f",
        (time.perf_counter() - step_started) * 1000,
    )

    logger.info("index_step=faiss_disk_save status=started path=%s", INDEX_DIRECTORY)
    step_started = time.perf_counter()
    save_vectorstore(vectorstore,INDEX_DIRECTORY)
    logger.info(
        "index_step=faiss_disk_save status=complete duration_ms=%.1f",
        (time.perf_counter() - step_started) * 1000,
    )
    logger.info(
        "index_step=total status=complete duration_ms=%.1f",
        (time.perf_counter() - total_started) * 1000,
    )


if __name__=="__main__":
    main()    