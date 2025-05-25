import tempfile
import json
import os
import pytest
from src.utils.file_handler import FileHandler, ValidationError

def test_save_json_and_text(tmp_path):
    handler = FileHandler()
    data = {"price": 123.4567}
    output_json = tmp_path / "output.json"
    output_txt = tmp_path / "output.txt"

    assert handler.save_json(data, output_json)
    assert json.loads(output_json.read_text(encoding='utf-8'))["price"] == 123.46

    assert handler.save_text("Hello, World!", output_txt)
    assert output_txt.read_text(encoding='utf-8') == "Hello, World!"

def test_get_image_files(tmp_path):
    handler = FileHandler()
    img_file = tmp_path / "image.jpg"
    img_file.write_bytes(b"\x89PNG\r\n\x1a\n...")  # fake image header

    from src.utils.validators import Validators
    Validators.SUPPORTED_IMAGE_EXTENSIONS.add(".jpg")

    image_files = handler.get_image_files(tmp_path)
    assert img_file in image_files
