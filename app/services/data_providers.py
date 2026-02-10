"""Data provider for fetching crypto market data from CoinGecko."""
import asyncio
import logging
from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional

import httpx
import pandas as pd

from app.models.chart import ChartData, OHLCV
from app.services.asset_registry import get_coingecko_id
from app.services.cache import (
    get_cached_ohlcv,
    get_cached_price,
    set_cached_ohlcv,
    set_cached_price,
)

logger = logging.getLogger("trading_signal_api.data_providers")


class DataProvider(ABC):
    """Abstract base class for data providers."""

    @abstractmethod
    async def fetch_ohlcv(
        self, symbol: str, timeframe: str, limit: int = 100
    ) -> ChartData:
        """Fetch OHLCV data for a symbol."""
        pass

    @abstractmethod
    async def get_current_price(self, symbol: str) -> float:
        """Get current price for a symbol."""
        pass

    @abstractmethod
    async def get_price_change_24h(self, symbol: str) -> tuple[float, float]:
        """Get 24h price change (absolute and percentage)."""
        pass


class CoinGeckoProvider(DataProvider):
    """CoinGecko API provider for crypto data with proper volume support."""

    BASE_URL = "https://api.coingecko.com/api/v3"

    # Days to fetch for each timeframe
    # CoinGecko /ohlc valid values: 1, 7, 14, 30, 90, 180, 365, max
    # Granularity:
    #   1 day = 30 minute candles (48 candles)
    #   7-30 days = 4 hour candles
    #   31-365 days = 4 day candles
    TIMEFRAME_DAYS = {
        "1h": 7,   # Gets 4h candles (~42), display as-is (shows ~7 days)
        "4h": 30,  # Gets 4h candles directly (~180 candles, 30 days)
        "1d": 90,  # Use /ohlc endpoint, aggregate 4-day to daily
        "1w": 365, # Use /ohlc endpoint, aggregate to weekly
    }

    # Whether to use /ohlc (True) or market_chart (False) for each timeframe
    USE_OHLC = {
        "1h": True,   # /ohlc gives 4h candles which we display
        "4h": True,   # /ohlc gives 4h candles directly
        "1d": True,   # /ohlc gives 4-day candles, aggregate to daily
        "1w": True,   # /ohlc gives 4-day candles, aggregate to weekly
    }

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.client = httpx.AsyncClient(timeout=30.0)
        self._owns_client = True

    async def close(self) -> None:
        """Close the HTTP client and release resources."""
        if self._owns_client and self.client is not None:
            await self.client.aclose()
            self.client = None

    async def __aenter__(self) -> "CoinGeckoProvider":
        """Async context manager entry."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Async context manager exit - ensures client is closed."""
        await self.close()

    def _get_coin_id(self, symbol: str) -> str:
        """Convert symbol to CoinGecko ID using the asset registry."""
        symbol_upper = symbol.upper().replace("-USD", "").replace("USDT", "")
        coin_id = get_coingecko_id(symbol_upper)
        return coin_id if coin_id else symbol.lower()

    async def fetch_ohlcv(
        self, symbol: str, timeframe: str, limit: int = 200
    ) -> ChartData:
        """Fetch OHLCV data from CoinGecko with proper volume."""
        # Check cache first
        cached = get_cached_ohlcv(symbol, timeframe)
        if cached:
            logger.debug(f"Cache hit for OHLCV {symbol}/{timeframe}")
            return cached

        coin_id = self._get_coin_id(symbol)
        days = self.TIMEFRAME_DAYS.get(timeframe, 30)

        # Use /ohlc endpoint for all timeframes (provides real candlestick data)
        result = await self._fetch_ohlcv_with_real_candles(
            coin_id=coin_id,
            symbol=symbol,
            timeframe=timeframe,
            days=days,
            limit=limit,
        )
        set_cached_ohlcv(symbol, timeframe, result)
        return result

    async def _fetch_ohlcv_with_real_candles(
        self,
        coin_id: str,
        symbol: str,
        timeframe: str,
        days: int,
        limit: int,
    ) -> ChartData:
        """Fetch OHLCV using /ohlc endpoint for real candlestick data."""
        ohlc_url = f"{self.BASE_URL}/coins/{coin_id}/ohlc"
        ohlc_params = {"vs_currency": "usd", "days": days}

        volume_url = f"{self.BASE_URL}/coins/{coin_id}/market_chart"
        volume_params = {"vs_currency": "usd", "days": days}

        if self.api_key:
            ohlc_params["x_cg_pro_api_key"] = self.api_key
            volume_params["x_cg_pro_api_key"] = self.api_key

        # Fetch OHLC and volume data in parallel
        ohlc_response, volume_response = await asyncio.gather(
            self.client.get(ohlc_url, params=ohlc_params),
            self.client.get(volume_url, params=volume_params),
        )

        ohlc_response.raise_for_status()
        ohlc_data = ohlc_response.json()

        if not ohlc_data:
            raise ValueError(f"No OHLC data found for {symbol}")

        volume_response.raise_for_status()
        volume_data = volume_response.json()

        volumes = volume_data.get("total_volumes", [])

        # Build volume lookup (by date)
        volume_df = None
        if volumes:
            volume_df = pd.DataFrame(volumes, columns=["timestamp", "volume"])
            volume_df["timestamp"] = pd.to_datetime(volume_df["timestamp"], unit="ms")
            volume_df["date"] = volume_df["timestamp"].dt.date
            volume_df = volume_df.groupby("date")["volume"].sum()

        candles = []
        for item in ohlc_data:
            timestamp_ms, open_price, high, low, close = item
            ts = datetime.fromtimestamp(timestamp_ms / 1000)

            volume = 0.0
            if volume_df is not None:
                date_key = ts.date()
                if date_key in volume_df.index:
                    volume = float(volume_df[date_key])

            candles.append(
                OHLCV(
                    timestamp=ts,
                    open=float(open_price),
                    high=float(high),
                    low=float(low),
                    close=float(close),
                    volume=volume,
                )
            )

        # Aggregate candles based on timeframe
        # Note: CoinGecko /ohlc gives 4h candles for 7-30 day requests
        if timeframe == "1d":
            # 4-day candles -> daily candles (approximate)
            candles = self._aggregate_candles(candles, "1D")
        elif timeframe == "1w":
            # 4-day candles -> weekly candles
            candles = self._aggregate_candles(candles, "1W")
        # 1h and 4h: Display the 4h candles as-is (best available from free API)

        candles = candles[-limit:]

        return ChartData(
            symbol=symbol,
            timeframe=timeframe,
            candles=candles,
            last_updated=datetime.utcnow(),
        )

    def _aggregate_candles(self, candles: List[OHLCV], rule: str) -> List[OHLCV]:
        """Aggregate candles to a larger timeframe using pandas resample."""
        if not candles:
            return []

        df = pd.DataFrame([
            {
                "timestamp": c.timestamp,
                "open": c.open,
                "high": c.high,
                "low": c.low,
                "close": c.close,
                "volume": c.volume,
            }
            for c in candles
        ])
        df.set_index("timestamp", inplace=True)

        aggregated = df.resample(rule).agg({
            "open": "first",
            "high": "max",
            "low": "min",
            "close": "last",
            "volume": "sum",
        }).dropna()

        return [
            OHLCV(
                timestamp=idx.to_pydatetime(),
                open=float(row["open"]),
                high=float(row["high"]),
                low=float(row["low"]),
                close=float(row["close"]),
                volume=float(row["volume"]),
            )
            for idx, row in aggregated.iterrows()
        ]

    def _aggregate_to_ohlcv(
        self,
        prices: List[List],
        volumes: List[List],
        timeframe: str,
        limit: int,
    ) -> List[OHLCV]:
        """Aggregate price/volume data into OHLCV candles."""
        if not prices:
            return []

        df = pd.DataFrame(prices, columns=["timestamp", "price"])
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        df.set_index("timestamp", inplace=True)

        if volumes:
            vol_df = pd.DataFrame(volumes, columns=["timestamp", "volume"])
            vol_df["timestamp"] = pd.to_datetime(vol_df["timestamp"], unit="ms")
            vol_df.set_index("timestamp", inplace=True)
            df = df.join(vol_df, how="left")
            df["volume"] = df["volume"].fillna(0)
        else:
            df["volume"] = 0

        resample_rules = {
            "1h": "1h",
            "4h": "4h",
            "1d": "1D",
            "1w": "1W",
        }
        rule = resample_rules.get(timeframe, "4h")

        ohlcv = df["price"].resample(rule).agg({
            "open": "first",
            "high": "max",
            "low": "min",
            "close": "last",
        })

        vol_resampled = df["volume"].resample(rule).sum()
        ohlcv["volume"] = vol_resampled

        ohlcv = ohlcv.dropna()
        ohlcv = ohlcv.tail(limit)

        candles = []
        for idx, row in ohlcv.iterrows():
            candles.append(
                OHLCV(
                    timestamp=idx.to_pydatetime(),
                    open=float(row["open"]),
                    high=float(row["high"]),
                    low=float(row["low"]),
                    close=float(row["close"]),
                    volume=float(row["volume"]),
                )
            )

        return candles

    async def get_current_price(self, symbol: str) -> float:
        """Get current price from CoinGecko."""
        cached = get_cached_price(symbol)
        if cached is not None:
            return cached

        coin_id = self._get_coin_id(symbol)
        url = f"{self.BASE_URL}/simple/price"
        params = {"ids": coin_id, "vs_currencies": "usd"}

        response = await self.client.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        price = data.get(coin_id, {}).get("usd", 0.0)

        set_cached_price(symbol, price)
        return price

    async def get_price_change_24h(self, symbol: str) -> tuple[float, float]:
        """Get 24h price change (absolute and percentage)."""
        coin_id = self._get_coin_id(symbol)
        url = f"{self.BASE_URL}/simple/price"
        params = {
            "ids": coin_id,
            "vs_currencies": "usd",
            "include_24hr_change": "true",
        }

        response = await self.client.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        coin_data = data.get(coin_id, {})
        current_price = coin_data.get("usd", 0.0)
        change_pct = coin_data.get("usd_24h_change", 0.0)
        change_abs = current_price * (change_pct / 100)

        return change_abs, change_pct


def get_provider(api_key: Optional[str] = None) -> CoinGeckoProvider:
    """Get the CoinGecko data provider."""
    return CoinGeckoProvider(api_key=api_key)
