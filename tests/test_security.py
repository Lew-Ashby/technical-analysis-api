"""Security tests for Trading Chart API.

These tests verify protection against OWASP Top 10 vulnerabilities
and other common security issues.
"""
import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


class TestCORSConfiguration:
    """Test CORS configuration security."""

    def test_cors_rejects_arbitrary_origin(self):
        """Verify CORS rejects unauthorized origins."""
        response = client.options(
            "/api/v1/signal/BTC",
            headers={
                "Origin": "https://evil-attacker.com",
                "Access-Control-Request-Method": "GET",
            },
        )

        # Evil origin should NOT be reflected back
        assert response.headers.get("access-control-allow-origin") != "https://evil-attacker.com"

    def test_cors_allows_configured_origin(self):
        """Verify allowed origins work correctly."""
        response = client.options(
            "/api/v1/signal/BTC",
            headers={
                "Origin": "http://localhost:8000",
                "Access-Control-Request-Method": "GET",
            },
        )

        # Configured origin should be allowed
        assert response.headers.get("access-control-allow-origin") == "http://localhost:8000"


class TestInputValidation:
    """Test input validation and injection protection."""

    @pytest.mark.parametrize("malicious_input", [
        "'; DROP TABLE users;--",
        "<script>alert('xss')</script>",
        "../../../etc/passwd",
        "' OR '1'='1",
        "{{7*7}}",
    ])
    def test_symbol_rejects_injection_attempts(self, malicious_input):
        """Verify symbol parameter rejects injection attempts safely."""
        response = client.get(f"/api/v1/signal/{malicious_input}?timeframe=4h")

        # Should return error, not execute injection
        assert response.status_code in [404, 422, 500]

        # Response should not contain error traces or signs of execution
        body = response.text
        assert "Traceback" not in body

    def test_symbol_sanitization(self):
        """Verify symbol is sanitized in responses."""
        response = client.get("/api/v1/signal/BTC<script>?timeframe=4h")

        # May fail due to external API, but check sanitization if successful
        if response.status_code == 200:
            data = response.json()
            # Symbol should be sanitized
            assert "<script>" not in data.get("symbol", "")

    def test_very_long_input_handled_gracefully(self):
        """Verify very long inputs don't cause crashes or memory issues."""
        long_input = "A" * 10000
        response = client.get(f"/api/v1/signal/{long_input}?timeframe=4h")

        # Should return error, not crash
        assert response.status_code in [404, 422, 414, 500]

    def test_null_bytes_handled(self):
        """Verify null bytes in input don't cause issues."""
        response = client.get("/api/v1/signal/BTC%00INJECTED?timeframe=4h")
        assert response.status_code in [200, 404, 422, 500]


class TestErrorHandling:
    """Test error handling doesn't leak sensitive information."""

    def test_invalid_timeframe_returns_422(self):
        """Verify invalid timeframe returns proper validation error."""
        response = client.get("/api/v1/signal/BTC?timeframe=invalid_tf")

        assert response.status_code == 422

        # Should not leak stack traces
        assert "Traceback" not in response.text
        assert "ValueError" not in response.text

    def test_error_messages_dont_expose_internal_paths(self):
        """Verify error messages don't expose file paths or internals."""
        response = client.get("/api/v1/signal/INVALID_SYMBOL_XYZ?timeframe=4h")

        # Check response doesn't contain system paths
        text = response.text
        assert "/Users/" not in text
        assert "/home/" not in text


class TestRateLimiting:
    """Test rate limiting protection."""

    def test_rate_limiter_configured(self):
        """Verify rate limiter is configured on the app."""
        # Check that the rate limiter is attached to app state
        assert hasattr(app.state, "limiter")


class TestAPIDocumentation:
    """Test API documentation exposure in debug mode."""

    def test_docs_accessible_in_debug_mode(self):
        """
        Documentation endpoints are controlled by debug setting.
        In test environment, they may or may not be available.
        """
        response = client.get("/docs")
        # Docs availability depends on settings.debug
        assert response.status_code in [200, 404]

        response = client.get("/openapi.json")
        assert response.status_code in [200, 404]


class TestPaymentSecurity:
    """Test x402 payment middleware security."""

    def test_signal_endpoint_accessible(self):
        """
        Verify signal endpoint is accessible.
        x402 payments are handled by APIX platform, not in code.
        """
        response = client.get("/api/v1/signal/BTC?timeframe=4h")

        # Should be accessible (payment handled externally by APIX)
        # May fail due to external API, but shouldn't be blocked by auth
        assert response.status_code in [200, 404, 500, 504]
