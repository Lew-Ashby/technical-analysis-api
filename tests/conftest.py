"""Pytest configuration and fixtures for Trading Chart API tests."""
import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture(scope="session")
def client():
    """Create a test client for the FastAPI application."""
    return TestClient(app)


@pytest.fixture
def sample_crypto_symbol():
    """Return a sample crypto symbol for testing."""
    return "BTC"


@pytest.fixture
def sample_stock_symbol():
    """Return a sample stock symbol for testing."""
    return "AAPL"


@pytest.fixture
def valid_timeframes():
    """Return list of valid timeframes."""
    return ["1m", "5m", "15m", "30m", "1h", "4h", "1d", "1w"]


@pytest.fixture
def invalid_inputs():
    """Return list of invalid/malicious inputs for security testing."""
    return [
        "'; DROP TABLE users;--",
        "<script>alert('xss')</script>",
        "../../../etc/passwd",
        "A" * 10000,
        "\x00\x01\x02",
        "{{7*7}}",
        "${7*7}",
        "|ls -la",
        "; cat /etc/passwd",
        "' OR '1'='1",
    ]
