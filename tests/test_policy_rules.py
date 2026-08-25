from src.document_loader import load_knowledge_base
from src.chunker import chunk_document
from src.policy_rules import (
    is_customer_authoritative,
    precedence_score,
)


def get_chunk_for_source(source):
    documents = load_knowledge_base()

    document = next(
        document
        for document in documents
        if document["source"] == source
    )

    chunks = chunk_document(document)

    return chunks[0]


def test_current_returns_policy_is_authoritative():
    chunk = get_chunk_for_source(
        "01-returns-policy-current.md"
    )

    assert is_customer_authoritative(chunk) is True


def test_legacy_returns_policy_is_not_authoritative():
    chunk = get_chunk_for_source(
        "02-returns-policy-legacy.md"
    )

    assert is_customer_authoritative(chunk) is False


def test_internal_notes_are_not_customer_authoritative():
    chunk = get_chunk_for_source(
        "14-internal-content-migration-notes.md"
    )

    assert is_customer_authoritative(chunk) is False


def test_current_policy_has_higher_precedence_than_legacy():
    current = get_chunk_for_source(
        "01-returns-policy-current.md"
    )

    legacy = get_chunk_for_source(
        "02-returns-policy-legacy.md"
    )

    assert precedence_score(current) > precedence_score(legacy)