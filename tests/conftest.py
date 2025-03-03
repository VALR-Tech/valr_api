"""
Pytest fixtures for VALR API tests
"""

import pytest

from valr_api.client import ValrClient


@pytest.fixture
def client():
    """Create a VALR API client for testing"""
    return ValrClient(
        api_key="test_api_key",
        api_secret="test_api_secret",
        base_url="https://api.valr.com",
    )


@pytest.fixture
def unauthenticated_client():
    """Create an unauthenticated VALR API client for testing"""
    return ValrClient(base_url="https://api.valr.com")
