from src.conflict_detector import find_conflicts
from src.retriever import KnowledgeRetriever


def get_breeze_results():
    retriever = KnowledgeRetriever()

    return retriever.search(
        "How should I clean my Breeze Tumbler?",
        top_k=10,
    )


def test_breeze_tumbler_conflict_is_detected():
    results = get_breeze_results()

    conflicts = find_conflicts(results)

    assert len(conflicts) == 1


def test_conflict_contains_both_sources():
    results = get_breeze_results()

    conflicts = find_conflicts(results)

    sources = conflicts[0]["sources"]

    assert "11-product-care.md" in sources
    assert "12-breeze-tumbler-product-card.md" in sources


def test_conflict_explains_the_problem():
    results = get_breeze_results()

    conflicts = find_conflicts(results)

    assert "conflicting cleaning instructions" in (
        conflicts[0]["reason"]
    )