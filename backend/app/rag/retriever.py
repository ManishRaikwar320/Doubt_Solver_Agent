from app.rag.ocr import extract_text_from_image
from app.rag.text_splitter import split_text
from app.rag.vector_store import search_documents, add_documents


def index_image(
        image_path: str,
        source_id: str | None = None,
        language: str = "eng"
) -> dict:
    """Extract, split and index a page image."""

    source = source_id or image_path 

    # Step 1: Extract text using OCR
    text = extract_text_from_image(
        image_path,
        language=language
    )

    # Step 2: Split the into chunks 
    chunks = split_text(
        text,
        source=source
    )

    # Step 3: Store chunks and their embeddings 
    ids = add_documents(chunks)

    return {
        "source": source,
        "text": text,
        "chunks_created": len(chunks),
        "document_ids": ids
    }
 

def retrieve_context(
    question: str,
    k: int = 4,
) -> dict:
    """Retrieve relevant content for a user question."""

    documents = search_documents(
        question=question,
        k=k,
    )

    context = "\n\n".join(
        [
            f"Source: {doc.metadata.get('source', 'unknown')}\n"
            f"Content: {doc.page_content}"
            for doc in documents
        ]
    )

    return {
        "question": question,
        "context": context,
        "sources": [
            doc.metadata.get("source", "unknown")
            for doc in documents
        ],
    }
