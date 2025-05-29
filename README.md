# Invoice Processor

A simple Python tool to extract structured JSON data from invoice images using Google Gemini.

## Features

* Uploads invoice images (`.jpg`, `.jpeg`, `.png`)
* Extracts key fields (number, date, supplier, client, items, totals)
* Saves cleaned JSON files
* Rounds numeric values to 2 decimals

## Prerequisites

* Python 3.8+
* Google Gemini API key
* Install dependencies:

```bash
pip install google-genai
```

## Project Structure

```
invoice_processor.py         # Main processor class
src/
  models/
    invoice_data.py         # Invoice data model
  utils/
    file_handler.py         # JSON & text saving utilities
    validators.py           # Input validations
invoices/                   # Place your invoice images here
json_outputs/               # JSON outputs will appear here
```

## Usage

1. **Set API key**

   ```bash
   export GEMINI_API_KEY="your_api_key_here"
   ```

2. **Run the processor**

   ```python
   from invoice_processor import InvoiceProcessor, InvoiceProcessorConfig
   import os

   config = InvoiceProcessorConfig(
       api_key=os.getenv("GEMINI_API_KEY"),
       image_dir="invoices",
       output_dir="json_outputs"
   )
   processor = InvoiceProcessor(config)
   processor.process_all_images()
   ```

3. **Check console** — you’ll see messages like:

   ```
   📄 Processing: invoice1.png
   ✅ JSON saved: invoice1.json
   ```

4. **Review output** — JSON files are in `json_outputs/`.

---

Keep it simple and direct—just drop your images and let the processor handle the rest!
