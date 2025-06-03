# Troubleshooting Guide

This guide covers common issues and their solutions when using the Invoice Extractor.

## Common Issues

### 1. API Authentication Errors

**Symptoms:**
- "Invalid API key" error
- Authentication failures
- Connection errors to Google Gemini API

**Solutions:**
1. Verify your API key is correctly stored in `api_key.txt`
2. Ensure no whitespace or newlines in the API key
3. Check if your API key has expired
4. Verify your internet connection

### 2. Image Processing Failures

**Symptoms:**
- No JSON output
- Invalid or incomplete extraction results
- OCR errors

**Solutions:**

1. **Image Quality Issues**
   - Ensure image is clear and well-lit
   - Check image resolution (recommended: at least 300 DPI)
   - Verify file format (supported: JPG, PNG)
   - Remove any watermarks or overlays

2. **File Format Problems**
   ```python
   from PIL import Image
   
   def check_image(image_path):
       try:
           with Image.open(image_path) as img:
               print(f"Format: {img.format}")
               print(f"Size: {img.size}")
               print(f"Mode: {img.mode}")
       except Exception as e:
           print(f"Error: {str(e)}")
   ```

3. **Optimization Tips**
   - Convert images to RGB mode
   - Resize large images
   - Improve contrast if needed

### 3. Validation Errors

**Symptoms:**
- `is_valid: false` in validation results
- Mathematical inconsistencies
- Missing required fields

**Solutions:**

1. **Check Required Fields**
   - Invoice number
   - Invoice date
   - Total amount
   - Supplier name
   - Client name

2. **Mathematical Validation**
   - Verify line item calculations
   - Check subtotal computation
   - Validate tax and discount calculations

3. **Data Type Issues**
   - Ensure numeric fields contain numbers
   - Verify date format (YYYY-MM-DD)
   - Check quantity fields are integers

### 4. Performance Issues

**Symptoms:**
- Slow processing times
- Memory errors
- Timeouts

**Solutions:**

1. **Optimize Batch Processing**
   ```python
   def optimize_image_batch(directory):
       for filename in os.listdir(directory):
           if filename.endswith(('.jpg', '.png')):
               filepath = os.path.join(directory, filename)
               # Check file size
               if os.path.getsize(filepath) > 5_000_000:  # 5MB
                   optimize_image(filepath)
   ```

2. **Memory Management**
   - Process large batches in chunks
   - Implement proper cleanup
   - Monitor memory usage

3. **Connection Handling**
   - Implement retry logic
   - Add timeouts
   - Handle network errors

## Debugging Tips

### 1. Enable Detailed Logging

```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('debug.log'),
        logging.StreamHandler()
    ]
)
```

### 2. Validation Debugging

```python
def debug_validation(invoice_data):
    validation = validate_invoice_data(invoice_data)
    if not validation["is_valid"]:
        print("=== Validation Debug ===")
        print("Required Fields:")
        for field in ["invoice_number", "invoice_date", "total"]:
            print(f"{field}: {invoice_data.get(field)}")
        
        print("\nCalculations:")
        if "items" in invoice_data:
            total = sum(item.get("total_price", 0) for item in invoice_data["items"])
            print(f"Calculated total: {total}")
            print(f"Given total: {invoice_data.get('total')}")
```

### 3. Image Processing Debug

```python
def debug_image_processing(image_path):
    try:
        # Check image properties
        check_image(image_path)
        
        # Try processing with debug info
        result = processor.extract_json_from_image(image_path)
        
        # Analyze result
        if isinstance(result, dict):
            print("Extraction successful")
            print(f"Fields extracted: {list(result.keys())}")
            print(f"Total fields: {len(result)}")
        else:
            print("Extraction failed")
            print(f"Result type: {type(result)}")
            
    except Exception as e:
        print(f"Processing error: {str(e)}")
```

## When to Contact Support

Contact support if:
1. You've tried all relevant troubleshooting steps
2. The error is consistent and reproducible
3. You suspect it's a bug in the library

Provide the following information:
- Error messages and stack traces
- Sample invoice (with sensitive information removed)
- Steps to reproduce
- Environment details (Python version, OS, etc.)
