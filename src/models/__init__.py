# src/models/__init__.py
"""
Data Models Module

Contains all data structures used for representing invoice information.
"""

from .invoice_data import InvoiceData, InvoiceItem, Supplier, Client

__all__ = [
    "InvoiceData",
    "InvoiceItem", 
    "Supplier",
    "Client",
]

# Model version for compatibility tracking
MODEL_VERSION = "1.0.0"

# Default field values
DEFAULT_CURRENCY = "USD"
DEFAULT_PAYMENT_TERMS = "Net 30"