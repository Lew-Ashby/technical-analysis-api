"""x402 payment middleware placeholder.

Note: When deployed behind APIX (https://apix-v2.web.app/), the x402 payment
handling is managed by the APIX platform. This API receives requests only
after payment verification is completed by APIX.

Pricing and payment addresses are configured in the APIX dashboard,
not in this codebase.
"""
import logging
from typing import Any, Dict, Tuple, Type

logger = logging.getLogger("trading_signal_api.x402")


def create_x402_middleware() -> Tuple[Type[Any], Dict[str, Any]]:
    """
    Return a no-op middleware.

    When deployed behind APIX, the platform handles x402 payment verification.
    This API receives only authenticated/paid requests.
    """
    logger.info("API configured for APIX marketplace (x402 handled by platform)")
    return _NoOpMiddleware, {}


class _NoOpMiddleware:
    """Pass-through middleware - APIX handles x402 payments."""

    def __init__(self, app: Any, **kwargs: Any) -> None:
        self.app = app

    async def __call__(self, scope: Any, receive: Any, send: Any) -> None:
        await self.app(scope, receive, send)
