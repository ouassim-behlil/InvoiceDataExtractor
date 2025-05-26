# tests/test_validators.py
import pytest
import os
import tempfile
from pathlib import Path
from unittest.mock import patch, mock_open

from src.utils.validators import Validators, ValidationError


class TestValidators:
    """Test suite for Validators class"""

    def test_validate_api_key_valid(self):
        """Test valid API key validation"""
        valid_key = "AIzaSyDhVyKw8b7lMnOpQ1234567890abcdefg"
        assert Validators.validate_api_key(valid_key) is True

    def test_validate_api_key_empty(self):
        """Test empty API key validation"""
        with pytest.raises(ValidationError, match="API key is required"):
            Validators.validate_api_key("")

    def test_validate_api_key_none(self):
        """Test None API key validation"""
        with pytest.raises(ValidationError, match="API key is required"):
            Validators.validate_api_key(None)

    def test_validate_api_key_not_string(self):
        """Test non-string API key validation"""
        with pytest.raises(ValidationError, match="API key must be a string"):
            Validators.validate_api_key(123)

    def test_validate_api_key_too_short(self):
        """Test API key that's too short"""
        with pytest.raises(ValidationError, match="API key appears to be too short"):
            Validators.validate_api_key("short")

    def test_validate_api_key_invalid_format(self):
        """Test API key with invalid format"""
        with pytest.raises(ValidationError, match="API key format appears invalid"):
            Validators.validate_api_key("invalid_format_that_is_long_enough_but_wrong")

    def test_validate_image_file_success(self):
        """Test successful image file validation"""
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp_file:
            tmp_file.write(b"fake image data")
            tmp_path = Path(tmp_file.name)

        try:
            assert Validators.validate_image_file(tmp_path) is True
        finally:
            tmp_path.unlink()

    def test_validate_image_file_not_exists(self):
        """Test validation of non-existent file"""
        fake_path = Path("non_existent_file.jpg")
        with pytest.raises(ValidationError, match="File does not exist"):
            Validators.validate_image_file(fake_path)

    def test_validate_image_file_is_directory(self):
        """Test validation when path is a directory"""
        with tempfile.TemporaryDirectory() as tmp_dir:
            dir_path = Path(tmp_dir)
            with pytest.raises(ValidationError, match="Path is not a file"):
                Validators.validate_image_file(dir_path)

    def test_validate_image_file_unsupported_extension(self):
        """Test validation of unsupported file type"""
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as tmp_file:
            tmp_file.write(b"text data")
            tmp_path = Path(tmp_file.name)

        try:
            with pytest.raises(ValidationError, match="Unsupported file type"):
                Validators.validate_image_file(tmp_path)
        finally:
            tmp_path.unlink()

    def test_validate_image_file_too_large(self):
        """Test validation of file that's too large"""
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp_file:
            # Create a file larger than MAX_FILE_SIZE
            large_data = b"0" * (Validators.MAX_FILE_SIZE + 1)
            tmp_file.write(large_data)
            tmp_path = Path(tmp_file.name)

        try:
            with pytest.raises(ValidationError, match="File too large"):
                Validators.validate_image_file(tmp_path)
        finally:
            tmp_path.unlink()

    @patch("builtins.open", side_effect=IOError("Cannot read file"))
    def test_validate_image_file_unreadable(self, mock_file):
        """Test validation of unreadable file"""
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp_file:
            tmp_path = Path(tmp_file.name)

        try:
            with pytest.raises(ValidationError, match="Cannot read file"):
                Validators.validate_image_file(tmp_path)
        finally:
            tmp_path.unlink()

    def test_validate_directory_success(self):
        """Test successful directory validation"""
        with tempfile.TemporaryDirectory() as tmp_dir:
            assert Validators.validate_directory(tmp_dir) is True

    def test_validate_directory_not_exists_no_create(self):
        """Test validation of non-existent directory without creation"""
        fake_dir = Path("non_existent_directory")
        with pytest.raises(ValidationError, match="Directory does not exist"):
            Validators.validate_directory(fake_dir)

    def test_validate_directory_create_if_missing(self):
        """Test directory creation when missing"""
        with tempfile.TemporaryDirectory() as parent_dir:
            new_dir = Path(parent_dir) / "new_subdir"
            assert (
                Validators.validate_directory(new_dir, create_if_missing=True) is True
            )
            assert new_dir.exists()
            assert new_dir.is_dir()

    @patch("pathlib.Path.mkdir", side_effect=PermissionError("Permission denied"))
    def test_validate_directory_creation_fails(self, mock_mkdir):
        """Test directory creation failure"""
        fake_dir = Path("permission_denied_dir")
        with pytest.raises(ValidationError, match="Cannot create directory"):
            Validators.validate_directory(fake_dir, create_if_missing=True)

    def test_validate_directory_is_file(self):
        """Test validation when path is a file, not directory"""
        with tempfile.NamedTemporaryFile() as tmp_file:
            file_path = Path(tmp_file.name)
            with pytest.raises(ValidationError, match="Path is not a directory"):
                Validators.validate_directory(file_path)

    @patch("os.access", return_value=False)
    def test_validate_directory_no_write_permission(self, mock_access):
        """Test validation of directory without write permission"""
        with tempfile.TemporaryDirectory() as tmp_dir:
            with pytest.raises(ValidationError, match="No write permission"):
                Validators.validate_directory(tmp_dir)

    def test_sanitize_filename_basic(self):
        """Test basic filename sanitization"""
        result = Validators.sanitize_filename("normal_file.txt")
        assert result == "normal_file.txt"

    def test_sanitize_filename_dangerous_chars(self):
        """Test sanitization of dangerous characters"""
        dangerous = 'file<>:"/\\|?*.txt'
        result = Validators.sanitize_filename(dangerous)
        assert result == "file_________.txt"

    def test_sanitize_filename_directory_traversal(self):
        traversal = "../../../etc/passwd"
        result = Validators.sanitize_filename(traversal)
        assert result == "______etc_passwd"


    def test_sanitize_filename_empty(self):
        """Test sanitization of empty filename"""
        result = Validators.sanitize_filename("")
        assert result == "unnamed_file"

    def test_sanitize_filename_whitespace_only(self):
        """Test sanitization of whitespace-only filename"""
        result = Validators.sanitize_filename("   ")
        assert result == "unnamed_file"

    def test_sanitize_filename_too_long(self):
        """Test sanitization of filename that's too long"""
        long_name = "a" * 300 + ".txt"
        result = Validators.sanitize_filename(long_name)
        assert len(result) == 255
        assert result.endswith("a")

    def test_supported_image_extensions(self):
        """Test that supported image extensions are correctly defined"""
        expected_extensions = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff"}
        assert Validators.SUPPORTED_IMAGE_EXTENSIONS == expected_extensions

    def test_max_file_size_constant(self):
        """Test that MAX_FILE_SIZE constant is correctly defined"""
        expected_size = 50 * 1024 * 1024  # 50MB
        assert Validators.MAX_FILE_SIZE == expected_size

    @pytest.mark.parametrize(
        "extension", [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff"]
    )
    def test_validate_image_file_all_extensions(self, extension):
        """Test validation of all supported image extensions"""
        with tempfile.NamedTemporaryFile(suffix=extension, delete=False) as tmp_file:
            tmp_file.write(b"fake image data")
            tmp_path = Path(tmp_file.name)

        try:
            assert Validators.validate_image_file(tmp_path) is True
        finally:
            tmp_path.unlink()

    @pytest.mark.parametrize("extension", [".JPG", ".JPEG", ".PNG"])
    def test_validate_image_file_case_insensitive(self, extension):
        """Test that file extension validation is case insensitive"""
        with tempfile.NamedTemporaryFile(suffix=extension, delete=False) as tmp_file:
            tmp_file.write(b"fake image data")
            tmp_path = Path(tmp_file.name)

        try:
            assert Validators.validate_image_file(tmp_path) is True
        finally:
            tmp_path.unlink()
