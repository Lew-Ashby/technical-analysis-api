"""HTML chart generator using TradingView Lightweight Charts."""
import json
from typing import Optional

import pandas as pd

from app.models.analysis import TechnicalIndicators, TradingSuggestion
from app.models.chart import ChartData


def generate_html_chart(
    chart_data: ChartData,
    indicators: TechnicalIndicators,
    suggestion: Optional[TradingSuggestion] = None,
    analyzer_df: Optional[pd.DataFrame] = None,
) -> str:
    """
    Generate a standalone HTML page with interactive TradingView chart.

    Includes:
    - Candlestick chart with EMA overlays (20, 50, 100)
    - Volume histogram
    - RSI indicator panel
    - Support/resistance horizontal lines
    - Trade entry/SL/TP markers (if suggestion provided)
    """
    # Prepare candle data for Lightweight Charts
    candles = [
        {
            "time": int(c.timestamp.timestamp()),
            "open": float(c.open),
            "high": float(c.high),
            "low": float(c.low),
            "close": float(c.close),
        }
        for c in chart_data.candles
    ]

    # Prepare volume data
    volumes = [
        {
            "time": int(c.timestamp.timestamp()),
            "value": float(c.volume),
            "color": "rgba(38, 166, 154, 0.5)" if c.close >= c.open else "rgba(239, 83, 80, 0.5)",
        }
        for c in chart_data.candles
    ]

    # Prepare EMA line data from analyzer DataFrame
    ema_20_data = []
    ema_50_data = []
    ema_100_data = []
    rsi_data = []

    if analyzer_df is not None:
        # EMA 20
        if "ema_20" in analyzer_df.columns:
            for idx, val in analyzer_df["ema_20"].dropna().items():
                ema_20_data.append({"time": int(idx.timestamp()), "value": float(val)})

        # EMA 50
        if "ema_50" in analyzer_df.columns:
            for idx, val in analyzer_df["ema_50"].dropna().items():
                ema_50_data.append({"time": int(idx.timestamp()), "value": float(val)})

        # EMA 100
        if "ema_100" in analyzer_df.columns:
            for idx, val in analyzer_df["ema_100"].dropna().items():
                ema_100_data.append({"time": int(idx.timestamp()), "value": float(val)})

        # RSI
        if "rsi" in analyzer_df.columns:
            for idx, val in analyzer_df["rsi"].dropna().items():
                rsi_data.append({"time": int(idx.timestamp()), "value": float(val)})

    # Extract support/resistance levels
    support_levels = [
        lvl.price for lvl in indicators.structure.key_levels if lvl.type == "support"
    ][:3]
    resistance_levels = [
        lvl.price for lvl in indicators.structure.key_levels if lvl.type == "resistance"
    ][:3]

    # Pre-compute CSS classes
    bias_class = "bullish" if indicators.summary.bias_score > 0 else "bearish" if indicators.summary.bias_score < 0 else "neutral"
    rsi_class = "bullish" if indicators.rsi.value > 50 else "bearish" if indicators.rsi.value < 50 else "neutral"
    trend_class = "bullish" if indicators.ema_ribbon.trend_direction.value == "bullish" else "bearish"

    # Build HTML
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{chart_data.symbol} - {chart_data.timeframe} Chart</title>
    <script src="https://unpkg.com/lightweight-charts@4.1.0/dist/lightweight-charts.standalone.production.js"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #131722;
            color: #d1d4dc;
        }}
        .container {{ padding: 20px; max-width: 1400px; margin: 0 auto; }}
        .header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }}
        .symbol {{ font-size: 24px; font-weight: bold; color: #fff; }}
        .timeframe {{
            background: #2962ff;
            padding: 4px 12px;
            border-radius: 4px;
            font-size: 14px;
        }}
        .chart-container {{
            width: 100%;
            height: 450px;
            border-radius: 8px;
            overflow: hidden;
            background: #1e222d;
        }}
        .rsi-container {{
            width: 100%;
            height: 120px;
            margin-top: 5px;
            border-radius: 8px;
            overflow: hidden;
            background: #1e222d;
        }}
        .info-panel {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 12px;
            margin-top: 20px;
        }}
        .info-card {{
            background: #1e222d;
            padding: 12px;
            border-radius: 8px;
        }}
        .info-card h3 {{
            font-size: 11px;
            color: #787b86;
            margin-bottom: 6px;
            text-transform: uppercase;
        }}
        .info-card .value {{
            font-size: 16px;
            font-weight: bold;
        }}
        .bullish {{ color: #26a69a; }}
        .bearish {{ color: #ef5350; }}
        .neutral {{ color: #787b86; }}
        .trade-box {{
            background: #1e222d;
            padding: 16px;
            border-radius: 8px;
            margin-top: 20px;
        }}
        .trade-box h2 {{
            margin-bottom: 12px;
            color: #fff;
            font-size: 16px;
        }}
        .trade-row {{
            display: flex;
            justify-content: space-between;
            padding: 6px 0;
            border-bottom: 1px solid #2a2e39;
            font-size: 14px;
        }}
        .trade-row:last-child {{ border-bottom: none; }}
        .label {{ color: #787b86; }}
        .legend {{
            display: flex;
            gap: 20px;
            margin-top: 8px;
            font-size: 12px;
        }}
        .legend-item {{
            display: flex;
            align-items: center;
            gap: 5px;
        }}
        .legend-color {{
            width: 20px;
            height: 3px;
            border-radius: 2px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <span class="symbol">{chart_data.symbol}/USDT</span>
            <span class="timeframe">{chart_data.timeframe.upper()}</span>
        </div>

        <div id="chart" class="chart-container"></div>
        <div class="legend">
            <div class="legend-item">
                <div class="legend-color" style="background: #f7931a;"></div>
                <span>EMA 20</span>
            </div>
            <div class="legend-item">
                <div class="legend-color" style="background: #2962ff;"></div>
                <span>EMA 50</span>
            </div>
            <div class="legend-item">
                <div class="legend-color" style="background: #7b1fa2;"></div>
                <span>EMA 100</span>
            </div>
            <div class="legend-item">
                <div class="legend-color" style="background: #26a69a;"></div>
                <span>Support</span>
            </div>
            <div class="legend-item">
                <div class="legend-color" style="background: #ef5350;"></div>
                <span>Resistance</span>
            </div>
        </div>

        <div id="rsi" class="rsi-container"></div>

        <div class="info-panel">
            <div class="info-card">
                <h3>Bias Score</h3>
                <div class="value {bias_class}">
                    {indicators.summary.bias_score:+d}/100
                </div>
            </div>
            <div class="info-card">
                <h3>Confidence</h3>
                <div class="value">{indicators.summary.confidence:.0%}</div>
            </div>
            <div class="info-card">
                <h3>RSI</h3>
                <div class="value {rsi_class}">
                    {indicators.rsi.value:.1f}
                </div>
            </div>
            <div class="info-card">
                <h3>Trend</h3>
                <div class="value {trend_class}">
                    {indicators.ema_ribbon.trend_direction.value.upper()}
                </div>
            </div>
            <div class="info-card">
                <h3>Signal</h3>
                <div class="value {bias_class}">
                    {indicators.summary.recommended_action.replace('_', ' ').upper()}
                </div>
            </div>
        </div>

        {_generate_trade_box_html(suggestion) if suggestion else ''}
    </div>

    <script>
        // Data
        const candles = {json.dumps(candles)};
        const volumes = {json.dumps(volumes)};
        const ema20Data = {json.dumps(ema_20_data)};
        const ema50Data = {json.dumps(ema_50_data)};
        const ema100Data = {json.dumps(ema_100_data)};
        const rsiData = {json.dumps(rsi_data)};
        const supportLevels = {json.dumps(support_levels)};
        const resistanceLevels = {json.dumps(resistance_levels)};

        // Main chart
        const chartContainer = document.getElementById('chart');
        const chart = LightweightCharts.createChart(chartContainer, {{
            width: chartContainer.clientWidth,
            height: 450,
            layout: {{
                background: {{ type: 'solid', color: '#1e222d' }},
                textColor: '#d1d4dc',
            }},
            grid: {{
                vertLines: {{ color: '#2a2e39' }},
                horzLines: {{ color: '#2a2e39' }},
            }},
            crosshair: {{
                mode: LightweightCharts.CrosshairMode.Normal,
            }},
            rightPriceScale: {{
                borderColor: '#2a2e39',
                scaleMargins: {{ top: 0.1, bottom: 0.2 }},
            }},
            timeScale: {{
                borderColor: '#2a2e39',
                timeVisible: true,
                secondsVisible: false,
            }},
        }});

        // Candlestick series
        const candleSeries = chart.addCandlestickSeries({{
            upColor: '#26a69a',
            downColor: '#ef5350',
            borderUpColor: '#26a69a',
            borderDownColor: '#ef5350',
            wickUpColor: '#26a69a',
            wickDownColor: '#ef5350',
        }});
        candleSeries.setData(candles);

        // Volume series
        const volumeSeries = chart.addHistogramSeries({{
            priceFormat: {{ type: 'volume' }},
            priceScaleId: '',
            scaleMargins: {{ top: 0.85, bottom: 0 }},
        }});
        volumeSeries.setData(volumes);

        // EMA 20 line
        if (ema20Data.length > 0) {{
            const ema20Series = chart.addLineSeries({{
                color: '#f7931a',
                lineWidth: 1,
                priceLineVisible: false,
                lastValueVisible: false,
            }});
            ema20Series.setData(ema20Data);
        }}

        // EMA 50 line
        if (ema50Data.length > 0) {{
            const ema50Series = chart.addLineSeries({{
                color: '#2962ff',
                lineWidth: 1,
                priceLineVisible: false,
                lastValueVisible: false,
            }});
            ema50Series.setData(ema50Data);
        }}

        // EMA 100 line
        if (ema100Data.length > 0) {{
            const ema100Series = chart.addLineSeries({{
                color: '#7b1fa2',
                lineWidth: 1,
                priceLineVisible: false,
                lastValueVisible: false,
            }});
            ema100Series.setData(ema100Data);
        }}

        // Support lines
        supportLevels.forEach(level => {{
            candleSeries.createPriceLine({{
                price: level,
                color: '#26a69a',
                lineWidth: 1,
                lineStyle: LightweightCharts.LineStyle.Dashed,
                axisLabelVisible: true,
                title: 'S',
            }});
        }});

        // Resistance lines
        resistanceLevels.forEach(level => {{
            candleSeries.createPriceLine({{
                price: level,
                color: '#ef5350',
                lineWidth: 1,
                lineStyle: LightweightCharts.LineStyle.Dashed,
                axisLabelVisible: true,
                title: 'R',
            }});
        }});

        {_generate_trade_lines_js(suggestion) if suggestion else ''}

        chart.timeScale().fitContent();

        // RSI Chart
        const rsiContainer = document.getElementById('rsi');
        const rsiChart = LightweightCharts.createChart(rsiContainer, {{
            width: rsiContainer.clientWidth,
            height: 120,
            layout: {{
                background: {{ type: 'solid', color: '#1e222d' }},
                textColor: '#d1d4dc',
            }},
            grid: {{
                vertLines: {{ color: '#2a2e39' }},
                horzLines: {{ color: '#2a2e39' }},
            }},
            rightPriceScale: {{
                borderColor: '#2a2e39',
                scaleMargins: {{ top: 0.1, bottom: 0.1 }},
            }},
            timeScale: {{
                borderColor: '#2a2e39',
                visible: false,
            }},
        }});

        // RSI line
        const rsiSeries = rsiChart.addLineSeries({{
            color: '#7b1fa2',
            lineWidth: 2,
            priceLineVisible: false,
        }});

        if (rsiData.length > 0) {{
            rsiSeries.setData(rsiData);
        }}

        // RSI levels
        rsiSeries.createPriceLine({{ price: 70, color: '#ef5350', lineWidth: 1, lineStyle: 2, axisLabelVisible: true, title: 'OB' }});
        rsiSeries.createPriceLine({{ price: 30, color: '#26a69a', lineWidth: 1, lineStyle: 2, axisLabelVisible: true, title: 'OS' }});
        rsiSeries.createPriceLine({{ price: 50, color: '#787b86', lineWidth: 1, lineStyle: 2 }});

        // Sync charts
        chart.timeScale().subscribeVisibleLogicalRangeChange(range => {{
            rsiChart.timeScale().setVisibleLogicalRange(range);
        }});

        // Handle resize
        window.addEventListener('resize', () => {{
            chart.applyOptions({{ width: chartContainer.clientWidth }});
            rsiChart.applyOptions({{ width: rsiContainer.clientWidth }});
        }});
    </script>
</body>
</html>"""
    return html


def _generate_trade_box_html(suggestion: TradingSuggestion) -> str:
    """Generate trade suggestion HTML box."""
    if suggestion.position_type.value == "no_trade":
        return f"""
        <div class="trade-box">
            <h2>Trade Suggestion</h2>
            <p class="neutral">No trade recommended at this time.</p>
            <p style="color: #787b86; margin-top: 10px;">{suggestion.reasoning}</p>
        </div>
        """

    position_class = "bullish" if suggestion.position_type.value == "long" else "bearish"
    position_text = suggestion.position_type.value.upper()
    tp2_display = f"${suggestion.take_profit_2:,.2f}" if suggestion.take_profit_2 else "N/A"
    tp3_display = f"${suggestion.take_profit_3:,.2f}" if suggestion.take_profit_3 else "N/A"

    return f"""
    <div class="trade-box">
        <h2>Trade Suggestion</h2>
        <div class="trade-row">
            <span class="label">Position</span>
            <span class="value {position_class}">{position_text} {suggestion.leverage}x</span>
        </div>
        <div class="trade-row">
            <span class="label">Entry</span>
            <span class="value">${suggestion.entry_price:,.2f}</span>
        </div>
        <div class="trade-row">
            <span class="label">Stop Loss</span>
            <span class="value bearish">${suggestion.stop_loss:,.2f}</span>
        </div>
        <div class="trade-row">
            <span class="label">Take Profit 1</span>
            <span class="value bullish">${suggestion.take_profit_1:,.2f}</span>
        </div>
        <div class="trade-row">
            <span class="label">Take Profit 2</span>
            <span class="value bullish">{tp2_display}</span>
        </div>
        <div class="trade-row">
            <span class="label">Take Profit 3</span>
            <span class="value bullish">{tp3_display}</span>
        </div>
        <div class="trade-row">
            <span class="label">Risk/Reward</span>
            <span class="value">{suggestion.risk_reward_ratio:.1f}:1</span>
        </div>
    </div>
    """


def _generate_trade_lines_js(suggestion: TradingSuggestion) -> str:
    """Generate JavaScript for trade price lines."""
    if suggestion.position_type.value == "no_trade":
        return ""

    lines = []

    # Entry line
    lines.append(f"""
        candleSeries.createPriceLine({{
            price: {suggestion.entry_price},
            color: '#2196F3',
            lineWidth: 2,
            lineStyle: LightweightCharts.LineStyle.Solid,
            axisLabelVisible: true,
            title: 'Entry',
        }});
    """)

    # Stop loss line
    lines.append(f"""
        candleSeries.createPriceLine({{
            price: {suggestion.stop_loss},
            color: '#ef5350',
            lineWidth: 2,
            lineStyle: LightweightCharts.LineStyle.Solid,
            axisLabelVisible: true,
            title: 'SL',
        }});
    """)

    # Take profit lines
    lines.append(f"""
        candleSeries.createPriceLine({{
            price: {suggestion.take_profit_1},
            color: '#26a69a',
            lineWidth: 2,
            lineStyle: LightweightCharts.LineStyle.Solid,
            axisLabelVisible: true,
            title: 'TP1',
        }});
    """)

    if suggestion.take_profit_2:
        lines.append(f"""
            candleSeries.createPriceLine({{
                price: {suggestion.take_profit_2},
                color: '#26a69a',
                lineWidth: 1,
                lineStyle: LightweightCharts.LineStyle.Dashed,
                axisLabelVisible: true,
                title: 'TP2',
            }});
        """)

    if suggestion.take_profit_3:
        lines.append(f"""
            candleSeries.createPriceLine({{
                price: {suggestion.take_profit_3},
                color: '#26a69a',
                lineWidth: 1,
                lineStyle: LightweightCharts.LineStyle.Dotted,
                axisLabelVisible: true,
                title: 'TP3',
            }});
        """)

    return "\n".join(lines)
