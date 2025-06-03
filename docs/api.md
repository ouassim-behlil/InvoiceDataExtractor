# API Documentation

## Processor Class

The main class for processing invoice images.

### Constructor

```python
processor = Processor(api_key: str)
```

**Parameters:**
- `api_key` (str): Google Gemini API key

### Methods

#### extract_json_from_image

```python
def extract_json_from_image(image_path: str) -> Optional[Union[dict, str]]
```

Processes an invoice image and returns structured data.

**Parameters:**
- `image_path` (str): Path to the invoice image file

**Returns:**
- `dict`: Parsed JSON data if successful
- `str`: Raw JSON string if parsing fails
- `None`: If no JSON block was detected

**Example:**
```python
result = processor.extract_json_from_image('invoices/invoice.jpg')
if isinstance(result, dict):
    print(f"Invoice number: {result.get('invoice_number')}")
```

## Invoice Validation

### validate_invoice_data

```python
from src.utils.invoice_checker import validate_invoice_data

result = validate_invoice_data(invoice_data: Dict[str, Any]) -> Dict[str, Any]
```

Validates the mathematical consistency and data types of invoice data.

**Parameters:**
- `invoice_data` (dict): Invoice data in JSON format

**Returns:**
Dictionary with:
- `is_valid` (bool): Validation result
- `errors` (list): List of error messages
- `total_errors` (int): Number of errors

**Example:**
```python
validation = validate_invoice_data(invoice_data)
if not validation['is_valid']:
    print(f"Found {validation['total_errors']} errors:")
    for error in validation['errors']:
        print(f"- {error}")
```

## Data Structures

### Invoice JSON Structure

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
  "total": number or null
  // ... other fields ...
}
```

## Error Handling

The validation system returns detailed error messages for:
- Missing required fields
- Invalid data types
- Mathematical inconsistencies
- Business rule violations

See [Error Examples](examples.md#error-handling) for common scenarios.
