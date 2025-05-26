# src/utils/file_handler.py
import json
import os
from pathlib import Path
from typing import Dict, Any, List, Union
import logging

from .validators import Validators, ValidationError


class FileHandler:
    """Utility class for file operations"""

    def __init__(self, logger: logging.Logger = None):
        self.logger = logger or logging.getLogger(__name__)

    def save_json(self, data: Dict[str, Any], output_path: Union[str, Path]) -> bool:
        """
        Save data as JSON file

        Args:
            data: Data to save
            output_path: Output file path

        Returns:
            bool: True if successful

        Raises:
            ValidationError: If operation fails
        """
        try:
            output_path = Path(output_path)

            # Validate output directory
            Validators.validate_directory(output_path.parent, create_if_missing=True)

            # Round numeric values
            rounded_data = self._round_numbers_in_dict(data.copy())

            # Save JSON
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(rounded_data, f, indent=2, ensure_ascii=False)

            self.logger.info(f"JSON saved successfully: {output_path}")
            return True

        except (IOError, OSError, TypeError) as e:
            raise ValidationError(f"Failed to save JSON to {output_path}: {e}")

    def save_text(self, text: str, output_path: Union[str, Path]) -> bool:
        """
        Save text to file

        Args:
            text: Text content
            output_path: Output file path

        Returns:
            bool: True if successful

        Raises:
            ValidationError: If operation fails
        """
        try:
            output_path = Path(output_path)

            # Validate output directory
            Validators.validate_directory(output_path.parent, create_if_missing=True)

            with open(output_path, "w", encoding="utf-8") as f:
                f.write(text)

            self.logger.info(f"Text saved successfully: {output_path}")
            return True

        except (IOError, OSError) as e:
            raise ValidationError(f"Failed to save text to {output_path}: {e}")

    def get_image_files(self, directory: Union[str, Path]) -> List[Path]:
        """
        Get list of image files in directory

        Args:
            directory: Directory path

        Returns:
            List[Path]: List of image file paths

        Raises:
            ValidationError: If directory is invalid
        """
        directory = Path(directory)
        Validators.validate_directory(directory)

        image_files = []

        try:
            for file_path in directory.iterdir():
                if file_path.is_file():
                    try:
                        Validators.validate_image_file(file_path)
                        image_files.append(file_path)
                    except ValidationError:
                        # Skip invalid files
                        self.logger.warning(f"Skipping invalid file: {file_path}")
                        continue
        except (OSError, PermissionError) as e:
            raise ValidationError(f"Cannot access directory {directory}: {e}")

        return sorted(image_files)

    @staticmethod
    def _round_numbers_in_dict(data: Union[Dict, List, Any]) -> Union[Dict, List, Any]:
        """
        Recursively round all numeric values to 2 decimals

        Args:
            data: Data structure to process

        Returns:
            Processed data structure
        """
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, (int, float)) and not isinstance(value, bool):
                    data[key] = round(value, 2)
                elif isinstance(value, (dict, list)):
                    data[key] = FileHandler._round_numbers_in_dict(value)
        elif isinstance(data, list):
            for i, item in enumerate(data):
                if isinstance(item, (int, float)) and not isinstance(item, bool):
                    data[i] = round(item, 2)
                elif isinstance(item, (dict, list)):
                    data[i] = FileHandler._round_numbers_in_dict(item)

        return data
