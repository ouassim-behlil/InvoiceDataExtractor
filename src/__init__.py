# src/__init__.py
"""
Invoice Processor Package

A Python package for processing invoice images using Google Gemini AI.
Extracts structured data from invoice images and saves results in JSON format.
"""

from .invoice_processor import InvoiceProcessor, InvoiceProcessorError
from .models import InvoiceData, InvoiceItem, Supplier, Client
from .utils import FileHandler, Validators, ValidationError

__version__ = "1.0.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

# Main exports
__all__ = [
    # Main processor
    "InvoiceProcessor",
    "InvoiceProcessorError",
    
    # Data models
    "InvoiceData",
    "InvoiceItem", 
    "Supplier",
    "Client",
    
    # Utilities
    "FileHandler",
    "Validators",
    "ValidationError",
]

# Package metadata
PACKAGE_NAME = "invoice-processor"
DESCRIPTION = "AI-powered invoice processing using Google Gemini"
SUPPORTED_FORMATS = [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff"]
MAX_FILE_SIZE_MB = 50