import os
import json
import re
from dataclasses import dataclass
from google import genai
from src.models.invoice_data import InvoiceData


@dataclass
class InvoiceProcessorConfig:
    api_key: str
    image_dir: str = "invoices"
    output_dir: str = "./json_outputs"


class InvoiceProcessor:
    def __init__(self, config: InvoiceProcessorConfig):
        self.client = genai.Client(api_key=config.api_key)
        self.image_dir = config.image_dir
        self.output_dir = config.output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        self.prompt = self._get_prompt()

    def _get_prompt(self):
        return """
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

    def _round_invoice_data(self, invoice_data: InvoiceData):
        def round_optional(value):
            return round(value, 2) if isinstance(value, (int, float)) else value

        invoice_data.subtotal = round_optional(invoice_data.subtotal)
        invoice_data.discount = round_optional(invoice_data.discount)
        invoice_data.discount_percentage = round_optional(
            invoice_data.discount_percentage
        )
        invoice_data.tax = round_optional(invoice_data.tax)
        invoice_data.shipping_cost = round_optional(invoice_data.shipping_cost)
        invoice_data.rounding_adjustment = round_optional(
            invoice_data.rounding_adjustment
        )
        invoice_data.total = round_optional(invoice_data.total)

        for item in invoice_data.items:
            item.quantity = round_optional(item.quantity)
            item.unit_price = round_optional(item.unit_price)
            item.total_price = round_optional(item.total_price)

    def _extract_json(self, response_text):
        match = re.search(r"\{[\s\S]+\}", response_text)
        if not match:
            return None
        json_str = match.group().replace("\n", "")
        json_str = re.sub(r",\s*\}", "}", json_str)
        json_str = re.sub(r",\s*\]", "]", json_str)
        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            return json_str  # raw string if it fails

    def process_image(self, image_path: str):
        filename = os.path.basename(image_path)
        print(f"\U0001f4c4 Processing: {filename}")
        uploaded_file = self.client.files.upload(file=image_path)

        response = self.client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[uploaded_file, self.prompt],
        )

        json_filename = os.path.splitext(filename)[0] + ".json"
        output_path = os.path.join(self.output_dir, json_filename)
        result = self._extract_json(response.text)

        if result is None:
            print(f"❌ No JSON detected in {filename}. Saving raw response.")
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(response.text)
        elif isinstance(result, dict):
            try:
                invoice = InvoiceData.from_dict(result)
                self._round_invoice_data(invoice)
                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(invoice.to_json(indent=2))
                print(f"✅ JSON saved: {json_filename}")
            except Exception as e:
                print(
                    f"⚠️ Failed to create InvoiceData object for {filename}: {e}. Saving raw JSON."
                )
                with open(output_path, "w", encoding="utf-8") as f:
                    json.dump(result, f, indent=2, ensure_ascii=False)
        else:
            print(f"⚠️ Could not parse cleaned JSON for {filename}, saving raw content.")
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(result)

    def process_all_images(self):
        for filename in os.listdir(self.image_dir):
            if filename.lower().endswith((".jpg", ".jpeg", ".png")):
                image_path = os.path.join(self.image_dir, filename)
                self.process_image(image_path)
