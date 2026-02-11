"""Signal API endpoint for crypto trading analysis."""
import logging
from typing import Literal, Union

from fastapi import APIRouter, HTTPException, Query, Request
from fastapi.responses import PlainTextResponse
import httpx

from app.config import settings
from app.middleware.security import limiter
from app.models.signal import SignalResponse
from app.services.data_providers import get_provider
from app.services.signal_formatter import format_json_response, format_text_response
from app.services.technical_analysis import TechnicalAnalyzer

logger = logging.getLogger("trading_signal_api.signal")

router = APIRouter()


async def _generate_signal(
    symbol: str,
    timeframe: str,
    format: str,
) -> Union[SignalResponse, PlainTextResponse]:
    """Core signal generation logic used by both endpoints."""
    symbol = symbol.upper().strip()

    provider = get_provider(api_key=settings.coingecko_api_key or None)

    try:
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
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 429:
            logger.warning(f"Rate limited by data provider for {symbol}")
            raise HTTPException(
                status_code=503,
                detail="Data provider temporarily unavailable. Please try again in a few seconds.",
            )
        raise HTTPException(
            status_code=502,
            detail=f"Data provider error: {e.response.status_code}",
        )

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


@router.get(
    "/signal",
    response_model=SignalResponse,
    responses={
        200: {"description": "Signal analysis complete"},
        404: {"description": "Symbol not found or no data available"},
        422: {"description": "Invalid parameters"},
        429: {"description": "Rate limit exceeded"},
        500: {"description": "Internal server error"},
        503: {"description": "Data provider temporarily unavailable"},
    },
)
@limiter.limit("60/minute")
async def get_signal_query(
    request: Request,
    symbol: str = Query(
        description="Crypto symbol (BTC, ETH, SOL) or full name (bitcoin, ethereum, solana)",
    ),
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
    Get trading signal analysis (query parameter version for APIX compatibility).

    Use: /api/v1/signal?symbol=BTC&timeframe=4h
    """
    return await _generate_signal(symbol, timeframe, format)


@router.get(
    "/signal/{symbol}",
    response_model=SignalResponse,
    responses={
        200: {"description": "Signal analysis complete"},
        404: {"description": "Symbol not found or no data available"},
        422: {"description": "Invalid parameters"},
        429: {"description": "Rate limit exceeded"},
        500: {"description": "Internal server error"},
        503: {"description": "Data provider temporarily unavailable"},
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
    Get trading signal analysis (path parameter version).

    Use: /api/v1/signal/BTC?timeframe=4h
    """
    return await _generate_signal(symbol, timeframe, format)
