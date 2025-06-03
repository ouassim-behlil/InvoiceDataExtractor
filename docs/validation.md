# Validation Guide

This guide explains the validation system used in the Invoice Extractor project.

## Overview

The validation system ensures:
1. Data integrity
2. Mathematical consistency
3. Required field presence
4. Proper data types
5. Business rule compliance

## Validation Rules

### Required Fields

```python
required_fields = [
    "invoice_number",
    "invoice_date",
    "total"
]
```

These fields must be present and non-empty in every invoice.

### Data Types

| Field | Required Type | Notes |
|-------|--------------|-------|
| invoice_number | string | Non-empty |
| invoice_date | string | YYYY-MM-DD format |
| total | number | Positive value |
| quantity | integer | Positive value |
| unit_price | number | Positive value |
| subtotal | number | Positive value |
| discount_percentage | number | 0-100 range |

### Mathematical Validations

1. **Line Item Calculations**
   ```python
   item_total = quantity * unit_price
   ```

2. **Subtotal Calculation**
   ```python
   subtotal = sum(item["total_price"] for item in items)
   ```

3. **Total Calculation**
   ```python
   total = subtotal
   if discount:
       total -= discount
   if tax:
       total += tax
   if shipping_cost:
       total += shipping_cost
   if rounding_adjustment:
       total += rounding_adjustment
   ```

### Business Rules

1. **Quantity Rules**
   - Must be positive integer
   - No fractional quantities allowed

2. **Price Rules**
   - All prices must be positive
   - Minimum unit price: 0.001

3. **Discount Rules**
   - Percentage must be between 0-100
   - Amount must not exceed subtotal

4. **Client/Supplier Rules**
   - Must have at least a name
   - Email must be valid format if present

## Validation Process

The validation occurs in multiple stages:

1. **Field Presence Check**
   ```python
   def check_required_fields(invoice_data):
       missing = []
       for field in required_fields:
           if field not in invoice_data or invoice_data[field] is None:
               missing.append(field)
       return missing
   ```

2. **Type Validation**
   ```python
   def validate_types(invoice_data):
       errors = []
       if not isinstance(invoice_data.get("total"), (int, float)):
           errors.append("Total must be numeric")
       # ... more type checks ...
       return errors
   ```

3. **Mathematical Validation**
   ```python
   def validate_calculations(invoice_data):
       errors = []
       # Check line items
       for item in invoice_data.get("items", []):
           expected = item["quantity"] * item["unit_price"]
           if item["total_price"] != expected:
               errors.append(f"Line item total mismatch")
       # ... more calculation checks ...
       return errors
   ```

## Error Messages

The validation system provides detailed error messages:

```python
{
    "is_valid": false,
    "errors": [
        "Missing required field: invoice_number",
        "Field 'total' must be numeric",
        "Item 1: quantity must be an integer",
        "Subtotal mismatch: sum of line items (95.00) ≠ subtotal (90.00)"
    ],
    "total_errors": 4
}
```

## Best Practices

### 1. Pre-validation Checks

```python
def pre_validate(data):
    if not isinstance(data, dict):
        return False, ["Input must be a dictionary"]
    if "items" in data and not isinstance(data["items"], list):
        return False, ["Items must be an array"]
    return True, []
```

### 2. Custom Validation Rules

```python
def add_custom_validation(invoice_data, rules):
    errors = []
    for rule in rules:
        result = rule(invoice_data)
        if not result["valid"]:
            errors.append(result["error"])
    return errors
```

### 3. Validation Helpers

```python
def validate_email(email):
    import re
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

def validate_date_format(date_str):
    from datetime import datetime
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False
```

## Examples

### Basic Validation

```python
from src.utils.invoice_checker import validate_invoice_data

# Valid invoice
valid_invoice = {
    "invoice_number": "INV-001",
    "invoice_date": "2024-06-01",
    "supplier": {"name": "Supplier Inc."},
    "client": {"name": "Client LLC"},
    "items": [
        {
            "description": "Item 1",
            "quantity": 2,
            "unit_price": 10,
            "total_price": 20
        }
    ],
    "subtotal": 20,
    "total": 20
}

result = validate_invoice_data(valid_invoice)
print(f"Valid invoice check: {result['is_valid']}")
```

### Common Validation Errors

```python
# Missing required field
invalid_invoice = {
    "invoice_date": "2024-06-01",
    # Missing invoice_number
    "total": 100
}

# Invalid data type
invalid_invoice = {
    "invoice_number": "INV-001",
    "total": "100"  # Should be numeric
}

# Mathematical inconsistency
invalid_invoice = {
    "invoice_number": "INV-001",
    "items": [
        {"quantity": 2, "unit_price": 10, "total_price": 25}  # 2 * 10 ≠ 25
    ],
    "total": 25
}
```

## Handling Validation Results

```python
def process_validation_result(validation_result):
    if validation_result["is_valid"]:
        return True
    
    # Group errors by type
    error_types = {
        "missing": [],
        "type": [],
        "calculation": [],
        "other": []
    }
    
    for error in validation_result["errors"]:
        if "Missing required field" in error:
            error_types["missing"].append(error)
        elif "must be" in error:
            error_types["type"].append(error)
        elif "mismatch" in error:
            error_types["calculation"].append(error)
        else:
            error_types["other"].append(error)
    
    # Handle each error type appropriately
    if error_types["missing"]:
        print("Missing Fields:", error_types["missing"])
    if error_types["type"]:
        print("Type Errors:", error_types["type"])
    if error_types["calculation"]:
        print("Calculation Errors:", error_types["calculation"])
    if error_types["other"]:
        print("Other Errors:", error_types["other"])
    
    return False
```
