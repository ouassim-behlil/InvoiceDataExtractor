# src/invoice_processor.py
import json
import logging
import os
import re
from pathlib import Path
from typing import Union, List, Optional, Dict, Any

from google import genai

from .models.invoice_data import InvoiceData
from .utils.file_handler import FileHandler
from .utils.validators import Validators, ValidationError


class InvoiceProcessorError(Exception):
    """Custom exception for invoice processor"""
    pass


class InvoiceProcessor:
    """Main class for processing invoices using Google Gemini AI"""
    
    DEFAULT_PROMPT = """
You are an intelligent document processing assistant. You are given the OCR result of an invoice extracted from an image. 
Your task is to extract the relevant information and return a structured JSON object strictly following the format below.

Return only the JSON structure exactly as shown, using null if a value is not found. Pay attention to common invoice terminology and numeric patterns.

=== STRUCTURE ===

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

Return only the JSON result. Do not add explanations or text outside the JSON.
"""
    
    def __init__(self, api_key: str, model: str = "gemini-2.0-flash", 
                 custom_prompt: Optional[str] = None, log_level: int = logging.INFO):
        """
        Initialize InvoiceProcessor
        
        Args:
            api_key: Google Gemini API key
            model: Gemini model to use
            custom_prompt: Custom extraction prompt
            log_level: Logging level
            
        Raises:
            ValidationError: If API key is invalid
        """
        # Validate API key
        Validators.validate_api_key(api_key)
        
        self.api_key = api_key
        self.model = model
        self.prompt = custom_prompt or self.DEFAULT_PROMPT
        
        # Setup logging
        self.logger = self._setup_logger(log_level)
        
        # Initialize components
        self.file_handler = FileHandler(self.logger)
        
        # Initialize Gemini client
        try:
            self.client = genai.Client(api_key=api_key)
            self.logger.info("Gemini client initialized successfully")
        except Exception as e:
            raise InvoiceProcessorError(f"Failed to initialize Gemini client: {e}")
    
    def process_single_image(self, image_path: Union[str, Path], 
                           output_path: Optional[Union[str, Path]] = None) -> InvoiceData:
        """
        Process a single invoice image
        
        Args:
            image_path: Path to image file
            output_path: Optional output JSON path
            
        Returns:
            InvoiceData: Extracted invoice data
            
        Raises:
            InvoiceProcessorError: If processing fails
        """
        image_path = Path(image_path)
        
        try:
            # Validate image file
            Validators.validate_image_file(image_path)
            self.logger.info(f"Processing image: {image_path}")
            
            # Upload image to Gemini
            uploaded_file = self._upload_image(image_path)
            
            # Generate content
            response = self._generate_content(uploaded_file)
            
            # Extract invoice data
            invoice_data = self._extract_invoice_data(response.text)
            
            # Save to file if output path provided
            if output_path:
                output_path = Path(output_path)
                if output_path.suffix.lower() != '.json':
                    output_path = output_path.with_suffix('.json')
                
                self.file_handler.save_json(invoice_data.to_dict(), output_path)
            
            self.logger.info(f"Successfully processed: {image_path}")
            return invoice_data
            
        except ValidationError as e:
            raise InvoiceProcessorError(f"Validation error: {e}")
        except Exception as e:
            self.logger.error(f"Error processing {image_path}: {e}")
            raise InvoiceProcessorError(f"Processing failed: {e}")
    
    def process_directory(self, image_dir: Union[str, Path], 
                         output_dir: Union[str, Path]) -> Dict[str, InvoiceData]:
        """
        Process all images in a directory
        
        Args:
            image_dir: Directory containing images
            output_dir: Output directory for JSON files
            
        Returns:
            Dict[str, InvoiceData]: Mapping of filenames to invoice data
            
        Raises:
            InvoiceProcessorError: If processing fails
        """
        image_dir = Path(image_dir)
        output_dir = Path(output_dir)
        
        try:
            # Get image files
            image_files = self.file_handler.get_image_files(image_dir)
            
            if not image_files:
                self.logger.warning(f"No valid image files found in {image_dir}")
                return {}
            
            self.logger.info(f"Found {len(image_files)} image files to process")
            
            results = {}
            
            for image_file in image_files:
                try:
                    # Generate output path
                    output_filename = image_file.stem + '.json'
                    output_path = output_dir / output_filename
                    
                    # Process image
                    invoice_data = self.process_single_image(image_file, output_path)
                    results[image_file.name] = invoice_data
                    
                except InvoiceProcessorError as e:
                    self.logger.error(f"Failed to process {image_file}: {e}")
                    # Continue processing other files
                    continue
            
            self.logger.info(f"Successfully processed {len(results)} out of {len(image_files)} files")
            return results
            
        except Exception as e:
            raise InvoiceProcessorError(f"Directory processing failed: {e}")
    
    def _upload_image(self, image_path: Path):
        """Upload image to Gemini"""
        try:
            return self.client.files.upload(file=str(image_path))
        except Exception as e:
            raise InvoiceProcessorError(f"Failed to upload image {image_path}: {e}")
    
    def _generate_content(self, uploaded_file):
        """Generate content using Gemini"""
        try:
            return self.client.models.generate_content(
                model=self.model,
                contents=[uploaded_file, self.prompt],
            )
        except Exception as e:
            raise InvoiceProcessorError(f"Failed to generate content: {e}")
    
    def _extract_invoice_data(self, response_text: str) -> InvoiceData:
        """
        Extract invoice data from response text
        
        Args:
            response_text: Raw response from Gemini
            
        Returns:
            InvoiceData: Parsed invoice data
        """
        # Try to extract JSON using regex
        match = re.search(r"\{[\s\S]+\}", response_text)
        
        if not match:
            self.logger.warning("No JSON found in response, creating empty invoice data")
            return InvoiceData()
        
        json_str = match.group()
        
        try:
            # Clean JSON string
            json_str = self._clean_json_string(json_str)
            
            # Parse JSON
            data = json.loads(json_str)
            
            # Convert to InvoiceData
            return InvoiceData.from_dict(data)
            
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse JSON: {e}")
            self.logger.debug(f"Raw JSON string: {json_str}")
            
            # Return empty invoice data with raw response
            invoice_data = InvoiceData()
            # Could add raw_response field to InvoiceData if needed
            return invoice_data
    
    @staticmethod
    def _clean_json_string(json_str: str) -> str:
        """Clean JSON string for parsing"""
        # Remove newlines and extra spaces
        json_str = json_str.replace("\n", "").strip()
        
        # Remove trailing commas
        json_str = re.sub(r",\s*}", "}", json_str)
        json_str = re.sub(r",\s*]", "]", json_str)
        
        return json_str
    
    @staticmethod
    def _setup_logger(log_level: int = logging.INFO) -> logging.Logger:
        """Setup logger"""
        logger = logging.getLogger(__name__)
        logger.setLevel(log_level)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger