import json
from pathlib import Path


ORDERS_FILE = Path(__file__).resolve().parents[2] / "data" / "orders.json"


def load_orders():
    """Load the order dataset from the assignment."""
    with ORDERS_FILE.open("r", encoding="utf-8") as file:
        data = json.load(file)

    return data["orders"]


def get_order_status(order_id: str):
    """
    Look up an order and return only customer-safe information.

    The raw orders contain private/internal fields.
    Those fields must never be returned by this tool.
    """
    if not order_id:
        return {
            "found": False,
            "error": "order_id_required",
        }

    normalized_id = order_id.strip().upper()

    orders = load_orders()

    order = next(
        (order for order in orders if order["order_id"] == normalized_id),
        None,
    )

    if order is None:
        return {
            "found": False,
            "error": "order_not_found",
            "order_id": normalized_id,
        }

    return {
        "found": True,
        "order_id": order["order_id"],
        "status": order["status"],
        "carrier": order["carrier"],
        "estimated_delivery": order["estimated_delivery"],
        "customer_safe_message": order["customer_safe_message"],
    }