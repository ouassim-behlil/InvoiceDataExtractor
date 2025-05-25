# Invoice Utility System

A modular Python package for handling invoice data structures, file I/O, and validation utilities. Designed for extensibility and integration with OCR or document analysis pipelines.


## 📦 Features

### Models
- Dataclasses for `Supplier`, `Client`, `InvoiceItem`, and `InvoiceData`
- Convert invoice data to dictionary and JSON
- Instantiate invoices from raw dictionary data

### Utilities
- Save data to JSON or plain text files
- Recursively round numeric values to two decimal places
- Fetch and validate image files from a directory

### Validators
- Validate:
  - Google API keys
  - Image files (type, size, readability)
  - Directory existence and permissions
  - Safe filenames (sanitization)



## 📥 Installation

```bash
git clone https://github.com/ouassim-behlil/InvoiceDataExtractor.git
cd InvoiceDataExtractor
pip install -r requirements.txt
```


## ✨ Example Usage

```python
from src.models.invoice_data import InvoiceData

invoice = InvoiceData(invoice_number="INV001", subtotal=100.00, total=120.00)
print(invoice.to_json())
```

```python
from src.utils.file_handler import FileHandler

handler = FileHandler()
handler.save_json(invoice.to_dict(), "output/invoice.json")
```


## ✅ Requirements

* Python 3.8+


## 📄 License

MIT License — see [`LICENSE`](LICENSE) file for details.
