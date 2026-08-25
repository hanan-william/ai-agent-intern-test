from datetime import date


def is_customer_authoritative(chunk: dict) -> bool:
    """
    Determine whether a knowledge-base chunk can be used
    as current customer-facing policy.
    """
    metadata = chunk["metadata"]

    return (
        metadata.get("status") == "active"
        and metadata.get("audience") == "customer"
        and metadata.get("policy_authority") == "official"
    )


def precedence_score(chunk: dict) -> int:
    """
    Give higher priority to current authoritative customer documents.
    """
    metadata = chunk["metadata"]

    score = 0

    if metadata.get("status") == "active":
        score += 100

    if metadata.get("policy_authority") == "official":
        score += 50

    if metadata.get("audience") == "customer":
        score += 25

    return score