# Invoice Extractor Documentation

Welcome to the Invoice Extractor documentation. This comprehensive guide will help you understand and use the Invoice Extractor system effectively.

## Table of Contents

### 1. [Getting Started](getting_started.md)
- Quick start guide
- Installation
- Basic usage
- Directory structure

### 2. [API Documentation](api.md)
- Processor class reference
- Methods and parameters
- Data structures
- Error handling

### 3. [Examples](examples.md)
- Basic usage examples
- Batch processing
- Error handling
- Best practices
- Common patterns

### 4. [Validation Guide](validation.md)
- Validation rules
- Data types
- Mathematical validations
- Business rules
- Error messages

### 5. [Troubleshooting](troubleshooting.md)
- Common issues
- Solutions
- Debugging tips
- When to contact support

### 6. [FAQ](faq.md)
- General questions
- Technical questions
- Performance optimization
- Integration guidance

## Quick Navigation

### For New Users
1. Start with the [Getting Started](getting_started.md) guide
2. Review the [Examples](examples.md)
3. Check the [FAQ](faq.md) for common questions

### For Developers
1. Review the [API Documentation](api.md)
2. Understand the [Validation Guide](validation.md)
3. Implement error handling using the [Troubleshooting](troubleshooting.md) guide

### For System Integration
1. Study the [API Documentation](api.md)
2. Review integration examples in [Examples](examples.md)
3. Understand validation requirements in [Validation Guide](validation.md)

## Quick Reference

### Basic Usage
```python
from src._processor import Processor

# Initialize
with open('api_key.txt', 'r') as f:
    api_key = f.read().strip()
processor = Processor(api_key)

# Process invoice
result = processor.extract_json_from_image('invoices/invoice.jpg')
```

### Key Features
- OCR-based invoice data extraction
- Structured JSON output
- Comprehensive validation
- Error handling
- Batch processing support

### Support Channels
- Documentation (you are here)
- GitHub Issues
- Community Forums
- Direct Support

## Contributing

We welcome contributions! To contribute:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License. See the [LICENSE](../LICENSE) file for details.
