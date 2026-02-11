"""Signal API endpoint for crypto trading analysis."""
import logging
from typing import Literal, Union

from fastapi import APIRouter, HTTPException, Query, Request
from fastapi.responses import PlainTextResponse

from app.config import settings
from app.middleware.security import limiter
from app.models.signal import SignalResponse
from app.services.data_providers import get_provider
from app.services.signal_formatter import format_json_response, format_text_response
from app.services.technical_analysis import TechnicalAnalyzer

logger = logging.getLogger("trading_signal_api.signal")

router = APIRouter()


@router.get(
    "/signal/{symbol}",
    response_model=SignalResponse,
    responses={
        200: {"description": "Signal analysis complete"},
        404: {"description": "Symbol not found or no data available"},
        422: {"description": "Invalid parameters"},
        429: {"description": "Rate limit exceeded"},
        500: {"description": "Internal server error"},
        504: {"description": "External service timeout"},
    },
)
@limiter.limit("60/minute")
async def get_signal(
    request: Request,
    symbol: str,
    timeframe: str = Query(
        default="4h",
        pattern="^(1h|4h|1d|1w)$",
        description="Chart timeframe: 1h, 4h, 1d, or 1w",
    ),
    format: Literal["json", "text"] = Query(
        default="json",
        description="Response format: json or text",
    ),
) -> Union[SignalResponse, PlainTextResponse]:
    """
    Get comprehensive trading signal analysis for a crypto symbol.

    This endpoint provides:
    - Price information (current, 24h change)
    - Technical analysis (trend, momentum, volume, volatility)
    - Market structure analysis (support/resistance levels)
    - Trading suggestion with entry, stop loss, and take profit levels
    - Verbal analysis summary

    **Supported Timeframes:**
    - 1h: Hourly candles
    - 4h: 4-hour candles (default)
    - 1d: Daily candles
    - 1w: Weekly candles

    **Response Formats:**
    - json: Structured JSON response
    - text: Human-readable text format

    **Payment:**
    When accessed via APIX marketplace, x402 payments are handled by the platform.
    """
    symbol = symbol.upper().strip()

    provider = get_provider(api_key=settings.coingecko_api_key or None)

    chart_data = await provider.fetch_ohlcv(
        symbol=symbol,
        timeframe=timeframe,
        limit=200,
    )

    if not chart_data.candles:
        raise HTTPException(
            status_code=404,
            detail=f"No data found for symbol: {symbol}",
        )

    current_price = await provider.get_current_price(symbol)
    price_change, price_change_pct = await provider.get_price_change_24h(symbol)

    analyzer = TechnicalAnalyzer(chart_data)
    indicators = analyzer.get_technical_indicators()
    suggestion = analyzer.generate_trading_suggestion(indicators)

    if format == "text":
        text_response = format_text_response(
            symbol=symbol,
            timeframe=timeframe,
            current_price=current_price,
            price_change=price_change,
            price_change_pct=price_change_pct,
            indicators=indicators,
            suggestion=suggestion,
        )
        return PlainTextResponse(content=text_response, media_type="text/plain")

    signal_response = format_json_response(
        symbol=symbol,
        timeframe=timeframe,
        current_price=current_price,
        price_change=price_change,
        price_change_pct=price_change_pct,
        indicators=indicators,
        suggestion=suggestion,
    )

    logger.info(f"Signal generated for {symbol}/{timeframe}")
    return signal_response
