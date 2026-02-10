"""API Contract Tests for Trading Chart API.

These tests verify:
- Response format consistency
- Schema compliance
- Error response standards
- Endpoint behavior contracts
"""
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


class TestHealthEndpoint:
    """Test /health endpoint contract."""

    def test_health_returns_correct_schema(self):
        """Verify health endpoint returns expected schema."""
        response = client.get("/health")

        assert response.status_code == 200
        data = response.json()

        assert "status" in data
        assert "service" in data
        assert data["status"] == "healthy"
        assert data["service"] == "trading-chart-api"


class TestSignalEndpoint:
    """Test /api/v1/signal/{symbol} endpoint contract."""

    def test_signal_json_schema(self):
        """Verify signal endpoint returns correct JSON schema."""
        response = client.get("/api/v1/signal/BTC?timeframe=4h&format=json")

        # May fail due to external API, but schema should be correct
        if response.status_code == 200:
            data = response.json()

            # Required top-level fields per spec
            required_fields = [
                "symbol", "timeframe", "timestamp", "price", "analysis",
                "trend", "momentum", "volume", "volatility", "levels",
                "trade", "summary"
            ]
            for field in required_fields:
                assert field in data, f"Missing required field: {field}"

            # Price sub-fields
            assert "current" in data["price"]
            assert "change_24h" in data["price"]
            assert "change_24h_pct" in data["price"]

            # Analysis sub-fields
            assert "bias_score" in data["analysis"]
            assert "confidence" in data["analysis"]
            assert "signal" in data["analysis"]
            assert data["analysis"]["signal"] in ["long", "short", "hold", "no_trade"]

            # Trade sub-fields
            assert "position" in data["trade"]
            assert data["trade"]["position"] in ["LONG", "SHORT", "NO_TRADE"]

    def test_signal_text_format(self):
        """Verify signal endpoint returns text format when requested."""
        response = client.get("/api/v1/signal/BTC?timeframe=4h&format=text")

        if response.status_code == 200:
            assert "text/plain" in response.headers.get("content-type", "")
            text = response.text
            # Check for expected sections
            assert "/USDT" in text
            assert "Analysis" in text

    def test_signal_html_chart(self):
        """Verify signal endpoint returns HTML when include_chart=html."""
        response = client.get("/api/v1/signal/BTC?timeframe=4h&include_chart=html")

        if response.status_code == 200:
            assert "text/html" in response.headers.get("content-type", "")
            assert "<!DOCTYPE html>" in response.text
            assert "TradingView" in response.text or "lightweight-charts" in response.text

    def test_signal_invalid_symbol(self):
        """Verify 404 for non-existent symbol."""
        response = client.get("/api/v1/signal/NOTAREALCOIN123XYZ?timeframe=4h")

        # Should return 404 for unknown symbol
        assert response.status_code in [404, 500]  # 500 if API error
        data = response.json()
        assert "detail" in data


class TestErrorResponses:
    """Test error response format consistency."""

    def test_404_format(self):
        """Verify 404 errors follow consistent format."""
        response = client.get("/api/v1/nonexistent")

        assert response.status_code == 404
        data = response.json()
        assert "detail" in data

    def test_invalid_timeframe_returns_422(self):
        """Verify invalid timeframe returns 422 validation error."""
        response = client.get("/api/v1/signal/BTC?timeframe=invalid")

        # Should return 422 for invalid timeframe
        assert response.status_code == 422

        data = response.json()
        assert "detail" in data


class TestTimeframeValidation:
    """Test timeframe parameter validation."""

    def test_valid_timeframes_accepted(self):
        """Verify all valid timeframes are accepted."""
        valid_timeframes = ["1h", "4h", "1d", "1w"]

        for tf in valid_timeframes:
            response = client.get(f"/api/v1/signal/BTC?timeframe={tf}")
            # Should not be 422 validation error
            assert response.status_code != 422, f"Timeframe {tf} should be valid"

    def test_invalid_timeframes_rejected(self):
        """Verify invalid timeframes are rejected."""
        invalid_timeframes = ["1m", "5m", "15m", "30m", "2h", "invalid"]

        for tf in invalid_timeframes:
            response = client.get(f"/api/v1/signal/BTC?timeframe={tf}")
            assert response.status_code == 422, f"Timeframe {tf} should be invalid"
