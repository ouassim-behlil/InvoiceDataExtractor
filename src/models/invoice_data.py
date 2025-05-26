# src/models/invoice_data.py
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
import json


@dataclass
class Supplier:
    """Supplier information"""

    name: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "address": self.address,
            "phone": self.phone,
            "email": self.email,
        }


@dataclass
class Client:
    """Client information"""

    name: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "address": self.address,
            "phone": self.phone,
            "email": self.email,
        }


@dataclass
class InvoiceItem:
    """Individual invoice item"""

    description: Optional[str] = None
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    total_price: Optional[float] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "description": self.description,
            "quantity": self.quantity,
            "unit_price": self.unit_price,
            "total_price": self.total_price,
        }


@dataclass
class InvoiceData:
    """Complete invoice data structure"""

    invoice_number: Optional[str] = None
    invoice_date: Optional[str] = None
    supplier: Supplier = field(default_factory=Supplier)
    client: Client = field(default_factory=Client)
    items: List[InvoiceItem] = field(default_factory=list)
    subtotal: Optional[float] = None
    discount: Optional[float] = None
    discount_percentage: Optional[float] = None
    tax: Optional[float] = None
    shipping_cost: Optional[float] = None
    rounding_adjustment: Optional[float] = None
    payment_terms: Optional[str] = None
    currency: Optional[str] = None
    total: Optional[float] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format"""
        return {
            "invoice_number": self.invoice_number,
            "invoice_date": self.invoice_date,
            "supplier": self.supplier.to_dict(),
            "client": self.client.to_dict(),
            "items": [item.to_dict() for item in self.items],
            "subtotal": self.subtotal,
            "discount": self.discount,
            "discount_percentage": self.discount_percentage,
            "tax": self.tax,
            "shipping_cost": self.shipping_cost,
            "rounding_adjustment": self.rounding_adjustment,
            "payment_terms": self.payment_terms,
            "currency": self.currency,
            "total": self.total,
        }

    def to_json(self, indent: int = 2) -> str:
        """Convert to JSON string"""
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "InvoiceData":
        """Create InvoiceData from dictionary"""
        supplier = Supplier(**data.get("supplier", {}))
        client = Client(**data.get("client", {}))
        items = [InvoiceItem(**item) for item in data.get("items", [])]

        return cls(
            invoice_number=data.get("invoice_number"),
            invoice_date=data.get("invoice_date"),
            supplier=supplier,
            client=client,
            items=items,
            subtotal=data.get("subtotal"),
            discount=data.get("discount"),
            discount_percentage=data.get("discount_percentage"),
            tax=data.get("tax"),
            shipping_cost=data.get("shipping_cost"),
            rounding_adjustment=data.get("rounding_adjustment"),
            payment_terms=data.get("payment_terms"),
            currency=data.get("currency"),
            total=data.get("total"),
        )
