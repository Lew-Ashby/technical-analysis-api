"""FastAPI application entry point for Trading Signal API."""
import logging

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.config import settings
from app.middleware.security import limiter
from app.middleware.x402 import create_x402_middleware
from app.routers import health, signal

logger = logging.getLogger("trading_signal_api")

app = FastAPI(
    title=settings.app_name,
    description="Crypto Trading Signal API for APIX x402 Marketplace",
    version="1.0.0",
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
    openapi_url="/openapi.json",  # APIX requires this - always enabled
)

# Rate limiter state
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS middleware - allow all origins for APIX marketplace
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# x402 payment middleware
middleware_cls, middleware_config = create_x402_middleware()
if middleware_config:
    app.add_middleware(middleware_cls, **middleware_config)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all incoming requests."""
    client_host = request.client.host if request.client else "unknown"
    logger.info(f"{request.method} {request.url.path} from {client_host}")
    response = await call_next(request)
    return response


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler - shows error details for debugging."""
    logger.exception(f"Unhandled exception for {request.url.path}: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc), "type": type(exc).__name__},
    )


# Include routers
app.include_router(health.router, tags=["Health"])
app.include_router(signal.router, prefix="/api/v1", tags=["Signal"])


@app.get("/", include_in_schema=False)
async def root():
    """API root endpoint."""
    return {
        "name": settings.app_name,
        "version": "1.0.0",
        "docs": "/docs" if settings.debug else None,
        "endpoints": {
            "signal": "/api/v1/signal?symbol={symbol}",
            "signal_alt": "/api/v1/signal/{symbol}",
            "health": "/health",
        },
    }
