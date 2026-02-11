"""Application configuration."""
import logging
from typing import List

from pydantic import ConfigDict, field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment."""

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    app_name: str = "Trading Signal API"
    debug: bool = False

    # Data Provider
    coingecko_api_key: str = ""  # Optional for higher rate limits

    # Note: x402 payments are handled by APIX platform
    # Configure pricing and wallet address in the APIX dashboard

    # CORS Settings (comma-separated string in .env)
    cors_origins: str = "*"

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, v):
        """Handle both string and list inputs."""
        if isinstance(v, list):
            return ",".join(v)
        return v

    @property
    def cors_origins_list(self) -> List[str]:
        """Return CORS origins as a list."""
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]

    # Rate Limiting (requests per minute)
    rate_limit_signal: int = 60  # Signal endpoint
    rate_limit_chart: int = 20  # Chart generation
    rate_limit_assets: int = 60  # Asset queries

    # Cache Settings
    cache_ttl_seconds: int = 300  # 5 minutes
    cache_max_size: int = 1000  # Max cached items

    # Logging
    log_level: str = "INFO"


settings = Settings()

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level.upper()),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("trading_signal_api")
