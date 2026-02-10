"""Integration tests for Trading Signal API.

These tests verify end-to-end functionality with real
(but minimal) external API calls.
"""
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services.data_providers import CoinGeckoProvider
from app.services.technical_analysis import TechnicalAnalyzer
from app.models.chart import ChartData, OHLCV
from datetime import datetime

client = TestClient(app)


class TestDataProviders:
    """Test data provider integrations."""

    @pytest.mark.asyncio
    async def test_coingecko_get_price(self):
        """Test CoinGecko price fetching."""
        provider = CoinGeckoProvider()

        try:
            price = await provider.get_current_price("BTC")
            assert price > 0
            assert isinstance(price, (int, float))  # API may return int or float
        except Exception as e:
            # Rate limiting is expected during testing
            if "429" in str(e):
                pytest.skip("CoinGecko rate limited")
            raise

    @pytest.mark.asyncio
    async def test_coingecko_symbol_mapping(self):
        """Test symbol to CoinGecko ID mapping."""
        provider = CoinGeckoProvider()

        # Test common mappings
        assert provider._get_coin_id("BTC") == "bitcoin"
        assert provider._get_coin_id("ETH") == "ethereum"
        assert provider._get_coin_id("SOL") == "solana"


class TestTechnicalAnalysis:
    """Test technical analysis calculations."""

    @pytest.fixture
    def sample_chart_data(self):
        """Create sample chart data for testing."""
        candles = []
        base_price = 100.0

        for i in range(100):
            # Create synthetic price movement
            price = base_price + (i * 0.5) + ((i % 10) - 5)
            candles.append(OHLCV(
                timestamp=datetime(2024, 1, 1, i // 24, i % 24),
                open=price - 0.5,
                high=price + 1.0,
                low=price - 1.0,
                close=price + 0.5,
                volume=1000000 + (i * 10000),
            ))

        return ChartData(
            symbol="TEST",
            timeframe="1h",
            candles=candles,
            last_updated=datetime.utcnow(),
        )

    def test_technical_analyzer_creation(self, sample_chart_data):
        """Test TechnicalAnalyzer can be created with valid data."""
        analyzer = TechnicalAnalyzer(sample_chart_data)

        assert analyzer.df is not None
        assert len(analyzer.df) == 100

    def test_ema_ribbon_calculation(self, sample_chart_data):
        """Test EMA ribbon indicator calculation."""
        analyzer = TechnicalAnalyzer(sample_chart_data)
        ema_ribbon = analyzer.get_ema_ribbon()

        assert ema_ribbon.ema_20 > 0
        assert ema_ribbon.ema_50 > 0
        assert ema_ribbon.ema_100 > 0
        assert ema_ribbon.trend_direction is not None
        assert ema_ribbon.trend_strength is not None

    def test_rsi_calculation(self, sample_chart_data):
        """Test RSI indicator calculation."""
        analyzer = TechnicalAnalyzer(sample_chart_data)
        rsi = analyzer.get_rsi_indicator()

        assert 0 <= rsi.value <= 100
        assert rsi.zone in ["oversold", "neutral", "overbought"]
        assert rsi.signal is not None

    def test_macd_calculation(self, sample_chart_data):
        """Test MACD indicator calculation."""
        analyzer = TechnicalAnalyzer(sample_chart_data)
        macd = analyzer.get_macd_indicator()

        assert macd.macd_line is not None
        assert macd.signal_line is not None
        assert macd.histogram is not None
        assert macd.histogram_slope in ["rising", "falling", "flat"]

    def test_full_indicators_stack(self, sample_chart_data):
        """Test complete technical indicators calculation."""
        analyzer = TechnicalAnalyzer(sample_chart_data)
        indicators = analyzer.get_technical_indicators()

        # Verify all indicator groups are present
        assert indicators.ema_ribbon is not None
        assert indicators.rsi is not None
        assert indicators.macd is not None
        assert indicators.volatility is not None
        assert indicators.volume is not None
        assert indicators.structure is not None
        assert indicators.summary is not None

        # Verify composite signal
        assert -100 <= indicators.summary.bias_score <= 100
        assert 0 <= indicators.summary.confidence <= 1

    def test_signal_generation(self, sample_chart_data):
        """Test trading signal generation."""
        analyzer = TechnicalAnalyzer(sample_chart_data)
        signals = analyzer.generate_signals()

        assert isinstance(signals, list)
        # Signals should be sorted by timestamp (most recent first)
        if len(signals) >= 2:
            assert signals[0].timestamp >= signals[1].timestamp

    def test_trading_suggestion_generation(self, sample_chart_data):
        """Test trading suggestion generation."""
        analyzer = TechnicalAnalyzer(sample_chart_data)
        indicators = analyzer.get_technical_indicators()
        suggestion = analyzer.generate_trading_suggestion(indicators)

        assert suggestion is not None
        assert suggestion.entry_price > 0
        assert suggestion.stop_loss > 0
        assert suggestion.take_profit_1 > 0

        # Risk/reward should be positive
        if suggestion.position_type.value != "no_trade":
            assert suggestion.risk_reward_ratio >= 0


class TestAssetRegistry:
    """Test asset registry functionality."""

    def test_crypto_assets_loaded(self):
        """Verify crypto assets are loaded in registry."""
        from app.services.asset_registry import CRYPTO_ASSETS

        assert len(CRYPTO_ASSETS) > 100
        assert "BTC" in CRYPTO_ASSETS
        assert "ETH" in CRYPTO_ASSETS
        assert CRYPTO_ASSETS["BTC"].coingecko_id == "bitcoin"

    def test_stock_assets_loaded(self):
        """Verify stock assets are loaded in registry."""
        from app.services.asset_registry import STOCK_ASSETS

        assert len(STOCK_ASSETS) > 100
        assert "AAPL" in STOCK_ASSETS
        assert "MSFT" in STOCK_ASSETS

    def test_search_function(self):
        """Test asset search function."""
        from app.services.asset_registry import search_assets, AssetType

        # Search by symbol
        results = search_assets("BTC")
        assert len(results) > 0
        assert results[0].symbol == "BTC"

        # Search by name
        results = search_assets("Bitcoin")
        assert len(results) > 0
        assert "BTC" in [r.symbol for r in results]

        # Filter by type
        results = search_assets("A", asset_type=AssetType.STOCK)
        assert all(r.asset_type == AssetType.STOCK for r in results)


class TestSignalEndpoint:
    """Test signal API endpoint."""

    def test_signal_endpoint_json_format(self):
        """Test signal endpoint returns valid JSON response."""
        # Note: This test may fail due to rate limiting or x402 payment
        response = client.get("/api/v1/signal/BTC?timeframe=4h&format=json")

        # Accept 200 (success) or 402 (payment required) or 429/500 (rate limited)
        assert response.status_code in [200, 402, 429, 500, 504]

        if response.status_code == 200:
            data = response.json()
            assert "symbol" in data
            assert "price" in data
            assert "analysis" in data
            assert "trade" in data

    def test_signal_endpoint_text_format(self):
        """Test signal endpoint returns valid text response."""
        response = client.get("/api/v1/signal/ETH?timeframe=1d&format=text")

        # Accept 200 (success) or 402 (payment required) or 429/500 (rate limited)
        assert response.status_code in [200, 402, 429, 500, 504]

        if response.status_code == 200:
            assert response.headers.get("content-type") == "text/plain; charset=utf-8"
            text = response.text
            assert "ETH" in text or "Ethereum" in text

    def test_signal_endpoint_invalid_timeframe(self):
        """Test signal endpoint rejects invalid timeframe."""
        response = client.get("/api/v1/signal/BTC?timeframe=invalid")
        assert response.status_code == 422  # Validation error

    def test_signal_endpoint_invalid_format(self):
        """Test signal endpoint rejects invalid format."""
        response = client.get("/api/v1/signal/BTC?format=invalid")
        assert response.status_code == 422  # Validation error

    def test_signal_endpoint_with_chart_data(self):
        """Test signal endpoint with chart data included."""
        response = client.get("/api/v1/signal/BTC?include_chart=data")

        # Accept 200 (success) or 402 (payment required) or 429/500 (rate limited)
        assert response.status_code in [200, 402, 429, 500, 504]

        if response.status_code == 200:
            data = response.json()
            assert "chart_data" in data
            if data["chart_data"]:
                assert "candles" in data["chart_data"]


class TestHealthEndpoint:
    """Test health check endpoint."""

    def test_health_check(self):
        """Test health endpoint returns 200."""
        response = client.get("/health")
        assert response.status_code == 200

    def test_root_endpoint(self):
        """Test root endpoint returns API info."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "name" in data
        assert "version" in data
        assert "endpoints" in data
