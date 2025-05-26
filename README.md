# 🧾 Invoice Extraction System
![Tests](https://github.com/ouassim-behlil/InvoiceDataExtractor/actions/workflows/python-tests.yml/badge.svg)
<!-- ![Tests](https://github.com/<user>/<repo>/actions/workflows/<workflow>.yml/badge.svg) -->


A Python tool to extract structured invoice data (JSON) from image files using Google Gemini AI.


## 🚀 Usage

```python
from invoice_runner import InvoiceProcessor, InvoiceProcessorConfig

config = InvoiceProcessorConfig(
    api_key="your-google-api-key",
    image_dir="invoices",
    output_dir="json_outputs"
)

processor = InvoiceProcessor(config)
processor.process_all_images()  # or processor.process_image("invoice1.jpg")
````


Install dependencies:

```bash
pip install -r requirements.txt
```


## 📁 Output

Each invoice image is saved as `.json` in the output folder.


✅ Clean, simple, and ready to plug into your invoice automation workflow.
