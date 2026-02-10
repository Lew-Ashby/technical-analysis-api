"""Signal response formatters for JSON and text output."""
import re
from datetime import datetime
from typing import Optional

from app.models.analysis import (
    PositionType,
    TechnicalIndicators,
    TradingSuggestion,
)
from app.models.signal import (
    AnalysisInfo,
    ChartDataInfo,
    LevelsInfo,
    MomentumInfo,
    PriceInfo,
    SignalResponse,
    TradeInfo,
    TrendInfo,
    VolatilityInfo,
    VolumeInfo,
)


def _sanitize_symbol(symbol: str) -> str:
    """Sanitize symbol to prevent injection."""
    return re.sub(r"[^a-zA-Z0-9\-]", "", symbol)[:20]


def format_json_response(
    symbol: str,
    timeframe: str,
    current_price: float,
    price_change: float,
    price_change_pct: float,
    indicators: TechnicalIndicators,
    suggestion: Optional[TradingSuggestion],
    chart_data: Optional[ChartDataInfo] = None,
) -> SignalResponse:
    """Format technical analysis into SignalResponse JSON structure."""
    sanitized_symbol = _sanitize_symbol(symbol)

    # Extract support/resistance levels
    support_levels = [
        lvl.price
        for lvl in indicators.structure.key_levels
        if lvl.type == "support"
    ][:3]
    resistance_levels = [
        lvl.price
        for lvl in indicators.structure.key_levels
        if lvl.type == "resistance"
    ][:3]

    # Determine signal direction (spec: long, short, hold, no_trade)
    if suggestion and suggestion.position_type == PositionType.NO_TRADE:
        signal_direction = "no_trade"
    elif indicators.summary.bias_score > 30:
        signal_direction = "long"
    elif indicators.summary.bias_score < -30:
        signal_direction = "short"
    else:
        signal_direction = "hold"

    # Build trade info (position is uppercase per spec: SHORT, LONG, NO_TRADE)
    if suggestion and suggestion.position_type != PositionType.NO_TRADE:
        trade_info = TradeInfo(
            position=suggestion.position_type.value.upper(),
            leverage=suggestion.leverage,
            entry=suggestion.entry_price,
            stop_loss=suggestion.stop_loss,
            take_profit_1=suggestion.take_profit_1,
            take_profit_2=suggestion.take_profit_2,
            take_profit_3=suggestion.take_profit_3,
            risk_reward=suggestion.risk_reward_ratio,
            position_risk_pct=suggestion.position_risk_pct,
            invalidation=suggestion.invalidation,
        )
    else:
        trade_info = TradeInfo(
            position="NO_TRADE",
            leverage=None,
            entry=current_price,
            stop_loss=current_price,
            take_profit_1=current_price,
            take_profit_2=None,
            take_profit_3=None,
            risk_reward=0.0,
            position_risk_pct=0.0,
            invalidation="No trade suggested - wait for better conditions",
        )

    # Generate summary text
    summary = _generate_summary(
        symbol=sanitized_symbol,
        timeframe=timeframe,
        current_price=current_price,
        price_change_pct=price_change_pct,
        indicators=indicators,
        suggestion=suggestion,
    )

    return SignalResponse(
        symbol=sanitized_symbol,
        timeframe=timeframe,
        timestamp=datetime.utcnow(),
        price=PriceInfo(
            current=current_price,
            change_24h=price_change,
            change_24h_pct=price_change_pct,
        ),
        analysis=AnalysisInfo(
            bias_score=indicators.summary.bias_score,
            confidence=indicators.summary.confidence,
            signal=signal_direction,
            regime=indicators.summary.regime.value,
            entry_quality=indicators.summary.entry_quality,
            risk_level=indicators.summary.risk_level,
        ),
        trend=TrendInfo(
            direction=indicators.ema_ribbon.trend_direction.value,
            strength=indicators.ema_ribbon.trend_strength.value,
            ema_20=indicators.ema_ribbon.ema_20,
            ema_50=indicators.ema_ribbon.ema_50,
            ema_100=indicators.ema_ribbon.ema_100,
            price_position=indicators.ema_ribbon.price_position,
            structure=indicators.structure.structure.value,
        ),
        momentum=MomentumInfo(
            rsi=indicators.rsi.value,
            rsi_zone=indicators.rsi.zone,
            macd_state=indicators.macd.state,
            macd_histogram=indicators.macd.histogram,
            histogram_slope=indicators.macd.histogram_slope,
        ),
        volume=VolumeInfo(
            state=indicators.volume.trend.value,
            relative=indicators.volume.relative_volume,
            confirmation=indicators.volume.confirmation,
        ),
        volatility=VolatilityInfo(
            state=indicators.volatility.state.value,
            atr_pct=indicators.volatility.atr_pct,
            squeeze=indicators.volatility.squeeze,
            breakout_potential=indicators.volatility.breakout_potential,
        ),
        levels=LevelsInfo(
            support=support_levels,
            resistance=resistance_levels,
        ),
        trade=trade_info,
        summary=summary,
        chart_data=chart_data,
    )


def _generate_summary(
    symbol: str,
    timeframe: str,
    current_price: float,
    price_change_pct: float,
    indicators: TechnicalIndicators,
    suggestion: Optional[TradingSuggestion],
) -> str:
    """Generate rule-based verbal analysis summary."""
    summary = indicators.summary
    ema = indicators.ema_ribbon
    rsi = indicators.rsi
    macd = indicators.macd
    vol = indicators.volatility
    volume = indicators.volume
    structure = indicators.structure

    parts = []

    # Composite signal summary
    bias_desc = (
        "bullish"
        if summary.bias_score > 0
        else "bearish" if summary.bias_score < 0 else "neutral"
    )
    parts.append(
        f"{symbol} on the {timeframe} timeframe shows {bias_desc} bias "
        f"(score: {summary.bias_score:+d}/100, confidence: {summary.confidence:.0%}) "
        f"at ${current_price:,.2f} ({price_change_pct:+.2f}% 24h). "
        f"Market regime: {summary.regime.value.replace('_', ' ')}."
    )

    # EMA trend
    parts.append(
        f"EMA ribbon indicates {ema.trend_direction.value} trend with "
        f"{ema.trend_strength.value} strength. "
        f"Price is {ema.price_position.replace('_', ' ')}."
    )

    # Momentum
    rsi_desc = f"RSI at {rsi.value:.1f} ({rsi.zone})"
    if rsi.divergence:
        rsi_desc += f" with {rsi.divergence_type} divergence detected"
    parts.append(f"{rsi_desc}. MACD showing {macd.state.replace('_', ' ')}.")

    # Volume
    vol_desc = f"Volume {volume.trend.value}"
    if volume.confirmation:
        vol_desc += " with price confirmation"
    parts.append(f"{vol_desc} (relative volume: {volume.relative_volume:.2f}x).")

    # Volatility
    if vol.squeeze:
        parts.append(
            f"Volatility squeeze detected with {vol.breakout_potential} "
            "breakout potential."
        )

    # Structure and levels
    support_levels = [l for l in structure.key_levels if l.type == "support"]
    resistance_levels = [l for l in structure.key_levels if l.type == "resistance"]

    if support_levels or resistance_levels:
        levels_desc = "Key levels: "
        if support_levels:
            levels_desc += f"support at ${support_levels[0].price:,.2f}"
        if support_levels and resistance_levels:
            levels_desc += ", "
        if resistance_levels:
            levels_desc += f"resistance at ${resistance_levels[0].price:,.2f}"
        parts.append(levels_desc + ".")

    # Action
    parts.append(
        f"Recommended action: {summary.recommended_action.replace('_', ' ')}. "
        f"Entry quality: {summary.entry_quality}, risk level: {summary.risk_level}."
    )

    # Trading suggestion
    if suggestion and suggestion.position_type != PositionType.NO_TRADE:
        position_type = suggestion.position_type.value.upper().replace("_", " ")
        leverage_str = (
            f"with {suggestion.leverage}x leverage" if suggestion.leverage else "(spot)"
        )
        # Build TP string with all available take profits
        tp_parts = [f"TP1: ${suggestion.take_profit_1:,.2f}"]
        if suggestion.take_profit_2:
            tp_parts.append(f"TP2: ${suggestion.take_profit_2:,.2f}")
        if suggestion.take_profit_3:
            tp_parts.append(f"TP3: ${suggestion.take_profit_3:,.2f}")
        tp_str = ", ".join(tp_parts)

        parts.append(
            f"TRADE SUGGESTION: {position_type} {leverage_str} - "
            f"Entry: ${suggestion.entry_price:,.2f}, "
            f"Stop Loss: ${suggestion.stop_loss:,.2f}, "
            f"Take Profits: {tp_str}. "
            f"R:R ratio {suggestion.risk_reward_ratio:.1f}:1, "
            f"trade confidence {suggestion.trade_confidence:.0%}."
        )
        if suggestion.warning:
            parts.append(f"Warning: {suggestion.warning}")
    elif suggestion and suggestion.position_type == PositionType.NO_TRADE:
        parts.append(f"No trade suggested at this time. {suggestion.reasoning}")

    parts.append(
        "Note: This is technical analysis, not financial advice. "
        "Trading involves risk."
    )

    return " ".join(parts)


def format_text_response(
    symbol: str,
    timeframe: str,
    current_price: float,
    price_change: float,
    price_change_pct: float,
    indicators: TechnicalIndicators,
    suggestion: Optional[TradingSuggestion],
) -> str:
    """Format technical analysis into human-readable text matching spec format."""
    sanitized_symbol = _sanitize_symbol(symbol)
    summary = indicators.summary
    ema = indicators.ema_ribbon
    rsi = indicators.rsi
    macd = indicators.macd
    vol = indicators.volatility
    volume = indicators.volume
    structure = indicators.structure

    # Extract levels
    support_levels = [
        lvl.price for lvl in structure.key_levels if lvl.type == "support"
    ][:3]
    resistance_levels = [
        lvl.price for lvl in structure.key_levels if lvl.type == "resistance"
    ][:3]

    support_str = ", ".join(f"${s:,.2f}" for s in support_levels) or "None identified"
    resistance_str = ", ".join(f"${r:,.2f}" for r in resistance_levels) or "None identified"

    # Determine signal direction
    if summary.bias_score > 30:
        signal_text = "LONG"
    elif summary.bias_score < -30:
        signal_text = "SHORT"
    else:
        signal_text = "HOLD"

    # Build trade section
    if suggestion and suggestion.position_type != PositionType.NO_TRADE:
        position_type = suggestion.position_type.value.upper()
        leverage_str = f"with {suggestion.leverage}x leverage" if suggestion.leverage else "spot"
        tp2_line = f"- Take Profit 2: ${suggestion.take_profit_2:,.2f}\n" if suggestion.take_profit_2 else ""
        tp3_line = f"- Take Profit 3: ${suggestion.take_profit_3:,.2f}\n" if suggestion.take_profit_3 else ""
        trade_section = f"""Trade Setup
- Position: {position_type} {leverage_str}
- Entry: ${suggestion.entry_price:,.2f}
- Stop Loss: ${suggestion.stop_loss:,.2f}
- Take Profit 1: ${suggestion.take_profit_1:,.2f}
{tp2_line}{tp3_line}- Risk/Reward: {suggestion.risk_reward_ratio:.1f}:1"""
    else:
        reason = suggestion.reasoning if suggestion else "Wait for better conditions"
        trade_section = f"""Trade Setup
- Position: NO TRADE RECOMMENDED
- Reason: {reason}"""

    # Generate commentary (summary text)
    commentary = _generate_summary(
        symbol=sanitized_symbol,
        timeframe=timeframe,
        current_price=current_price,
        price_change_pct=price_change_pct,
        indicators=indicators,
        suggestion=suggestion,
    )

    text = f"""{sanitized_symbol}/USDT - {timeframe} Analysis
{'═' * 39}

Price: ${current_price:,.2f} ({price_change_pct:+.2f}% 24h)
Bias: {summary.bias_score:+d}/100 | Confidence: {summary.confidence:.0%}
Signal: {signal_text}

Trend Analysis
- EMA Ribbon: {ema.trend_direction.value} trend with {ema.trend_strength.value} strength
- Price position: {ema.price_position.replace('_', ' ')}
- Market structure: {structure.structure.value.replace('_', ' ')}

Momentum
- RSI: {rsi.value:.1f} ({rsi.zone})
- MACD: {macd.state.replace('_', ' ')} (Histogram: {macd.histogram_slope})

Volume & Volatility
- Volume: {volume.trend.value} ({volume.relative_volume:.2f}x average)
- Volatility: {vol.state.value} (ATR: {vol.atr_pct:.2f}%)

Signal Summary
- Recommended action: {summary.recommended_action.replace('_', ' ')}
- Entry quality: {summary.entry_quality} | Risk level: {summary.risk_level}

{trade_section}

Key Levels
- Support: {support_str}
- Resistance: {resistance_str}

Commentary
{commentary}"""
    return text.strip()
