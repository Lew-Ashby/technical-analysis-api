"""Chart data models."""
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class OHLCV(BaseModel):
    """OHLCV candlestick data."""

    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float


class ChartData(BaseModel):
    """Chart data with OHLCV candles."""

    symbol: str
    timeframe: str
    candles: List[OHLCV]
    last_updated: datetime


class ChartResponse(BaseModel):
    """Response containing chart HTML."""

    symbol: str
    timeframe: str
    chart_html: str
    indicators_html: Optional[str] = None
