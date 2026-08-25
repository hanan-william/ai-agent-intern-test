from src.chunker import chunk_document
from src.document_loader import load_knowledge_base


def test_document_is_split_into_sections():
    documents = load_knowledge_base()

    returns_policy = next(
        document
        for document in documents
        if document["source"] == "01-returns-policy-current.md"
    )

    chunks = chunk_document(returns_policy)

    assert len(chunks) > 1


def test_chunk_keeps_source():
    documents = load_knowledge_base()

    returns_policy = next(
        document
        for document in documents
        if document["source"] == "01-returns-policy-current.md"
    )

    chunks = chunk_document(returns_policy)

    assert all(
        chunk["source"] == "01-returns-policy-current.md"
        for chunk in chunks
    )


def test_return_window_section_is_retrievable():
    documents = load_knowledge_base()

    returns_policy = next(
        document
        for document in documents
        if document["source"] == "01-returns-policy-current.md"
    )

    chunks = chunk_document(returns_policy)

    headings = [chunk["heading"] for chunk in chunks]

    assert "Standard return window" in headings