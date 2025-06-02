import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from src.utils.invoice_checker import validate_invoice_data


# Valid base invoice for reuse
def base_invoice():
    return {
        "invoice_number": "INV-001",
        "invoice_date": "2024-06-01",
        "supplier": {"name": "Supplier Inc."},
        "client": {"name": "Client LLC"},
        "items": [
            {
                "description": "Item 1",
                "quantity": 2,
                "unit_price": 10,
                "total_price": 20,
            },
            {"description": "Item 2", "quantity": 1, "unit_price": 5, "total_price": 5},
        ],
        "subtotal": 25,
        "total": 25,
        "tax": 0,
        "shipping_cost": 0,
        "discount": 0,
        "discount_percentage": 0,
        "rounding_adjustment": 0,
        "currency": "USD",
    }


def test_valid_invoice():
    invoice = base_invoice()
    result = validate_invoice_data(invoice)
    assert result["is_valid"]
    assert result["total_errors"] == 0


def test_total_as_string():
    invoice = base_invoice()
    invoice["total"] = "25"
    result = validate_invoice_data(invoice)
    assert not result["is_valid"]
    assert any("total" in e and "type" in e for e in result["errors"])


def test_quantity_as_float():
    invoice = base_invoice()
    invoice["items"][0]["quantity"] = 2.0
    result = validate_invoice_data(invoice)
    assert not result["is_valid"]
    assert any("quantity must be an integer" in e for e in result["errors"])


def test_quantity_as_string():
    invoice = base_invoice()
    invoice["items"][0]["quantity"] = "2"
    result = validate_invoice_data(invoice)
    assert not result["is_valid"]
    assert any("quantity must be an integer" in e for e in result["errors"])


def test_unit_price_as_string():
    invoice = base_invoice()
    invoice["items"][0]["unit_price"] = "10"
    result = validate_invoice_data(invoice)
    assert not result["is_valid"]
    assert any("unit_price" in e and "type" in e for e in result["errors"])


def test_discount_percentage_out_of_range():
    invoice = base_invoice()
    invoice["discount_percentage"] = 150
    result = validate_invoice_data(invoice)
    assert not result["is_valid"]
    assert any("discount_percentage" in e and "at most" in e for e in result["errors"])


def test_missing_required_numeric():
    invoice = base_invoice()
    del invoice["total"]
    result = validate_invoice_data(invoice)
    assert not result["is_valid"]
    assert any("Missing required field: total" in e for e in result["errors"])


def test_negative_total():
    invoice = base_invoice()
    invoice["total"] = -5
    result = validate_invoice_data(invoice)
    assert not result["is_valid"]
    assert any("total" in e and "positive" in e for e in result["errors"])


def test_valid_rounding_adjustment_negative():
    invoice = base_invoice()
    invoice["rounding_adjustment"] = -0.01
    invoice["total"] = 24.99
    result = validate_invoice_data(invoice)
    assert result["is_valid"]


def test_invalid_item_total_price_type():
    invoice = base_invoice()
    invoice["items"][0]["total_price"] = "20"
    result = validate_invoice_data(invoice)
    assert not result["is_valid"]
    assert any("total_price" in e and "type" in e for e in result["errors"])


def test_missing_required_fields():
    invoice = base_invoice()
    del invoice["invoice_number"]
    del invoice["invoice_date"]
    del invoice["supplier"]
    del invoice["client"]
    del invoice["items"]
    result = validate_invoice_data(invoice)
    assert not result["is_valid"]
    assert any("Missing required field: invoice_number" in e for e in result["errors"])
    assert any("Missing required field: invoice_date" in e for e in result["errors"])
    assert any("Missing required field: supplier" in e for e in result["errors"])
    assert any("Missing required field: client" in e for e in result["errors"])
    assert any("Missing required field: items" in e for e in result["errors"])


def test_empty_required_strings():
    invoice = base_invoice()
    invoice["invoice_number"] = "  "
    invoice["invoice_date"] = ""
    invoice["supplier"]["name"] = ""
    invoice["client"]["name"] = "  "
    result = validate_invoice_data(invoice)
    assert not result["is_valid"]
    assert any(
        "Required field 'invoice_number' cannot be empty" in e for e in result["errors"]
    )
    assert any(
        "Required field 'invoice_date' cannot be empty" in e for e in result["errors"]
    )
    assert any("Field 'supplier.name' cannot be empty" in e for e in result["errors"])
    assert any("Field 'client.name' cannot be empty" in e for e in result["errors"])


def test_items_array_structure():
    invoice = base_invoice()
    invoice["items"] = None
    result = validate_invoice_data(invoice)
    assert not result["is_valid"]
    assert any("Missing required field: items" in e for e in result["errors"])
    invoice["items"] = "notalist"
    result = validate_invoice_data(invoice)
    assert not result["is_valid"]
    assert any("Field 'items' must be an array" in e for e in result["errors"])
    invoice["items"] = []
    result = validate_invoice_data(invoice)
    assert not result["is_valid"]
    assert any("Invoice must contain at least one item" in e for e in result["errors"])


def test_item_required_fields():
    invoice = base_invoice()
    invoice["items"][0].pop("description")
    invoice["items"][0].pop("quantity")
    invoice["items"][0].pop("unit_price")
    invoice["items"][0].pop("total_price")
    result = validate_invoice_data(invoice)
    assert not result["is_valid"]
    assert any(
        "Item 1: missing required field 'description'" in e for e in result["errors"]
    )
    assert any(
        "Item 1: missing required field 'quantity'" in e for e in result["errors"]
    )
    assert any(
        "Item 1: missing required field 'unit_price'" in e for e in result["errors"]
    )
    assert any(
        "Item 1: missing required field 'total_price'" in e for e in result["errors"]
    )


def test_item_description_empty():
    invoice = base_invoice()
    invoice["items"][0]["description"] = "  "
    result = validate_invoice_data(invoice)
    assert not result["is_valid"]
    assert any("Item 1: description cannot be empty" in e for e in result["errors"])


def test_currency_validation():
    invoice = base_invoice()
    invoice["currency"] = 123
    result = validate_invoice_data(invoice)
    assert not result["is_valid"]
    assert any("Currency must be a string" in e for e in result["errors"])
    invoice["currency"] = "  "
    result = validate_invoice_data(invoice)
    assert not result["is_valid"]
    assert any("Currency cannot be empty" in e for e in result["errors"])


def test_item_object_type():
    invoice = base_invoice()
    invoice["items"][0] = "notadict"
    result = validate_invoice_data(invoice)
    assert not result["is_valid"]
    assert any("Item 1 must be an object" in e for e in result["errors"])


def test_supplier_and_client_type():
    invoice = base_invoice()
    invoice["supplier"] = "notadict"
    invoice["client"] = 123
    result = validate_invoice_data(invoice)
    assert not result["is_valid"]
    assert any("Field 'supplier' must be an object" in e for e in result["errors"])
    assert any("Field 'client' must be an object" in e for e in result["errors"])


def test_item_total_price_calculation():
    invoice = base_invoice()
    invoice["items"][0]["total_price"] = 19
    result = validate_invoice_data(invoice)
    assert not result["is_valid"]
    assert any(
        "Item 1: quantity (2) × unit_price (10) = 20" in e for e in result["errors"]
    )


def test_subtotal_mismatch():
    invoice = base_invoice()
    invoice["subtotal"] = 30
    result = validate_invoice_data(invoice)
    assert not result["is_valid"]
    assert any("Subtotal mismatch" in e for e in result["errors"])


def test_total_mismatch():
    invoice = base_invoice()
    invoice["total"] = 24
    result = validate_invoice_data(invoice)
    assert not result["is_valid"]
    assert any("Total calculation mismatch" in e for e in result["errors"])


def test_discount_inconsistency():
    invoice = base_invoice()
    invoice["discount"] = 5
    invoice["discount_percentage"] = 10
    result = validate_invoice_data(invoice)
    assert not result["is_valid"]
    assert any("Discount inconsistency" in e for e in result["errors"])


def test_shipping_cost_and_tax_types():
    invoice = base_invoice()
    invoice["shipping_cost"] = "foo"
    invoice["tax"] = "bar"
    result = validate_invoice_data(invoice)
    assert not result["is_valid"]
    assert any("shipping_cost" in e and "type" in e for e in result["errors"])
    assert any("tax" in e and "type" in e for e in result["errors"])


def test_rounding_adjustment_type():
    invoice = base_invoice()
    invoice["rounding_adjustment"] = "baz"
    result = validate_invoice_data(invoice)
    assert not result["is_valid"]
    assert any("rounding_adjustment" in e and "type" in e for e in result["errors"])
