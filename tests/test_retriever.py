from src.retriever import KnowledgeRetriever


def test_retriever_returns_results():
    retriever = KnowledgeRetriever()

    results = retriever.search(
        "How long can I return an unused backpack?"
    )

    assert len(results) > 0


def test_return_question_retrieves_returns_policy():
    retriever = KnowledgeRetriever()

    results = retriever.search(
        "How long can I return an unused backpack?"
    )

    sources = [result["source"] for result in results]

    assert "01-returns-policy-current.md" in sources


def test_retrieval_results_have_scores():
    retriever = KnowledgeRetriever()

    results = retriever.search(
        "Do you ship to Canada?"
    )

    assert all("score" in result for result in results)


def test_canada_shipping_retrieval():
    retriever = KnowledgeRetriever()

    results = retriever.search(
        "Can you ship my order to Canada?"
    )

    sources = [result["source"] for result in results]

    assert "06-international-shipping.md" in sources

def test_customer_policy_filter_excludes_legacy_documents():
    retriever = KnowledgeRetriever()

    results = retriever.search(
        "How long can I return an unused backpack?",
        customer_policy_only=True,
    )

    sources = [result["source"] for result in results]

    assert "01-returns-policy-current.md" in sources
    assert "02-returns-policy-legacy.md" not in sources