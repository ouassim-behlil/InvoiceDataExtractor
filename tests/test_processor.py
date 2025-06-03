import pytest
from src._processor import Processor


def test_processor_initialization():
    """Test that Processor class can be initialized with an API key"""
    api_key = "test_key"
    processor = Processor(api_key)
    assert processor.client is not None
    assert isinstance(processor, Processor)
