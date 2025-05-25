import os
import json
import re
from google import genai

# Initialize Gemini client
client = genai.Client(api_key="AIzaSyBc5V_m3cstdCH-zwDKl5q6SLh7UVOCfpY")

# Define folders
image_dir = "invoices"
output_dir = "./json_outputs"
os.makedirs(output_dir, exist_ok=True)

# Extended Gemini prompt for structured extraction with additional fields
prompt = """
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

def round_numbers_in_dict(d):
    """
    Recursively round all numeric values in dictionary or list to 2 decimals.
    """
    if isinstance(d, dict):
        for k, v in d.items():
            if isinstance(v, (int, float)):
                d[k] = round(v, 2)
            elif isinstance(v, (dict, list)):
                round_numbers_in_dict(v)
    elif isinstance(d, list):
        for item in d:
            round_numbers_in_dict(item)

# Process each image
for filename in os.listdir(image_dir):
    if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        image_path = os.path.join(image_dir, filename)
        print(f"📄 Processing: {filename}")

        # Upload image to Gemini
        uploaded_file = client.files.upload(file=image_path)

        # Generate content
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[uploaded_file, prompt],
        )

        # Prepare output file path
        json_filename = os.path.splitext(filename)[0] + ".json"
        output_path = os.path.join(output_dir, json_filename)

        # Try to extract JSON using regex
        match = re.search(r"\{[\s\S]+\}", response.text)

        if match:
            json_str = match.group()

            try:
                # Clean JSON string
                json_str = json_str.replace("\n", "")
                json_str = re.sub(r",\s*}", "}", json_str)
                json_str = re.sub(r",\s*]", "]", json_str)

                # Load JSON
                data = json.loads(json_str)

                # Round all numeric values to 2 decimals
                round_numbers_in_dict(data)

                # Save JSON to file
                with open(output_path, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)

                print(f"✅ JSON saved: {json_filename}")
            except json.JSONDecodeError:
                print(f"⚠️ Could not parse cleaned JSON for {filename}, saving raw content.")
                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(json_str)
        else:
            print(f"❌ No JSON detected in {filename}. Saving raw response.")
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(response.text)
