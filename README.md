# Invoice Processor

An AI-powered invoice processing system using Google Gemini AI to extract structured data from invoice images.

## Features

- 🤖 **AI-Powered Extraction**: Uses Google Gemini AI for intelligent invoice data extraction
- 🔒 **Security First**: Built-in validation and security checks for file handling
- 📁 **Batch Processing**: Process single images or entire directories
- 🏗️ **Object-Oriented Design**: Clean, modular, and extensible codebase
- ✅ **Comprehensive Testing**: Full unit test coverage
- 🛡️ **Error Handling**: Robust error handling and logging
- 📊 **Structured Output**: Clean JSON output with standardized invoice data structure

## Installation

### From Source

```bash
git clone https://github.com/yourusername/invoice-processor.git
cd invoice-processor
pip install -e .
```

### For Development

```bash
git clone https://github.com/yourusername/invoice-processor.git
cd invoice-processor
pip install -e ".[dev]"
```

## Quick Start

### 1. Set up your API key

Get your Google Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey).

#### Option A: Environment Variable
```bash
export GEMINI_API_KEY="your-api-key-here"
```

#### Option B: .env File
Create a `.env` file in your project root:
```
GEMINI_API_KEY=your-api-key-here
```

### 2. Process invoices

#### Single Image
```bash
# Process single image and save to JSON
invoice-processor single invoice.jpg --output result.json

# Process single image and print to console
invoice-processor single invoice.jpg
```

#### Batch Processing
```bash
# Process all images in a directory
invoice-processor batch ./invoices ./json_outputs
```

## Python API Usage

### Basic Usage

```python
from invoice_processor import InvoiceProcessor

# Initialize processor
processor = InvoiceProcessor(api_key="your-api-key")

# Process single image
invoice_data = processor.process_single_image("invoice.jpg")
print(invoice_data.to_json())

# Process directory
results = processor.process_directory("./invoices", "./outputs")
```

### Advanced Usage

```python
from invoice_processor import InvoiceProcessor
import logging

# Custom configuration
processor = InvoiceProcessor(
    api_key="your-api-key",
    model="gemini-pro",  # Use different model
    log_level=logging.DEBUG  # Enable debug logging
)

# Process with custom output path
invoice_data = processor.process_single_image(
    image_path="invoice.jpg",
    output_path="custom_output.json"
)

# Access extracted data
print(f"Invoice Number: {invoice_data.invoice_number}")
print(f"Total: {invoice_data.total}")
print(f"Supplier: {invoice_data.supplier.name}")
```

### Custom Prompt

```python
custom_prompt = """
Extract invoice data and return JSON with these specific fields:
- invoice_id
- date
- vendor_name
- amount_due
Return only JSON, no explanations.
"""

processor = InvoiceProcessor(
    api_key="your-api-key",
    custom_prompt=custom_prompt
)
```

## Data Structure

The extracted invoice data follows this structure:

```json
{
  "invoice_number": "string or null",
  "invoice_date": "string (YYYY-MM-DD) or null",
  "supplier": {
    "name": "string or null",
    "address": "string or null",
    "phone": "string or null",
    "email": "string or null"
  },
  "client": {
    "name": "string or null",
    "address": "string or null",
    "phone": "string or null",
    "email": "string or null"
  },
  "items": [
    {
      "description": "string or null",
      "quantity": "number or null",
      "unit_price": "number or null",
      "total_price": "number or null"
    }
  ],
  "subtotal": "number or null",
  "discount": "number or null",
  "discount_percentage": "number or null",
  "tax": "number or null",
  "shipping_cost": "number or null",
  "rounding_adjustment": "number or null",
  "payment_terms": "string or null",
  "currency": "string or null",
  "total": "number or null"
}
```

## Security Features

- **API Key Validation**: Validates Google Gemini API key format
- **File Type Validation**: Only processes supported image formats
- **File Size Limits**: Prevents processing of oversized files (50MB limit)
- **Path Sanitization**: Prevents directory traversal attacks
- **Input Validation**: Comprehensive validation of all inputs
- **Safe File Handling**: Secure file operations with proper error handling

## Supported File Types

- JPEG (.jpg, .jpeg)
- PNG (.png)
- GIF (.gif)
- BMP (.bmp)
- TIFF (.tiff)

## CLI Commands

### Process Single Image
```bash
invoice-processor single <image_path> [OPTIONS]

Options:
  --output, -o    Output JSON file path
  --model, -m     Gemini model to use (default: gemini-2.0-flash)
  --verbose, -v   Enable verbose logging
```

### Batch Process Directory
```bash
invoice-processor batch <input_dir> <output_dir> [OPTIONS]

Options:
  --model, -m     Gemini model to use (default: gemini-2.0-flash)
  --verbose, -v   Enable verbose logging
```

## Testing

Run the test suite:

```bash
# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=src

# Run specific test file
python -m pytest tests/test_invoice_processor.py

# Run with verbose output
python -m pytest -v
```

## Development

### Project Structure

```
invoice_processor/
├── src/
│   ├── __init__.py
│   ├── invoice_processor.py      # Main processor class
│   ├── cli.py                    # Command-line interface
│   ├── models/
│   │   ├── __init__.py
│   │   └── invoice_data.py       # Data models
│   └── utils/
│       ├── __init__.py
│       ├── file_handler.py       # File operations
│       └── validators.py         # Validation utilities
├── tests/
│   ├── __init__.py
│   ├── test_invoice_processor.py
│   ├── test_models.py
│   └── test_utils.py
├── requirements.txt
├── setup.py
└── README.md
```



### Adding New Features

1. **Create feature branch**: `git checkout -b feature/new-feature`
2. **Write tests first**: Add tests in appropriate test files
3. **Implement feature**: Add code following existing patterns
4. **Update documentation**: Update README and docstrings
5. **Run tests**: Ensure all tests pass
6. **Submit PR**: Create pull request with clear description

## Configuration

### Environment Variables

- `GEMINI_API_KEY`: Your Google Gemini API key (required)

### .env File Example

Create a `.env` file in your project root:

```
# Google Gemini API Configuration
GEMINI_API_KEY=AIzaSyBc5V_m3cstdCH-zwDKl5q6SLh7UVOCfpY

# Optional: Custom model
GEMINI_MODEL=gemini-2.0-flash

# Optional: Log level
LOG_LEVEL=INFO
```

## Error Handling

The system includes comprehensive error handling:

- **ValidationError**: Input validation failures
- **InvoiceProcessorError**: Processing-specific errors
- **File I/O Errors**: File access and permission issues
- **API Errors**: Google Gemini API communication issues
- **JSON Parsing Errors**: Malformed response handling

## Performance Considerations

- **File Size Limits**: 50MB maximum per image
- **Batch Processing**: Processes files sequentially to avoid API rate limits
- **Memory Management**: Efficient handling of large image files
- **Error Recovery**: Continues processing remaining files if one fails

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/yourusername/invoice-processor/issues) page
2. Create a new issue with detailed information
3. Include error messages and steps to reproduce

## Changelog

### v1.0.0
- Initial release
- AI-powered invoice extraction
- Batch processing support
- Comprehensive security validation
- Full test coverage
- CLI interface