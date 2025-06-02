# Invoice Extractor & Validator

## Overview
This project provides an end-to-end workflow for extracting structured invoice data from images using Google Gemini AI, and validating the extracted data for logical and mathematical consistency. It features a modern Streamlit web app for easy interaction and visual comparison between the original invoice image and the extracted/validated data.

## Workflow
1. **User uploads an invoice image** via the Streamlit web interface.
2. **The image is sent to the Gemini AI model** (via the `Processor` class) which extracts relevant invoice fields and returns a structured JSON.
3. **The extracted data is displayed** as non-editable fields in the web app, grouped by logical sections (Invoice, Supplier, Client, Items, Summary).
4. **The extracted data is validated** using the `validate_invoice_data` function, which checks for missing fields, type errors, and mathematical consistency (e.g., totals, item calculations).
5. **Validation results are shown** side-by-side with the extracted data, highlighting any errors or confirming validity.
6. **The user can visually compare** the uploaded image and the extracted/validated data for accuracy and completeness.

## Detailed Process Explanation

### 1. Image Upload & Display
- The user provides their Google GenAI API key and uploads an invoice image (JPG/PNG).
- The image is saved temporarily and displayed in the app with zoom capability for easy review.

### 2. Extraction with Gemini AI
- The `Processor` class (in `src/_processor.py`) handles communication with the Gemini API:
  - It sends the image and a detailed prompt describing the required JSON structure.
  - The model returns a JSON string with all relevant invoice fields (invoice number, date, supplier/client info, items, totals, etc.).
  - The processor extracts and parses this JSON from the model's response.

### 3. Display of Extracted Data
- The extracted invoice data is shown as non-editable fields in the Streamlit app, grouped for clarity:
  - Invoice details (number, date)
  - Supplier and client info
  - Line items (description, quantity, unit price, total price)
  - Summary fields (subtotal, discount, tax, shipping, total, etc.)
- This allows the user to quickly review the structured data.

### 4. Validation of Extracted Data
- The `validate_invoice_data` function (in `src/utils/invoice_checker.py`) performs comprehensive checks:
  - Ensures all required fields are present and not empty.
  - Checks that numeric fields are of the correct type (e.g., quantity is integer, totals are decimal).
  - Validates the structure of supplier, client, and items.
  - Checks mathematical consistency (e.g., subtotal matches sum of items, total matches calculation with discounts/tax/shipping, item totals are correct).
  - Reports all errors found, or confirms validity if all checks pass.

### 5. Validation Results Display
- Validation results are shown next to the extracted data in the app:
  - If valid, a success message is shown.
  - If errors are found, each error is listed for the user to review and correct as needed.

### 6. Clean-up
- The temporary image file is deleted after processing to keep the workspace clean.

## How to Run
1. Install requirements:
   ```sh
   pip install -r requirements.txt
   ```
2. Start the Streamlit app:
   ```sh
   streamlit run app.py
   ```
3. Enter your Google GenAI API key and upload an invoice image.
4. Review the extracted and validated data side-by-side with the original image.

## File Structure
- `app.py` — Streamlit web app for user interaction.
- `src/_processor.py` — Handles AI extraction from images.
- `src/utils/invoice_checker.py` — Validates extracted invoice data.
- `tests/` — Pytest-based tests for validation logic.
- `requirements.txt` — Python dependencies.

## Notes
- The app is designed for accuracy, clarity, and ease of use.
- All validation logic is robust and thoroughly tested.
- The UI is modern, responsive, and supports easy visual comparison.

---
For any issues or contributions, please open an issue or pull request.
