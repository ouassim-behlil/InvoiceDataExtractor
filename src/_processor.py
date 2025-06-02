import json
from google import genai
import re
from typing import Optional, Union


class Processor:

    def __init__(self, api_key):
        self.client = self.client = genai.Client(api_key=api_key)
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

    def _extract_json(self, response_text):
        match = re.search(r"\{[\s\S]+\}", response_text)
        if not match:
            return None  # Changed: Now returns None when no JSON is found
        json_str = match.group().replace("\n", "")
        json_str = re.sub(r",\s*\}", "}", json_str)
        json_str = re.sub(r",\s*\]", "]", json_str)
        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            return json_str

    def extract_json_from_image(self, image_path: str) -> Optional[Union[dict, str]]:
        """
        Upload the image at `image_path` to the API, run the model, and attempt to extract JSON.
        Returns:
          - a dict if valid JSON was parsed,
          - a cleaned JSON string if parsing failed,
          - None if no {…} block was detected at all.
        """

        # 2. Upload the file and call the generation endpoint
        uploaded_file = self.client.files.upload(file=image_path)
        response = self.client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[uploaded_file, self.prompt],
        )

        # 3. Try to extract JSON (dict or string) from `response.text`
        result = self._extract_json(response.text)

        # 4. Return exactly what _extract_json returned
        return result
