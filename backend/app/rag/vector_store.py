
from pathlib import Path

from langchain_chroma import Chroma

from app.rag.embeddings import get_embeddings


BACKEND_DIR = Path(__file__).resolve().parents[2]
CHROMA_DIR = BACKEND_DIR / "data" / "chroma_db"

COLLECTION_NAME = "doubt_solver_pages"


def get_vector_store() -> Chroma:
    """Create or reopen the persistent ChromaDB collection."""

    CHROMA_DIR.mkdir(parents=True, exist_ok=True)

    return Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=get_embeddings(),
        persist_directory=str(CHROMA_DIR),
    )


def add_documents(documents: list) -> list[str]:
    """Save document chunks and return their IDs."""

    if not documents:
        raise ValueError("No document chunks provided.")

    vector_store = get_vector_store()

    return vector_store.add_documents(documents=documents)


def search_documents(
    question: str,
    k: int = 4,
) -> list:
    """Search for the most relevant document chunks."""

    if not question.strip():
        raise ValueError("Question cannot be empty.")

    vector_store = get_vector_store()

    return vector_store.similarity_search(
        query=question,
        k=k,
    )
