# Getting Started with Invoice Extractor

This guide will help you get up and running with the Invoice Extractor project.

## Quick Start

1. **System Requirements**
   - Python 3.7 or higher
   - Operating System: Windows, macOS, or Linux
   - Sufficient disk space for dependencies
   - Internet connection for API access

2. **Installation Steps**

   ```bash
   # Clone the repository
   git clone https://github.com/ouassim-behlil/InvoiceDataExtractor.git
   cd invoiceExtractor

   # Install dependencies
   pip install -r requirements.txt

   # Set up API key
   echo "your-api-key-here" > api_key.txt
   ```

3. **First Run**

   ```python
   from src._processor import Processor

   # Initialize with API key
   with open('api_key.txt', 'r') as f:
       api_key = f.read().strip()
   processor = Processor(api_key)

   # Process an invoice
   result = processor.extract_json_from_image('invoices/your_invoice.jpg')
   ```

## Directory Structure

```
invoiceExtractor/
├── src/               # Source code
├── tests/             # Test files
├── invoices/          # Place invoice images here
├── docs/              # Documentation
└── requirements.txt   # Dependencies
```

## Next Steps

1. Read the [API Documentation](api.md) for detailed function references
2. Check out the [Examples](examples.md) for common use cases
3. Review the [Validation Guide](validation.md) for data validation details
4. See [Troubleshooting](troubleshooting.md) for common issues

## Support

For issues and questions:
1. Check the [FAQ](faq.md)
2. Open an issue on GitHub
3. Contact the maintainers
