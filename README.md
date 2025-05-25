# 🧾 Invoice Utility System

A modular Python package for handling invoice data structures, file I/O, and validation utilities. Designed for extensibility and integration with OCR or document analysis pipelines.


## 📦 Features

### 🔹 Models (`src/models/invoice_data.py`)
- Dataclasses for `Supplier`, `Client`, `InvoiceItem`, and `InvoiceData`
- Convert invoice data to dictionary and JSON
- Instantiate invoices from raw dictionary data

### 🔹 Utilities (`src/utils/file_handler.py`)
- Save data to JSON or plain text files
- Recursively round numeric values to two decimal places
- Fetch and validate image files from a directory

### 🔹 Validators (`src/utils/validators.py`)
- Validate:
  - Google API keys
  - Image files (type, size, readability)
  - Directory existence and permissions
  - Safe filenames (sanitization)




## 🧪 Running Tests

We use [`pytest`](https://pytest.org) for unit testing.

### ▶️ Locally

1. Install dependencies:

```bash
pip install -r requirements.txt
````

2. Run all tests:

```bash
pytest
```

### 🤖 Automatically on GitHub

This project includes GitHub Actions CI to run tests on every push and pull request. The workflow is defined in:

```
.github/workflows/python-tests.yml
```

To enable it:

* Push the project to GitHub
* Go to the **Actions** tab to monitor test results


## 📥 Installation

```bash
git clone https://github.com/your-username/invoice-utility.git
cd invoice-utility
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
* `pytest` for testing


## 📄 License

MIT License — see [`LICENSE`](LICENSE) file for details.
