"""Analysis request/response models - Enhanced Indicator Stack."""
from datetime import datetime
from enum import Enum
from typing import List, Literal, Optional

from pydantic import BaseModel, Field


class Timeframe(str, Enum):
    """Supported chart timeframes."""

    M1 = "1m"
    M5 = "5m"
    M15 = "15m"
    M30 = "30m"
    H1 = "1h"
    H4 = "4h"
    D1 = "1d"
    W1 = "1w"


class SignalType(str, Enum):
    """Trading signal types."""

    BUY = "buy"
    SELL = "sell"
    HOLD = "hold"
    STRONG_BUY = "strong_buy"
    STRONG_SELL = "strong_sell"


class TrendDirection(str, Enum):
    """Trend direction classification."""

    BULLISH = "bullish"
    BEARISH = "bearish"
    NEUTRAL = "neutral"


class TrendStrength(str, Enum):
    """Trend strength classification."""

    WEAK = "weak"
    MODERATE = "moderate"
    STRONG = "strong"


class MomentumRegime(str, Enum):
    """Momentum regime classification."""

    BULLISH_EXTREME = "bullish_extreme"
    BULLISH_CONTINUATION = "bullish_continuation"
    NEUTRAL = "neutral"
    BEARISH_CONTINUATION = "bearish_continuation"
    BEARISH_EXTREME = "bearish_extreme"


class VolatilityState(str, Enum):
    """Volatility state classification."""

    CONTRACTING = "contracting"
    STABLE = "stable"
    EXPANDING = "expanding"


class VolumeState(str, Enum):
    """Volume trend classification."""

    ACCUMULATION = "accumulation"
    DISTRIBUTION = "distribution"
    NEUTRAL = "neutral"


class MarketStructure(str, Enum):
    """Market structure classification."""

    HIGHER_HIGHS = "higher_highs"
    LOWER_LOWS = "lower_lows"
    CONSOLIDATING = "consolidating"


class MarketRegime(str, Enum):
    """Overall market regime."""

    BULLISH_TREND = "bullish_trend"
    BEARISH_TREND = "bearish_trend"
    RANGE_BOUND = "range_bound"
    BREAKOUT = "breakout"
    BREAKDOWN = "breakdown"


# =============================================================================
# INDICATOR MODELS
# =============================================================================


class EMARibbon(BaseModel):
    """EMA Ribbon indicator for trend detection."""

    ema_20: float
    ema_50: float
    ema_100: float
    ema_200: Optional[float] = None
    trend_direction: TrendDirection
    trend_strength: TrendStrength
    price_position: str = Field(description="Price position relative to EMAs")
    ribbon_spread_pct: float = Field(description="Spread between fastest and slowest EMA")


class RSIIndicator(BaseModel):
    """Enhanced RSI with zones and divergence."""

    value: float
    regime: MomentumRegime
    zone: str = Field(description="oversold/neutral/overbought")
    divergence: bool = False
    divergence_type: Optional[str] = None  # bullish/bearish
    signal: SignalType


class MACDIndicator(BaseModel):
    """Enhanced MACD with histogram analysis."""

    macd_line: float
    signal_line: float
    histogram: float
    histogram_slope: str = Field(description="rising/falling/flat")
    zero_line_position: str = Field(description="above/below")
    state: str = Field(description="positive_acceleration/positive_deceleration/negative_acceleration/negative_deceleration")
    signal: SignalType


class VolatilityEngine(BaseModel):
    """Volatility analysis with ATR and Bollinger."""

    atr: float
    atr_pct: float = Field(description="ATR as percentage of price")
    state: VolatilityState
    bb_upper: float
    bb_middle: float
    bb_lower: float
    bb_width: float
    bb_pband: float = Field(description="Price position within bands (0-1)")
    squeeze: bool = Field(description="Bollinger squeeze detected")
    breakout_potential: str = Field(description="high/medium/low")


class VolumeAnalysis(BaseModel):
    """Volume analysis with OBV and confirmation."""

    current_volume: float
    avg_volume: float
    relative_volume: float = Field(description="Current vs average volume ratio")
    obv: float
    obv_trend: str = Field(description="rising/falling/flat")
    trend: VolumeState
    confirmation: bool = Field(description="Volume confirms price action")


class KeyLevel(BaseModel):
    """Support/Resistance level with strength."""

    price: float
    type: str = Field(description="support/resistance")
    strength: str = Field(description="weak/moderate/strong")
    touches: int = Field(description="Number of times tested")


class MarketStructureAnalysis(BaseModel):
    """Market structure layer for price action."""

    structure: MarketStructure
    last_swing_high: float
    last_swing_low: float
    last_bos: Optional[str] = Field(None, description="Last break of structure direction")
    bos_price: Optional[float] = None
    key_levels: List[KeyLevel]
    current_range: Optional[float] = Field(None, description="Range width if ranging")


class VWAPAnalysis(BaseModel):
    """VWAP with institutional bias."""

    vwap: float
    position: str = Field(description="above/below")
    deviation_pct: float = Field(description="Distance from VWAP as %")
    upper_band: float
    lower_band: float
    bias: TrendDirection


class CompositeSignal(BaseModel):
    """Composite signal engine output."""

    bias_score: int = Field(ge=-100, le=100, description="Overall bias from -100 to +100")
    confidence: float = Field(ge=0, le=1, description="Confidence score 0-1")
    regime: MarketRegime
    recommended_action: str
    risk_level: str = Field(description="low/medium/high")
    entry_quality: str = Field(description="poor/fair/good/excellent")


# =============================================================================
# AGGREGATED INDICATORS
# =============================================================================


class TechnicalIndicators(BaseModel):
    """Complete technical indicator stack."""

    # Trend Detection
    ema_ribbon: EMARibbon

    # Momentum & Exhaustion
    rsi: RSIIndicator
    macd: MACDIndicator

    # Volatility & Risk
    volatility: VolatilityEngine

    # Volume Confirmation
    volume: VolumeAnalysis

    # Market Structure
    structure: MarketStructureAnalysis

    # VWAP (optional - mainly for intraday)
    vwap: Optional[VWAPAnalysis] = None

    # Composite Signal
    summary: CompositeSignal


# =============================================================================
# LEGACY SUPPORT
# =============================================================================


class Indicator(BaseModel):
    """Legacy indicator format for backwards compatibility."""

    name: str
    value: float
    signal: SignalType
    description: str


class Signal(BaseModel):
    """Trading signal with timestamp and price."""

    type: SignalType
    price: float
    timestamp: datetime
    reason: str
    confidence: float = Field(default=0.5, ge=0, le=1)


# =============================================================================
# TRADING SUGGESTION MODEL
# =============================================================================


class PositionType(str, Enum):
    """Position type for trading suggestion."""

    LONG = "long"
    SHORT = "short"
    SPOT_BUY = "spot_buy"
    SPOT_SELL = "spot_sell"
    NO_TRADE = "no_trade"


class TradingSuggestion(BaseModel):
    """Comprehensive trading suggestion with levels."""

    # Position details
    position_type: PositionType
    leverage: Optional[int] = Field(None, ge=1, le=10, description="Leverage 1-10x, None for spot")
    is_futures: bool = Field(default=False, description="True if futures trade suggested")

    # Price levels
    entry_price: float
    stop_loss: float
    take_profit_1: float = Field(description="Conservative target")
    take_profit_2: Optional[float] = Field(None, description="Extended target")
    take_profit_3: Optional[float] = Field(None, description="Aggressive target")

    # Risk metrics
    risk_reward_ratio: float = Field(description="Risk/Reward ratio")
    position_risk_pct: float = Field(description="Risk as % of entry")
    suggested_position_size_pct: float = Field(description="Suggested position size as % of portfolio")

    # Reasoning
    reasoning: str = Field(description="Why this trade is suggested")
    invalidation: str = Field(description="When this trade idea is invalid")

    # Confidence
    trade_confidence: float = Field(ge=0, le=1, description="Confidence in this specific trade")
    warning: Optional[str] = Field(None, description="Risk warning if any")


# =============================================================================
# REQUEST/RESPONSE MODELS
# =============================================================================


class AnalysisRequest(BaseModel):
    """Request model for chart analysis."""

    symbol: str = Field(..., description="Trading symbol (e.g., BTC, AAPL, ETH)")
    timeframe: Timeframe = Field(default=Timeframe.H4, description="Chart timeframe")
    asset_type: Literal["crypto", "stock"] = Field(
        default="crypto", description="Asset type for data source selection"
    )
    include_chart: bool = Field(default=True, description="Include HTML chart in response")


class AnalysisResponse(BaseModel):
    """Enhanced response model for chart analysis."""

    symbol: str
    timeframe: str
    current_price: float
    price_change_24h: float
    price_change_pct_24h: float

    # Enhanced Technical Analysis
    indicators: TechnicalIndicators
    signals: List[Signal]

    # Composite Signal Summary
    bias_score: int = Field(ge=-100, le=100)
    confidence: float = Field(ge=0, le=1)
    regime: MarketRegime
    recommended_action: str

    # Rule-based Verbal Analysis
    verbal_analysis: str

    # Trading Suggestion
    suggestion: Optional[TradingSuggestion] = None

    # Chart HTML (optional)
    chart_html: Optional[str] = None

    # Metadata
    analyzed_at: datetime
    data_points: int
