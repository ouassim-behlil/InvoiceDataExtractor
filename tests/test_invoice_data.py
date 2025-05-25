import pytest
from src.models.invoice_data import InvoiceData, Supplier, Client, InvoiceItem

def test_invoice_to_dict_and_json():
    invoice = InvoiceData(
        invoice_number="INV123",
        invoice_date="2024-01-01",
        supplier=Supplier(name="Supplier Inc"),
        client=Client(name="Client LLC"),
        items=[InvoiceItem(description="Item A", quantity=2, unit_price=100.0, total_price=200.0)],
        subtotal=200.0,
        total=200.0
    )
    invoice_dict = invoice.to_dict()
    assert invoice_dict["invoice_number"] == "INV123"
    assert invoice_dict["supplier"]["name"] == "Supplier Inc"
    assert invoice_dict["items"][0]["description"] == "Item A"

    invoice_json = invoice.to_json()
    assert isinstance(invoice_json, str)

def test_invoice_from_dict():
    data = {
        "invoice_number": "INV999",
        "invoice_date": "2023-12-12",
        "supplier": {"name": "My Supplier"},
        "client": {"name": "My Client"},
        "items": [{"description": "Service", "quantity": 1, "unit_price": 100, "total_price": 100}],
        "subtotal": 100,
        "total": 100
    }
    invoice = InvoiceData.from_dict(data)
    assert invoice.invoice_number == "INV999"
    assert invoice.items[0].description == "Service"
