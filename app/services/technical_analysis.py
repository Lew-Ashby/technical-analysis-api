"""Enhanced Technical Analysis Engine - Production Indicator Stack."""
from datetime import datetime
from typing import List, Optional, Tuple

import numpy as np
import pandas as pd
import ta

from app.models.analysis import (
    CompositeSignal,
    EMARibbon,
    KeyLevel,
    MACDIndicator,
    MarketRegime,
    MarketStructure,
    MarketStructureAnalysis,
    MomentumRegime,
    PositionType,
    RSIIndicator,
    Signal,
    SignalType,
    TechnicalIndicators,
    TradingSuggestion,
    TrendDirection,
    TrendStrength,
    VolatilityEngine,
    VolatilityState,
    VolumeAnalysis,
    VolumeState,
    VWAPAnalysis,
)
from app.models.chart import ChartData


class TechnicalAnalyzer:
    """Enhanced technical analyzer with production indicator stack."""

    def __init__(self, chart_data: ChartData):
        self.chart_data = chart_data
        self.df = self._to_dataframe()
        self._compute_all_indicators()

    def _to_dataframe(self) -> pd.DataFrame:
        """Convert chart data to pandas DataFrame."""
        data = [
            {
                "timestamp": c.timestamp,
                "open": c.open,
                "high": c.high,
                "low": c.low,
                "close": c.close,
                "volume": c.volume,
            }
            for c in self.chart_data.candles
        ]
        df = pd.DataFrame(data)
        df.set_index("timestamp", inplace=True)
        return df

    def _compute_all_indicators(self) -> None:
        """Compute all technical indicators."""
        close = self.df["close"]
        high = self.df["high"]
        low = self.df["low"]
        volume = self.df["volume"]

        # =================================================================
        # EMA RIBBON
        # =================================================================
        self.df["ema_20"] = ta.trend.EMAIndicator(close, window=20).ema_indicator()
        self.df["ema_50"] = ta.trend.EMAIndicator(close, window=50).ema_indicator()
        self.df["ema_100"] = ta.trend.EMAIndicator(close, window=100).ema_indicator()
        if len(close) >= 200:
            self.df["ema_200"] = ta.trend.EMAIndicator(close, window=200).ema_indicator()
        else:
            self.df["ema_200"] = np.nan

        # =================================================================
        # RSI
        # =================================================================
        self.df["rsi"] = ta.momentum.RSIIndicator(close, window=14).rsi()

        # =================================================================
        # MACD
        # =================================================================
        macd = ta.trend.MACD(close)
        self.df["macd"] = macd.macd()
        self.df["macd_signal"] = macd.macd_signal()
        self.df["macd_histogram"] = macd.macd_diff()

        # =================================================================
        # BOLLINGER BANDS
        # =================================================================
        bb = ta.volatility.BollingerBands(close, window=20, window_dev=2)
        self.df["bb_upper"] = bb.bollinger_hband()
        self.df["bb_middle"] = bb.bollinger_mavg()
        self.df["bb_lower"] = bb.bollinger_lband()
        self.df["bb_pband"] = bb.bollinger_pband()
        self.df["bb_width"] = bb.bollinger_wband()

        # =================================================================
        # ATR
        # =================================================================
        self.df["atr"] = ta.volatility.AverageTrueRange(high, low, close, window=14).average_true_range()

        # =================================================================
        # VOLUME INDICATORS
        # =================================================================
        self.df["volume_sma"] = volume.rolling(window=20).mean()
        self.df["obv"] = ta.volume.OnBalanceVolumeIndicator(close, volume).on_balance_volume()

        # =================================================================
        # VWAP (cumulative for session)
        # =================================================================
        typical_price = (high + low + close) / 3
        cumulative_vol = volume.cumsum()
        cumulative_vol = cumulative_vol.replace(0, np.nan)  # Avoid division by zero
        self.df["vwap"] = (typical_price * volume).cumsum() / cumulative_vol
        # VWAP standard deviation
        squared_diff = (close - self.df["vwap"]) ** 2
        self.df["vwap_std"] = np.sqrt((squared_diff * volume).cumsum() / cumulative_vol)

    # =========================================================================
    # EMA RIBBON
    # =========================================================================

    def get_ema_ribbon(self) -> EMARibbon:
        """Calculate EMA Ribbon with trend direction and strength."""
        close = self.df["close"].iloc[-1]
        ema_20 = self.df["ema_20"].iloc[-1]
        ema_50 = self.df["ema_50"].iloc[-1]
        ema_100 = self.df["ema_100"].iloc[-1]
        ema_200_val = self.df["ema_200"].iloc[-1]
        ema_200 = ema_200_val if not pd.isna(ema_200_val) else None

        # Determine trend direction
        emas_available = [ema_20, ema_50, ema_100]
        if ema_200:
            emas_available.append(ema_200)

        bullish_count = sum(1 for i in range(len(emas_available) - 1) if emas_available[i] > emas_available[i + 1])

        if bullish_count >= len(emas_available) - 1:
            trend_direction = TrendDirection.BULLISH
        elif bullish_count <= 0:
            trend_direction = TrendDirection.BEARISH
        else:
            trend_direction = TrendDirection.NEUTRAL

        # Determine trend strength based on alignment and separation
        base_ema = ema_200 if ema_200 else ema_100
        ribbon_spread = abs(ema_20 - base_ema) / close * 100

        if ribbon_spread > 5:
            trend_strength = TrendStrength.STRONG
        elif ribbon_spread > 2:
            trend_strength = TrendStrength.MODERATE
        else:
            trend_strength = TrendStrength.WEAK

        # Price position
        if close > ema_20 > ema_50:
            price_position = "above_all_bullish"
        elif close < ema_20 < ema_50:
            price_position = "below_all_bearish"
        elif close > ema_50:
            price_position = "above_ema50"
        else:
            price_position = "below_ema50"

        return EMARibbon(
            ema_20=ema_20,
            ema_50=ema_50,
            ema_100=ema_100,
            ema_200=ema_200,
            trend_direction=trend_direction,
            trend_strength=trend_strength,
            price_position=price_position,
            ribbon_spread_pct=ribbon_spread,
        )

    # =========================================================================
    # RSI
    # =========================================================================

    def get_rsi_indicator(self) -> RSIIndicator:
        """Calculate enhanced RSI with zones and divergence detection."""
        rsi = self.df["rsi"].iloc[-1]

        if pd.isna(rsi):
            rsi = 50.0

        # Zone classification
        if rsi < 30:
            zone = "oversold"
        elif rsi > 70:
            zone = "overbought"
        else:
            zone = "neutral"

        # Momentum regime
        if rsi > 70:
            regime = MomentumRegime.BULLISH_EXTREME
        elif rsi > 60:
            regime = MomentumRegime.BULLISH_CONTINUATION
        elif rsi < 30:
            regime = MomentumRegime.BEARISH_EXTREME
        elif rsi < 40:
            regime = MomentumRegime.BEARISH_CONTINUATION
        else:
            regime = MomentumRegime.NEUTRAL

        # Divergence detection
        divergence = False
        divergence_type = None

        if len(self.df) >= 14:
            price_series = self.df["close"].tail(14)
            rsi_series = self.df["rsi"].tail(14).dropna()

            if len(rsi_series) >= 5:
                # Bullish divergence: price making lower lows, RSI making higher lows
                price_min = price_series.min()
                price_recent_min = price_series.iloc[-5:].min()
                rsi_min = rsi_series.min()
                rsi_recent_min = rsi_series.iloc[-5:].min() if len(rsi_series) >= 5 else rsi_min

                if price_recent_min <= price_min and rsi_recent_min > rsi_min:
                    divergence = True
                    divergence_type = "bullish"

                # Bearish divergence: price making higher highs, RSI making lower highs
                price_max = price_series.max()
                price_recent_max = price_series.iloc[-5:].max()
                rsi_max = rsi_series.max()
                rsi_recent_max = rsi_series.iloc[-5:].max() if len(rsi_series) >= 5 else rsi_max

                if price_recent_max >= price_max and rsi_recent_max < rsi_max:
                    divergence = True
                    divergence_type = "bearish"

        # Signal
        if rsi < 30:
            signal = SignalType.BUY
        elif rsi > 70:
            signal = SignalType.SELL
        elif divergence and divergence_type == "bullish":
            signal = SignalType.BUY
        elif divergence and divergence_type == "bearish":
            signal = SignalType.SELL
        else:
            signal = SignalType.HOLD

        return RSIIndicator(
            value=rsi,
            regime=regime,
            zone=zone,
            divergence=divergence,
            divergence_type=divergence_type,
            signal=signal,
        )

    # =========================================================================
    # MACD
    # =========================================================================

    def get_macd_indicator(self) -> MACDIndicator:
        """Calculate enhanced MACD with histogram analysis."""
        macd = self.df["macd"].iloc[-1]
        signal_line = self.df["macd_signal"].iloc[-1]
        histogram = self.df["macd_histogram"].iloc[-1]

        if pd.isna(macd) or pd.isna(signal_line):
            return MACDIndicator(
                macd_line=0.0,
                signal_line=0.0,
                histogram=0.0,
                histogram_slope="flat",
                zero_line_position="below",
                state="neutral",
                signal=SignalType.HOLD,
            )

        # Histogram slope
        if len(self.df) > 1:
            prev_histogram = self.df["macd_histogram"].iloc[-2]
            if pd.isna(prev_histogram):
                histogram_slope = "flat"
            elif histogram > prev_histogram:
                histogram_slope = "rising"
            elif histogram < prev_histogram:
                histogram_slope = "falling"
            else:
                histogram_slope = "flat"
        else:
            histogram_slope = "flat"

        # Zero line position
        zero_line_position = "above" if macd > 0 else "below"

        # State classification
        if histogram > 0 and histogram_slope == "rising":
            state = "positive_acceleration"
        elif histogram > 0 and histogram_slope == "falling":
            state = "positive_deceleration"
        elif histogram < 0 and histogram_slope == "falling":
            state = "negative_acceleration"
        elif histogram < 0 and histogram_slope == "rising":
            state = "negative_deceleration"
        else:
            state = "neutral"

        # Signal
        prev_histogram = self.df["macd_histogram"].iloc[-2] if len(self.df) > 1 else 0
        if not pd.isna(prev_histogram):
            if histogram > 0 and prev_histogram <= 0:
                signal = SignalType.STRONG_BUY
            elif histogram < 0 and prev_histogram >= 0:
                signal = SignalType.STRONG_SELL
            elif histogram > 0:
                signal = SignalType.BUY
            elif histogram < 0:
                signal = SignalType.SELL
            else:
                signal = SignalType.HOLD
        else:
            signal = SignalType.HOLD

        return MACDIndicator(
            macd_line=macd,
            signal_line=signal_line,
            histogram=histogram,
            histogram_slope=histogram_slope,
            zero_line_position=zero_line_position,
            state=state,
            signal=signal,
        )

    # =========================================================================
    # VOLATILITY ENGINE
    # =========================================================================

    def get_volatility_engine(self) -> VolatilityEngine:
        """Calculate volatility analysis with ATR and Bollinger."""
        close = self.df["close"].iloc[-1]
        atr = self.df["atr"].iloc[-1]
        bb_upper = self.df["bb_upper"].iloc[-1]
        bb_middle = self.df["bb_middle"].iloc[-1]
        bb_lower = self.df["bb_lower"].iloc[-1]
        bb_width = self.df["bb_width"].iloc[-1]
        bb_pband = self.df["bb_pband"].iloc[-1]

        if pd.isna(atr):
            atr = 0.0
        if pd.isna(bb_pband):
            bb_pband = 0.5

        # ATR as percentage of price
        atr_pct = (atr / close * 100) if close > 0 else 0

        # Volatility state based on BB width trend
        bb_width_series = self.df["bb_width"].tail(10).dropna()
        if len(bb_width_series) >= 5:
            recent_avg = bb_width_series.iloc[-3:].mean()
            older_avg = bb_width_series.iloc[:3].mean()
            if recent_avg < older_avg * 0.9:
                state = VolatilityState.CONTRACTING
            elif recent_avg > older_avg * 1.1:
                state = VolatilityState.EXPANDING
            else:
                state = VolatilityState.STABLE
        else:
            state = VolatilityState.STABLE

        # Squeeze detection
        squeeze = bb_width < (atr_pct * 0.04) if atr_pct > 0 else False

        # Breakout potential
        if squeeze and state == VolatilityState.CONTRACTING:
            breakout_potential = "high"
        elif squeeze:
            breakout_potential = "medium"
        else:
            breakout_potential = "low"

        return VolatilityEngine(
            atr=atr,
            atr_pct=atr_pct,
            state=state,
            bb_upper=bb_upper if not pd.isna(bb_upper) else close,
            bb_middle=bb_middle if not pd.isna(bb_middle) else close,
            bb_lower=bb_lower if not pd.isna(bb_lower) else close,
            bb_width=bb_width if not pd.isna(bb_width) else 0,
            bb_pband=bb_pband,
            squeeze=squeeze,
            breakout_potential=breakout_potential,
        )

    # =========================================================================
    # VOLUME ANALYSIS
    # =========================================================================

    def get_volume_analysis(self) -> VolumeAnalysis:
        """Calculate volume analysis with OBV and trend."""
        current_volume = self.df["volume"].iloc[-1]
        avg_volume = self.df["volume_sma"].iloc[-1]
        obv = self.df["obv"].iloc[-1]

        if pd.isna(avg_volume) or avg_volume == 0:
            avg_volume = current_volume if current_volume > 0 else 1

        relative_volume = current_volume / avg_volume if avg_volume > 0 else 1.0

        # OBV trend
        obv_series = self.df["obv"].tail(10).dropna()
        if len(obv_series) >= 5:
            obv_slope = obv_series.iloc[-1] - obv_series.iloc[0]
            if obv_slope > 0:
                obv_trend = "rising"
            elif obv_slope < 0:
                obv_trend = "falling"
            else:
                obv_trend = "flat"
        else:
            obv_trend = "flat"

        # Volume trend (accumulation/distribution)
        close_series = self.df["close"].tail(10)

        if len(close_series) >= 5:
            price_rising = close_series.iloc[-1] > close_series.iloc[0]
            volume_rising = obv_trend == "rising"

            if price_rising and volume_rising:
                trend = VolumeState.ACCUMULATION
            elif not price_rising and not volume_rising:
                trend = VolumeState.DISTRIBUTION
            else:
                trend = VolumeState.NEUTRAL
        else:
            trend = VolumeState.NEUTRAL

        # Confirmation
        price_change = self.df["close"].iloc[-1] - self.df["close"].iloc[-2] if len(self.df) > 1 else 0
        confirmation = (price_change > 0 and relative_volume > 1.0) or (price_change < 0 and relative_volume > 1.0)

        return VolumeAnalysis(
            current_volume=current_volume,
            avg_volume=avg_volume,
            relative_volume=relative_volume,
            obv=obv if not pd.isna(obv) else 0,
            obv_trend=obv_trend,
            trend=trend,
            confirmation=confirmation,
        )

    # =========================================================================
    # MARKET STRUCTURE
    # =========================================================================

    def get_market_structure(self) -> MarketStructureAnalysis:
        """Analyze market structure with HH/HL detection and key levels."""
        highs = self.df["high"]
        lows = self.df["low"]
        close = self.df["close"].iloc[-1]

        # Find swing highs and lows
        swing_highs = []
        swing_lows = []

        lookback = min(len(self.df), 50)
        for i in range(2, lookback - 2):
            idx = -(i + 1)
            # Swing high
            if (highs.iloc[idx] > highs.iloc[idx + 1] and
                highs.iloc[idx] > highs.iloc[idx - 1] and
                highs.iloc[idx] > highs.iloc[idx + 2] and
                highs.iloc[idx] > highs.iloc[idx - 2]):
                swing_highs.append((self.df.index[idx], float(highs.iloc[idx])))

            # Swing low
            if (lows.iloc[idx] < lows.iloc[idx + 1] and
                lows.iloc[idx] < lows.iloc[idx - 1] and
                lows.iloc[idx] < lows.iloc[idx + 2] and
                lows.iloc[idx] < lows.iloc[idx - 2]):
                swing_lows.append((self.df.index[idx], float(lows.iloc[idx])))

        # Determine market structure
        if len(swing_highs) >= 2 and len(swing_lows) >= 2:
            recent_highs = sorted(swing_highs, key=lambda x: x[0], reverse=True)[:2]
            recent_lows = sorted(swing_lows, key=lambda x: x[0], reverse=True)[:2]

            higher_highs = recent_highs[0][1] > recent_highs[1][1] if len(recent_highs) >= 2 else False
            higher_lows = recent_lows[0][1] > recent_lows[1][1] if len(recent_lows) >= 2 else False

            if higher_highs and higher_lows:
                structure = MarketStructure.HIGHER_HIGHS
            elif not higher_highs and not higher_lows:
                structure = MarketStructure.LOWER_LOWS
            else:
                structure = MarketStructure.CONSOLIDATING
        else:
            structure = MarketStructure.CONSOLIDATING

        # Last swing high/low
        last_swing_high = swing_highs[0][1] if swing_highs else float(highs.max())
        last_swing_low = swing_lows[0][1] if swing_lows else float(lows.min())

        # Break of Structure detection
        last_bos = None
        bos_price = None
        if structure == MarketStructure.HIGHER_HIGHS and close > last_swing_high:
            last_bos = "bullish"
            bos_price = last_swing_high
        elif structure == MarketStructure.LOWER_LOWS and close < last_swing_low:
            last_bos = "bearish"
            bos_price = last_swing_low

        # Key levels with strength
        key_levels = self._find_key_levels(swing_highs, swing_lows, close)

        # Range calculation
        current_range = None
        if structure == MarketStructure.CONSOLIDATING:
            current_range = last_swing_high - last_swing_low

        return MarketStructureAnalysis(
            structure=structure,
            last_swing_high=last_swing_high,
            last_swing_low=last_swing_low,
            last_bos=last_bos,
            bos_price=bos_price,
            key_levels=key_levels,
            current_range=current_range,
        )

    def _find_key_levels(
        self,
        swing_highs: List[Tuple],
        swing_lows: List[Tuple],
        current_price: float
    ) -> List[KeyLevel]:
        """Find key support/resistance levels with strength."""
        levels = []

        # Process swing highs as resistance
        for _, price in swing_highs[:5]:
            if price > current_price:
                touches = sum(1 for h in swing_highs if abs(h[1] - price) / price < 0.01)
                strength = "strong" if touches >= 3 else "moderate" if touches >= 2 else "weak"
                levels.append(KeyLevel(
                    price=price,
                    type="resistance",
                    strength=strength,
                    touches=touches,
                ))

        # Process swing lows as support
        for _, price in swing_lows[:5]:
            if price < current_price:
                touches = sum(1 for l in swing_lows if abs(l[1] - price) / price < 0.01)
                strength = "strong" if touches >= 3 else "moderate" if touches >= 2 else "weak"
                levels.append(KeyLevel(
                    price=price,
                    type="support",
                    strength=strength,
                    touches=touches,
                ))

        # Sort by distance from current price
        levels.sort(key=lambda x: abs(x.price - current_price))
        return levels[:6]

    # =========================================================================
    # VWAP
    # =========================================================================

    def get_vwap_analysis(self) -> Optional[VWAPAnalysis]:
        """Calculate VWAP with institutional bias."""
        vwap = self.df["vwap"].iloc[-1]
        vwap_std = self.df["vwap_std"].iloc[-1]
        close = self.df["close"].iloc[-1]

        if pd.isna(vwap) or vwap == 0:
            return None

        if pd.isna(vwap_std):
            vwap_std = 0

        position = "above" if close > vwap else "below"
        deviation_pct = (close - vwap) / vwap * 100

        upper_band = vwap + vwap_std
        lower_band = vwap - vwap_std

        if close > vwap:
            bias = TrendDirection.BULLISH
        elif close < vwap:
            bias = TrendDirection.BEARISH
        else:
            bias = TrendDirection.NEUTRAL

        return VWAPAnalysis(
            vwap=vwap,
            position=position,
            deviation_pct=deviation_pct,
            upper_band=upper_band,
            lower_band=lower_band,
            bias=bias,
        )

    # =========================================================================
    # COMPOSITE SIGNAL ENGINE
    # =========================================================================

    def get_composite_signal(
        self,
        ema_ribbon: EMARibbon,
        rsi: RSIIndicator,
        macd: MACDIndicator,
        volatility: VolatilityEngine,
        volume: VolumeAnalysis,
        structure: MarketStructureAnalysis,
        vwap: Optional[VWAPAnalysis],
    ) -> CompositeSignal:
        """Calculate composite signal with bias score and confidence."""

        # Calculate bias score (-100 to +100)
        bias_score = 0

        # Trend contribution (weight: 30)
        if ema_ribbon.trend_direction == TrendDirection.BULLISH:
            bias_score += 30 if ema_ribbon.trend_strength == TrendStrength.STRONG else 20 if ema_ribbon.trend_strength == TrendStrength.MODERATE else 10
        elif ema_ribbon.trend_direction == TrendDirection.BEARISH:
            bias_score -= 30 if ema_ribbon.trend_strength == TrendStrength.STRONG else 20 if ema_ribbon.trend_strength == TrendStrength.MODERATE else 10

        # RSI contribution (weight: 20)
        if rsi.regime in [MomentumRegime.BULLISH_EXTREME, MomentumRegime.BULLISH_CONTINUATION]:
            bias_score += 15 if rsi.regime == MomentumRegime.BULLISH_CONTINUATION else 10
        elif rsi.regime in [MomentumRegime.BEARISH_EXTREME, MomentumRegime.BEARISH_CONTINUATION]:
            bias_score -= 15 if rsi.regime == MomentumRegime.BEARISH_CONTINUATION else 10

        if rsi.divergence:
            bias_score += 10 if rsi.divergence_type == "bullish" else -10

        # MACD contribution (weight: 25)
        if macd.signal in [SignalType.BUY, SignalType.STRONG_BUY]:
            bias_score += 25 if macd.signal == SignalType.STRONG_BUY else 15
        elif macd.signal in [SignalType.SELL, SignalType.STRONG_SELL]:
            bias_score -= 25 if macd.signal == SignalType.STRONG_SELL else 15

        # Volume contribution (weight: 15)
        if volume.trend == VolumeState.ACCUMULATION:
            bias_score += 15 if volume.confirmation else 10
        elif volume.trend == VolumeState.DISTRIBUTION:
            bias_score -= 15 if volume.confirmation else 10

        # Structure contribution (weight: 10)
        if structure.structure == MarketStructure.HIGHER_HIGHS:
            bias_score += 10
        elif structure.structure == MarketStructure.LOWER_LOWS:
            bias_score -= 10

        # VWAP contribution (weight: 5)
        if vwap:
            if vwap.bias == TrendDirection.BULLISH:
                bias_score += 5
            elif vwap.bias == TrendDirection.BEARISH:
                bias_score -= 5

        # Clamp to -100 to +100
        bias_score = max(-100, min(100, bias_score))

        # Calculate confidence (0-1) - Enhanced multi-factor analysis
        confidence_score = 0.0
        max_confidence = 0.0

        # 1. Trend alignment with bias (weight: 20)
        max_confidence += 20
        if bias_score > 0 and ema_ribbon.trend_direction == TrendDirection.BULLISH:
            confidence_score += 20 if ema_ribbon.trend_strength == TrendStrength.STRONG else 15 if ema_ribbon.trend_strength == TrendStrength.MODERATE else 10
        elif bias_score < 0 and ema_ribbon.trend_direction == TrendDirection.BEARISH:
            confidence_score += 20 if ema_ribbon.trend_strength == TrendStrength.STRONG else 15 if ema_ribbon.trend_strength == TrendStrength.MODERATE else 10
        elif ema_ribbon.trend_direction == TrendDirection.NEUTRAL and abs(bias_score) < 20:
            confidence_score += 12  # Neutral trend with neutral bias is okay
        # Misaligned trend reduces confidence (adds 0)

        # 2. RSI alignment with bias (weight: 15)
        max_confidence += 15
        if bias_score > 0 and rsi.regime in [MomentumRegime.BULLISH_CONTINUATION, MomentumRegime.BULLISH_EXTREME]:
            confidence_score += 15
        elif bias_score < 0 and rsi.regime in [MomentumRegime.BEARISH_CONTINUATION, MomentumRegime.BEARISH_EXTREME]:
            confidence_score += 15
        elif rsi.regime == MomentumRegime.NEUTRAL:
            confidence_score += 8
        elif rsi.divergence:
            confidence_score += 5  # Divergence detected but not aligned

        # 3. MACD momentum clarity (weight: 15)
        max_confidence += 15
        if macd.state == "positive_acceleration" and bias_score > 0:
            confidence_score += 15
        elif macd.state == "negative_acceleration" and bias_score < 0:
            confidence_score += 15
        elif macd.state in ["positive_deceleration", "negative_deceleration"]:
            confidence_score += 8
        elif macd.state == "neutral":
            confidence_score += 5

        # 4. Volume confirmation (weight: 15)
        max_confidence += 15
        if volume.confirmation:
            if volume.relative_volume > 1.5:
                confidence_score += 15  # Strong volume confirmation
            elif volume.relative_volume > 1.0:
                confidence_score += 12
            else:
                confidence_score += 8
        elif volume.relative_volume > 0.5:
            confidence_score += 5

        # 5. Structure alignment (weight: 10)
        max_confidence += 10
        if bias_score > 0 and structure.structure == MarketStructure.HIGHER_HIGHS:
            confidence_score += 10
        elif bias_score < 0 and structure.structure == MarketStructure.LOWER_LOWS:
            confidence_score += 10
        elif structure.structure == MarketStructure.CONSOLIDATING:
            confidence_score += 5
        # Break of structure bonus
        if structure.last_bos:
            if (structure.last_bos == "bullish" and bias_score > 0) or \
               (structure.last_bos == "bearish" and bias_score < 0):
                confidence_score += 3

        # 6. Volatility environment (weight: 10)
        max_confidence += 10
        if volatility.state == VolatilityState.STABLE:
            confidence_score += 10  # Stable = predictable
        elif volatility.state == VolatilityState.EXPANDING and abs(bias_score) > 30:
            confidence_score += 8  # Expanding volatility with clear direction
        elif volatility.state == VolatilityState.CONTRACTING:
            confidence_score += 6  # Squeeze building
        else:
            confidence_score += 4

        # 7. VWAP alignment (weight: 10)
        max_confidence += 10
        if vwap:
            if bias_score > 0 and vwap.bias == TrendDirection.BULLISH:
                confidence_score += 10 if vwap.deviation_pct > 1 else 7
            elif bias_score < 0 and vwap.bias == TrendDirection.BEARISH:
                confidence_score += 10 if vwap.deviation_pct < -1 else 7
            elif abs(vwap.deviation_pct) < 0.5:
                confidence_score += 5  # Near VWAP
        else:
            confidence_score += 5  # No VWAP data, neutral

        # 8. Signal agreement bonus (weight: 5)
        max_confidence += 5
        bullish_signals = sum([
            1 if ema_ribbon.trend_direction == TrendDirection.BULLISH else 0,
            1 if rsi.signal in [SignalType.BUY, SignalType.STRONG_BUY] else 0,
            1 if macd.signal in [SignalType.BUY, SignalType.STRONG_BUY] else 0,
            1 if volume.trend == VolumeState.ACCUMULATION else 0,
        ])
        bearish_signals = sum([
            1 if ema_ribbon.trend_direction == TrendDirection.BEARISH else 0,
            1 if rsi.signal in [SignalType.SELL, SignalType.STRONG_SELL] else 0,
            1 if macd.signal in [SignalType.SELL, SignalType.STRONG_SELL] else 0,
            1 if volume.trend == VolumeState.DISTRIBUTION else 0,
        ])
        signal_agreement = max(bullish_signals, bearish_signals)
        if signal_agreement >= 4:
            confidence_score += 5
        elif signal_agreement >= 3:
            confidence_score += 3
        elif signal_agreement >= 2:
            confidence_score += 1

        # Calculate final confidence as percentage
        confidence = confidence_score / max_confidence if max_confidence > 0 else 0.5

        # Determine regime
        if volatility.squeeze and volatility.breakout_potential == "high":
            regime = MarketRegime.BREAKOUT if bias_score > 0 else MarketRegime.BREAKDOWN
        elif structure.structure == MarketStructure.CONSOLIDATING:
            regime = MarketRegime.RANGE_BOUND
        elif bias_score > 30:
            regime = MarketRegime.BULLISH_TREND
        elif bias_score < -30:
            regime = MarketRegime.BEARISH_TREND
        else:
            regime = MarketRegime.RANGE_BOUND

        # Recommended action
        if bias_score > 60:
            recommended_action = "trend_continuation_long"
        elif bias_score > 30:
            recommended_action = "look_for_long_entry"
        elif bias_score < -60:
            recommended_action = "trend_continuation_short"
        elif bias_score < -30:
            recommended_action = "look_for_short_entry"
        elif regime == MarketRegime.RANGE_BOUND:
            recommended_action = "range_trade"
        else:
            recommended_action = "wait_for_clarity"

        # Risk level
        if volatility.atr_pct > 5:
            risk_level = "high"
        elif volatility.atr_pct > 2:
            risk_level = "medium"
        else:
            risk_level = "low"

        # Entry quality
        if confidence > 0.8 and abs(bias_score) > 50:
            entry_quality = "excellent"
        elif confidence > 0.7 and abs(bias_score) > 30:
            entry_quality = "good"
        elif confidence > 0.6 and abs(bias_score) > 20:
            entry_quality = "fair"
        else:
            entry_quality = "poor"

        return CompositeSignal(
            bias_score=bias_score,
            confidence=round(confidence, 2),
            regime=regime,
            recommended_action=recommended_action,
            risk_level=risk_level,
            entry_quality=entry_quality,
        )

    # =========================================================================
    # MAIN API
    # =========================================================================

    def get_technical_indicators(self) -> TechnicalIndicators:
        """Get complete technical indicator stack."""
        ema_ribbon = self.get_ema_ribbon()
        rsi = self.get_rsi_indicator()
        macd = self.get_macd_indicator()
        volatility = self.get_volatility_engine()
        volume = self.get_volume_analysis()
        structure = self.get_market_structure()
        vwap = self.get_vwap_analysis()

        summary = self.get_composite_signal(
            ema_ribbon=ema_ribbon,
            rsi=rsi,
            macd=macd,
            volatility=volatility,
            volume=volume,
            structure=structure,
            vwap=vwap,
        )

        return TechnicalIndicators(
            ema_ribbon=ema_ribbon,
            rsi=rsi,
            macd=macd,
            volatility=volatility,
            volume=volume,
            structure=structure,
            vwap=vwap,
            summary=summary,
        )

    def generate_signals(self) -> List[Signal]:
        """Generate trading signals based on indicators."""
        signals = []
        close = self.df["close"]
        timestamps = self.df.index

        # RSI signals
        rsi = self.df["rsi"]
        for i in range(1, len(rsi)):
            if pd.isna(rsi.iloc[i]):
                continue

            if rsi.iloc[i - 1] < 30 and rsi.iloc[i] > 30:
                signals.append(Signal(
                    type=SignalType.BUY,
                    price=float(close.iloc[i]),
                    timestamp=timestamps[i],
                    reason="RSI bounced from oversold (<30)",
                    confidence=0.7,
                ))
            elif rsi.iloc[i - 1] > 70 and rsi.iloc[i] < 70:
                signals.append(Signal(
                    type=SignalType.SELL,
                    price=float(close.iloc[i]),
                    timestamp=timestamps[i],
                    reason="RSI dropped from overbought (>70)",
                    confidence=0.7,
                ))

        # MACD crossover signals
        histogram = self.df["macd_histogram"]
        for i in range(1, len(histogram)):
            if pd.isna(histogram.iloc[i]) or pd.isna(histogram.iloc[i - 1]):
                continue

            if histogram.iloc[i - 1] < 0 and histogram.iloc[i] > 0:
                signals.append(Signal(
                    type=SignalType.STRONG_BUY,
                    price=float(close.iloc[i]),
                    timestamp=timestamps[i],
                    reason="MACD bullish crossover",
                    confidence=0.8,
                ))
            elif histogram.iloc[i - 1] > 0 and histogram.iloc[i] < 0:
                signals.append(Signal(
                    type=SignalType.STRONG_SELL,
                    price=float(close.iloc[i]),
                    timestamp=timestamps[i],
                    reason="MACD bearish crossover",
                    confidence=0.8,
                ))

        # Bollinger Band signals
        bb_pband = self.df["bb_pband"]
        for i in range(1, len(bb_pband)):
            if pd.isna(bb_pband.iloc[i]):
                continue

            if bb_pband.iloc[i - 1] > 0 and bb_pband.iloc[i] <= 0:
                signals.append(Signal(
                    type=SignalType.BUY,
                    price=float(close.iloc[i]),
                    timestamp=timestamps[i],
                    reason="Price touched lower Bollinger Band",
                    confidence=0.6,
                ))
            elif bb_pband.iloc[i - 1] < 1 and bb_pband.iloc[i] >= 1:
                signals.append(Signal(
                    type=SignalType.SELL,
                    price=float(close.iloc[i]),
                    timestamp=timestamps[i],
                    reason="Price touched upper Bollinger Band",
                    confidence=0.6,
                ))

        signals.sort(key=lambda s: s.timestamp, reverse=True)
        return signals[:10]

    # =========================================================================
    # TRADING SUGGESTION ENGINE
    # =========================================================================

    def generate_trading_suggestion(
        self,
        indicators: TechnicalIndicators,
    ) -> Optional[TradingSuggestion]:
        """
        Generate comprehensive trading suggestion based on technical analysis.

        Returns entry, stop loss, take profit levels with leverage recommendation.
        """
        current_price = float(self.df["close"].iloc[-1])
        atr = float(self.df["atr"].iloc[-1]) if not pd.isna(self.df["atr"].iloc[-1]) else current_price * 0.02

        summary = indicators.summary
        structure = indicators.structure
        volatility = indicators.volatility

        bias_score = summary.bias_score
        confidence = summary.confidence
        entry_quality = summary.entry_quality

        # Determine if we should suggest a trade
        if entry_quality == "poor" or abs(bias_score) < 15:
            return TradingSuggestion(
                position_type=PositionType.NO_TRADE,
                leverage=None,
                is_futures=False,
                entry_price=current_price,
                stop_loss=current_price,
                take_profit_1=current_price,
                take_profit_2=None,
                take_profit_3=None,
                risk_reward_ratio=0.0,
                position_risk_pct=0.0,
                suggested_position_size_pct=0.0,
                reasoning="Market conditions are unclear. Entry quality is poor or bias is too weak.",
                invalidation="N/A - No trade suggested",
                trade_confidence=confidence,
                warning="Wait for better entry conditions with clearer directional bias.",
            )

        # Determine position direction
        is_long = bias_score > 0

        # Get key levels for stop loss and take profit
        supports = [lvl for lvl in structure.key_levels if lvl.type == "support"]
        resistances = [lvl for lvl in structure.key_levels if lvl.type == "resistance"]

        # Calculate entry price (current price or slight improvement)
        entry_price = current_price

        # Calculate stop loss based on ATR and structure
        if is_long:
            # For long: stop below recent support or 1.5x ATR below entry
            if supports:
                nearest_support = min(supports, key=lambda x: abs(x.price - current_price))
                structure_stop = nearest_support.price * 0.995  # 0.5% below support
            else:
                structure_stop = current_price - (atr * 2)

            atr_stop = current_price - (atr * 1.5)
            stop_loss = max(structure_stop, atr_stop)  # Use tighter stop

            # Take profit levels based on resistance and R:R
            risk = entry_price - stop_loss
            take_profit_1 = entry_price + (risk * 1.5)  # 1.5:1 R:R
            take_profit_2 = entry_price + (risk * 2.5)  # 2.5:1 R:R
            take_profit_3 = entry_price + (risk * 4.0)  # 4:1 R:R

            # Adjust to resistance levels if available
            if resistances:
                sorted_res = sorted(resistances, key=lambda x: x.price)
                if sorted_res[0].price > entry_price:
                    take_profit_1 = min(take_profit_1, sorted_res[0].price * 0.995)
                if len(sorted_res) > 1 and sorted_res[1].price > entry_price:
                    take_profit_2 = sorted_res[1].price * 0.995
                if len(sorted_res) > 2 and sorted_res[2].price > entry_price:
                    take_profit_3 = sorted_res[2].price * 0.995
        else:
            # For short: stop above recent resistance or 1.5x ATR above entry
            if resistances:
                nearest_resistance = min(resistances, key=lambda x: abs(x.price - current_price))
                structure_stop = nearest_resistance.price * 1.005  # 0.5% above resistance
            else:
                structure_stop = current_price + (atr * 2)

            atr_stop = current_price + (atr * 1.5)
            stop_loss = min(structure_stop, atr_stop)  # Use tighter stop

            # Take profit levels based on support and R:R
            risk = stop_loss - entry_price
            take_profit_1 = entry_price - (risk * 1.5)  # 1.5:1 R:R
            take_profit_2 = entry_price - (risk * 2.5)  # 2.5:1 R:R
            take_profit_3 = entry_price - (risk * 4.0)  # 4:1 R:R

            # Adjust to support levels if available
            # For SHORT: TP must be BELOW entry price (we profit when price goes down)
            # Use min() to ensure TP doesn't go above entry price
            if supports:
                sorted_sup = sorted(supports, key=lambda x: x.price, reverse=True)
                if sorted_sup[0].price < entry_price:
                    take_profit_1 = min(take_profit_1, sorted_sup[0].price * 1.005)
                if len(sorted_sup) > 1 and sorted_sup[1].price < entry_price:
                    take_profit_2 = min(take_profit_2, sorted_sup[1].price * 1.005)
                if len(sorted_sup) > 2 and sorted_sup[2].price < entry_price:
                    take_profit_3 = min(take_profit_3, sorted_sup[2].price * 1.005)

        # Calculate risk metrics
        risk_amount = abs(entry_price - stop_loss)
        reward_amount = abs(take_profit_1 - entry_price)
        risk_reward_ratio = reward_amount / risk_amount if risk_amount > 0 else 0
        position_risk_pct = (risk_amount / entry_price) * 100

        # Determine leverage based on confidence and volatility
        # Higher confidence + lower volatility = more leverage potential
        leverage = None
        is_futures = False

        if confidence >= 0.75 and entry_quality in ["excellent", "good"]:
            # Strong signal - can use futures with leverage
            is_futures = True

            if volatility.atr_pct < 2:  # Low volatility
                if confidence >= 0.85:
                    leverage = 10
                elif confidence >= 0.80:
                    leverage = 7
                else:
                    leverage = 5
            elif volatility.atr_pct < 4:  # Medium volatility
                if confidence >= 0.85:
                    leverage = 5
                elif confidence >= 0.80:
                    leverage = 4
                else:
                    leverage = 3
            else:  # High volatility
                if confidence >= 0.85:
                    leverage = 3
                else:
                    leverage = 2
        elif confidence >= 0.60 and entry_quality in ["good", "fair"]:
            # Moderate signal - low leverage or spot
            is_futures = True
            leverage = 2

        # Position type
        if is_long:
            position_type = PositionType.LONG if is_futures else PositionType.SPOT_BUY
        else:
            position_type = PositionType.SHORT if is_futures else PositionType.SPOT_SELL

        # Suggested position size based on risk
        # Standard: risk 1-2% of portfolio per trade
        if confidence >= 0.80:
            suggested_position_size_pct = 2.0
        elif confidence >= 0.70:
            suggested_position_size_pct = 1.5
        elif confidence >= 0.60:
            suggested_position_size_pct = 1.0
        else:
            suggested_position_size_pct = 0.5

        # Generate reasoning
        direction = "LONG" if is_long else "SHORT"
        reasoning_parts = [f"{direction} position suggested based on:"]

        if indicators.ema_ribbon.trend_direction.value == ("bullish" if is_long else "bearish"):
            reasoning_parts.append(f"• EMA ribbon shows {indicators.ema_ribbon.trend_strength.value} {indicators.ema_ribbon.trend_direction.value} trend")

        if is_long and indicators.rsi.zone == "oversold":
            reasoning_parts.append("• RSI in oversold zone indicating potential bounce")
        elif not is_long and indicators.rsi.zone == "overbought":
            reasoning_parts.append("• RSI in overbought zone indicating potential pullback")

        if indicators.macd.state in ["positive_acceleration"] and is_long:
            reasoning_parts.append("• MACD showing positive acceleration")
        elif indicators.macd.state in ["negative_acceleration"] and not is_long:
            reasoning_parts.append("• MACD showing negative acceleration")

        if indicators.volume.confirmation:
            reasoning_parts.append(f"• Volume confirmation with {indicators.volume.relative_volume:.1f}x relative volume")

        reasoning_parts.append(f"• Entry quality: {entry_quality}, Confidence: {confidence*100:.0f}%")

        reasoning = " ".join(reasoning_parts)

        # Invalidation conditions
        if is_long:
            invalidation = f"Trade invalidated if price closes below ${stop_loss:.2f} (stop loss) or if bearish structure break occurs below ${structure.last_swing_low:.2f}"
        else:
            invalidation = f"Trade invalidated if price closes above ${stop_loss:.2f} (stop loss) or if bullish structure break occurs above ${structure.last_swing_high:.2f}"

        # Warning based on risk
        warning = None
        if volatility.atr_pct > 5:
            warning = "HIGH VOLATILITY: Consider reducing position size. Wide price swings expected."
        elif summary.risk_level == "high":
            warning = "Elevated risk environment. Use strict risk management."
        elif indicators.rsi.divergence:
            warning = f"RSI divergence detected ({indicators.rsi.divergence_type}). Watch for potential reversal."

        return TradingSuggestion(
            position_type=position_type,
            leverage=leverage,
            is_futures=is_futures,
            entry_price=round(entry_price, 2),
            stop_loss=round(stop_loss, 2),
            take_profit_1=round(take_profit_1, 2),
            take_profit_2=round(take_profit_2, 2) if take_profit_2 else None,
            take_profit_3=round(take_profit_3, 2) if take_profit_3 else None,
            risk_reward_ratio=round(risk_reward_ratio, 2),
            position_risk_pct=round(position_risk_pct, 2),
            suggested_position_size_pct=suggested_position_size_pct,
            reasoning=reasoning,
            invalidation=invalidation,
            trade_confidence=confidence,
            warning=warning,
        )

