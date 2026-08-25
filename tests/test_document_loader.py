from src.document_loader import load_knowledge_base


def test_loads_knowledge_base():
    documents = load_knowledge_base()

    assert len(documents) == 14


def test_document_has_required_structure():
    documents = load_knowledge_base()

    document = documents[0]

    assert "source" in document
    assert "metadata" in document
    assert "content" in document


def test_current_returns_policy_metadata():
    documents = load_knowledge_base()

    returns_policy = next(
        document
        for document in documents
        if document["source"] == "01-returns-policy-current.md"
    )

    assert returns_policy["metadata"]["status"] == "active"
    assert returns_policy["metadata"]["policy_authority"] == "official"


def test_legacy_returns_policy_is_marked_superseded():
    documents = load_knowledge_base()

    legacy_policy = next(
        document
        for document in documents
        if document["source"] == "02-returns-policy-legacy.md"
    )

    assert legacy_policy["metadata"]["status"] == "superseded"


def test_internal_migration_notes_are_not_customer_policy():
    documents = load_knowledge_base()

    internal_notes = next(
        document
        for document in documents
        if document["source"] == "14-internal-content-migration-notes.md"
    )

    assert internal_notes["metadata"]["audience"] == "internal"
    assert internal_notes["metadata"]["policy_authority"] == "none"