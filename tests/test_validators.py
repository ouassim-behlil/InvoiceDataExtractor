import tempfile
import pytest
from pathlib import Path
from src.utils.validators import Validators, ValidationError

def test_validate_api_key_valid():
    key = "AIza" + "A" * 35
    assert Validators.validate_api_key(key)

def test_validate_api_key_invalid():
    with pytest.raises(ValidationError):
        Validators.validate_api_key("short-key")

def test_validate_image_file(tmp_path):
    img = tmp_path / "test.png"
    img.write_bytes(b"\x89PNG\r\n\x1a\n....")
    assert Validators.validate_image_file(img)

def test_validate_image_file_invalid_extension(tmp_path):
    fake = tmp_path / "test.txt"
    fake.write_text("Not an image")
    with pytest.raises(ValidationError):
        Validators.validate_image_file(fake)

def test_validate_directory_creation(tmp_path):
    new_dir = tmp_path / "newdir"
    assert Validators.validate_directory(new_dir, create_if_missing=True)
    assert new_dir.exists() and new_dir.is_dir()

def test_sanitize_filename():
    assert Validators.sanitize_filename("../../../evil.txt") == "______evil.txt"

