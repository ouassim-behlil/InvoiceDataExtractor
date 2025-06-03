# Invoice Extractor

[![Documentation](https://github.com/ouassim-behlil/InvoiceDataExtractor/actions/workflows/documentation.yml/badge.svg)](https://ouassim-behlil.github.io/InvoiceDataExtractor)
[![Python Tests](https://github.com/ouassim-behlil/InvoiceDataExtractor/actions/workflows/python-tests.yml/badge.svg)](https://github.com/ouassim-behlil/InvoiceDataExtractor/actions/workflows/python-tests.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Python-based tool that uses Google's Gemini model to extract structured information from invoice images.

## Documentation

Full documentation is available at: [https://ouassim-behlil.github.io/InvoiceDataExtractor](https://ouassim-behlil.github.io/InvoiceDataExtractor)

## Overview

This project provides a robust solution for extracting data from invoice images and converting it into structured JSON format. It includes validation to ensure mathematical consistency and proper data types in the extracted information.

## Features

- Extract key invoice information including:
  - Invoice number and date
  - Supplier and client details
  - Line items with quantities and prices
  - Subtotals, taxes, and discounts
- Validate mathematical consistency of extracted values
- Strict type checking for numeric fields
- Comprehensive error reporting

## Prerequisites

- Python 3.7 or higher
- Google API key for Gemini model
- Required Python packages (see Installation section)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/ouassim-behlil/InvoiceDataExtractor.git
cd invoiceExtractor
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Create an `api_key.txt` file in the project root and add your Google API key:
```bash
echo "your-api-key-here" > api_key.txt
```

## Usage

### Basic Usage

1. Place your invoice images in the `invoices` directory.

2. Use the processor to extract information:

```python
from src._processor import Processor

# Initialize the processor with your API key
with open('api_key.txt', 'r') as f:
    api_key = f.read().strip()
processor = Processor(api_key)

# Extract information from an image
result = processor.extract_json_from_image('invoices/your_invoice.jpg')
```

### Data Validation

The project includes a comprehensive validation system (`invoice_checker.py`) that ensures:

- All required fields are present
- Numeric fields have correct data types
- Mathematical consistency across all calculations
- Valid ranges for percentage values
- String field constraints

## Output Format

The extracted data is returned in a structured JSON format:

```json
{
  "invoice_number": string or null,
  "invoice_date": string (YYYY-MM-DD) or null,
  "supplier": {
    "name": string or null,
    "address": string or null,
    "phone": string or null,
    "email": string or null
  },
  "client": {
    "name": string or null,
    "address": string or null,
    "phone": string or null,
    "email": string or null
  },
  "items": [
    {
      "description": string or null,
      "quantity": number or null,
      "unit_price": number or null,
      "total_price": number or null
    }
  ],
  "subtotal": number or null,
  "discount": number or null,
  "discount_percentage": number or null,
  "tax": number or null,
  "shipping_cost": number or null,
  "rounding_adjustment": number or null,
  "payment_terms": string or null,
  "currency": string or null,
  "total": number or null
}
```

## Validation Rules

- Invoice number, date, and total are required fields
- Supplier and client must have at least a name
- Items array must contain at least one item
- Each item must have description, quantity, unit_price, and total_price
- Quantity must be an integer
- Unit prices and totals must be numeric
- Discount percentage must be between 0 and 100
- All calculations must be mathematically consistent

## Error Handling

The validation process returns a result object:

```python
{
    "is_valid": boolean,
    "errors": list of string error messages,
    "total_errors": number
}
```

## Internal Process Flow

The invoice extraction process follows these steps:

1. **Image Upload**
   - Place invoice images in the `invoices` directory
   - Supported formats: JPG, PNG
   - Images should be clear and readable for optimal results

2. **OCR Processing**
   - The Google Gemini model processes the image
   - Text and layout information is extracted
   - Structure and relationships between elements are analyzed

3. **Data Extraction**
   - The processor applies a specialized prompt to extract structured data
   - Key fields are identified and mapped to JSON structure
   - Values are converted to appropriate data types
   - Relationships between items, totals, and calculations are preserved

4. **Validation**
   - All extracted data goes through rigorous validation:
     1. Field presence check for required information
     2. Data type validation for all fields
     3. Mathematical validation of calculations
     4. Business rule validation (e.g., quantity as integers)
     5. Consistency checks between related fields

5. **Result Generation**
   - Valid data is returned in structured JSON format
   - Any validation errors are collected and reported
   - Final output includes validation status and error count

### Error Handling Examples

Here are some common validation errors and their meanings:

```python
# Missing required field
{"is_valid": false, "errors": ["Missing required field: invoice_number"], "total_errors": 1}

# Invalid data type
{"is_valid": false, "errors": ["Field 'total' must be numeric"], "total_errors": 1}

# Mathematical inconsistency
{"is_valid": false, "errors": ["Total calculation mismatch: calculated total (105.00) ≠ given total (100.00)"], "total_errors": 1}

# Multiple errors
{"is_valid": false, "errors": [
    "Item 1: quantity must be an integer",
    "Subtotal mismatch: sum of line items (95.00) ≠ subtotal (90.00)"
], "total_errors": 2}
```

### Best Practices

1. **Image Quality**
   - Use high-resolution, clear images
   - Ensure good lighting and contrast
   - Avoid skewed or rotated images
   - Remove any obstructions or overlays

2. **Data Validation**
   - Always check the validation result before using the data
   - Handle all potential error cases in your code
   - Log validation errors for debugging
   - Consider implementing retry logic for failed extractions

3. **Performance**
   - Process images in batches when possible
   - Implement caching if processing the same image multiple times
   - Monitor API usage and rate limits
   - Consider implementing queue systems for large-scale processing

## Testing

Run the test suite to verify functionality:

```bash
pytest tests/
```

The test suite includes comprehensive tests for:
- Data type validation
- Mathematical consistency
- Required field presence
- Edge cases and error conditions

## Project Structure

```
invoiceExtractor/
├── src/
│   ├── _processor.py     # Main processing logic
│   └── utils/
│       └── invoice_checker.py  # Validation utilities
├── tests/
│   └── test_invoice_checker.py # Test suite
├── invoices/             # Directory for invoice images
├── api_key.txt          # API key storage
├── requirements.txt     # Project dependencies
└── README.md           # This file
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License.