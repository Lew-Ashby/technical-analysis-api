# APIX Signal API - Implementation Plan

**Mission ID:** APIX-SIGNAL-API
**Date:** 2026-02-11
**Agent:** ENG-041 (Python/FastAPI Principal)
**Status:** STEP 1 - PLAN & RESEARCH COMPLETE

---

## 1. EXECUTIVE SUMMARY

Refactor the existing Trading Chart Analysis API into a simplified, payment-enabled single endpoint for the APIX x402 marketplace. The new `/api/v1/signal/{symbol}` endpoint will provide comprehensive crypto trading analysis with x402 micropayment integration.

---

## 2. CURRENT ARCHITECTURE ANALYSIS

### 2.1 Existing Structure
```
backend/
├── app/
│   ├── main.py                    # FastAPI app entry point
│   ├── config.py                  # Settings with Pydantic
│   ├── routers/
│   │   ├── analysis.py            # POST/GET /analyze endpoints (KEEP LOGIC)
│   │   ├── assets.py              # Asset search endpoints (KEEP)
│   │   ├── charts.py              # Chart HTML endpoints (KEEP)
│   │   ├── health.py              # Health check (KEEP)
│   │   ├── perp_simulation.py     # Perp calculator (REMOVE)
│   │   └── websocket.py           # WebSocket streams (REMOVE)
│   ├── middleware/
│   │   └── security.py            # API key auth + rate limiting (MODIFY)
│   ├── models/
│   │   ├── analysis.py            # Technical indicator models (KEEP)
│   │   ├── chart.py               # OHLCV models (KEEP)
│   │   └── perp.py                # Perp models (REMOVE)
│   └── services/
│       ├── technical_analysis.py  # Full TA engine (KEEP)
│       ├── data_providers.py      # CoinGecko + Yahoo (MODIFY)
│       ├── llm_analysis.py        # Claude integration (REMOVE)
│       ├── cache.py               # TTL caching (KEEP)
│       ├── chart_generator.py     # HTML charts (KEEP)
│       ├── asset_registry.py      # 280+ crypto assets (KEEP)
│       └── perp_calculator.py     # Perp math (REMOVE)
└── tests/
```

### 2.2 Files to DELETE
| File | Reason |
|------|--------|
| `routers/perp_simulation.py` | Per mission spec: remove perp simulation |
| `routers/websocket.py` | Per mission spec: remove WebSocket endpoints |
| `models/perp.py` | No longer needed |
| `services/perp_calculator.py` | No longer needed |
| `services/llm_analysis.py` | Replace with enhanced rule-based analysis |

### 2.3 Files to MODIFY
| File | Changes |
|------|---------|
| `main.py` | Remove WS/perp routers, add x402 middleware, add signal router |
| `config.py` | Remove LLM settings, add x402 settings |
| `middleware/security.py` | Remove API key auth, keep rate limiting |
| `services/data_providers.py` | Remove YahooFinanceProvider class |
| `routers/analysis.py` | Rename/refactor to signal.py with new endpoint |

### 2.4 Files to CREATE
| File | Purpose |
|------|---------|
| `routers/signal.py` | New `/api/v1/signal/{symbol}` endpoint |
| `middleware/x402.py` | x402 payment middleware configuration |
| `models/signal.py` | SignalResponse model per spec |

---

## 3. TECHNICAL SPECIFICATIONS

### 3.1 New Signal Endpoint

```
GET /api/v1/signal/{symbol}

Query Parameters:
  - timeframe: 1h | 4h | 1d | 1w (default: 4h)
  - format: json | text (default: json)
  - include_chart: data | html | none (default: none)

Headers Required:
  - X-PAYMENT: <x402 payment token>

Responses:
  - 200: Analysis complete
  - 402: Payment required (x402 challenge)
  - 404: Symbol not found
  - 422: Invalid parameters
  - 429: Rate limited
```

### 3.2 JSON Response Schema

```json
{
  "symbol": "BTC",
  "timeframe": "4h",
  "timestamp": "2026-02-11T12:00:00Z",
  "price": {
    "current": 105000.00,
    "change_24h": 2500.00,
    "change_24h_pct": 2.44
  },
  "analysis": {
    "bias_score": 65,
    "confidence": 0.78,
    "signal": "bullish",
    "regime": "bullish_trend",
    "entry_quality": "good",
    "risk_level": "medium"
  },
  "trend": {
    "direction": "bullish",
    "strength": "moderate",
    "ema_20": 103500.00,
    "ema_50": 102000.00,
    "ema_100": 100500.00,
    "price_position": "above_all_bullish",
    "structure": "higher_highs"
  },
  "momentum": {
    "rsi": 58.5,
    "rsi_zone": "neutral",
    "macd_state": "positive_acceleration",
    "macd_histogram": 0.00125,
    "histogram_slope": "rising"
  },
  "volume": {
    "state": "accumulation",
    "relative": 1.35,
    "confirmation": true
  },
  "volatility": {
    "state": "stable",
    "atr_pct": 2.8,
    "squeeze": false,
    "breakout_potential": "low"
  },
  "levels": {
    "support": [102000.00, 100500.00, 98000.00],
    "resistance": [107000.00, 110000.00, 115000.00]
  },
  "trade": {
    "position": "long",
    "leverage": 3,
    "entry": 105000.00,
    "stop_loss": 102500.00,
    "take_profit_1": 108750.00,
    "take_profit_2": 112500.00,
    "take_profit_3": 120000.00,
    "risk_reward": 1.5,
    "position_risk_pct": 2.38,
    "invalidation": "Close below $102,500"
  },
  "summary": "BTC on the 4h timeframe shows bullish bias (score: +65/100, confidence: 78%)...",
  "chart_data": null
}
```

### 3.3 Text Response Format

```
═══════════════════════════════════════════════════════════════
                    BTC/USD - 4H TRADING SIGNAL
═══════════════════════════════════════════════════════════════

PRICE
  Current: $105,000.00
  24h Change: +$2,500.00 (+2.44%)

TREND ANALYSIS
  Direction: BULLISH (Moderate)
  Structure: Higher Highs
  EMA Ribbon: Price above all EMAs - bullish alignment
  - EMA 20: $103,500.00
  - EMA 50: $102,000.00
  - EMA 100: $100,500.00

MOMENTUM
  RSI: 58.5 (Neutral zone)
  MACD: Positive acceleration, histogram rising

VOLUME & VOLATILITY
  Volume State: Accumulation (1.35x relative)
  Volatility: Stable (2.8% ATR)
  Squeeze: No

SIGNAL SUMMARY
  Bias Score: +65/100
  Confidence: 78%
  Regime: Bullish Trend
  Action: Look for long entry
  Entry Quality: Good
  Risk Level: Medium

TRADE SETUP
  Position: LONG (3x leverage)
  Entry: $105,000.00
  Stop Loss: $102,500.00 (-2.38%)
  Take Profit 1: $108,750.00 (R:R 1.5:1)
  Take Profit 2: $112,500.00 (R:R 3.0:1)
  Take Profit 3: $120,000.00 (R:R 6.0:1)
  Invalidation: Close below $102,500

KEY LEVELS
  Support: $102,000 | $100,500 | $98,000
  Resistance: $107,000 | $110,000 | $115,000

COMMENTARY
  BTC on the 4h timeframe shows bullish bias with moderate trend
  strength. EMA ribbon indicates price above all EMAs in bullish
  alignment. RSI at 58.5 in neutral zone with room to run.
  MACD showing positive acceleration. Volume confirms with 1.35x
  relative volume during accumulation. No squeeze detected.
  Recommended action: look for long entry opportunities.

═══════════════════════════════════════════════════════════════
Disclaimer: This is technical analysis, not financial advice.
Trading involves risk. Past performance does not guarantee results.
═══════════════════════════════════════════════════════════════
```

### 3.4 x402 Payment Integration

```python
# middleware/x402.py
from x402.http.middleware.fastapi import PaymentMiddlewareASGI
from x402.http import HTTPFacilitatorClient, FacilitatorConfig, PaymentOption
from x402.http.types import RouteConfig
from x402.server import x402ResourceServer
from x402.mechanisms.evm.exact import ExactEvmServerScheme

from app.config import settings

def create_x402_middleware():
    """Create x402 payment middleware for signal endpoint."""
    server = x402ResourceServer(
        HTTPFacilitatorClient(FacilitatorConfig(url=settings.x402_facilitator_url))
    )
    server.register("eip155:8453", ExactEvmServerScheme())  # Base mainnet

    routes = {
        "GET /api/v1/signal/{symbol}": RouteConfig(
            accepts=[
                PaymentOption(
                    scheme="exact",
                    price=settings.signal_price,  # e.g., "$0.10"
                    network="eip155:8453",
                    pay_to=settings.payment_address,
                )
            ]
        ),
    }

    return PaymentMiddlewareASGI, {"routes": routes, "server": server}
```

---

## 4. IMPLEMENTATION PHASES

### Phase 1: Cleanup (Files to Delete)
| Task | File | Evidence Needed |
|------|------|-----------------|
| Delete perp_simulation router | `routers/perp_simulation.py` | File removed |
| Delete websocket router | `routers/websocket.py` | File removed |
| Delete perp models | `models/perp.py` | File removed |
| Delete perp calculator | `services/perp_calculator.py` | File removed |
| Delete LLM analysis | `services/llm_analysis.py` | File removed |

### Phase 2: Simplification (Files to Modify)

#### 2a. Remove Stock Support from data_providers.py
- Delete `YahooFinanceProvider` class (lines 420-545)
- Modify `get_provider()` to only return `CoinGeckoProvider`
- Remove yfinance import and thread pool executor

#### 2b. Update config.py
- Remove: `anthropic_api_key`, `llm_model`, `llm_max_tokens`
- Add: `x402_facilitator_url`, `payment_address`, `signal_price`

#### 2c. Update middleware/security.py
- Remove `verify_api_key` dependency
- Keep rate limiter

#### 2d. Update main.py
- Remove: websocket, perp_simulation router imports
- Add: signal router, x402 middleware

### Phase 3: New Signal Endpoint

Create `routers/signal.py`:
```python
@router.get("/signal/{symbol}")
async def get_signal(
    request: Request,
    symbol: str,
    timeframe: str = Query(default="4h", pattern="^(1h|4h|1d|1w)$"),
    format: Literal["json", "text"] = Query(default="json"),
    include_chart: Literal["data", "html", "none"] = Query(default="none"),
) -> Union[SignalResponse, PlainTextResponse]:
    """Get trading signal for a crypto symbol."""
    # Implementation using existing technical_analysis.py
```

### Phase 4: Response Formatting

Create formatters in `services/signal_formatter.py`:
- `format_json_response()` - Maps TechnicalIndicators to SignalResponse
- `format_text_response()` - Generates ASCII text output
- Uses existing `_generate_fallback_analysis()` logic from llm_analysis.py

### Phase 5: Testing

Update `tests/test_integration.py`:
- Remove perp simulation tests
- Remove LLM analysis tests
- Add signal endpoint tests
- Add x402 payment flow tests (mocked facilitator)

---

## 5. DEPENDENCY CHANGES

### Remove from pyproject.toml:
```toml
"anthropic>=0.18.0",
"yfinance>=0.2.36",
"websockets>=12.0",
```

### Add to pyproject.toml:
```toml
"x402[fastapi]>=2.0.0",
```

### Updated dependencies list:
```toml
dependencies = [
    "fastapi>=0.109.0",
    "uvicorn[standard]>=0.27.0",
    "pydantic>=2.5.0",
    "pydantic-settings>=2.1.0",
    "httpx>=0.26.0",
    "pandas>=2.1.0",
    "numpy>=1.26.0",
    "ta>=0.11.0",
    "python-dotenv>=1.0.0",
    "slowapi>=0.1.9",
    "cachetools>=5.3.0",
    "x402[fastapi]>=2.0.0",
]
```

---

## 6. CONFIGURATION CHANGES

### New .env.example:
```bash
# x402 Payment Configuration
X402_FACILITATOR_URL=https://x402.org/facilitator
PAYMENT_ADDRESS=0xYourBaseAddress
SIGNAL_PRICE=$0.10

# CoinGecko API Key (optional for higher rate limits)
COINGECKO_API_KEY=

# Debug mode
DEBUG=true

# Cache Settings
CACHE_TTL_SECONDS=300
CACHE_MAX_SIZE=1000

# Rate Limiting
RATE_LIMIT_SIGNAL=60
```

---

## 7. FILE-BY-FILE IMPLEMENTATION GUIDE

### 7.1 DELETE Files
```bash
rm app/routers/perp_simulation.py
rm app/routers/websocket.py
rm app/models/perp.py
rm app/services/perp_calculator.py
rm app/services/llm_analysis.py
```

### 7.2 CREATE app/routers/signal.py
- Single `/signal/{symbol}` GET endpoint
- Uses `TechnicalAnalyzer` from existing services
- Uses `CoinGeckoProvider` for data
- Returns JSON or text based on format parameter
- Optional chart_data inclusion

### 7.3 CREATE app/models/signal.py
- `PriceInfo` model
- `AnalysisInfo` model
- `TrendInfo` model
- `MomentumInfo` model
- `VolumeInfo` model
- `VolatilityInfo` model
- `LevelsInfo` model
- `TradeInfo` model
- `SignalResponse` aggregated model

### 7.4 CREATE app/middleware/x402.py
- x402 server configuration
- Route configuration for signal endpoint
- Payment option with Base network

### 7.5 MODIFY app/main.py
```python
# Remove these imports:
- from app.routers import websocket, perp_simulation

# Add these imports:
+ from app.routers import signal
+ from app.middleware.x402 import create_x402_middleware

# Remove these router includes:
- app.include_router(websocket.router, ...)
- app.include_router(perp_simulation.router, ...)

# Add signal router:
+ app.include_router(signal.router, prefix="/api/v1", tags=["Signal"])

# Add x402 middleware:
+ middleware_cls, middleware_config = create_x402_middleware()
+ app.add_middleware(middleware_cls, **middleware_config)
```

### 7.6 MODIFY app/config.py
```python
class Settings(BaseSettings):
    # Remove:
    - anthropic_api_key: str = ""
    - llm_model: str = "claude-sonnet-4-20250514"
    - llm_max_tokens: int = 1024

    # Add:
    + x402_facilitator_url: str = "https://x402.org/facilitator"
    + payment_address: str = ""
    + signal_price: str = "$0.10"
    + rate_limit_signal: int = 60
```

### 7.7 MODIFY app/services/data_providers.py
- Remove `YahooFinanceProvider` class entirely
- Remove `yfinance` import
- Simplify `get_provider()` to only return `CoinGeckoProvider`

### 7.8 CREATE app/services/signal_formatter.py
- `format_json_response(symbol, timeframe, price, change, indicators, suggestion) -> SignalResponse`
- `format_text_response(symbol, timeframe, price, change, indicators, suggestion) -> str`
- Port and enhance `_generate_fallback_analysis()` logic

---

## 8. TEST PLAN

### 8.1 Unit Tests
| Test | File | Description |
|------|------|-------------|
| test_signal_json_format | test_signal.py | Verify JSON schema compliance |
| test_signal_text_format | test_signal.py | Verify text output format |
| test_signal_timeframes | test_signal.py | Test 1h, 4h, 1d, 1w |
| test_signal_invalid_symbol | test_signal.py | 404 for unknown symbol |
| test_signal_invalid_timeframe | test_signal.py | 422 for bad timeframe |

### 8.2 Integration Tests
| Test | Description |
|------|-------------|
| test_signal_flow | Full request -> analysis -> response |
| test_x402_402_response | Verify 402 without payment |
| test_rate_limiting | Verify rate limit enforcement |

### 8.3 Remove Tests
- All tests in `test_llm_analysis.py`
- Perp-related tests
- WebSocket tests

---

## 9. RISKS AND MITIGATIONS

| Risk | Impact | Mitigation |
|------|--------|------------|
| CoinGecko rate limiting | Service degradation | Implement aggressive caching, add API key support |
| x402 facilitator downtime | 402s fail | Fallback to direct payment verification |
| Response size too large | Performance | Limit chart_data option, compress responses |
| Breaking existing clients | Client errors | N/A - new API, clean break |

---

## 10. QUALITY GATES

| Metric | Target | Measurement |
|--------|--------|-------------|
| Response Time (p99) | <100ms | APM/logging |
| Type Coverage | 100% | mypy --strict |
| Test Coverage | >90% | pytest-cov |
| Memory Usage | <512MB | py-spy |

---

## 11. EXECUTION CHECKLIST

- [ ] Phase 1: Delete deprecated files (5 files)
- [ ] Phase 2: Update dependencies in pyproject.toml
- [ ] Phase 3: Create models/signal.py
- [ ] Phase 4: Create routers/signal.py
- [ ] Phase 5: Create middleware/x402.py
- [ ] Phase 6: Create services/signal_formatter.py
- [ ] Phase 7: Modify main.py
- [ ] Phase 8: Modify config.py
- [ ] Phase 9: Modify data_providers.py
- [ ] Phase 10: Update tests
- [ ] Phase 11: Run full test suite
- [ ] Phase 12: Type check with mypy
- [ ] Phase 13: Manual integration test
- [ ] Phase 14: Production validation

---

## 12. ESTIMATED EFFORT

| Phase | Files | LOC Changed | Time |
|-------|-------|-------------|------|
| Cleanup | 5 deleted | -1200 | 15 min |
| Simplification | 4 modified | -400 | 30 min |
| New Endpoint | 4 created | +600 | 60 min |
| Testing | 3 modified | +200 | 45 min |
| Validation | N/A | N/A | 30 min |
| **Total** | **16 files** | **-800 net** | **~3 hours** |

---

## APPROVAL REQUEST

This plan is ready for Human Principal review.

**Key Decisions Requiring Approval:**
1. Remove ALL stock support (no Yahoo Finance)
2. Remove ALL LLM integration (rule-based only)
3. Single endpoint architecture (`/signal/{symbol}`)
4. x402 payment on Base mainnet
5. Pricing at $0.10 per signal

**Proceed with implementation?**

---

*Generated by ENG-041: Python/FastAPI Principal*
*Mission: APIX-SIGNAL-API*

Sources:
- [x402 on PyPI](https://pypi.org/project/x402/)
- [x402 FastAPI Example](https://github.com/coinbase/x402/tree/main/examples/python/servers/fastapi)
- [x402 Protocol](https://github.com/coinbase/x402)
