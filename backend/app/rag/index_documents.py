from pathlib import Path
from dotenv import load_dotenv
from app.rag.chunker import split_documents
from app.rag.embeddings import get_embeddings
from app.rag.loader import document_loader
from app.rag.vectorstore import create_vectorstore,save_vectorstore

BACKEND_ROOT=Path(__file__).resolve().parents[2]
DOCUMENTS_DIRECTORY=BACKEND_ROOT/"data"/"documents"
INDEX_DIRECTORY=BACKEND_ROOT/"data"/"faiss_index"

def main()->None:
    load_dotenv(BACKEND_ROOT/'.env')
    documents=document_loader(str(DOCUMENTS_DIRECTORY))
    if not documents:
        raise FileNotFoundError(
              f"No PDF documents found in {DOCUMENTS_DIRECTORY}"
        )
    chunks=split_documents(documents)
    vectorstore=create_vectorstore(chunks,get_embeddings())
    save_vectorstore(vectorstore,INDEX_DIRECTORY)

if __name__=="__main__":
    main()    