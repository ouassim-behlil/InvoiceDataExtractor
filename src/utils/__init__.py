# src/utils/__init__.py
"""
Utilities Module

Contains utility classes and functions for file handling, validation, and other common operations.
"""

from .file_handler import FileHandler
from .validators import Validators, ValidationError

__all__ = [
    "FileHandler",
    "Validators", 
    "ValidationError",
]

# Utility constants
SUPPORTED_IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff'}
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
DEFAULT_JSON_INDENT = 2

# Validation patterns
API_KEY_PATTERN = r'^AIza[0-9A-Za-z_-]{35}$'