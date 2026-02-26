"""Signal API endpoint for crypto trading analysis."""
import json
import logging
from typing import Literal, Union
from urllib.parse import parse_qs

from fastapi import APIRouter, HTTPException, Query, Request
from fastapi.responses import PlainTextResponse, JSONResponse
import httpx

from app.config import settings
from app.middleware.security import limiter
from app.models.signal import SignalResponse
from app.services.data_providers import get_provider
from app.services.signal_formatter import format_json_response, format_text_response
from app.services.technical_analysis import TechnicalAnalyzer

logger = logging.getLogger("trading_signal_api.signal")

router = APIRouter()


def parse_apix_query_field(query_string: str) -> dict:
    """
    Parse APIX query field format: "symbol=BTC" or "key1=val1&key2=val2"
    Returns dict of parsed parameters.
    """
    result = {}
    if not query_string:
        return result
    parsed = parse_qs(query_string)
    for key, values in parsed.items():
        result[key] = values[0] if values else None
    return result


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
    response_model=None,  # Disable auto response model - we return multiple types
    responses={
        200: {"description": "Signal analysis complete"},
        404: {"description": "Symbol not found or no data available"},
        429: {"description": "Rate limit exceeded"},
        500: {"description": "Internal server error"},
        503: {"description": "Data provider temporarily unavailable"},
    },
    include_in_schema=False,  # Hide GET, APIX uses POST
)
@limiter.limit("60/minute")
async def get_signal_query(
    request: Request,
    symbol: str = Query(
        None,  # Make optional to avoid 422
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
):
    """
    Get trading signal analysis (query parameter version).

    Use: /api/v1/signal?symbol=BTC&timeframe=4h
    """
    if not symbol:
        return JSONResponse(
            status_code=200,
            content={
                "status": "ready",
                "message": "GET /signal - provide 'symbol' query parameter",
                "example": "/api/v1/signal?symbol=BTC&timeframe=4h",
                "parameters": {
                    "symbol": "Crypto symbol (required) - BTC, ETH, SOL, etc.",
                    "timeframe": "Chart timeframe (optional) - 1h, 4h, 1d, 1w (default: 4h)",
                    "format": "Response format (optional) - json or text (default: json)"
                }
            }
        )
    return await _generate_signal(symbol, timeframe, format)


@router.get(
    "/signal/{symbol}",
    response_model=None,  # Disable auto response model - we return multiple types
    responses={
        200: {"description": "Signal analysis complete"},
        404: {"description": "Symbol not found or no data available"},
        422: {"description": "Invalid parameters"},
        429: {"description": "Rate limit exceeded"},
        500: {"description": "Internal server error"},
        503: {"description": "Data provider temporarily unavailable"},
    },
    include_in_schema=False,  # Hide path version from OpenAPI
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
):
    """
    Get trading signal analysis (path parameter version).

    Use: /api/v1/signal/BTC?timeframe=4h
    """
    return await _generate_signal(symbol, timeframe, format)


@router.post(
    "/signal",
    responses={
        200: {"description": "Signal analysis complete"},
        404: {"description": "Symbol not found or no data available"},
        429: {"description": "Rate limit exceeded"},
        500: {"description": "Internal server error"},
        503: {"description": "Data provider temporarily unavailable"},
    },
    summary="Get trading signal analysis (APIX POST)",
    description="POST endpoint for APIX x402 marketplace. Send symbol in JSON body.",
)
@limiter.limit("60/minute")
async def post_signal(request: Request):
    """
    APIX-compatible POST endpoint for trading signal analysis.

    APIX sends body as: {"query": "symbol=BTC&timeframe=4h"}
    """
    # Log everything APIX sends for debugging
    logger.info(f"POST DEBUG - Headers: {dict(request.headers)}")
    logger.info(f"POST DEBUG - Query params: {dict(request.query_params)}")

    symbol = None
    timeframe = "4h"
    format_type = "json"

    # Try to get parameters from body
    try:
        body_bytes = await request.body()
        logger.info(f"POST DEBUG - Raw body: {body_bytes}")
        if body_bytes:
            body_json = json.loads(body_bytes)
            logger.info(f"POST DEBUG - Parsed body: {body_json}")
            if isinstance(body_json, dict):
                # Method 1: Direct field access (standard JSON body)
                symbol = body_json.get("symbol")
                if body_json.get("timeframe"):
                    timeframe = body_json.get("timeframe")

                # Method 2: APIX sends {"query": "symbol=BTC&timeframe=4h"} format
                if not symbol and "query" in body_json:
                    query_string = body_json.get("query", "")
                    logger.info(f"POST DEBUG - Parsing APIX query field: {query_string}")
                    parsed_query = parse_apix_query_field(query_string)
                    logger.info(f"POST DEBUG - Parsed query params: {parsed_query}")
                    symbol = parsed_query.get("symbol")
                    if parsed_query.get("timeframe"):
                        timeframe = parsed_query.get("timeframe")
                    if parsed_query.get("format"):
                        format_type = parsed_query.get("format")
    except Exception as e:
        logger.warning(f"POST DEBUG - Body parse error: {e}")

    # Also check URL query params as fallback
    if not symbol:
        symbol = request.query_params.get("symbol")
        if request.query_params.get("timeframe"):
            timeframe = request.query_params.get("timeframe")

    if not symbol:
        # Return 200 OK with ready status (not 422)
        return JSONResponse(
            status_code=200,
            content={
                "status": "ready",
                "message": "POST /signal - send JSON body with symbol field",
                "example": {"symbol": "BTC", "timeframe": "4h"},
                "apix_format": {"query": "symbol=BTC&timeframe=4h"},
                "parameters": {
                    "symbol": "Crypto symbol (required) - BTC, ETH, SOL, etc.",
                    "timeframe": "Chart timeframe (optional) - 1h, 4h, 1d, 1w (default: 4h)",
                    "format": "Response format (optional) - json or text (default: json)"
                }
            }
        )

    logger.info(f"POST - Analyzing signal for: {symbol} / {timeframe}")
    return await _generate_signal(symbol, timeframe, format_type)


# ============================================================================
# APIX V2 ENDPOINT - Fresh registration with correct POST format
# ============================================================================

@router.post(
    "/technical-analysis",
    responses={
        200: {"description": "Technical analysis complete"},
        404: {"description": "Symbol not found or no data available"},
        429: {"description": "Rate limit exceeded"},
        500: {"description": "Internal server error"},
        503: {"description": "Data provider temporarily unavailable"},
    },
    summary="Technical Analysis V2 (APIX POST)",
    description="APIX-compatible POST endpoint for technical analysis. Use POST method with JSON body.",
)
@limiter.limit("60/minute")
async def post_technical_analysis_v2(request: Request):
    """
    APIX V2 endpoint for technical analysis.

    APIX sends: {"query": "symbol=BTC&timeframe=4h&format=json"}

    Parameters:
        symbol: Crypto symbol (required) - BTC, ETH, SOL, etc.
        timeframe: Chart timeframe (optional) - 1h, 4h, 1d, 1w (default: 4h)
        format: Response format (optional) - json or text (default: json)
    """
    # Log everything for debugging
    logger.info(f"[APIX V2] Request received")
    logger.info(f"[APIX V2] Headers: {dict(request.headers)}")
    logger.info(f"[APIX V2] Query params: {dict(request.query_params)}")

    symbol = None
    timeframe = "4h"
    format_type = "json"

    # Parse body
    try:
        body_bytes = await request.body()
        logger.info(f"[APIX V2] Raw body: {body_bytes}")

        if body_bytes:
            body_json = json.loads(body_bytes)
            logger.info(f"[APIX V2] Parsed body: {body_json}")

            if isinstance(body_json, dict):
                # CRITICAL: Handle APIX {"query": "symbol=BTC&timeframe=4h"} format
                if "query" in body_json:
                    query_string = body_json.get("query", "")
                    logger.info(f"[APIX V2] Parsing query field: {query_string}")
                    parsed_query = parse_apix_query_field(query_string)
                    logger.info(f"[APIX V2] Parsed params: {parsed_query}")
                    # APIX sends "base" instead of "symbol", "interval" instead of "timeframe"
                    symbol = parsed_query.get("symbol") or parsed_query.get("base")
                    if parsed_query.get("timeframe") or parsed_query.get("interval"):
                        timeframe = parsed_query.get("timeframe") or parsed_query.get("interval")
                    if parsed_query.get("format"):
                        format_type = parsed_query.get("format")
                else:
                    # Standard JSON body {"symbol": "BTC", "timeframe": "4h"}
                    symbol = body_json.get("symbol")
                    if body_json.get("timeframe"):
                        timeframe = body_json.get("timeframe")
                    if body_json.get("format"):
                        format_type = body_json.get("format")
    except Exception as e:
        logger.warning(f"[APIX V2] Body parse error: {e}")

    # Fallback to query params
    if not symbol:
        symbol = request.query_params.get("symbol")
    if request.query_params.get("timeframe"):
        timeframe = request.query_params.get("timeframe")

    # CRITICAL: Return 200 OK for validation requests (not 422!)
    if not symbol:
        return JSONResponse(
            status_code=200,
            content={
                "status": "ready",
                "message": "Technical Analysis API V2 - provide symbol parameter",
                "example": {"symbol": "BTC", "timeframe": "4h", "format": "json"},
                "apix_format": {"query": "symbol=BTC&timeframe=4h&format=json"},
                "parameters": {
                    "symbol": "Crypto symbol (required) - BTC, ETH, SOL, bitcoin, ethereum, solana",
                    "timeframe": "Chart timeframe (optional) - 1h, 4h, 1d, 1w (default: 4h)",
                    "format": "Response format (optional) - json or text (default: json)"
                },
                "supported_symbols": ["BTC", "ETH", "SOL", "BNB", "XRP", "ADA", "DOGE", "AVAX", "DOT", "MATIC"]
            }
        )

    logger.info(f"[APIX V2] Generating analysis for: {symbol} / {timeframe} / {format_type}")
    return await _generate_signal(symbol, timeframe, format_type)
