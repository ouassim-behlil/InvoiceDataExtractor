# tests/test_file_handler.py
import pytest
import json
import tempfile
import logging
from pathlib import Path
from unittest.mock import patch, mock_open, MagicMock

from src.utils.file_handler import FileHandler
from src.utils.validators import ValidationError


class TestFileHandler:
    """Test suite for FileHandler class"""

    @pytest.fixture
    def file_handler(self):
        """Create FileHandler instance for testing"""
        return FileHandler()

    @pytest.fixture
    def file_handler_with_logger(self):
        """Create FileHandler instance with custom logger"""
        logger = logging.getLogger("test_logger")
        return FileHandler(logger)

    def test_init_default_logger(self):
        """Test FileHandler initialization with default logger"""
        handler = FileHandler()
        assert handler.logger is not None
        assert handler.logger.name == "src.utils.file_handler"

    def test_init_custom_logger(self):
        """Test FileHandler initialization with custom logger"""
        custom_logger = logging.getLogger("custom")
        handler = FileHandler(custom_logger)
        assert handler.logger is custom_logger

    def test_save_json_success(self, file_handler):
        """Test successful JSON saving"""
        test_data = {
            "name": "test",
            "value": 123.456789,
            "nested": {"float_val": 987.654321},
        }

        with tempfile.TemporaryDirectory() as tmp_dir:
            output_path = Path(tmp_dir) / "test.json"
            result = file_handler.save_json(test_data, output_path)

            assert result is True
            assert output_path.exists()

            # Verify content and rounding
            with open(output_path, "r", encoding="utf-8") as f:
                saved_data = json.load(f)

            assert saved_data["name"] == "test"
            assert saved_data["value"] == 123.46  # Rounded to 2 decimals
            assert saved_data["nested"]["float_val"] == 987.65  # Rounded to 2 decimals

    def test_save_json_creates_directory(self, file_handler):
        """Test that save_json creates parent directory if missing"""
        test_data = {"test": "data"}

        with tempfile.TemporaryDirectory() as tmp_dir:
            output_path = Path(tmp_dir) / "subdir" / "test.json"
            result = file_handler.save_json(test_data, output_path)

            assert result is True
            assert output_path.exists()
            assert output_path.parent.exists()

    @patch("builtins.open", side_effect=IOError("Permission denied"))
    def test_save_json_io_error(self, mock_file, file_handler):
        """Test save_json with IO error"""
        test_data = {"test": "data"}
        output_path = Path("test.json")

        with pytest.raises(ValidationError, match="Failed to save JSON"):
            file_handler.save_json(test_data, output_path)

    @patch("json.dump", side_effect=TypeError("Invalid JSON"))
    def test_save_json_encode_error(self, mock_json_dump, file_handler):
        """Test save_json with JSON encoding error"""
        test_data = {"test": "data"}
        
        with tempfile.TemporaryDirectory() as tmp_dir:
            output_path = Path(tmp_dir) / "test.json"
            
            with pytest.raises(ValidationError, match="Failed to save JSON"):
                file_handler.save_json(test_data, output_path)


    def test_save_text_success(self, file_handler):
        """Test successful text saving"""
        test_text = "Hello, World!\nThis is a test."

        with tempfile.TemporaryDirectory() as tmp_dir:
            output_path = Path(tmp_dir) / "test.txt"
            result = file_handler.save_text(test_text, output_path)

            assert result is True
            assert output_path.exists()

            # Verify content
            with open(output_path, "r", encoding="utf-8") as f:
                saved_text = f.read()

            assert saved_text == test_text

    def test_save_text_creates_directory(self, file_handler):
        """Test that save_text creates parent directory if missing"""
        test_text = "test content"

        with tempfile.TemporaryDirectory() as tmp_dir:
            output_path = Path(tmp_dir) / "subdir" / "test.txt"
            result = file_handler.save_text(test_text, output_path)

            assert result is True
            assert output_path.exists()
            assert output_path.parent.exists()

    @patch("builtins.open", side_effect=IOError("Permission denied"))
    def test_save_text_io_error(self, mock_file, file_handler):
        """Test save_text with IO error"""
        test_text = "test content"
        output_path = Path("test.txt")

        with pytest.raises(ValidationError, match="Failed to save text"):
            file_handler.save_text(test_text, output_path)

    def test_get_image_files_success(self, file_handler):
        """Test successful image file retrieval"""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)

            # Create test files
            image_files = ["test1.jpg", "test2.png", "test3.gif"]
            other_files = ["document.txt", "data.csv"]

            for filename in image_files + other_files:
                file_path = tmp_path / filename
                file_path.write_bytes(b"fake content")

            result = file_handler.get_image_files(tmp_path)

            # Should only return image files, sorted
            expected_paths = sorted([tmp_path / f for f in image_files])
            assert result == expected_paths

    def test_get_image_files_empty_directory(self, file_handler):
        """Test get_image_files with empty directory"""
        with tempfile.TemporaryDirectory() as tmp_dir:
            result = file_handler.get_image_files(tmp_dir)
            assert result == []

    def test_get_image_files_no_images(self, file_handler):
        """Test get_image_files with no image files"""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)

            # Create non-image files
            (tmp_path / "document.txt").write_text("content")
            (tmp_path / "data.csv").write_text("data")

            result = file_handler.get_image_files(tmp_path)
            assert result == []

    @patch(
        "src.utils.validators.Validators.validate_directory",
        side_effect=ValidationError("Invalid directory"),
    )
    def test_get_image_files_invalid_directory(self, mock_validate, file_handler):
        """Test get_image_files with invalid directory"""
        with pytest.raises(ValidationError, match="Invalid directory"):
            file_handler.get_image_files("invalid_dir")

    @patch("pathlib.Path.iterdir", side_effect=PermissionError("Permission denied"))
    def test_get_image_files_permission_error(self, mock_iterdir, file_handler):
        """Test get_image_files with permission error"""
        with tempfile.TemporaryDirectory() as tmp_dir:
            with pytest.raises(ValidationError, match="Cannot access directory"):
                file_handler.get_image_files(tmp_dir)

    def test_get_image_files_skips_invalid_files(self, file_handler):
        """Test that get_image_files skips invalid files with warning"""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)

            # Create valid image file
            valid_image = tmp_path / "valid.jpg"
            valid_image.write_bytes(b"fake image content")

            # Create file with image extension but invalid (too large)
            invalid_image = tmp_path / "invalid.jpg"
            large_content = b"0" * (50 * 1024 * 1024 + 1)  # Larger than max size
            invalid_image.write_bytes(large_content)

            with patch.object(file_handler.logger, "warning") as mock_warning:
                result = file_handler.get_image_files(tmp_path)

                # Should only return valid image
                assert len(result) == 1
                assert result[0] == valid_image

                # Should log warning for invalid file
                mock_warning.assert_called_once()
                assert "Skipping invalid file" in str(mock_warning.call_args)

    def test_round_numbers_in_dict_simple(self):
        """Test _round_numbers_in_dict with simple dictionary"""
        data = {
            "int_val": 42,
            "float_val": 3.14159,
            "bool_val": True,
            "str_val": "text",
        }

        result = FileHandler._round_numbers_in_dict(data.copy())

        assert result["int_val"] == 42  # Integers remain unchanged
        assert result["float_val"] == 3.14  # Floats rounded to 2 decimals
        assert result["bool_val"] is True  # Booleans remain unchanged
        assert result["str_val"] == "text"  # Strings remain unchanged

    def test_round_numbers_in_dict_nested(self):
        """Test _round_numbers_in_dict with nested structures"""
        data = {
            "level1": {
                "level2": {"float_val": 123.456789},
                "list_val": [1.234, 5.678, {"nested_float": 9.87654}],
            },
            "top_level_float": 2.71828,
        }

        result = FileHandler._round_numbers_in_dict(data.copy())

        assert result["level1"]["level2"]["float_val"] == 123.46
        assert result["level1"]["list_val"][0] == 1.23
        assert result["level1"]["list_val"][1] == 5.68
        assert result["level1"]["list_val"][2]["nested_float"] == 9.88
        assert result["top_level_float"] == 2.72

    def test_round_numbers_in_dict_list(self):
        """Test _round_numbers_in_dict with list input"""
        data = [1.234, 5.678, {"float_val": 9.87654}]

        result = FileHandler._round_numbers_in_dict(data.copy())

        assert result[0] == 1.23
        assert result[1] == 5.68
        assert result[2]["float_val"] == 9.88

    def test_round_numbers_in_dict_preserves_non_numeric(self):
        """Test that _round_numbers_in_dict preserves non-numeric values"""
        data = {
            "none_val": None,
            "empty_string": "",
            "zero": 0,
            "false": False,
            "empty_list": [],
            "empty_dict": {},
        }

        result = FileHandler._round_numbers_in_dict(data.copy())

        assert result["none_val"] is None
        assert result["empty_string"] == ""
        assert result["zero"] == 0
        assert result["false"] is False
        assert result["empty_list"] == []
        assert result["empty_dict"] == {}

    def test_round_numbers_in_dict_boolean_handling(self):
        """Test that booleans are not rounded (they inherit from int)"""
        data = {"true_val": True, "false_val": False}

        result = FileHandler._round_numbers_in_dict(data.copy())

        assert result["true_val"] is True
        assert result["false_val"] is False

    def test_logger_info_called_on_success(self, file_handler_with_logger):
        """Test that logger.info is called on successful operations"""
        with patch.object(file_handler_with_logger.logger, "info") as mock_info:
            test_data = {"test": "data"}

            with tempfile.TemporaryDirectory() as tmp_dir:
                output_path = Path(tmp_dir) / "test.json"
                file_handler_with_logger.save_json(test_data, output_path)

                mock_info.assert_called_once()
                assert "JSON saved successfully" in str(mock_info.call_args)

    def test_logger_info_called_on_text_save(self, file_handler_with_logger):
        """Test that logger.info is called on successful text save"""
        with patch.object(file_handler_with_logger.logger, "info") as mock_info:
            test_text = "test content"

            with tempfile.TemporaryDirectory() as tmp_dir:
                output_path = Path(tmp_dir) / "test.txt"
                file_handler_with_logger.save_text(test_text, output_path)

                mock_info.assert_called_once()
                assert "Text saved successfully" in str(mock_info.call_args)

    def test_save_json_with_string_path(self, file_handler):
        """Test save_json with string path instead of Path object"""
        test_data = {"test": "data"}

        with tempfile.TemporaryDirectory() as tmp_dir:
            output_path = str(Path(tmp_dir) / "test.json")  # String path
            result = file_handler.save_json(test_data, output_path)

            assert result is True
            assert Path(output_path).exists()

    def test_save_text_with_string_path(self, file_handler):
        """Test save_text with string path instead of Path object"""
        test_text = "test content"

        with tempfile.TemporaryDirectory() as tmp_dir:
            output_path = str(Path(tmp_dir) / "test.txt")  # String path
            result = file_handler.save_text(test_text, output_path)

            assert result is True
            assert Path(output_path).exists()

    def test_get_image_files_with_string_path(self, file_handler):
        """Test get_image_files with string path instead of Path object"""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)

            # Create test image file
            (tmp_path / "test.jpg").write_bytes(b"fake content")

            result = file_handler.get_image_files(str(tmp_dir))  # String path

            assert len(result) == 1
            assert result[0] == tmp_path / "test.jpg"
