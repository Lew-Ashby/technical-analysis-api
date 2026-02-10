"""In-memory caching service for API responses."""
import hashlib
import logging
from functools import wraps
from typing import Any, Callable, Optional

from cachetools import TTLCache

from app.config import settings

logger = logging.getLogger("trading_chart_api.cache")

# Global cache instances
_price_cache: TTLCache = TTLCache(
    maxsize=settings.cache_max_size,
    ttl=60,  # 1 minute for prices
)

_ohlcv_cache: TTLCache = TTLCache(
    maxsize=settings.cache_max_size,
    ttl=settings.cache_ttl_seconds,  # 5 minutes for OHLCV data
)

_analysis_cache: TTLCache = TTLCache(
    maxsize=settings.cache_max_size // 2,
    ttl=settings.cache_ttl_seconds,  # 5 minutes for analysis
)


def _make_cache_key(*args, **kwargs) -> str:
    """Generate a cache key from function arguments."""
    key_parts = [str(arg) for arg in args]
    key_parts.extend(f"{k}={v}" for k, v in sorted(kwargs.items()))
    key_string = ":".join(key_parts)
    return hashlib.md5(key_string.encode()).hexdigest()


def get_cached_price(symbol: str) -> Optional[float]:
    """Get cached price for a symbol."""
    return _price_cache.get(symbol.upper())


def set_cached_price(symbol: str, price: float) -> None:
    """Cache a price for a symbol."""
    _price_cache[symbol.upper()] = price
    logger.debug(f"Cached price for {symbol}: {price}")


def get_cached_ohlcv(symbol: str, timeframe: str) -> Optional[Any]:
    """Get cached OHLCV data."""
    key = f"{symbol.upper()}:{timeframe}"
    return _ohlcv_cache.get(key)


def set_cached_ohlcv(symbol: str, timeframe: str, data: Any) -> None:
    """Cache OHLCV data."""
    key = f"{symbol.upper()}:{timeframe}"
    _ohlcv_cache[key] = data
    logger.debug(f"Cached OHLCV for {key}")


def get_cached_analysis(symbol: str, timeframe: str, asset_type: str) -> Optional[Any]:
    """Get cached analysis response."""
    key = f"{symbol.upper()}:{timeframe}:{asset_type}"
    return _analysis_cache.get(key)


def set_cached_analysis(
    symbol: str, timeframe: str, asset_type: str, data: Any
) -> None:
    """Cache analysis response."""
    key = f"{symbol.upper()}:{timeframe}:{asset_type}"
    _analysis_cache[key] = data
    logger.debug(f"Cached analysis for {key}")


def cache_stats() -> dict:
    """Get cache statistics."""
    return {
        "price_cache": {
            "size": len(_price_cache),
            "maxsize": _price_cache.maxsize,
        },
        "ohlcv_cache": {
            "size": len(_ohlcv_cache),
            "maxsize": _ohlcv_cache.maxsize,
        },
        "analysis_cache": {
            "size": len(_analysis_cache),
            "maxsize": _analysis_cache.maxsize,
        },
    }


def clear_cache() -> None:
    """Clear all caches."""
    _price_cache.clear()
    _ohlcv_cache.clear()
    _analysis_cache.clear()
    logger.info("All caches cleared")
