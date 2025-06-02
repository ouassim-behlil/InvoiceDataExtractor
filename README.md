# Invoice Extractor & Validator

## Overview
This project provides a complete workflow for extracting structured data from invoice images using Google Gemini AI, and validating the extracted data for correctness. The solution includes a modern Streamlit web app for user interaction, robust backend validation, and automated tests.

---

## Workflow Summary
1. **User uploads an invoice image** via the web interface.
2. **Image is processed by Gemini AI** to extract invoice fields as JSON.
3. **Extracted data is displayed** as non-editable fields for easy review.
4. **Validation logic checks** the extracted data for completeness, type correctness, and mathematical consistency.
5. **Validation results are shown** alongside the extracted data.
6. **Temporary files are cleaned up** after processing.

---

## Detailed Process Explanation

### 1. Image Upload & Display
- The user provides their Google GenAI API key and uploads an invoice image (JPG/PNG).
- The image is saved temporarily and displayed in the app with zoom capability for easy review.

### 2. Extraction with Gemini AI
- The `Processor` class (in `src/_processor.py`) handles communication with the Gemini API:
  - It sends the image and a detailed prompt describing the required JSON structure.
  - The model returns a JSON string with all relevant invoice fields (invoice number, date, supplier/client info, items, totals, etc.).
  - The processor extracts and parses this JSON from the model's response.

#### _Processor Class Details_
- **Initialization:** Requires a valid API key to create a Gemini client.
- **Prompt:** The prompt instructs the model to return a strict JSON structure, using `null` for missing values.
- **Image Upload:** The image is uploaded to the Gemini API, and the model is invoked with the image and prompt.
- **JSON Extraction:** The response is parsed to extract the JSON block, which is then loaded as a Python dictionary (or returned as a string if parsing fails).

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

#### _Validation Logic Details_
- **Type Checking:** Ensures fields like `total`, `subtotal`, `tax`, etc. are numeric, and `quantity` is an integer.
- **Required Fields:** Checks for presence and non-emptiness of all required fields (invoice number, date, supplier/client info, items, totals).
- **Structure Validation:** Ensures supplier and client are objects, items is a list, and each item has required fields.
- **Mathematical Consistency:**
  - Each item's `total_price` must equal `quantity * unit_price`.
  - `subtotal` must equal the sum of all item `total_price` values.
  - `total` must match the sum of subtotal, tax, shipping, discounts, and rounding adjustments.
  - Discount amount and percentage must be consistent if both are present.
- **Error Reporting:** All validation errors are collected and returned for display.

### 5. Validation Results Display
- Validation results are shown next to the extracted data in the app:
  - If valid, a success message is shown.
  - If errors are found, each error is listed for the user to review and correct as needed.

### 6. Clean-up
- The temporary image file is deleted after processing to keep the workspace clean.

---

## File Structure
- `src/_processor.py` — Handles AI extraction from images.
- `src/utils/invoice_checker.py` — Validates extracted invoice data.
- `tests/` — Pytest-based tests for validation logic.
- `requirements.txt` — Python dependencies.
- `.gitignore` — Excludes app.py and other non-source files from version control.

---

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

---

## Notes
- The app is designed for accuracy, clarity, and ease of use.
- All validation logic is robust and thoroughly tested.
- The UI is modern, responsive, and supports easy visual comparison.

For any issues or contributions, please open an issue or pull request.
