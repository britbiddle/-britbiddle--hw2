"""
Pytest configuration and fixtures for the Numeric Converter test suite.
"""
import sys
import os
import pytest
from flask import Flask

# Add the api directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'api'))

from index import app

@pytest.fixture
def client():
    """Create a test client for the Flask application."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def sample_numbers():
    """Provide a set of test numbers for conversion testing."""
    return {
        'small': 42,
        'medium': 1234,
        'large': 98765,
        'zero': 0,
        'one': 1,
        'negative': -42,
        'max_byte': 255,
        'max_short': 65535
    }

@pytest.fixture
def sample_text_numbers():
    """Provide text representations of numbers for testing."""
    return {
        0: 'zero',
        1: 'one',
        42: 'forty-two',
        123: 'one hundred and twenty-three',
        1000: 'one thousand'
    }
