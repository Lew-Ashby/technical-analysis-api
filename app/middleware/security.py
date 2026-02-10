"""Security middleware for rate limiting.

Note: API authentication is handled by x402 payment middleware.
"""
import logging

from slowapi import Limiter
from slowapi.util import get_remote_address

from app.config import settings

logger = logging.getLogger("trading_signal_api.security")

# Rate limiter with IP-based key function
limiter = Limiter(key_func=get_remote_address)


def get_rate_limit_signal() -> str:
    """Get rate limit string for signal endpoint."""
    return f"{settings.rate_limit_signal}/minute"


def get_rate_limit_chart() -> str:
    """Get rate limit string for chart endpoints."""
    return f"{settings.rate_limit_chart}/minute"


def get_rate_limit_assets() -> str:
    """Get rate limit string for asset endpoints."""
    return f"{settings.rate_limit_assets}/minute"
