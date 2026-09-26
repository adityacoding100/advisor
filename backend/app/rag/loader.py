from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader

def document_loader(file_path: str):
    """
    Load a document from the given file path.

    Args:
        file_path (str): The path to the document file.
    """
    documents=[]
    for pdf_path in Path(file_path).rglob("*.pdf"):
        loader = PyPDFLoader(str(pdf_path))
        documents.extend(loader.load())
    return documents

