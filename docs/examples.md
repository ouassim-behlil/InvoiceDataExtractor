# Examples

This document provides practical examples of using the Invoice Extractor.

## Basic Usage

### Processing a Single Invoice

```python
from src._processor import Processor

# Initialize
with open('api_key.txt', 'r') as f:
    api_key = f.read().strip()
processor = Processor(api_key)

# Process invoice
result = processor.extract_json_from_image('invoices/sample.jpg')

# Check results
if isinstance(result, dict):
    print(f"Invoice Number: {result.get('invoice_number')}")
    print(f"Total Amount: {result.get('total')}")
else:
    print("Failed to process invoice")
```

### Processing Multiple Invoices

```python
import os
from src._processor import Processor

def process_invoice_batch(directory):
    # Initialize processor
    with open('api_key.txt', 'r') as f:
        api_key = f.read().strip()
    processor = Processor(api_key)
    
    results = []
    errors = []
    
    # Process each invoice
    for filename in os.listdir(directory):
        if filename.endswith(('.jpg', '.png')):
            try:
                filepath = os.path.join(directory, filename)
                result = processor.extract_json_from_image(filepath)
                if isinstance(result, dict):
                    results.append(result)
                else:
                    errors.append(f"Failed to process {filename}")
            except Exception as e:
                errors.append(f"Error processing {filename}: {str(e)}")
    
    return results, errors

# Usage
results, errors = process_invoice_batch('invoices')
print(f"Processed {len(results)} invoices successfully")
print(f"Found {len(errors)} errors")
```

## Validation Examples

### Basic Validation

```python
from src.utils.invoice_checker import validate_invoice_data

invoice_data = {
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

result = validate_invoice_data(invoice_data)
if result["is_valid"]:
    print("Invoice data is valid")
else:
    print("Validation errors:")
    for error in result["errors"]:
        print(f"- {error}")
```

### Error Handling Examples

1. **Missing Required Field**
```python
invalid_invoice = {
    # Missing invoice_number
    "invoice_date": "2024-06-01",
    "total": 100
}
```

2. **Invalid Data Type**
```python
invalid_invoice = {
    "invoice_number": "INV-001",
    "total": "100",  # Should be numeric
}
```

3. **Mathematical Inconsistency**
```python
invalid_invoice = {
    "invoice_number": "INV-001",
    "items": [
        {"quantity": 2, "unit_price": 10, "total_price": 25}  # 2 * 10 ≠ 25
    ],
    "total": 25
}
```

## Best Practices

### Image Preparation
```python
from PIL import Image

def prepare_image(image_path):
    """Optimize image for processing"""
    with Image.open(image_path) as img:
        # Convert to RGB if needed
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Resize if too large
        max_size = 2000
        if max(img.size) > max_size:
            ratio = max_size / max(img.size)
            new_size = tuple(int(dim * ratio) for dim in img.size)
            img = img.resize(new_size, Image.LANCZOS)
        
        # Save optimized image
        output_path = f"optimized_{os.path.basename(image_path)}"
        img.save(output_path, quality=85, optimize=True)
        return output_path

# Usage
optimized_path = prepare_image('invoices/large_invoice.jpg')
result = processor.extract_json_from_image(optimized_path)
```

### Error Logging
```python
import logging

logging.basicConfig(
    filename='invoice_processing.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def process_with_logging(image_path):
    try:
        result = processor.extract_json_from_image(image_path)
        if isinstance(result, dict):
            logging.info(f"Successfully processed {image_path}")
            validation = validate_invoice_data(result)
            if not validation["is_valid"]:
                logging.warning(f"Validation errors in {image_path}: {validation['errors']}")
        else:
            logging.error(f"Failed to process {image_path}")
    except Exception as e:
        logging.error(f"Error processing {image_path}: {str(e)}")
        raise
```

## Common Patterns

### Batch Processing with Progress
```python
from tqdm import tqdm
import concurrent.futures

def process_batch_with_progress(directory, max_workers=4):
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        files = [f for f in os.listdir(directory) if f.endswith(('.jpg', '.png'))]
        futures = {executor.submit(processor.extract_json_from_image, 
                                 os.path.join(directory, f)): f 
                  for f in files}
        
        results = {}
        for future in tqdm(concurrent.futures.as_completed(futures), 
                          total=len(files),
                          desc="Processing invoices"):
            filename = futures[future]
            try:
                results[filename] = future.result()
            except Exception as e:
                results[filename] = f"Error: {str(e)}"
    
    return results
```
