# tests/models/test_invoice_data.py
import pytest
from src.models.invoice_data import Supplier, Client, InvoiceItem, InvoiceData
import json


def test_supplier_initialization():
    """Test Supplier class initialization and default values"""
    supplier = Supplier()
    assert supplier.name is None
    assert supplier.address is None
    assert supplier.phone is None
    assert supplier.email is None


def test_supplier_to_dict():
    """Test Supplier to_dict method"""
    supplier = Supplier(
        name="Test Supplier",
        address="123 Supplier St",
        phone="123-456-7890",
        email="supplier@example.com",
    )
    result = supplier.to_dict()
    assert result == {
        "name": "Test Supplier",
        "address": "123 Supplier St",
        "phone": "123-456-7890",
        "email": "supplier@example.com",
    }


def test_client_initialization():
    """Test Client class initialization and default values"""
    client = Client()
    assert client.name is None
    assert client.address is None
    assert client.phone is None
    assert client.email is None


def test_client_to_dict():
    """Test Client to_dict method"""
    client = Client(
        name="Test Client",
        address="456 Client Ave",
        phone="987-654-3210",
        email="client@example.com",
    )
    result = client.to_dict()
    assert result == {
        "name": "Test Client",
        "address": "456 Client Ave",
        "phone": "987-654-3210",
        "email": "client@example.com",
    }


def test_invoice_item_initialization():
    """Test InvoiceItem class initialization and default values"""
    item = InvoiceItem()
    assert item.description is None
    assert item.quantity is None
    assert item.unit_price is None
    assert item.total_price is None


def test_invoice_item_to_dict():
    """Test InvoiceItem to_dict method"""
    item = InvoiceItem(
        description="Test Item", quantity=2, unit_price=10.50, total_price=21.00
    )
    result = item.to_dict()
    assert result == {
        "description": "Test Item",
        "quantity": 2,
        "unit_price": 10.50,
        "total_price": 21.00,
    }


def test_invoice_data_initialization():
    """Test InvoiceData class initialization and default values"""
    invoice = InvoiceData()
    assert invoice.invoice_number is None
    assert invoice.invoice_date is None
    assert isinstance(invoice.supplier, Supplier)
    assert isinstance(invoice.client, Client)
    assert invoice.items == []
    assert invoice.subtotal is None
    assert invoice.discount is None
    assert invoice.discount_percentage is None
    assert invoice.tax is None
    assert invoice.shipping_cost is None
    assert invoice.rounding_adjustment is None
    assert invoice.payment_terms is None
    assert invoice.currency is None
    assert invoice.total is None


def test_invoice_data_to_dict():
    """Test InvoiceData to_dict method"""
    supplier = Supplier(name="Test Supplier")
    client = Client(name="Test Client")
    items = [InvoiceItem(description="Test Item")]

    invoice = InvoiceData(
        invoice_number="INV-001",
        invoice_date="2023-01-01",
        supplier=supplier,
        client=client,
        items=items,
        subtotal=100.00,
        discount=10.00,
        discount_percentage=10.0,
        tax=9.00,
        shipping_cost=5.00,
        rounding_adjustment=-0.50,
        payment_terms="Net 30",
        currency="USD",
        total=103.50,
    )

    result = invoice.to_dict()
    assert result == {
        "invoice_number": "INV-001",
        "invoice_date": "2023-01-01",
        "supplier": {
            "name": "Test Supplier",
            "address": None,
            "phone": None,
            "email": None,
        },
        "client": {
            "name": "Test Client",
            "address": None,
            "phone": None,
            "email": None,
        },
        "items": [
            {
                "description": "Test Item",
                "quantity": None,
                "unit_price": None,
                "total_price": None,
            }
        ],
        "subtotal": 100.00,
        "discount": 10.00,
        "discount_percentage": 10.0,
        "tax": 9.00,
        "shipping_cost": 5.00,
        "rounding_adjustment": -0.50,
        "payment_terms": "Net 30",
        "currency": "USD",
        "total": 103.50,
    }


def test_invoice_data_to_json():
    """Test InvoiceData to_json method"""
    invoice = InvoiceData(invoice_number="INV-001")
    json_str = invoice.to_json()
    data = json.loads(json_str)
    assert data["invoice_number"] == "INV-001"
    assert isinstance(json_str, str)


def test_invoice_data_from_dict():
    """Test InvoiceData from_dict classmethod"""
    data = {
        "invoice_number": "INV-002",
        "invoice_date": "2023-02-01",
        "supplier": {"name": "Another Supplier", "email": "another@example.com"},
        "client": {"name": "Another Client"},
        "items": [
            {"description": "Item 1", "quantity": 1, "unit_price": 50.00},
            {"description": "Item 2", "quantity": 2, "unit_price": 25.00},
        ],
        "subtotal": 100.00,
        "total": 100.00,
    }

    invoice = InvoiceData.from_dict(data)
    assert invoice.invoice_number == "INV-002"
    assert invoice.supplier.name == "Another Supplier"
    assert invoice.supplier.email == "another@example.com"
    assert invoice.client.name == "Another Client"
    assert len(invoice.items) == 2
    assert invoice.items[0].description == "Item 1"
    assert invoice.items[1].quantity == 2
    assert invoice.subtotal == 100.00
    assert invoice.total == 100.00


def test_invoice_data_with_empty_dict():
    """Test InvoiceData from_dict with empty dictionary"""
    invoice = InvoiceData.from_dict({})
    assert invoice.invoice_number is None
    assert isinstance(invoice.supplier, Supplier)
    assert isinstance(invoice.client, Client)
    assert invoice.items == []


def test_invoice_data_with_partial_data():
    """Test InvoiceData with partial data"""
    invoice = InvoiceData(
        invoice_number="INV-003", supplier=Supplier(name="Partial Supplier")
    )
    assert invoice.invoice_number == "INV-003"
    assert invoice.supplier.name == "Partial Supplier"
    assert invoice.supplier.address is None
    assert invoice.client.name is None
    assert invoice.items == []
    assert invoice.total is None
