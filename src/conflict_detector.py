def find_conflicts(results: list[dict]) -> list[dict]:
    """
    Detect known contradictory guidance among active,
    official, customer-facing knowledge-base sources.
    """

    authoritative = [
        result
        for result in results
        if (
            result["metadata"].get("status") == "active"
            and result["metadata"].get("audience") == "customer"
            and result["metadata"].get("policy_authority") == "official"
        )
    ]

    conflicts = []

    product_care = [
        result
        for result in authoritative
        if result["source"] == "11-product-care.md"
    ]

    product_card = [
        result
        for result in authoritative
        if result["source"] == "12-breeze-tumbler-product-card.md"
    ]

    care_text = " ".join(
        result["content"].lower()
        for result in product_care
    )

    card_text = " ".join(
        result["content"].lower()
        for result in product_card
    )

    handwash_guidance = "hand-washed" in care_text
    dishwasher_guidance = "dishwasher safe" in card_text

    if handwash_guidance and dishwasher_guidance:
        conflicts.append(
            {
                "topic": "Breeze Tumbler cleaning",
                "sources": [
                    "11-product-care.md",
                    "12-breeze-tumbler-product-card.md",
                ],
                "reason": (
                    "Active official customer-facing sources "
                    "provide conflicting cleaning instructions."
                ),
            }
        )

    return conflicts