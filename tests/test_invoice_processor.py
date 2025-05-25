# tests/test_invoice_processor.py
import unittest
from unittest.mock import Mock, patch, MagicMock
import tempfile
import json
from pathlib import Path

from src.invoice_processor import InvoiceProcessor, InvoiceProcessorError
from src.models.invoice_data import InvoiceData
from src.utils.validators import ValidationError


class TestInvoiceProcessor(unittest.TestCase):
    """Test InvoiceProcessor class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.valid_api_key = "AIzaSyBc5V_m3cstdCH-zwDKl5q6SLh7UVOCfpY"
        self.temp_dir = tempfile.mkdtemp()
        
    @patch('src.invoice_processor.genai.Client')
    def test_init_success(self, mock_client):
        """Test successful initialization"""
        processor = InvoiceProcessor(self.valid_api_key)
        
        self.assertEqual(processor.api_key, self.valid_api_key)
        self.assertEqual(processor.model, "gemini-2.0-flash")
        mock_client.assert_called_once_with(api_key=self.valid_api_key)
    
    def test_init_invalid_api_key(self):
        """Test initialization with invalid API key"""
        with self.assertRaises(ValidationError):
            InvoiceProcessor("invalid_key")
    
    @patch('src.invoice_processor.genai.Client')
    def test_init_client_error(self, mock_client):
        """Test initialization with client error"""
        mock_client.side_effect = Exception("Client error")
        
        with self.assertRaises(InvoiceProcessorError):
            InvoiceProcessor(self.valid_api_key)
    
    @patch('src.invoice_processor.genai.Client')
    def test_process_single_image_success(self, mock_client):
        """Test successful single image processing"""
        # Create a temporary image file
        image_path = Path(self.temp_dir) / "test.jpg"
        image_path.write_bytes(b"fake image data")
        
        # Mock Gemini client responses
        mock_uploaded_file = Mock()
        mock_response = Mock()
        mock_response.text = """
        {
            "invoice_number": "INV-001",
            "invoice_date": "2023-01-01",
            "total": 100.50
        }
        """
        
        mock_client_instance = Mock()
        mock_client_instance.files.upload.return_value = mock_uploaded_file
        mock_client_instance.models.generate_content.return_value = mock_response
        mock_client.return_value = mock_client_instance
        
        # Process image
        processor = InvoiceProcessor(self.valid_api_key)
        result = processor.process_single_image(image_path)
        
        # Verify results
        self.assertIsInstance(result, InvoiceData)
        self.assertEqual(result.invoice_number, "INV-001")
        self.assertEqual(result.invoice_date, "2023-01-01")
        self.assertEqual(result.total, 100.50)
    
    @patch('src.invoice_processor.genai.Client')
    def test_process_single_image_invalid_file(self, mock_client):
        """Test processing with invalid file"""
        processor = InvoiceProcessor(self.valid_api_key)
        
        with self.assertRaises(InvoiceProcessorError):
            processor.process_single_image("nonexistent.jpg")
    
    @patch('src.invoice_processor.genai.Client')
    def test_clean_json_string(self, mock_client):
        """Test JSON string cleaning"""
        dirty_json = """
        {
            "field1": "value1",
            "field2": "value2",
        }
        """
        
        clean_json = InvoiceProcessor._clean_json_string(dirty_json)
        
        # Should be valid JSON now
        parsed = json.loads(clean_json)
        self.assertEqual(parsed["field1"], "value1")
        self.assertEqual(parsed["field2"], "value2")


# tests/test_models.py
import unittest
from src.models.invoice_data import InvoiceData, Supplier, Client, InvoiceItem


class TestInvoiceDataModels(unittest.TestCase):
    """Test invoice data models"""
    
    def test_supplier_creation(self):
        """Test Supplier creation and conversion"""
        supplier = Supplier(
            name="Test Company",
            address="123 Main St",
            phone="555-1234",
            email="test@company.com"
        )
        
        supplier_dict = supplier.to_dict()
        expected = {
            "name": "Test Company",
            "address": "123 Main St",
            "phone": "555-1234",
            "email": "test@company.com"
        }
        
        self.assertEqual(supplier_dict, expected)
    
    def test_invoice_item_creation(self):
        """Test InvoiceItem creation and conversion"""
        item = InvoiceItem(
            description="Test Item",
            quantity=2.0,
            unit_price=10.50,
            total_price=21.00
        )
        
        item_dict = item.to_dict()
        expected = {
            "description": "Test Item",
            "quantity": 2.0,
            "unit_price": 10.50,
            "total_price": 21.00
        }
        
        self.assertEqual(item_dict, expected)
    
    def test_invoice_data_creation(self):
        """Test InvoiceData creation and conversion"""
        supplier = Supplier(name="Test Supplier")
        client = Client(name="Test Client")
        item = InvoiceItem(description="Test Item", quantity=1, unit_price=100)
        
        invoice = InvoiceData(
            invoice_number="INV-001",
            invoice_date="2023-01-01",
            supplier=supplier,
            client=client,
            items=[item],
            total=100.00
        )
        
        invoice_dict = invoice.to_dict()
        
        self.assertEqual(invoice_dict["invoice_number"], "INV-001")
        self.assertEqual(invoice_dict["supplier"]["name"], "Test Supplier")
        self.assertEqual(len(invoice_dict["items"]), 1)
        self.assertEqual(invoice_dict["total"], 100.00)
    
    def test_invoice_data_from_dict(self):
        """Test creating InvoiceData from dictionary"""
        data = {
            "invoice_number": "INV-002",
            "invoice_date": "2023-02-01",
            "supplier": {"name": "Supplier Inc"},
            "client": {"name": "Client Corp"},
            "items": [{"description": "Item 1", "quantity": 1, "unit_price": 50}],
            "total": 50.00
        }
        
        invoice = InvoiceData.from_dict(data)
        
        self.assertEqual(invoice.invoice_number, "INV-002")
        self.assertEqual(invoice.supplier.name, "Supplier Inc")
        self.assertEqual(invoice.client.name, "Client Corp")
        self.assertEqual(len(invoice.items), 1)
        self.assertEqual(invoice.items[0].description, "Item 1")
    
    def test_invoice_data_to_json(self):
        """Test JSON serialization"""
        invoice = InvoiceData(invoice_number="INV-003", total=75.25)
        json_str = invoice.to_json()
        
        # Should be valid JSON
        import json
        parsed = json.loads(json_str)
        self.assertEqual(parsed["invoice_number"], "INV-003")
        self.assertEqual(parsed["total"], 75.25)


# tests/test_utils.py
import unittest
import tempfile
from pathlib import Path
import json

from src.utils.validators import Validators, ValidationError
from src.utils.file_handler import FileHandler


class TestValidators(unittest.TestCase):
    """Test validation utilities"""
    
    def test_validate_api_key_valid(self):
        """Test valid API key validation"""
        valid_key = "AIzaSyBc5V_m3cstdCH-zwDKl5q6SLh7UVOCfpY"
        self.assertTrue(Validators.validate_api_key(valid_key))
    
    def test_validate_api_key_invalid(self):
        """Test invalid API key validation"""
        invalid_keys = [
            "",
            None,
            "short",
            "invalid_format_key_123456789012345678901234567890",
            123456
        ]
        
        for key in invalid_keys:
            with self.assertRaises(ValidationError):
                Validators.validate_api_key(key)
    
    def test_validate_image_file_success(self):
        """Test valid image file validation"""
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp:
            tmp.write(b"fake image data")
            tmp_path = Path(tmp.name)
        
        try:
            self.assertTrue(Validators.validate_image_file(tmp_path))
        finally:
            tmp_path.unlink()
    
    def test_validate_image_file_invalid_extension(self):
        """Test invalid image file extension"""
        with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as tmp:
            tmp.write(b"not an image")
            tmp_path = Path(tmp.name)
        
        try:
            with self.assertRaises(ValidationError):
                Validators.validate_image_file(tmp_path)
        finally:
            tmp_path.unlink()
    
    def test_validate_image_file_not_exists(self):
        """Test validation of non-existent file"""
        with self.assertRaises(ValidationError):
            Validators.validate_image_file("nonexistent.jpg")
    
    def test_sanitize_filename(self):
        """Test filename sanitization"""
        dangerous_name = "../../../etc/passwd<>:\"|?*"
        safe_name = Validators.sanitize_filename(dangerous_name)
        
        self.assertNotIn("..", safe_name)
        self.assertNotIn("/", safe_name)
        self.assertNotIn("<", safe_name)
        self.assertNotIn(">", safe_name)


class TestFileHandler(unittest.TestCase):
    """Test file handler utilities"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.file_handler = FileHandler()
    
    def test_save_json_success(self):
        """Test successful JSON saving"""
        data = {"test": "data", "number": 123.456}
        output_path = Path(self.temp_dir) / "test.json"
        
        result = self.file_handler.save_json(data, output_path)
        
        self.assertTrue(result)
        self.assertTrue(output_path.exists())
        
        # Verify content
        with open(output_path) as f:
            saved_data = json.load(f)
        
        self.assertEqual(saved_data["test"], "data")
        self.assertEqual(saved_data["number"], 123.46)  # Should be rounded
    
    def test_save_text_success(self):
        """Test successful text saving"""
        text = "This is test content"
        output_path = Path(self.temp_dir) / "test.txt"
        
        result = self.file_handler.save_text(text, output_path)
        
        self.assertTrue(result)
        self.assertTrue(output_path.exists())
        
        # Verify content
        with open(output_path) as f:
            saved_text = f.read()
        
        self.assertEqual(saved_text, text)
    
    def test_get_image_files(self):
        """Test getting image files from directory"""
        # Create test files
        (Path(self.temp_dir) / "image1.jpg").write_bytes(b"fake image")
        (Path(self.temp_dir) / "image2.png").write_bytes(b"fake image")
        (Path(self.temp_dir) / "not_image.txt").write_text("not an image")
        
        image_files = self.file_handler.get_image_files(self.temp_dir)
        
        self.assertEqual(len(image_files), 2)
        self.assertTrue(any(f.name == "image1.jpg" for f in image_files))
        self.assertTrue(any(f.name == "image2.png" for f in image_files))
    
    def test_round_numbers_in_dict(self):
        """Test number rounding in nested structures"""
        data = {
            "float_val": 123.456789,
            "int_val": 42,
            "nested": {
                "another_float": 98.765432
            },
            "list_vals": [1.23456, 2.34567, {"nested_float": 3.45678}]
        }
        
        rounded = FileHandler._round_numbers_in_dict(data.copy())
        
        self.assertEqual(rounded["float_val"], 123.46)
        self.assertEqual(rounded["int_val"], 42)
        self.assertEqual(rounded["nested"]["another_float"], 98.77)
        self.assertEqual(rounded["list_vals"][0], 1.23)
        self.assertEqual(rounded["list_vals"][2]["nested_float"], 3.46)


if __name__ == '__main__':
    unittest.main()