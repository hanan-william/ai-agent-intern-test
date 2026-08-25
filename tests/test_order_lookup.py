from src.tools.order_lookup import get_order_status


def test_valid_order():
    result = get_order_status("ORD-1007")

    assert result["found"] is True
    assert result["status"] == "shipped"
    assert result["carrier"] == "UPS"
    assert result["estimated_delivery"] == "2026-08-22"


def test_order_id_is_normalized():
    result = get_order_status("  ord-1007 ")

    assert result["found"] is True
    assert result["order_id"] == "ORD-1007"


def test_unknown_order():
    result = get_order_status("ORD-9999")

    assert result["found"] is False
    assert result["error"] == "order_not_found"


def test_cancelled_order():
    result = get_order_status("ORD-1004")

    assert result["found"] is True
    assert result["status"] == "cancelled"


def test_order_without_eta():
    result = get_order_status("ORD-1011")

    assert result["found"] is True
    assert result["carrier"] == "Canada Post"
    assert result["estimated_delivery"] is None


def test_private_data_is_not_returned():
    result = get_order_status("ORD-1007")

    assert "email" not in result
    assert "shipping_address" not in result
    assert "risk_score" not in result
    assert "warehouse_note" not in result