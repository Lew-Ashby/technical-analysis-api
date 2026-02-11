"""Signal response models for the APIX Signal API."""
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class PriceInfo(BaseModel):
    """Current price information."""

    current: float
    change_24h: float
    change_24h_pct: float


class AnalysisInfo(BaseModel):
    """Composite analysis summary."""

    bias_score: int = Field(ge=-100, le=100)
    confidence: float = Field(ge=0, le=1)
    signal: str
    regime: str
    entry_quality: str
    risk_level: str


class TrendInfo(BaseModel):
    """Trend analysis information."""

    direction: str
    strength: str
    ema_20: float
    ema_50: float
    ema_100: float
    price_position: str
    structure: str


class MomentumInfo(BaseModel):
    """Momentum indicators."""

    rsi: float
    rsi_zone: str
    macd_state: str
    macd_histogram: float
    histogram_slope: str


class VolumeInfo(BaseModel):
    """Volume analysis."""

    state: str
    relative: float
    confirmation: bool


class VolatilityInfo(BaseModel):
    """Volatility analysis."""

    state: str
    atr_pct: float
    squeeze: bool
    breakout_potential: str


class LevelsInfo(BaseModel):
    """Support and resistance levels."""

    support: List[float]
    resistance: List[float]


class TradeInfo(BaseModel):
    """Trading suggestion details."""

    position: str
    leverage: Optional[int] = None
    entry: float
    stop_loss: float
    take_profit_1: float
    take_profit_2: Optional[float] = None
    take_profit_3: Optional[float] = None
    risk_reward: float
    position_risk_pct: float
    invalidation: str


class SignalResponse(BaseModel):
    """Complete signal response matching APIX specification."""

    symbol: str
    timeframe: str
    timestamp: datetime
    price: PriceInfo
    analysis: AnalysisInfo
    trend: TrendInfo
    momentum: MomentumInfo
    volume: VolumeInfo
    volatility: VolatilityInfo
    levels: LevelsInfo
    trade: TradeInfo
    summary: str
