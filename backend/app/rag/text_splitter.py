
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=700,
    chunk_overlap=100,
    separators=["\n\n", "\n", ". ", " ", ""],
)


def split_text(
    text: str,
    source: str = "uploaded_page",
) -> list[Document]:
    """Convert extracted text into searchable chunks."""

    if not text or not text.strip():
        raise ValueError("Text cannot be empty.")

    document = Document(
        page_content=text.strip(),
        metadata={"source": source},
    )

    chunks = text_splitter.split_documents([document])

    for index, chunk in enumerate(chunks):
        chunk.metadata["chunk_index"] = index

    return chunks
