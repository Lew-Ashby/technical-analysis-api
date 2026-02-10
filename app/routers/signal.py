"""Signal API endpoint for crypto trading analysis."""
import logging
from typing import Literal, Union

from fastapi import APIRouter, HTTPException, Query, Request
from fastapi.responses import HTMLResponse, PlainTextResponse

from app.config import settings
from app.middleware.security import limiter
from app.models.signal import ChartDataInfo, SignalResponse
from app.services.chart_generator import generate_html_chart
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
    include_chart: Literal["data", "html", "none"] = Query(
        default="none",
        description="Include chart data: data, html, or none",
    ),
) -> Union[SignalResponse, PlainTextResponse, HTMLResponse]:
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
    # Normalize symbol
    symbol = symbol.upper().strip()

    try:
        # Get data provider
        provider = get_provider(api_key=settings.coingecko_api_key or None)

        # Fetch market data
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

        # Get current price and 24h change
        current_price = await provider.get_current_price(symbol)
        price_change, price_change_pct = await provider.get_price_change_24h(symbol)

        # Run technical analysis
        analyzer = TechnicalAnalyzer(chart_data)
        indicators = analyzer.get_technical_indicators()

        # Generate trading suggestion
        suggestion = analyzer.generate_trading_suggestion(indicators)

        # Prepare chart data if requested
        chart_data_info = None
        if include_chart == "data":
            chart_data_info = ChartDataInfo(
                candles=[
                    {
                        "time": int(c.timestamp.timestamp()),
                        "open": c.open,
                        "high": c.high,
                        "low": c.low,
                        "close": c.close,
                        "volume": c.volume,
                    }
                    for c in chart_data.candles[-100:]
                ],
                indicators={
                    "ema_20": [
                        {"time": int(idx.timestamp()), "value": float(val)}
                        for idx, val in analyzer.df["ema_20"].dropna().items()
                    ][-100:],
                    "ema_50": [
                        {"time": int(idx.timestamp()), "value": float(val)}
                        for idx, val in analyzer.df["ema_50"].dropna().items()
                    ][-100:],
                    "rsi": [
                        {"time": int(idx.timestamp()), "value": float(val)}
                        for idx, val in analyzer.df["rsi"].dropna().items()
                    ][-100:],
                },
            )

        # Return HTML chart if requested
        if include_chart == "html":
            html_content = generate_html_chart(
                chart_data=chart_data,
                indicators=indicators,
                suggestion=suggestion,
                analyzer_df=analyzer.df,
            )
            return HTMLResponse(content=html_content)

        # Format response based on requested format
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
            return PlainTextResponse(
                content=text_response,
                media_type="text/plain",
            )

        # JSON format
        signal_response = format_json_response(
            symbol=symbol,
            timeframe=timeframe,
            current_price=current_price,
            price_change=price_change,
            price_change_pct=price_change_pct,
            indicators=indicators,
            suggestion=suggestion,
            chart_data=chart_data_info,
        )

        logger.info(f"Signal generated for {symbol}/{timeframe}")
        return signal_response

    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except TimeoutError:
        raise HTTPException(status_code=504, detail="External service timeout")
    except Exception as e:
        logger.exception(f"Signal generation failed for {symbol}: {e}")
        raise HTTPException(
            status_code=500,
            detail="Signal generation failed. Please try again later.",
        )
